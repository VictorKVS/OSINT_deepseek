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
$TelethonAuthScript = Join-Path $RepoRoot 'scripts\authorize_telethon_session.py'

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

function Get-ScopedEnvironmentValue {
    param([Parameter(Mandatory = $true)][string] $Name)

    foreach ($scope in @('Process', 'User', 'Machine')) {
        $value = [Environment]::GetEnvironmentVariable($Name, $scope)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return [pscustomobject]@{ Value = $value.Trim(); Source = "WINDOWS_$($scope.ToUpperInvariant())_ENV" }
        }
    }
    return $null
}

function Read-DotEnvValue {
    param(
        [Parameter(Mandatory = $true)][string] $Path,
        [Parameter(Mandatory = $true)][string] $Name
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }

    foreach ($line in Get-Content -LiteralPath $Path -ErrorAction Stop) {
        $trimmed = $line.Trim()
        if (-not $trimmed -or $trimmed.StartsWith('#')) { continue }
        if ($trimmed.StartsWith('export ')) { $trimmed = $trimmed.Substring(7).Trim() }
        $prefix = "$Name="
        if (-not $trimmed.StartsWith($prefix, [StringComparison]::Ordinal)) { continue }
        $value = $trimmed.Substring($prefix.Length).Trim()
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        if (-not [string]::IsNullOrWhiteSpace($value)) { return $value }
    }
    return $null
}

function Convert-DpapiCipherToPlainText {
    param([Parameter(Mandatory = $true)][string] $CipherText)
    $secure = ConvertTo-SecureString $CipherText
    $credential = [PSCredential]::new('local', $secure)
    return $credential.GetNetworkCredential().Password
}

function Read-DpapiCredentials {
    if (-not (Test-Path -LiteralPath $DpapiStorePath -PathType Leaf)) { return $null }
    try {
        $payload = Get-Content -LiteralPath $DpapiStorePath -Raw -ErrorAction Stop | ConvertFrom-Json
        if ($payload.storage -ne 'WINDOWS_DPAPI_CURRENT_USER') { return $null }
        $apiId = Convert-DpapiCipherToPlainText -CipherText ([string]$payload.api_id_dpapi)
        $apiHash = Convert-DpapiCipherToPlainText -CipherText ([string]$payload.api_hash_dpapi)
        if ([string]::IsNullOrWhiteSpace($apiId) -or [string]::IsNullOrWhiteSpace($apiHash)) { return $null }
        return [pscustomobject]@{
            ApiId = $apiId
            ApiHash = $apiHash
            Source = 'WINDOWS_DPAPI_CURRENT_USER'
        }
    } catch {
        Write-Host 'DPAPI credential store exists but could not be decrypted in this Windows user context.'
        return $null
    }
}

function Resolve-SecretValue {
    param(
        [Parameter(Mandatory = $true)][string] $Name,
        [object] $DpapiCredentials
    )

    $scoped = Get-ScopedEnvironmentValue -Name $Name
    if ($scoped) { return $scoped }

    $dotenvCandidates = @(
        (Join-Path $RepoRoot '.env'),
        (Join-Path $RepoRoot 'legacy\telegram\.env'),
        (Join-Path $RepoRoot 'poc\tdlib\.env'),
        (Join-Path $RepoRoot '.runtime\telegram.env')
    )

    if ($env:FATHER_TDLIB_RUNTIME) {
        try {
            $runtimeParent = Split-Path -Parent ([IO.Path]::GetFullPath($env:FATHER_TDLIB_RUNTIME))
            if ($runtimeParent) {
                $dotenvCandidates += (Join-Path $runtimeParent '.env')
                $dotenvCandidates += (Join-Path $runtimeParent 'telegram.env')
            }
        } catch { }
    }

    $dotenvCandidates += 'G:\1\father-tdlib\.env'
    $dotenvCandidates += 'G:\1\father-tdlib\telegram.env'

    foreach ($path in ($dotenvCandidates | Select-Object -Unique)) {
        $value = Read-DotEnvValue -Path $path -Name $Name
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return [pscustomobject]@{ Value = $value; Source = "DOTENV:$path" }
        }
    }

    if ($DpapiCredentials) {
        if ($Name -eq 'TELEGRAM_API_ID') {
            return [pscustomobject]@{ Value = $DpapiCredentials.ApiId; Source = $DpapiCredentials.Source }
        }
        if ($Name -eq 'TELEGRAM_API_HASH') {
            return [pscustomobject]@{ Value = $DpapiCredentials.ApiHash; Source = $DpapiCredentials.Source }
        }
    }
    return $null
}

