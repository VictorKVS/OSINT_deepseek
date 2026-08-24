param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $RunnerArgs
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

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

function Resolve-SecretValue {
    param([Parameter(Mandatory = $true)][string] $Name)

    $scoped = Get-ScopedEnvironmentValue -Name $Name
    if ($scoped) { return $scoped }

    $dotenvCandidates = @(
        (Join-Path $RepoRoot '.env'),
        (Join-Path $RepoRoot 'legacy\telegram\.env'),
        (Join-Path $RepoRoot 'poc\tdlib\.env'),
        (Join-Path $RepoRoot '.runtime\telegram.env')
    )

    # Known local TDLib workspace convention; files are read locally only and
    # values are never written to Git or printed.
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
    return $null
}

$pythonExe = Resolve-Python
$apiId = Resolve-SecretValue -Name 'TELEGRAM_API_ID'
$apiHash = Resolve-SecretValue -Name 'TELEGRAM_API_HASH'
$sessionOverride = Get-ScopedEnvironmentValue -Name 'TELEGRAM_SESSION_PATH'

if ($apiId) {
    [Environment]::SetEnvironmentVariable('TELEGRAM_API_ID', $apiId.Value, 'Process')
}
if ($apiHash) {
    [Environment]::SetEnvironmentVariable('TELEGRAM_API_HASH', $apiHash.Value, 'Process')
}
if ($sessionOverride) {
    [Environment]::SetEnvironmentVariable('TELEGRAM_SESSION_PATH', $sessionOverride.Value, 'Process')
}

$apiIdStatus = if ($apiId) { 'SET' } else { 'MISSING' }
$apiHashStatus = if ($apiHash) { 'SET' } else { 'MISSING' }
$apiIdSource = if ($apiId) { $apiId.Source } else { 'NONE' }
$apiHashSource = if ($apiHash) { $apiHash.Source } else { 'NONE' }

Write-Host '============================================================'
Write-Host 'FATHER Architect - Telegram credential bootstrap'
Write-Host '============================================================'
Write-Host "Python: $pythonExe"
Write-Host "TELEGRAM_API_ID: $apiIdStatus [$apiIdSource]"
Write-Host "TELEGRAM_API_HASH: $apiHashStatus [$apiHashSource]"
Write-Host 'Secret values are not printed or persisted by this bootstrap.'
Write-Host ''

if (-not $apiId -or -not $apiHash) {
    Write-Host 'Credential bootstrap failed safely.'
    Write-Host 'Checked: Process/User/Machine environment and local gitignored .env candidates.'
    Write-Host 'If the credentials only exist in another old PowerShell process, set them locally in this shell or save them to the repo .env file; do not paste them into chat.'
    exit 3
}

$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"
& $pythonExe (Join-Path $RepoRoot 'scripts\run_architect_telegram_acquisition.py') @RunnerArgs
exit $LASTEXITCODE
