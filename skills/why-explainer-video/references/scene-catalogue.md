# Catalogue des scènes Apefully (30 vidéos, 8 250 plans classés)

Mesure faite le 27 octobre 2026 : chaque vidéo découpée en plans (détection de coupes à 4 i/s), une vignette par plan, classement de chaque vignette par des agents de vision. Les planches d'exemples par famille et les patrons relevés vidéo par vidéo sont dans `examples/apefully/` du repo (`<famille>.jpg`, `patterns-all.md`, `stats.md`).

## 1. Ce que la chaîne montre vraiment

| Famille | Part des plans | Durée moyenne | Ce que c'est |
|---|---|---|---|
| **scene** | 62 % | 4,0 s | personnage(s) dans un décor complet et coloré (salon, bureau, labo, savane, hôpital) ; c'est le fond de la vidéo |
| **schema** | 15 % | 4,8 s | coupe anatomique, mécanisme fléché, comparaison côte à côte, cycle, arbre, balance |
| **icon** | 15 % | 5,3 s | un objet, un organe ou un animal isolé sur fond uni crème, avec 0 à 3 mots |
| **timeline** | 1,8 % | 4,9 s | barre de durée, flèche du temps, alignement d'évolution, scène datée |
| **map** | 1,5 % | 4,6 s | silhouette de pays ou continent, épingle, flèche de migration |
| **gauge** | 1,2 % | 5,0 s | thermomètre, batterie, jauge à curseur, cadran, barre de progression |
| **chart-dots** | 1,0 % | 4,9 s | grand chiffre + grille de pictogrammes identiques, rangée de silhouettes, nuage de points |
| **chart-bar** | 0,7 % | 5,3 s | barre de ratio (minuscule vs énorme), 2 à 4 barres avec ligne de référence pointillée |
| **title** | 0,6 % | 4,6 s | texte seul (titre de chapitre, « SUBSCRIBE ») |
| **table** | 0,5 % | 6,1 s | 3 à 5 éléments alignés avec un label chacun, pilules, carré de Punnett |
| **chart-line** | 0,4 % | 6,5 s | escalier, crosse de hockey, pic puis plateau, deux courbes comparées |
| **chart-pie** | 0,3 % | 6,0 s | camembert pastel à une part orange détachée + pourcentage |

**Visuels de données** (chart-*, gauge, timeline, map, table) : 7,3 % des plans, soit **un toutes les 14 images, environ un par minute**. Ils sont tenus plus longtemps que les scènes (5 à 6,5 s contre 4 s) : un graphique se lit, une scène se regarde.

## 2. Ce que les vues disent

- La vidéo la plus vue (542 k, « The Real Reason Evolution Wants You to Die ») est **la plus riche en données** : 49 visuels de données sur 269 plans (18 %), 77 icônes, seulement 89 scènes, et 5,3 s par plan. C'est le modèle à suivre pour un sujet à études et chiffres.
- Les vidéos à 400 k (homosexualité, calvitie) sont au contraire des récits en scènes (77 à 80 % de scènes) avec 12 à 13 visuels de données : le modèle pour un sujet de comportement.
- Règle pratique : **sujet « corps et chiffres » → 12 à 18 % de visuels de données ; sujet « comportement et histoire » → 5 à 8 %, jamais moins d'un par minute.**

## 3. Enchaînements mesurés

- `scene → scene` domine (41 % des transitions), mais le deuxième motif est l'alternance **scene → icon → scene** et **scene → schema → scene** : une scène, un insert, retour à la scène. L'insert est ce qui donne le rythme ; trois scènes de suite sans insert est rare dans les vidéos à fort succès.
- Un visuel de données arrive presque toujours **entre deux scènes**, jamais après un autre visuel de données : `timeline → scene`, `map → scene`, `gauge → scene`.
- Le schéma anatomique revient par **séries de 2 à 4** (coupe, zoom, flèche, comparaison), c'est la seule famille qui s'enchaîne avec elle-même.

