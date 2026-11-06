# Producer -> checker loop against hallucinations, bounded and token-thrifty.
#   powershell -File hermes\loop.ps1 -Role story-architect -Brief work\angles-brief.txt
#   powershell -File hermes\loop.ps1 -Role packaging-strategist -Brief work\pack.txt -Checker fact-checker -Max 2
# Round 1: the role answers the brief. The checker (a different profile, so it does not grade its own
# work) reads ONLY that answer and returns PASS or FAIL + numbered problems. On FAIL the role gets the
# brief + its previous answer + the problems, nothing more. Stops at PASS or after -Max rounds; an
# answer that never passed is saved with an UNVERIFIED header so nobody ships it by mistake.
# Output: <brief>.out.md, and one usage report per call in <brief>.usage\ (tokens and cost).
param(
    [Parameter(Mandatory)][string]$Role,
    [Parameter(Mandatory)][string]$Brief,
    [string]$Checker = 'fact-checker',
    [int]$Max = 3
)
$ErrorActionPreference = 'Stop'
if ($Checker -eq $Role) { throw "The checker must be another profile than the role." }
$brief = Get-Content $Brief -Raw -Encoding utf8
$out   = [IO.Path]::ChangeExtension($Brief, '.out.md')
$usage = [IO.Path]::ChangeExtension($Brief, '.usage'); New-Item -ItemType Directory -Force $usage | Out-Null
$tmp   = New-TemporaryFile

function Ask($profile, $text, $tag) {
    Set-Content $tmp $text -Encoding utf8
    $r = hermes -p $profile -z --query-file $tmp --usage-file "$usage\$tag.json" | Out-String
    if ($LASTEXITCODE -ne 0 -or -not $r.Trim()) { throw "$profile returned nothing (exit $LASTEXITCODE)." }
    $r.Trim()
}

$query = $brief; $answer = ''; $verdict = ''
for ($i = 1; $i -le $Max; $i++) {
    $answer = Ask $Role $query "$i-$Role"
    $check = @"
Check the answer below for hallucinations. For every name, year, number, unit, study, quote and claimed tool
output: is it sourced (URL, file, "brief") and is the source right? Search the web when needed. Also flag
anything the brief did not ask for. First line exactly PASS or FAIL. If FAIL, then numbered problems, one line
each: the exact phrase, what is wrong, the correct value with its source or [to verify]. Nothing else.

ANSWER:
$answer
"@
    $verdict = Ask $Checker $check "$i-$Checker"
    $passed  = ($verdict -match '(?m)^\W*PASS\b') -and ($verdict -notmatch '(?m)^\W*FAIL\b')
    Write-Host "round $i : $(if ($passed) { 'PASS' } else { 'FAIL' })"
    if ($passed) { break }
    $query = "$brief`n`n--- YOUR PREVIOUS ANSWER ---`n$answer`n`n--- PROBLEMS FOUND BY $Checker (fix each, change nothing else) ---`n$verdict"
}
Remove-Item $tmp

if (-not $passed) { $answer = "<!-- UNVERIFIED after $Max rounds: open problems below -->`n$answer`n`n<!-- $verdict -->" }
Set-Content $out $answer -Encoding utf8
$tok = (Get-ChildItem "$usage\*.json" | ForEach-Object { (Get-Content $_ -Raw | ConvertFrom-Json).total_including_auxiliary.total_tokens } | Measure-Object -Sum).Sum
Write-Host "-> $out   ($tok tokens over $((Get-ChildItem "$usage\*.json").Count) calls)"
