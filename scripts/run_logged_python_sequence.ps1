param(
    [Parameter(Mandatory = $true)]
    [string]$RunId,

    [Parameter(Mandatory = $true)]
    [string]$Title,

    [Parameter(Mandatory = $true)]
    [string]$PythonExe,

    [Parameter(Mandatory = $true)]
    [string]$Scripts,

    [Parameter(Mandatory = $true)]
    [string]$SuccessMessage,

    [Parameter(Mandatory = $true)]
    [string]$FailureMessage
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$logDir = Join-Path $repoRoot "reports\pdn_live\run_logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

$safeRunId = ($RunId -replace '[^A-Za-z0-9_.-]', '_')
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$archiveLog = Join-Path $logDir ("{0}-{1}.txt" -f $safeRunId, $stamp)
$latestRunLog = Join-Path $logDir "LATEST_RUN.txt"
$latestNamedLog = Join-Path $logDir ("LATEST_{0}.txt" -f $safeRunId)

function Get-RepoRelativePath {
    param([Parameter(Mandatory = $true)][string]$Path)
    $prefix = $repoRoot.TrimEnd('\') + '\'
    if ($Path.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $Path.Substring($prefix.Length)
    }
    return $Path
}

Set-Content -LiteralPath $archiveLog -Value "" -Encoding UTF8

function Write-RunLine {
    param([AllowEmptyString()][string]$Text = "")
    Write-Output $Text
    Add-Content -LiteralPath $archiveLog -Value $Text -Encoding UTF8
}

$gitHead = "unknown"
try {
    $gitHead = (& git log -1 --format="%h %s" 2>$null | Out-String).Trim()
} catch {
    $gitHead = "unavailable"
}

Write-RunLine "============================================================"
Write-RunLine $Title
Write-RunLine "============================================================"
Write-RunLine ("RUN_ID={0}" -f $RunId)
Write-RunLine ("STARTED_LOCAL={0}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"))
Write-RunLine ("GIT_HEAD={0}" -f $gitHead)
Write-RunLine ("PYTHON_EXE={0}" -f $PythonExe)
Write-RunLine ("LOG_ARCHIVE={0}" -f (Get-RepoRelativePath -Path $archiveLog))
Write-RunLine ""

$overallRc = 0
$scriptList = @($Scripts -split ';' | Where-Object { $_ -and $_.Trim() })
if ($scriptList.Count -eq 0) {
    Write-RunLine "FAIL: no Python scripts were configured for this runner."
    $overallRc = 2
} else {
    foreach ($scriptPath in $scriptList) {
        $scriptPath = $scriptPath.Trim()
        Write-RunLine ("--- BEGIN {0} ---" -f $scriptPath)
        & $PythonExe $scriptPath 2>&1 | ForEach-Object {
            $line = $_.ToString()
            Write-RunLine $line
        }
        $rc = $LASTEXITCODE
        if ($null -eq $rc) { $rc = 0 }
        Write-RunLine ("--- END {0} EXIT_CODE={1} ---" -f $scriptPath, $rc)
        Write-RunLine ""
        if ($rc -ne 0) {
            $overallRc = [int]$rc
            break
        }
    }
}

if ($overallRc -eq 0) {
    Write-RunLine ("PASS: {0}" -f $SuccessMessage)
} else {
    Write-RunLine ("FAIL: {0}" -f $FailureMessage)
}
Write-RunLine ("FINISHED_LOCAL={0}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"))
Write-RunLine ("EXIT_CODE={0}" -f $overallRc)

Copy-Item -LiteralPath $archiveLog -Destination $latestNamedLog -Force
Copy-Item -LiteralPath $archiveLog -Destination $latestRunLog -Force

Write-Output ""
Write-Output ("FULL_LOG={0}" -f (Get-RepoRelativePath -Path $archiveLog))
Write-Output ("LATEST_LOG={0}" -f (Get-RepoRelativePath -Path $latestRunLog))
Write-Output "Upload reports\pdn_live\run_logs\LATEST_RUN.txt here instead of copying the console output."

exit $overallRc
