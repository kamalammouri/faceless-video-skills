# Format des specs (un objet JSON par insert)

Champs communs : `file` (nom du PNG sans extension ; avec `--shots`, calculé `H<i>` à partir du plan), `type`, `dark` (fond nuit, défaut `false`), `colour` (accent : `terra`, `blue`, `sage`, `orange`, `sand`, `grey`, `ink` ou un hexa). Les noms d'icônes sont ceux de Lucide (lucide.dev/icons).

| type | Champs | Exemple |
|---|---|---|
| `symbol` | `icon`, `caption` (optionnel), `colour`, `fill` (optionnel) | `{"type": "symbol", "icon": "check", "caption": "verified", "colour": "sage"}` |
| `card` | `icon`, `big`, `small`, `layout` = `left` (cadre, icône à gauche) ou `top` (icône au-dessus) | `{"type": "card", "icon": "clock", "big": "3:47", "small": "a.m."}` |
| `compare` | `left`, `right`, `icon_left`, `icon_right`, `sign` (défaut `=`), `colour`, `colour2` | `{"type": "compare", "left": "10 L SNOW", "right": "1 L WATER", "icon_left": "snowflake", "icon_right": "droplet"}` |
| `gauge` | `icon` (optionnel), `big`, `small`, `value` 0..1 | `{"type": "gauge", "icon": "pill", "big": "412 TABLETS", "small": "of 730", "value": 0.56}` |
| `scoreboard` | `left`, `right`, `left_name`, `right_name` | `{"type": "scoreboard", "left": "21", "right": "0", "left_name": "YOU", "right_name": "THEM", "dark": true}` |
| `phone` | `title`, `lines` (1 à 4 ; la dernière est le bouton d'accent s'il y en a plusieurs) | `{"type": "phone", "title": "MY BANK", "lines": ["$31,240.00", "SEND"]}` |
| `title` | `title`, `sub` (optionnel) | `{"type": "title", "title": "THE HIDDEN COST", "sub": "chapter three"}` |
| `bar` | `title`, `labels`, `values`, `unit` (suffixe), `units` (étiquettes de valeur si différentes des nombres) ; 2 à 7 barres | `{"type": "bar", "title": "Reaction time (s)", "labels": ["average", "sprinter", "you"], "values": [0.25, 0.13, 0.025]}` |
| `line` | `title`, `labels`, `series` = `[{"label", "data"}]` (1 à 3) ou `values`, `unit` | `{"type": "line", "labels": ["age 11", "12", "13"], "series": [{"label": "followers", "data": [0, 9, 40]}]}` |
| `pie` | `title`, `labels`, `values`, `donut` | `{"type": "pie", "labels": ["sleep", "school", "free"], "values": [8, 7, 9]}` |
| `timeline` | `title`, `start`, `end`, `marks` = `[{"at": 0..1, "label", "colour"}]` (2 à 6) | `{"type": "timeline", "start": "1872", "end": "2024", "marks": [{"at": 0, "label": "Darwin"}, {"at": 1, "label": "Nikolić 2024"}]}` |
| `list` | `title`, `items` = `[{"icon", "text", "colour"}]` (1 à 5) | `{"type": "list", "title": "The price", "items": [{"icon": "brain", "text": "headaches"}]}` |

## Dans `shots.json` (skills vidéo)

```json
{"i": 58, "sentence": "A tiny thermometer next to a huge cheek.", "family": "html",
 "html": {"type": "compare", "left": "0.5 °C", "right": "a whole room", "icon_left": "thermometer", "icon_right": "users", "sign": "→"}}
```

`node render.mjs shots.json flow/<video>/html --shots` ne rend que les plans qui portent `html` ; `build_slideshow.py` charge ensuite `flow/<video>/html/H0058.png`. Le champ `dark` du plan est repris par le spec.

## Export animé (`--anim`)

`node render.mjs shots.json out/ --shots --anim` écrit, en plus du PNG, `out/H0058.anim.json` :

```json
{"dark": false, "html": "<svg class=\"layer\" …>…</svg><div class=\"abs num\" id=\"__ID__-a1\" …>46%</div>",
 "items": [{"id": "__ID__-a0", "kind": "grow", "ox": 676.7, "oy": 860},
           {"id": "__ID__-a1", "kind": "count", "to": 46, "pre": "", "suf": "%", "dec": 0, "grp": false, "text": "46%"}]}
```

- `html` : le contenu de l'insert (1920 × 1080, positions absolues) à placer dans un bloc qui porte les polices `Patrick Hand` (texte) et `Caveat` 700 (classe `num`) ; `out/fonts/fonts.css` donne les `@font-face` vers `assets/fonts/*.woff2`.
- `items` : les entrées dans l'ordre de lecture. `__ID__` est à remplacer par un identifiant unique dans la page (l'id du plan). `kind` : `grow` / `growx` (échelle Y ou X depuis le point SVG `ox, oy`), `draw` (`paths` = `[{"id", "len"}]`, à tracer par `stroke-dashoffset` de `len` à 0), `pop` (opacité + échelle), `fade` (opacité + glissement), `count` (compter de 0 à `to` avec `pre`, `suf`, `dec` décimales, `grp` = séparateur de milliers ; `text` est le texte final exact).
- Un texte de classe `num` compte s'il contient un seul nombre ; deux nombres (`3:47`, `1 in 3`) ou une année (1500 à 2100) ne comptent pas.
- Un PNG redessiné sans `--anim` efface son `.anim.json`.

## Fonds

`BG=…` et `BG_DARK=…` (chemins d'images) peignent chaque insert sur ces images au lieu du crème ou de la nuit : utiliser les deux pages vides générées une fois dans Flow (`prompts.py` des skills vidéo ajoute `BG` et `BG_DARK` à `prompts.json`), pour que les inserts aient le même grain de papier et la même lumière que les scènes.

## Correspondance avec `cards.py` (secours sans navigateur)

| Ici | `cards.py` / `charts.py` |
|---|---|
| `symbol` | `cards.symbol(icon, caption)` (15 icônes seulement) |
| `card` | `cards.card(icon, big, small, layout)` |
| `compare` | `cards.card("compare", big, small, icons=(a, b))` |
| `gauge` | `cards.card("gauge", big, small, value=v, icon=i)` |
| `scoreboard`, `phone` | `cards.scoreboard(...)`, `cards.phone(...)` |
| `bar`, `line`, `pie`, `timeline` | `charts.bars`, `charts.line`, `charts.pie`, `charts.timeline_marks` |
