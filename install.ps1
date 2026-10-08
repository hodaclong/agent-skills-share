# Cài bộ skill trên Windows. Dùng: powershell -ExecutionPolicy Bypass -File install.ps1 [all|claude|agents]
param([string]$Target = "all")
$ErrorActionPreference = "Stop"

$Src = Join-Path $PSScriptRoot "skills"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Backup = Join-Path $HOME ".agent-skills-backup\$Stamp"

switch ($Target) {
    "all"    { $Dests = @("$HOME\.agents\skills", "$HOME\.claude\skills") }
    "claude" { $Dests = @("$HOME\.claude\skills") }
    "agents" { $Dests = @("$HOME\.agents\skills") }
    default  { throw "Tham so khong hop le: $Target (all|claude|agents)" }
}

foreach ($Dest in $Dests) {
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $Count = 0
    Get-ChildItem -Directory $Src | ForEach-Object {
        $Existing = Join-Path $Dest $_.Name
        if (Test-Path $Existing) {
            $Bk = Join-Path $Backup (Split-Path (Split-Path $Dest -Parent) -Leaf)
            New-Item -ItemType Directory -Force -Path $Bk | Out-Null
            Move-Item $Existing (Join-Path $Bk $_.Name)
        }
        Copy-Item -Recurse $_.FullName $Existing
        $Count++
    }
    Write-Host "Da cai $Count skill vao $Dest"
}
if (Test-Path $Backup) { Write-Host "Skill cu trung ten da sao luu tai: $Backup" }
Write-Host "Khoi dong lai Claude Code / Codex / DSH de nhan skill moi."
