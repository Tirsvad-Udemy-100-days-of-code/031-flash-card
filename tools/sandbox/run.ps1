<#
.SYNOPSIS
  Start the Windows Sandbox smoke test of dist\flash-card.exe from the host.

.DESCRIPTION
  Writes a configuration from flash-card.wsb with absolute paths, starts
  Windows Sandbox, waits for out\result.json and prints the summary.
  The tests themselves (window, click, progress file) run inside the sandbox
  with the sandbox's own mouse; the host's mouse and focus are not used.
  Windows Sandbox shows its own window while it runs. Needs Windows 11 Pro
  with the feature "Windows Sandbox" enabled.

.EXAMPLE
  powershell -File tools\sandbox\run.ps1 -Runs 5
#>
param(
    [int]$Runs = 5,
    [int]$TimeoutMinutes = 15
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$dist = Join-Path $root 'dist'
$scripts = $PSScriptRoot
$out = Join-Path $root 'build\sandbox-out'

if (-not (Test-Path (Join-Path $dist 'flash-card.exe'))) {
    throw "dist\flash-card.exe not found: build it first with python tools\build_executable.py"
}
if (-not (Get-Command WindowsSandbox.exe -ErrorAction SilentlyContinue)) {
    throw "WindowsSandbox.exe not found: enable the Windows feature 'Windows Sandbox' (Windows 11 Pro)"
}
if (Get-Process -Name 'WindowsSandbox*' -ErrorAction SilentlyContinue) {
    throw "A Windows Sandbox is already running: close it first (only one can run at a time)"
}

Remove-Item $out -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $out -Force | Out-Null

$config = (Get-Content (Join-Path $scripts 'flash-card.wsb') -Raw) `
    -replace '@DIST@', $dist -replace '@SCRIPTS@', $scripts -replace '@OUT@', $out -replace '@RUNS@', $Runs
$wsb = Join-Path $out 'run.wsb'
Set-Content -Path $wsb -Value $config -Encoding UTF8

Write-Host "Starting Windows Sandbox ($Runs runs); results in $out"
Start-Process -FilePath WindowsSandbox.exe -ArgumentList "`"$wsb`""

$result = Join-Path $out 'result.json'
$end = (Get-Date).AddMinutes($TimeoutMinutes)
while ((Get-Date) -lt $end -and -not (Test-Path $result)) { Start-Sleep -Seconds 5 }
if (-not (Test-Path $result)) { throw "No result.json after $TimeoutMinutes minutes" }
Start-Sleep -Seconds 3
$summary = Get-Content $result -Raw | ConvertFrom-Json
Write-Host ("passed {0} of {1} runs in {2}" -f $summary.passed, $summary.runs, $summary.os)
$summary.results | Format-Table run, window, clicked, progress_rows, ok, seconds
if ($summary.passed -ne $summary.runs) { exit 1 }
