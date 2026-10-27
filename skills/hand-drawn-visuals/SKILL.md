---
name: hand-drawn-visuals
description: Dessine par code, dans un vrai navigateur (HTML, CSS, JS avec rough.js et les icônes Lucide, capturé par Playwright), les inserts d'une vidéo faceless au look « dessiné à la main » : symbole seul (coche, cadeau, flèche en boucle, cadenas, loupe…), carte chiffre avec icône, comparaison, jauge, tableau de score, écran de téléphone, carte-titre, graphiques en barres, courbes et camemberts, frise chronologique, liste à icônes ; sur fond crème ou nuit, ou sur le fond généré une fois dans Google Flow pour l'homogénéité. Remplace les dessins PIL de cards.py et charts.py et toute image Flow qui n'est qu'un objet simple. Use whenever a video shot list needs a number, a score, a chart, a timeline, a title or a single symbol on screen, when the user says the code-drawn inserts look stiff or ugly, asks for « icônes », « graphiques », « cartes » by code, CSS/JS visuals, or wants inserts that match hand-drawn AI images, even if they don't name the skill.
---

# Hand-drawn visuals (inserts HTML + rough.js + Lucide, capturés par Playwright)

Les inserts d'un diaporama (symboles, chiffres, scores, graphiques, frises, titres) sont dessinés par code, pas par l'IA : exacts, instantanés, gratuits. Ce skill les dessine **dans un navigateur** avec [rough.js](https://roughjs.com) (traits tremblés, hachures), les icônes [Lucide](https://lucide.dev/icons) (1 600 pictogrammes, licence ISC) redessinées en style croquis, les polices manuscrites Patrick Hand et Caveat, et une capture 1920 × 1080 par Playwright. Résultat : des inserts qui ressemblent aux images Flow « storybook au crayon », là où les dessins PIL de `cards.py` restaient raides.

## Quand l'utiliser
- Tout plan d'une shot list qui n'est pas une scène avec personnage ni un objet à texture : un symbole seul, un chiffre, un score, un bulletin, un écran de téléphone, une comparaison, une jauge, un graphique, une frise, un titre de chapitre, une liste.
- À la place de `cards.py` / `charts.py` des skills vidéo (ils restent le secours sans navigateur) et à la place de toute image Flow que l'agent **Render router** a classée « code ».
- Pour une miniature ou une image isolée : même commande, un seul spec.

## Workflow
1. **Écrire les specs** : dans `shots.json`, un plan `{"i": 12, "sentence": "...", "family": "html", "html": {"type": "symbol", "icon": "check", "caption": "verified"}}` ; ou une liste à part `specs.json` = `[{"file": "H0012", "type": ..., ...}]`. Tous les types et leurs champs : `references/spec-format.md`. Nom d'icône = nom Lucide (chercher sur lucide.dev/icons : `check`, `gift`, `refresh-cw`, `lock`, `search`, `brain`, `clock`, `calendar-days`, `snowflake`, `droplet`, `pill`, `flame`, `heart`, `eye`…).
2. **Rendre** : `PLAYWRIGHT_DIR=$HOME/Desktop/nastro node scripts/render.mjs shots.json flow/<video>/html --shots` (ou `specs.json out/`). Un PNG par spec, les fichiers existants sont sautés (`--force` pour redessiner). Pour les fonds : `BG=flow/<video>/BG.jpg BG_DARK=flow/<video>/BG_DARK.jpg` avant la commande, et chaque insert est peint sur la page vide générée une fois dans Flow.
3. **Contrôler** : `python scripts/sheets.py flow/<video>/html sheets` puis regarder la planche : texte qui déborde, icône introuvable (le journal dit `icon "x" not found`), contraste sur fond sombre.
4. **Monter** : `build_slideshow.py` des skills vidéo charge `flow/<video>/html/H<i>.png` pour chaque plan `html`.

Première fois : Node 18+, Chrome installé, Playwright dans un dossier (`npm i playwright`, variable `PLAYWRIGHT_DIR`), accès réseau pour rough.js, les polices Google et les icônes (mises en cache dans `scripts/vendor/icons/`). `node scripts/render.mjs --demo out/` dessine les 16 exemples de `scripts/demo.json` pour vérifier l'installation.

## Le style (une seule charte, la même que les images Flow)
- Couleurs : crème `#f5efe0`, encre `#1e1b16`, terra `#c77b58`, bleu `#a8bacc`, sauge `#c4d2b8`, orange `#f0b478`, sable `#e8d5b0` ; nuit `#26303c`. Un insert = une couleur d'accent, jamais plus de trois.
- Traits tremblés (`roughness` 0,8 à 1,4), remplissages hachurés pour les icônes grandes et les barres, pleins pour les petits points.
- Texte : Patrick Hand pour les mots, Caveat gras pour les chiffres ; 2 à 4 mots par insert, jamais une phrase ; les chiffres à l'écran sont **identiques** à ceux de la voix.
- Un seul sujet par insert, centré, beaucoup de vide ; fond crème le jour, nuit pour le danger ou le secret (`"dark": true`).
- Variante avec `FONT="Segoe Print"` si les polices Google sont bloquées.

## Ajouter un type
Un type = une fonction dans l'objet `T` de `scripts/template.html` : créer la couche (`layer()`), dessiner avec `rc.*` (rectangle, circle, line, curve, polygon, path), poser le texte avec `text()` / `ctext()`, une icône avec `sketchIcon(svg, x, y, taille, couleur)`. Ajouter l'exemple à `demo.json` et au tableau de `spec-format.md`.

## Contrôle qualité
- [ ] Chaque chiffre à l'écran est celui de la phrase ; unité présente ; pas de nombre arrondi par le dessin
- [ ] Icône trouvée (journal sans `not found`) et lisible à 480 px de large sur la planche contact
- [ ] Texte dans le cadre, pas de débordement ; 2 à 4 mots ; capitales pour les titres
- [ ] Même palette et mêmes polices sur tous les inserts de la vidéo ; fond Flow partagé si disponible
- [ ] Deux inserts consécutifs n'ont pas le même type ; jamais trois inserts de suite sans scène
