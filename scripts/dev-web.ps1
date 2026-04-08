param(
  [int]$Port = 3000
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$webDir = Join-Path $repoRoot "apps\web"

Push-Location $webDir
try {
  $env:PORT = "$Port"
  npm run dev
}
finally {
  Pop-Location
}

