# One Hermes profile per production role. Each profile gets the agent brief of agents/<role>.md as its
# SOUL.md, reads skills from ~/.claude/skills (same files Claude Code uses), and preloads its own skills.
# Call a role from the orchestrator:   hermes -p <role> -z --query-file brief.txt
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent

# role = skills preloaded for that role (comma-separated, empty = none)
$team = [ordered]@{
    'story-architect'      = 'yt-script'
    'character-designer'   = ''
    'fact-checker'         = ''
    'visual-director'      = 'hand-drawn-visuals'
    'image-qc'             = ''
    'packaging-strategist' = 'yt-package,yt-seo,yt-chapters,yt-script'
}

$existing = hermes profile list 2>$null | Out-String
foreach ($role in $team.Keys) {
    $file = "$repo\agents\$role.md"
    $raw  = Get-Content $file -Raw -Encoding utf8
    $desc = [regex]::Match($raw, '(?m)^description:\s*(.+)$').Groups[1].Value
    $body = [regex]::Replace($raw, '(?s)\A---.*?---\s*', '')   # drop the Claude Code frontmatter

    if ($existing -notmatch "(?m)\b$([regex]::Escape($role))\b") {
        hermes profile create $role --clone --description $desc | Out-Null
    }
    $soul = $body
    if ($team[$role]) { $soul += "`n`nSkills to load before working: $($team[$role]). Skills live in ~/.claude/skills.`n" }
    Set-Content "$env:LOCALAPPDATA\hermes\profiles\$role\SOUL.md" $soul -Encoding utf8
    hermes -p $role config set skills.external_dirs '["~/.claude/skills"]' | Out-Null
    Write-Host "hermes profile  $role  skills: $(if ($team[$role]) { $team[$role] } else { '-' })"
}
Write-Host "Team ready. Test: hermes -p fact-checker -z 'Is the Mariana Trench 10,994 m deep? One line with source.'"