## 4. Les patrons réutilisables (tous rendus par `scripts/charts.py` ou `scripts/cards.py`)

| Patron | Fonction | Quand |
|---|---|---|
| Barre de ratio « 100x » : barre minuscule vs barre énorme, étiquette au-dessus | `charts.bar_ratio` | un écart extrême |
| 2 à 4 barres colorées + ligne de référence pointillée | `charts.bars` | comparer des cas |
| Camembert à part détachée orange + « 20 % » | `charts.pie` | une proportion |
| Escalier, crosse de hockey, pic puis plateau, deux courbes | `charts.line`, `charts.lines2` | une évolution |
| Grand chiffre + grille de pictogrammes, nuage de points | `charts.dots`, `charts.scatter` | une quantité, une corrélation |
| Thermomètre simple ou double, barre à curseur 3 zones, cadran, batterie | `charts.thermo`, `thermo2`, `hbar_gauge`, `dial`, `cards.card(..., 'gauge')` | un niveau, un seuil |
| Barre de durée avec point de départ, barre à repère « 8,500 YEARS AGO », flèche du temps à graduations, segment surligné « 8 WEEKS », repères multiples, courbe jour-nuit | `charts.timeline`, `timeline_bar`, `timeline_arrow`, `timeline_segment`, `timeline_marks`, `daynight` | une durée, une date, une période |
| Deux côtés séparés par une ligne pointillée verticale | `charts.split_compare` | avant/après, espèce A vs B |
| A → B avec deux images et des chiffres au-dessus | `charts.arrow_ab` | une transformation |
| Balance à deux plateaux | `charts.balance` | un compromis, risque/bénéfice |
| Cycle fléché à 3-5 images | `charts.cycle` | une boucle, un cycle de vie |
| Équation en pictogrammes « 1 STRIDE = 1 BREATH » | `charts.equation` | un rapport simple |
| Pilules alignées avec label | `charts.pills` | une liste de cas oui/non |
| Carte chiffre + icône (horloge, calendrier, bidon…), page de calendrier « DAY n » | `cards.card` | tout chiffre isolé |

Les cartes (map) ne sont pas rendues par code faute de fonds de carte propres : les demander à Flow (« simple flat silhouette of Africa, one red pin, no text ») et ajouter le nom de lieu par code.

## 5. Ce qui a changé dans le style de la chaîne

Les deux premières vidéos étudiées étaient en fond crème uni avec personnages à tête ronde blanche. Sur 30 vidéos, **la majorité des scènes ont maintenant un décor complet et coloré** (salon, bureau, labo, savane au crépuscule) ; le fond crème est réservé aux inserts (icônes, schémas, données) dans une carte à coins arrondis et contour noir. Les personnages gardent la tête ronde blanche ; les ancêtres ont des cheveux bruns hirsutes et une tunique de fourrure. Conséquence pour les prompts Flow : décrire un **décor complet** pour les scènes, et un **fond crème uni** pour les inserts. Le contraste entre les deux est le rythme visuel de la chaîne.

## 6. Règles tirées du catalogue (appliquées par `scripts/prompts.py`)

1. Une scène, un insert, une scène : jamais plus de 3 scènes consécutives sans icône, schéma ou visuel de données.
2. Un visuel de données au moins toutes les 14 images ; sur un sujet à chiffres, un toutes les 6 à 8.
3. Un visuel de données est tenu 5 à 6 s (la phrase qui l'accompagne doit être une phrase longue ou deux courtes).
4. Jamais deux visuels de données de suite ; entre deux, une scène.
5. Les schémas anatomiques vont par séries de 2 à 4, en zoomant.
6. Les inserts sont sur crème uni, les scènes dans un décor complet.
7. Chaque chiffre de la voix a son visuel (carte, jauge, barre) ; jamais un chiffre dit sans être vu.
