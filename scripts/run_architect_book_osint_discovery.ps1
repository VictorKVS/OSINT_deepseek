param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $RunnerArgs
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$DpapiStorePath = Join-Path $RepoRoot '.runtime\telegram\credentials.dpapi.json'
$SetupScript = Join-Path $RepoRoot 'scripts\setup_telegram_credentials.ps1'
$NetworkPreflightScript = Join-Path $RepoRoot 'scripts\test_telegram_network_path.ps1'
$AuthScript = Join-Path $RepoRoot 'scripts\authorize_telethon_session.py'
$DiscoveryScript = Join-Path $RepoRoot 'scripts\run_architect_book_osint_discovery.py'

function Resolve-Python {
    $venv = Join-Path $RepoRoot '.venv\Scripts\python.exe'
    if (Test-Path $venv) { return $venv }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) { return $python.Source }
    throw 'Python not found.'
}

function Get-EnvValue([string]$Name) {
    foreach ($scope in @('Process','User','Machine')) {
        $value = [Environment]::GetEnvironmentVariable($Name,$scope)
        if (-not [string]::IsNullOrWhiteSpace($value)) { return $value.Trim() }
    }
    return $null
}

function Convert-Dpapi([string]$CipherText) {
    $secure = ConvertTo-SecureString $CipherText
    $credential = [PSCredential]::new('local',$secure)
    return $credential.GetNetworkCredential().Password
}

$pythonExe = Resolve-Python
$apiId = Get-EnvValue 'TELEGRAM_API_ID'
$apiHash = Get-EnvValue 'TELEGRAM_API_HASH'
$session = Get-EnvValue 'TELEGRAM_SESSION_PATH'

if ((-not $apiId -or -not $apiHash) -and (Test-Path $DpapiStorePath)) {
    try {
        $payload = Get-Content $DpapiStorePath -Raw | ConvertFrom-Json
        if ($payload.storage -eq 'WINDOWS_DPAPI_CURRENT_USER') {
            if (-not $apiId) { $apiId = Convert-Dpapi ([string]$payload.api_id_dpapi) }
            if (-not $apiHash) { $apiHash = Convert-Dpapi ([string]$payload.api_hash_dpapi) }
        }
    } catch { }
}

if (-not $apiId -or -not $apiHash) {
    if (-not (Test-Path $SetupScript)) { throw 'Telegram credential setup script missing.' }
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $SetupScript
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $payload = Get-Content $DpapiStorePath -Raw | ConvertFrom-Json
    $apiId = Convert-Dpapi ([string]$payload.api_id_dpapi)
    $apiHash = Convert-Dpapi ([string]$payload.api_hash_dpapi)
}

$env:TELEGRAM_API_ID = $apiId
$env:TELEGRAM_API_HASH = $apiHash
if ($session) { $env:TELEGRAM_SESSION_PATH = $session }
$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"

if (Test-Path $NetworkPreflightScript) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $NetworkPreflightScript
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (Test-Path $AuthScript) {
    & $pythonExe $AuthScript
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& $pythonExe $DiscoveryScript @RunnerArgs
exit $LASTEXITCODE
