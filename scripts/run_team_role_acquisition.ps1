param(
    [Parameter(Mandatory = $true)][string] $Role,
    [Parameter(ValueFromRemainingArguments = $true)][string[]] $RunnerArgs
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$DpapiStorePath = Join-Path $RepoRoot '.runtime\telegram\credentials.dpapi.json'
$SetupScript = Join-Path $RepoRoot 'scripts\setup_telegram_credentials.ps1'
$NetworkPreflightScript = Join-Path $RepoRoot 'scripts\test_telegram_network_path.ps1'
$TelethonAuthScript = Join-Path $RepoRoot 'scripts\authorize_telethon_session.py'
$RunnerScript = Join-Path $RepoRoot 'scripts\run_team_role_acquisition.py'

function Resolve-Python {
    $venv = Join-Path $RepoRoot '.venv\Scripts\python.exe'
    if (Test-Path $venv) {
        & $venv -c "import telethon" *> $null
        if ($LASTEXITCODE -eq 0) { return $venv }
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        & $python.Source -c "import telethon" *> $null
        if ($LASTEXITCODE -eq 0) { return $python.Source }
    }
    throw 'Telethon is not installed in .venv or system Python.'
}

function Convert-DpapiCipherToPlainText {
    param([Parameter(Mandatory = $true)][string] $CipherText)
    $secure = ConvertTo-SecureString $CipherText
    $credential = [PSCredential]::new('local', $secure)
    return $credential.GetNetworkCredential().Password
}

function Get-EnvironmentSecret {
    param([Parameter(Mandatory = $true)][string] $Name)
    foreach ($scope in @('Process', 'User', 'Machine')) {
        $value = [Environment]::GetEnvironmentVariable($Name, $scope)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return [pscustomobject]@{ Value = $value.Trim(); Source = "WINDOWS_$($scope.ToUpperInvariant())_ENV" }
        }
    }
    return $null
}

function Read-DpapiCredentials {
    if (-not (Test-Path -LiteralPath $DpapiStorePath -PathType Leaf)) { return $null }
    try {
        $payload = Get-Content -LiteralPath $DpapiStorePath -Raw | ConvertFrom-Json
        if ($payload.storage -ne 'WINDOWS_DPAPI_CURRENT_USER') { return $null }
        $apiId = Convert-DpapiCipherToPlainText -CipherText ([string]$payload.api_id_dpapi)
        $apiHash = Convert-DpapiCipherToPlainText -CipherText ([string]$payload.api_hash_dpapi)
        if ([string]::IsNullOrWhiteSpace($apiId) -or [string]::IsNullOrWhiteSpace($apiHash)) { return $null }
        return [pscustomobject]@{ ApiId = $apiId; ApiHash = $apiHash; Source = 'WINDOWS_DPAPI_CURRENT_USER' }
    } catch {
        Write-Host 'DPAPI credential store could not be decrypted in this Windows user context.'
        return $null
    }
}

function Resolve-Credentials {
    $apiId = Get-EnvironmentSecret -Name 'TELEGRAM_API_ID'
    $apiHash = Get-EnvironmentSecret -Name 'TELEGRAM_API_HASH'
    if ($apiId -and $apiHash) {
        return [pscustomobject]@{ ApiId = $apiId; ApiHash = $apiHash }
    }
    $dpapi = Read-DpapiCredentials
    if ($dpapi) {
        return [pscustomobject]@{
            ApiId = [pscustomobject]@{ Value = $dpapi.ApiId; Source = $dpapi.Source }
            ApiHash = [pscustomobject]@{ Value = $dpapi.ApiHash; Source = $dpapi.Source }
        }
    }
    return $null
}

$pythonExe = Resolve-Python
$credentials = Resolve-Credentials
if (-not $credentials) {
    Write-Host 'No Telegram API credentials found. Starting local DPAPI setup.'
    if (-not (Test-Path -LiteralPath $SetupScript -PathType Leaf)) { exit 3 }
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $SetupScript
    if ($LASTEXITCODE -ne 0) { exit 3 }
    $credentials = Resolve-Credentials
}
if (-not $credentials) {
    Write-Host 'Telegram credential bootstrap failed safely.'
    exit 3
}

[Environment]::SetEnvironmentVariable('TELEGRAM_API_ID', $credentials.ApiId.Value, 'Process')
[Environment]::SetEnvironmentVariable('TELEGRAM_API_HASH', $credentials.ApiHash.Value, 'Process')
$sessionOverride = Get-EnvironmentSecret -Name 'TELEGRAM_SESSION_PATH'
if ($sessionOverride) {
    [Environment]::SetEnvironmentVariable('TELEGRAM_SESSION_PATH', $sessionOverride.Value, 'Process')
}

Write-Host '============================================================'
Write-Host 'FATHER Team Role - Telegram acquisition bootstrap'
Write-Host '============================================================'
Write-Host "Role: $($Role.ToUpperInvariant())"
Write-Host "Python: $pythonExe"
Write-Host "TELEGRAM_API_ID: SET [$($credentials.ApiId.Source)]"
Write-Host "TELEGRAM_API_HASH: SET [$($credentials.ApiHash.Source)]"
Write-Host 'Secret values are not printed.'
Write-Host ''

if (-not (Test-Path -LiteralPath $NetworkPreflightScript -PathType Leaf)) { exit 4 }
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $NetworkPreflightScript
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Network path is not proven reachable; team-role acquisition stopped before Telethon.'
    exit $LASTEXITCODE
}

$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"
if (-not (Test-Path -LiteralPath $TelethonAuthScript -PathType Leaf)) { exit 5 }
Write-Host ''
Write-Host '[AUTH] Checking shared local Telethon session...'
& $pythonExe $TelethonAuthScript
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Telethon authorization did not complete; role acquisition was not started.'
    exit $LASTEXITCODE
}

if (-not (Test-Path -LiteralPath $RunnerScript -PathType Leaf)) { exit 6 }
Write-Host ''
Write-Host "[ACQUIRE] Starting universal role acquisition for $($Role.ToUpperInvariant())."
& $pythonExe $RunnerScript --role $Role @RunnerArgs
exit $LASTEXITCODE
