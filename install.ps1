# Installs the faceless-video skills + agents for Claude Code and the vetted third-party YouTube skills.
# No API key: the agents run on the Claude subscription through Claude Code's Agent tool.
#   powershell -ExecutionPolicy Bypass -File install.ps1          # keeps skills already installed
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Force   # overwrites them with the repo version
param([switch]$Force)
$ErrorActionPreference = 'Stop'
$repo   = $PSScriptRoot
$skills = Join-Path $HOME '.claude\skills'
$agents = Join-Path $HOME '.claude\agents'
New-Item -ItemType Directory -Force $skills, $agents | Out-Null

Get-ChildItem "$repo\skills" -Directory | ForEach-Object {
    if ((Test-Path "$skills\$($_.Name)") -and -not $Force) {
        Write-Host "skill  $($_.Name) already installed, kept (-Force to overwrite)"; return
    }
    Copy-Item $_.FullName $skills -Recurse -Force
    Write-Host "skill  $($_.Name)"
}
Copy-Item "$repo\agents\*.md" $agents -Force
Write-Host "agents $((Get-ChildItem "$repo\agents\*.md").Count) -> $agents"

# Third-party skills, pinned to a reviewed commit (see README, "Third-party skills").
# yt-edit is kept because yt-chapters and yt-retention import its parser.
$vendor = @{
    url    = 'https://github.com/Jakeschincariol/youtube-agent-skill'
    commit = 'a2feb2104981a375ffd4f87ee04f4f5344ac43c6'
    keep   = 'yt-script', 'yt-package', 'yt-seo', 'yt-chapters', 'yt-retention', 'yt-shorts', 'yt-edit'
}
$tmp = Join-Path $env:TEMP "yt-agent-skill-$(Get-Random)"
git clone -q $vendor.url $tmp
git -C $tmp checkout -q $vendor.commit
foreach ($s in $vendor.keep) {
    Copy-Item "$tmp\skills\$s" $skills -Recurse -Force
    Write-Host "skill  $s (youtube-agent-skill @ $($vendor.commit.Substring(0,7)))"
}
Remove-Item $tmp -Recurse -Force

Write-Host "`nDone. Start a new Claude Code session to load the skills."
