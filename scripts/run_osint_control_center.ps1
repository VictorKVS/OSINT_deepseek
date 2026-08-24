$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Store = Join-Path $RepoRoot '.runtime\telegram\credentials.dpapi.json'
$Python = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { $Python = (Get-Command python).Source }
$App = Join-Path $RepoRoot 'osint_web\app.py'
$Url = 'http://127.0.0.1:8765/'
$HealthUrl = 'http://127.0.0.1:8765/api/overview'

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

if (-not (Test-Path -LiteralPath $App -PathType Leaf)) {
    throw "OSINT Control Center app is missing: $App"
}

Write-Host '[WEB] Starting local server...'
$server = Start-Process -FilePath $Python -ArgumentList @($App) -WorkingDirectory $RepoRoot -PassThru -NoNewWindow

$ready = $false
for ($i = 0; $i -lt 40; $i++) {
    if ($server.HasExited) { break }
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $HealthUrl -TimeoutSec 1
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch { }
    Start-Sleep -Milliseconds 250
}

if (-not $ready) {
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host '[WEB] FAILED: local server did not become healthy on 127.0.0.1:8765.'
    Write-Host 'Diagnostic commands:'
    Write-Host '  Test-NetConnection 127.0.0.1 -Port 8765'
    Write-Host '  .\.venv\Scripts\python.exe .\osint_web\app.py'
    exit 7
}

Write-Host '[WEB] READY: http://127.0.0.1:8765/'
Write-Host '[WEB] Opening browser...'
Start-Process $Url
Write-Host '[WEB] Server is running. Close this window or press Ctrl+C to stop it.'

try {
    Wait-Process -Id $server.Id
} finally {
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
    }
}
exit $server.ExitCode
