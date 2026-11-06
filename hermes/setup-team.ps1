# One Hermes profile per production role, built to spend as few tokens as possible per call:
#  - only the role's own skills in the profile (no bundled catalogue, no ~/.claude/skills index:
#    every listed skill costs its description in the system prompt of every call);
#  - a model sized to the job (cheap for rule-following roles, stronger for research and vision);
#  - memory off (workers are stateless, the brief carries everything), max 20 tool turns,
#    no "save a skill" nudges.
# Call a role:  hermes -p <role> -z --query-file brief.txt --usage-file usage\<role>.json
# Re-run after editing agents/*.md or a skill: it refreshes SOUL.md and the skill copies.
$ErrorActionPreference = 'Stop'
$repo   = Split-Path $PSScriptRoot -Parent
$home_h = "$env:LOCALAPPDATA\hermes"
$skills = Join-Path $HOME '.claude\skills'

# ponytail: model ids are calibration knobs; check `hermes model` for the exact names of your provider.
$cheap  = 'anthropic/claude-haiku-5.5'    # follows a checklist, runs scripts
$strong = 'anthropic/claude-sonnet-5.5'   # web research, story judgement, vision

$team = [ordered]@{
    'story-architect'      = @{ model = $strong; skills = @('yt-script') }
    'character-designer'   = @{ model = $cheap;  skills = @() }
    'fact-checker'         = @{ model = $strong; skills = @() }
    'visual-director'      = @{ model = $cheap;  skills = @('hand-drawn-visuals') }
    'image-qc'             = @{ model = $strong; skills = @() }
    'packaging-strategist' = @{ model = $cheap;  skills = @('yt-package', 'yt-seo', 'yt-chapters', 'yt-script', 'yt-edit') }
}

$existing = hermes profile list 2>$null | Out-String
foreach ($role in $team.Keys) {
    $cfg  = $team[$role]
    $raw  = Get-Content "$repo\agents\$role.md" -Raw -Encoding utf8
    $desc = [regex]::Match($raw, '(?m)^description:\s*(.+)$').Groups[1].Value
    $p    = "$home_h\profiles\$role"

    if ($existing -notmatch "(?m)\b$([regex]::Escape($role))\b") {
        hermes profile create $role --description $desc | Out-Null   # blank: no cloned skills or memory
        if (Test-Path "$home_h\.env") { Copy-Item "$home_h\.env" "$p\.env" }   # API keys of the main profile
    }
    hermes -p $role skills opt-out --remove --yes | Out-Null          # drop the bundled catalogue

    New-Item -ItemType Directory -Force "$p\skills" | Out-Null
    foreach ($s in $cfg.skills) { Copy-Item "$skills\$s" "$p\skills" -Recurse -Force }

    # SOUL.md = the agent brief without the Claude Code frontmatter + the shared grounding rules
    $soul = [regex]::Replace($raw, '(?s)\A---.*?---\s*', '') + "`n`n" + (Get-Content "$PSScriptRoot\grounding.md" -Raw -Encoding utf8)
    Set-Content "$p\SOUL.md" $soul -Encoding utf8

    foreach ($kv in @(
        @('model.default', $cfg.model),
        @('memory.memory_enabled', 'false'),
        @('memory.user_profile_enabled', 'false'),
        @('agent.max_turns', '20'),
        @('skills.creation_nudge_interval', '0')
    )) { hermes -p $role config set $kv[0] $kv[1] | Out-Null }

    Write-Host ("hermes  {0,-21} {1,-30} skills: {2}" -f $role, $cfg.model, ($(if ($cfg.skills) { $cfg.skills -join ',' } else { '-' })))
}
Write-Host "Team ready. Test: hermes -p fact-checker -z 'Is the Mariana Trench 10,994 m deep? One line with source.' --usage-file usage.json"
