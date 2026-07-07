$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$sourceSkills = Join-Path $repoRoot "codex-backup\skills"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$targetSkills = Join-Path $codexHome "skills"

if (-not (Test-Path -LiteralPath $sourceSkills)) {
    throw "Cannot find backup skills folder: $sourceSkills"
}

New-Item -ItemType Directory -Force -Path $targetSkills | Out-Null
Copy-Item -LiteralPath (Join-Path $sourceSkills "*") -Destination $targetSkills -Recurse -Force

Write-Host "Codex skills/agents restored to $targetSkills"
Write-Host "Restart Codex to load restored skills."
Write-Host "Reinstall remote plugins from Codex on this computer if needed."
