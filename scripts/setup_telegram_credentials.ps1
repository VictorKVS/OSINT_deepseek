param(
    [switch] $Force
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$StoreDir = Join-Path $RepoRoot '.runtime\telegram'
$StorePath = Join-Path $StoreDir 'credentials.dpapi.json'

function Convert-SecureStringToPlainText {
    param([Parameter(Mandatory = $true)][Security.SecureString] $Secure)
    $credential = [PSCredential]::new('local', $Secure)
    return $credential.GetNetworkCredential().Password
}

if ((Test-Path -LiteralPath $StorePath -PathType Leaf) -and -not $Force) {
    Write-Host "Encrypted Telegram credential store already exists: $StorePath"
    Write-Host 'Use -Force only if you intentionally want to replace it.'
    exit 0
}

Write-Host '============================================================'
Write-Host 'FATHER Telegram local credential setup (Windows DPAPI)'
Write-Host '============================================================'
Write-Host 'Values are entered locally and are never printed.'
Write-Host 'The encrypted payload can only be decrypted by this Windows user context.'
Write-Host ''

$apiIdSecure = Read-Host 'Telegram API ID' -AsSecureString
$apiHashSecure = Read-Host 'Telegram API HASH' -AsSecureString

$apiIdPlain = Convert-SecureStringToPlainText -Secure $apiIdSecure
$apiHashPlain = Convert-SecureStringToPlainText -Secure $apiHashSecure

if ([string]::IsNullOrWhiteSpace($apiIdPlain) -or $apiIdPlain -notmatch '^\d+$') {
    throw 'Telegram API ID must be a non-empty integer.'
}
if ([string]::IsNullOrWhiteSpace($apiHashPlain)) {
    throw 'Telegram API HASH must not be empty.'
}

New-Item -ItemType Directory -Force -Path $StoreDir | Out-Null

$payload = [ordered]@{
    schema_version = '1.0'
    storage = 'WINDOWS_DPAPI_CURRENT_USER'
    created_at = [DateTimeOffset]::UtcNow.ToString('o')
    api_id_dpapi = ConvertFrom-SecureString $apiIdSecure
    api_hash_dpapi = ConvertFrom-SecureString $apiHashSecure
}

$json = $payload | ConvertTo-Json -Depth 4
[IO.File]::WriteAllText($StorePath, $json + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))

# Best-effort ACL hardening. DPAPI remains the confidentiality boundary even if ACL hardening is unavailable.
try {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    & icacls.exe $StorePath /inheritance:r /grant:r "${currentUser}:(R,W)" *> $null
} catch {
    Write-Host 'Warning: ACL hardening was not applied; DPAPI encryption is still active.'
}

# Remove plaintext variables from this PowerShell scope as soon as validation/storage completes.
$apiIdPlain = $null
$apiHashPlain = $null

Write-Host ''
Write-Host 'Telegram credentials saved locally with Windows DPAPI.'
Write-Host "Store: $StorePath"
Write-Host 'No plaintext credential file was created.'
exit 0
