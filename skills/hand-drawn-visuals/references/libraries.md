# Bibliothèques retenues, et celles écartées (recherche du 27 octobre 2026)

| Besoin | Retenu | Pourquoi | Licence, version |
|---|---|---|---|
| Traits tremblés, hachures, formes croquis | **rough.js** (`roughjs@4.6.6`, CDN jsDelivr, 9 ko) | API minuscule (`rectangle`, `circle`, `line`, `curve`, `polygon`, `path`), rend en SVG, options `roughness` / `bowing` / `fillStyle` ; sert aussi à redessiner n'importe quel chemin SVG d'icône en croquis | MIT |
| Icônes | **Lucide** (`lucide-static@0.468.0` sur unpkg, un SVG par icône) | 1 600+ pictogrammes cohérents sur grille 24 px, traits 2 px, faciles à repasser avec rough.js ; noms stables, catalogue sur lucide.dev/icons | ISC |
| Polices manuscrites | **Patrick Hand** (texte) et **Caveat 700** (chiffres), Google Fonts | lisibles à 480 px, proches de l'écriture des cartes de la chaîne de référence ; secours local `Segoe Print` | OFL |
| Capture | **Playwright** + Chrome | déjà installé pour Google Flow ; capture 1920 × 1080 exacte, polices web chargées | Apache 2 |
| Graphiques | **dessinés avec rough.js dans `template.html`** (barres, courbes, camembert, frise) | les bibliothèques de graphiques croquis (ci-dessous) ont des légendes et des titres minuscules, pas de contrôle des polices à 1080p, et des couleurs difficiles à aligner sur la charte | |

## Écartées, et pourquoi

- **chart.xkcd** (MIT, `1.1.13`, basé sur rough.js) : charmant, mais police et légende fixées à l'échelle d'une page web (illisibles à 1080p sans bidouille), barres non remplies avec nos couleurs. Testé puis remplacé par nos propres fonctions.
- **roughViz** (MIT, `2.0.5`, D3 + rough.js) : plus de types (donut, horizontal, scatter) mais dépôt peu actif depuis 2024 et mêmes limites de typographie.
- **Tabler Icons** (MIT, 4 985 icônes) : excellente alternative à Lucide si un nom manque ; même grille 24 px, même méthode (`https://unpkg.com/@tabler/icons@3.31.0/icons/outline/<nom>.svg`). À utiliser en second choix pour garder un seul trait.
- **Phosphor** (MIT, 1 512 icônes, 6 graisses), **Heroicons** (MIT), **Feather** (MIT) : équivalents, pas de raison de mélanger.
- **Open Doodles** (CC0, dessins de personnages par Pablo Stanley), **Open Peeps** (CC0, personnages à assembler), **unDraw** (MIT, illustrations à couleur personnalisable), **Humaaans** : utiles pour un personnage ou une scène sans IA, mais leur style (vectoriel plat ou doodle) ne se fond pas dans les images Flow au crayon ; à réserver à une chaîne qui adopte ce style pour toutes ses images.

## Pistes à tester plus tard
- **rough-notation** (MIT) : soulignés, cercles et surlignages tremblés animés ; pour une version animée des inserts (vidéo plutôt qu'image).
- **Excalidraw** (MIT) : bibliothèques d'éléments croquis exportables en SVG ; pour des schémas complexes dessinés à la main par l'utilisateur, importés ensuite ici.
- Filtre SVG `feTurbulence` + `feDisplacementMap` : un « crayon » appliqué à n'importe quel SVG existant quand on ne veut pas le redessiner avec rough.js.

Sources : [rough.js](https://roughjs.com), [chart.xkcd](https://www.cssscript.com/hand-drawn-svg-chart-xkcd/), [roughViz](https://cdn.jsdelivr.net/npm/rough-viz@2.0.5/README.md), [Lucide](https://lucide.dev), [Tabler Icons](https://www.alternativeto.net/software/tabler-icons/about/), [Open Doodles / unDraw / Humaaans](https://dev.to/madza/16-places-to-find-illustrations-for-your-projects-h5n).
