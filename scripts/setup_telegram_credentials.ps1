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
Write-Host 'API ID is read as a local numeric identifier; API HASH input stays hidden.'
Write-Host 'Values are never printed after entry and no plaintext credential file is created.'
Write-Host 'The encrypted payload can only be decrypted by this Windows user context.'
Write-Host 'do not paste them into chat.'
Write-Host ''

# Read API ID as ordinary local console text. Using -AsSecureString for a numeric
# identifier proved unreliable on Windows PowerShell in the live operator path.
# It is validated immediately, converted to SecureString for DPAPI persistence,
# and the plaintext variable is cleared after storage.
$apiIdPlain = (Read-Host 'Telegram API ID').Trim()
$parsedApiId = 0L
if ([string]::IsNullOrWhiteSpace($apiIdPlain) -or -not [long]::TryParse($apiIdPlain, [ref]$parsedApiId) -or $parsedApiId -le 0) {
    throw 'Telegram API ID must be a non-empty positive integer.'
}

$apiHashSecure = Read-Host 'Telegram API HASH' -AsSecureString
$apiHashPlain = Convert-SecureStringToPlainText -Secure $apiHashSecure
if ([string]::IsNullOrWhiteSpace($apiHashPlain)) {
    throw 'Telegram API HASH must not be empty.'
}

# Convert the already validated numeric identifier to SecureString only for
# DPAPI-backed persistence. No plaintext file is ever written.
$apiIdSecure = ConvertTo-SecureString $apiIdPlain -AsPlainText -Force

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
$parsedApiId = 0L

Write-Host ''
Write-Host 'Telegram credentials saved locally with Windows DPAPI.'
Write-Host "Store: $StorePath"
Write-Host 'No plaintext credential file was created.'
exit 0
