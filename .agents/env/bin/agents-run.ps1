#Requires -Version 5.1
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python not found"; exit 127 }
& $py.Source (Join-Path $PSScriptRoot "agents-run.py") @Args
exit $LASTEXITCODE
