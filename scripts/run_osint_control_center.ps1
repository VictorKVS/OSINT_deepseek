$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Store = Join-Path $RepoRoot '.runtime\telegram\credentials.dpapi.json'
$Python = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { $Python = (Get-Command python).Source }

function Unprotect([string]$cipher) {
    $secure = ConvertTo-SecureString $cipher
    $cred = [PSCredential]::new('local', $secure)
    return $cred.GetNetworkCredential().Password
}

if (-not $env:TELEGRAM_API_ID -or -not $env:TELEGRAM_API_HASH) {
    if (-not (Test-Path $Store)) { throw 'Telegram DPAPI store is missing. Run the Telegram setup first.' }
    $payload = Get-Content $Store -Raw | ConvertFrom-Json
    if ($payload.storage -ne 'WINDOWS_DPAPI_CURRENT_USER') { throw 'Unsupported Telegram credential store.' }
    $env:TELEGRAM_API_ID = Unprotect ([string]$payload.api_id_dpapi)
    $env:TELEGRAM_API_HASH = Unprotect ([string]$payload.api_hash_dpapi)
}

Write-Host '============================================================'
Write-Host 'FATHER OSINT Control Center'
Write-Host '============================================================'
Write-Host "Python: $Python"
Write-Host 'Credentials: SET (values hidden)'
Write-Host 'Binding: 127.0.0.1:8765 (local only)'
Write-Host ''

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RepoRoot 'scripts\test_telegram_network_path.ps1')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"
& $Python (Join-Path $RepoRoot 'scripts\authorize_telethon_session.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Start-Process 'http://127.0.0.1:8765/'
& $Python (Join-Path $RepoRoot 'osint_web\app.py')
exit $LASTEXITCODE
