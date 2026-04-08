param(
  [int]$Port = 8000
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
$backendDir = Join-Path $repoRoot "apps\backend"

if (-not (Test-Path $python)) {
  Write-Error "Python venv not found at $python"
  exit 1
}

Push-Location $backendDir
try {
  & $python -m uvicorn app.main:app --reload --port $Port
}
finally {
  Pop-Location
}

