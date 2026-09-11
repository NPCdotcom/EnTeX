# Create .cursor/ junctions to .agents/ for Cursor IDE compatibility.
# Run from project root OR from ~/.agents kit root.
param(
    [string]$Root = (Get-Location).Path
)

$Root = (Resolve-Path $Root).Path
$agentsSub = Join-Path $Root ".agents"
$kitRoot = if (Test-Path (Join-Path $Root "skills")) { $Root } else { $agentsSub }
$agentsDir = if (Test-Path (Join-Path $Root "skills")) { $Root } else { $agentsSub }

if (-not (Test-Path (Join-Path $agentsDir "skills"))) {
    Write-Error "Cannot find .agents kit (skills/ missing). Run from project root or ~/.agents"
    exit 1
}

$cursorDir = Join-Path $Root ".cursor"
New-Item -ItemType Directory -Force -Path $cursorDir | Out-Null

function Ensure-Junction {
    param([string]$Name)
    $target = Join-Path $agentsDir $Name
    $link = Join-Path $cursorDir $Name
    if (-not (Test-Path $target)) {
        Write-Warning "Skip $Name — target missing: $target"
        return
    }
    if (Test-Path $link) {
        Write-Host "Exists: $link"
        return
    }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "Linked: $link -> $target"
}

foreach ($dir in @("rules", "skills", "hooks")) {
    Ensure-Junction $dir
}

$hooksSrc = Join-Path $agentsDir "hooks.json"
$hooksDst = Join-Path $cursorDir "hooks.json"
if (Test-Path $hooksSrc) {
    Copy-Item $hooksSrc $hooksDst -Force
    Write-Host "Copied hooks.json -> $hooksDst"
}

Write-Host "Done. See docs/CURSOR_COMPAT.md"
