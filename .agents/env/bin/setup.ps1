# Create agent env: Python venv + optional Node deps.
# Run from kit root or any cwd (resolves kit via script location).
$ErrorActionPreference = "Stop"
$KitRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$PyDir = Join-Path $KitRoot "env\python"
$Venv = Join-Path $PyDir ".venv"
$Req = Join-Path $PyDir "requirements.txt"

Write-Host "Kit: $KitRoot"

if (-not (Test-Path $Venv)) {
    python -m venv $Venv
    Write-Host "Created venv: $Venv"
}

& (Join-Path $Venv "Scripts\python.exe") -m pip install --upgrade pip
& (Join-Path $Venv "Scripts\pip.exe") install -r $Req

$NodePkg = Join-Path $KitRoot "env\node\package.json"
if ((Get-Command npm -ErrorAction SilentlyContinue) -and (Test-Path $NodePkg)) {
    Push-Location (Join-Path $KitRoot "env\node")
    $pkg = Get-Content package.json -Raw | ConvertFrom-Json
    if ($pkg.dependencies.PSObject.Properties.Count -gt 0) {
        npm install
        Write-Host "Node deps installed"
    } else {
        Write-Host "Node: no dependencies — skip npm install"
    }
    Pop-Location
} else {
    Write-Host "Node: skipped (npm missing or no package.json)"
}

Write-Host "Done. Test: python env\bin\agents-run.py maintain-adhoc audit-skill-layout skills"
