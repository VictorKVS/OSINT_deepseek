param(
    [string]$Repo = "VictorKVS/OSINT_deepseek",
    [string]$ArtifactNamePrefix = "fstec-official-recovery-"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Bundle = Join-Path $Root "fstec-official-recovery.zip"
$TmpDir = Join-Path $Root ".tmp-fstec-recovery-download"
if (Test-Path $TmpDir) { Remove-Item -Recurse -Force $TmpDir }
New-Item -ItemType Directory -Path $TmpDir | Out-Null

function Get-LatestArtifactFromApi {
    $uri = "https://api.github.com/repos/$Repo/actions/artifacts?per_page=100"
    $headers = @{ "User-Agent" = "FATHER-Security-Recovery/1.0"; "Accept" = "application/vnd.github+json" }
    if ($env:GH_TOKEN) { $headers["Authorization"] = "Bearer $($env:GH_TOKEN)" }
    elseif ($env:GITHUB_TOKEN) { $headers["Authorization"] = "Bearer $($env:GITHUB_TOKEN)" }
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    return $response.artifacts |
        Where-Object { -not $_.expired -and $_.name -like "$ArtifactNamePrefix*" } |
        Sort-Object created_at -Descending |
        Select-Object -First 1
}

$artifact = $null
try {
    $artifact = Get-LatestArtifactFromApi
} catch {
    Write-Host "[WARN] Artifact listing through GitHub API failed: $($_.Exception.Message)"
}

$downloaded = $false
if ($artifact) {
    Write-Host "[INFO] Latest artifact: $($artifact.name) id=$($artifact.id)"
    $downloadUri = "https://api.github.com/repos/$Repo/actions/artifacts/$($artifact.id)/zip"
    $headers = @{ "User-Agent" = "FATHER-Security-Recovery/1.0"; "Accept" = "application/vnd.github+json" }
    if ($env:GH_TOKEN) { $headers["Authorization"] = "Bearer $($env:GH_TOKEN)" }
    elseif ($env:GITHUB_TOKEN) { $headers["Authorization"] = "Bearer $($env:GITHUB_TOKEN)" }
    try {
        Invoke-WebRequest -Uri $downloadUri -Headers $headers -MaximumRedirection 10 -OutFile $Bundle
        if ((Test-Path $Bundle) -and ((Get-Item $Bundle).Length -gt 0)) { $downloaded = $true }
    } catch {
        Write-Host "[WARN] Direct artifact download failed: $($_.Exception.Message)"
    }
}

if (-not $downloaded) {
    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $gh) {
        throw "Could not download the Actions artifact anonymously and GitHub CLI 'gh' is not installed. Install/authenticate gh or set GH_TOKEN/GITHUB_TOKEN, then rerun."
    }
    Write-Host "[INFO] Falling back to GitHub CLI..."
    if (-not $artifact) {
        $json = gh api "repos/$Repo/actions/artifacts?per_page=100"
        if ($LASTEXITCODE -ne 0) { throw "gh api failed while listing artifacts" }
        $payload = $json | ConvertFrom-Json
        $artifact = $payload.artifacts |
            Where-Object { -not $_.expired -and $_.name -like "$ArtifactNamePrefix*" } |
            Sort-Object created_at -Descending |
            Select-Object -First 1
        if (-not $artifact) { throw "No non-expired FSTEC recovery artifact found" }
    }

    $runId = $artifact.workflow_run.id
    if (-not $runId) { throw "Artifact workflow run id is missing" }
    if (Test-Path $TmpDir) { Remove-Item -Recurse -Force $TmpDir }
    New-Item -ItemType Directory -Path $TmpDir | Out-Null

    gh run download $runId --repo $Repo -n $artifact.name -D $TmpDir
    if ($LASTEXITCODE -ne 0) { throw "gh run download failed" }
    $downloadedFiles = Get-ChildItem -Path $TmpDir -Recurse -File
    if (-not $downloadedFiles) { throw "gh run download returned no files" }
    if (Test-Path $Bundle) { Remove-Item -Force $Bundle }
    Compress-Archive -Path (Join-Path $TmpDir "*") -DestinationPath $Bundle -Force
    if (-not (Test-Path $Bundle) -or (Get-Item $Bundle).Length -eq 0) {
        throw "gh artifact packaging failed"
    }
    $downloaded = $true
}

Write-Host "[PASS] Bundle downloaded: $Bundle"
$cmd = Join-Path $Root "IMPORT_FSTEC_RECOVERY_BUNDLE.cmd"
& $cmd $Bundle
$rc = $LASTEXITCODE

if (Test-Path $TmpDir) { Remove-Item -Recurse -Force $TmpDir }
exit $rc
