param(
    [string]$DocumentId = "DOC-RU-FZ-152-2006",
    [int]$TimeoutSeconds = 180
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Profiles = @{
    "DOC-RU-FZ-152-2006" = @("152-ФЗ", "О персональных данных")
    "DOC-RU-PP-1119-2012" = @("1119", "персональных данных")
    "DOC-RU-FSTEC-21-2013" = @("21", "персональных данных", "ФСТЭК")
    "DOC-RU-FSB-378-2014" = @("378", "криптограф", "персональных данных")
}

if (-not $Profiles.ContainsKey($DocumentId)) {
    Write-Error "Unsupported DocumentId: $DocumentId"
    exit 2
}

$OutputDir = Join-Path $RepoRoot "data\operator_import\garant_timeline"
$OutputPath = Join-Path $OutputDir ($DocumentId + ".txt")
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

function Normalize-Text([string]$Value) {
    if ($null -eq $Value) { return "" }
    return (($Value.ToLowerInvariant().Replace("ё", "е") -replace "\s+", " ").Trim())
}

function Count-Text([string]$Text, [string]$Needle) {
    if ([string]::IsNullOrEmpty($Text) -or [string]::IsNullOrEmpty($Needle)) { return 0 }
    return [regex]::Matches($Text, [regex]::Escape($Needle), [System.Text.RegularExpressions.RegexOptions]::IgnoreCase).Count
}

$Markers = $Profiles[$DocumentId]
$Baseline = [string](Get-Clipboard -Raw -ErrorAction SilentlyContinue)
$Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$LastRejectedHash = ""

Write-Host "============================================================"
Write-Host "FATHER Knowledge Factory - GARANT CLIPBOARD CAPTURE"
Write-Host "Document: $DocumentId"
Write-Host "============================================================"
Write-Host ""
Write-Host "1. Keep this PowerShell window waiting."
Write-Host "2. Switch to the GARANT browser tab."
Write-Host "3. Open the document page / amendment information you want to capture."
Write-Host "4. Press Ctrl+A, then Ctrl+C in the browser."
Write-Host "5. Do NOT copy any other command afterwards. This watcher saves automatically."
Write-Host ""
Write-Host "Waiting up to $TimeoutSeconds seconds for a new clipboard capture..."

while ((Get-Date) -lt $Deadline) {
    Start-Sleep -Milliseconds 350
    $Current = [string](Get-Clipboard -Raw -ErrorAction SilentlyContinue)
    if ([string]::IsNullOrWhiteSpace($Current)) { continue }
    if ($Current -eq $Baseline) { continue }

    $Normalized = Normalize-Text $Current
    $Missing = @()
    foreach ($Marker in $Markers) {
        $NormalizedMarker = Normalize-Text $Marker
        if (-not $Normalized.Contains($NormalizedMarker)) {
            $Missing += $Marker
        }
    }

    $Bytes = [System.Text.Encoding]::UTF8.GetBytes($Current)
    $Sha = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($Bytes)).Replace("-", "").ToLowerInvariant()

    if ($Current.Length -lt 1000 -or $Missing.Count -gt 0) {
        if ($Sha -ne $LastRejectedHash) {
            Write-Host "Clipboard changed, but capture was rejected. chars=$($Current.Length); missing_markers=$($Missing -join ', ')"
            Write-Host "Copy the GARANT document page again; watcher is still waiting."
            $LastRejectedHash = $Sha
        }
        continue
    }

    $Utf8Bom = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText($OutputPath, $Current, $Utf8Bom)

    $ChangeHeading = Count-Text $Normalized "в настоящий документ внесены изменения"
    $CompactHistory = Count-Text $Normalized "с изменениями и дополнениями от"
    $EffectivePhrase = Count-Text $Normalized "изменения вступают в силу"
    $FederalLaw = Count-Text $Normalized "федеральный закон от"
    $FutureEdition = Count-Text $Normalized "будущую редакцию"

    Write-Host ""
    Write-Host "CAPTURE_SAVED"
    Write-Host "path=$OutputPath"
    Write-Host "chars=$($Current.Length)"
    Write-Host "sha256=$Sha"
    Write-Host "identity_markers=PASS"
    Write-Host "change_heading=$ChangeHeading"
    Write-Host "compact_history=$CompactHistory"
    Write-Host "effective_phrase=$EffectivePhrase"
    Write-Host "federal_law=$FederalLaw"
    Write-Host "future_edition=$FutureEdition"

    if ($EffectivePhrase -eq 0) {
        Write-Host ""
        Write-Warning "Document identity is valid, but detailed amendment/effective-rule metadata is not visible in this capture. Open GARANT 'ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ' / amendment history and run this capture again."
    } else {
        Write-Host "timeline_detail_candidate=YES"
    }
    exit 0
}

Write-Error "Timed out waiting for a valid GARANT clipboard capture."
exit 2