function Resolve-AllCredentials {
    $dpapi = Read-DpapiCredentials
    return [pscustomobject]@{
        ApiId = Resolve-SecretValue -Name 'TELEGRAM_API_ID' -DpapiCredentials $dpapi
        ApiHash = Resolve-SecretValue -Name 'TELEGRAM_API_HASH' -DpapiCredentials $dpapi
        Session = Get-ScopedEnvironmentValue -Name 'TELEGRAM_SESSION_PATH'
    }
}

$pythonExe = Resolve-Python
$credentials = Resolve-AllCredentials

if (-not $credentials.ApiId -or -not $credentials.ApiHash) {
    Write-Host '============================================================'
    Write-Host 'FATHER Architect - Telegram credential bootstrap'
    Write-Host '============================================================'
    Write-Host "Python: $pythonExe"
    Write-Host 'TELEGRAM_API_ID: MISSING'
    Write-Host 'TELEGRAM_API_HASH: MISSING'
    Write-Host 'Secret values are not printed or persisted by this bootstrap.'
    Write-Host 'No saved credentials were found. Starting one-time local DPAPI setup.'
    Write-Host 'Values will be entered only in this PowerShell window and will not be printed.'
    Write-Host 'do not paste them into chat'
    Write-Host ''

    if (-not (Test-Path -LiteralPath $SetupScript -PathType Leaf)) {
        Write-Host 'Credential setup script is missing.'
        exit 3
    }

    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $SetupScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Credential setup did not complete; Telegram acquisition was not started.'
        exit 3
    }
    $credentials = Resolve-AllCredentials
}

$apiId = $credentials.ApiId
$apiHash = $credentials.ApiHash
$sessionOverride = $credentials.Session

if (-not $apiId -or -not $apiHash) {
    Write-Host 'Credential bootstrap failed safely after local setup.'
    exit 3
}

[Environment]::SetEnvironmentVariable('TELEGRAM_API_ID', $apiId.Value, 'Process')
[Environment]::SetEnvironmentVariable('TELEGRAM_API_HASH', $apiHash.Value, 'Process')
if ($sessionOverride) {
    [Environment]::SetEnvironmentVariable('TELEGRAM_SESSION_PATH', $sessionOverride.Value, 'Process')
}

Write-Host '============================================================'
Write-Host 'FATHER Architect - Telegram credential bootstrap'
Write-Host '============================================================'
Write-Host "Python: $pythonExe"
Write-Host "TELEGRAM_API_ID: SET [$($apiId.Source)]"
Write-Host "TELEGRAM_API_HASH: SET [$($apiHash.Source)]"
Write-Host 'Secret values are not printed or persisted by this bootstrap.'
Write-Host 'When local setup is used, only DPAPI-encrypted ciphertext is stored under .runtime.'
Write-Host ''

if (-not (Test-Path -LiteralPath $NetworkPreflightScript -PathType Leaf)) {
    Write-Host 'Telegram network preflight script is missing; acquisition will not start blindly.'
    exit 4
}

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $NetworkPreflightScript
$networkRc = $LASTEXITCODE
if ($networkRc -ne 0) {
    Write-Host ''
    Write-Host 'Telegram acquisition stopped before Telethon connection retries because the network path is not proven reachable.'
    Write-Host 'Review reports\architect_telegram\LATEST_TELEGRAM_NETWORK_DIAGNOSTIC.json.'
    exit $networkRc
}

$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"

if (-not (Test-Path -LiteralPath $TelethonAuthScript -PathType Leaf)) {
    Write-Host 'Telethon session authorization helper is missing; acquisition will not start with an unaudited session.'
    exit 5
}

Write-Host ''
Write-Host '[AUTH] Checking local Telethon session...'
& $pythonExe $TelethonAuthScript
$authRc = $LASTEXITCODE
if ($authRc -ne 0) {
    Write-Host ''
    Write-Host 'Telethon session authorization did not complete; acquisition was not started.'
    exit $authRc
}

Write-Host ''
Write-Host '[ACQUIRE] Telethon session is authorized. Starting Architect acquisition.'
& $pythonExe (Join-Path $RepoRoot 'scripts\run_architect_telegram_acquisition.py') @RunnerArgs
exit $LASTEXITCODE
