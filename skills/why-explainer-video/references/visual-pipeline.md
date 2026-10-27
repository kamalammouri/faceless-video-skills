# Le diaporama : une image par phrase

## 1. Ce qui a été mesuré sur deux vidéos complètes de la référence

| Mesure | Vidéo « Wants You to Die » (542 k vues) | Vidéo « Morning Sickness » (10 k vues) |
|---|---|---|
| Durée | 23 min 53 | 22 min 15 |
| Images | 297 | 323 |
| Durée par image | 4,8 s (1,2 à 10,8) | 4,1 s (1,2 à 7,8) |
| Mots par image | 12 | 11 |
| Transitions | 0 (coupes franches) | 0 |
| Temps strictement fixe | 94,7 % | 94 % |
| Mouvements de caméra | 0 | 0 |
| Personnage récurrent | le grand-père et le bébé (3 apparitions) | la femme enceinte en robe jaune (presque chaque scène) |
| Part d'images « scène avec personnage » | ≈ 25 % | ≈ 55 % |
| Part de schémas et graphiques | ≈ 32 % | ≈ 15 % |

La vidéo qui a marché est celle qui montre **plus de schémas et de chiffres** et moins de scènes de personnage. Corrélation sur deux vidéos seulement, mais cohérente avec le script : plus de chiffres, plus de « you », plus de vues.

## 2. Règles du diaporama
- **Une image par phrase du script.** Durée = durée de la phrase à la voix (3 à 6 s). Jamais plus de 8 s sans nouvelle image.
- **Coupe franche** entre toutes les images. Pas de fondu, pas de zoom, pas de panoramique. Le rythme vient de la fréquence des coupes, pas du mouvement.
- Le **texte à l'écran** est le mot ou le chiffre exact que la voix dit à cet instant, en capitales manuscrites, 1 à 3 mots, jamais une phrase.
- **Motif visuel récurrent** : l'image de la scène d'ouverture revient au milieu (≈ 60 %, juste avant ou après le CTA) et à la fin.
- Fond **gris-bleu sombre** uniquement pour la nuit, la menace, la mort : 5 % des images au maximum, pour que le contraste reste un signal.
- Logo ou mot « SUBSCRIBE » en filigrane discret en bas à droite sur toute la vidéo.


### Cartes de chiffres : une icône, toujours, et jamais deux fois la même mise en page de suite
Une carte « chiffre seul dans un cadre » lue trois fois de suite fait pauvre : c'est le premier reproche fait à la vidéo polaire. Règles :
- Chaque carte est rendue par `scripts/cards.py` (`card(icon, big, small, layout)`), qui dessine l'icône à l'encre : clock, calendar, fuel, thermo, snow, water, food, pills, hourglass, key, radio, fire, plane, battery, wind, sun, moon, heart. Un chiffre sans icône n'est pas livrable ; s'il manque une icône, l'ajouter à `cards.py` (15 lignes de PIL) plutôt que de livrer une carte nue.
- Cinq mises en page à faire tourner : `left` (icône à gauche), `top` (icône au-dessus), `stamp` (page de calendrier pour « DAY n »), `compare` (A = B avec deux icônes), `gauge` (chiffre + barre de niveau). Deux cartes consécutives n'ont jamais la même mise en page.
- Le petit texte sous le chiffre dit ce que le chiffre fait (« nothing lands », « before the pipes freeze »), pas l'unité déjà visible.
- `python scripts/cards.py` rend une planche de démonstration : la regarder avant de produire.

### Variété des plans : les règles anti-doublon
- Jamais plus de **2 images consécutives de la même famille** (carte, scène, schéma, icône).
- Jamais **deux compositions identiques** (même cadrage, même objet, personnage à la même place) à moins de 10 images d'écart ; varier l'échelle : plan large, plan moyen, gros plan objet, vue en coupe, vue de dessus, POV.
- Chaque **analogie** du script a une image métaphorique (la chose comparée), pas une image littérale de la scène.
- Scènes sombres (`Dark variant`) : jamais plus de 3 de suite, pour que le retour au crème reste un soulagement.
- Le **Visual director** (`references/agents.md`) audite la shot list avant génération ; il ne faut pas s'auto-auditer.

## 3. Les familles de plans

**Parts mesurées sur 30 vidéos et 8 250 plans** (`references/scene-catalogue.md`) : scènes 62 %, schémas 15 %, icônes 15 %, visuels de données 7 % (un par minute), titres 0,6 %. La vidéo la plus vue monte à 18 % de visuels de données et 29 % d'icônes : viser cette répartition pour un sujet à études et chiffres, et la répartition moyenne pour un sujet de comportement. Les parts du tableau ci-dessous venaient des deux premières vidéos étudiées ; elles restent valables pour un format très « icône », mais le catalogue fait foi.

| Famille | Part cible | Quand l'utiliser | Exemple de contenu |
|---|---|---|---|
| **Icône + 1 à 3 mots** | 35 % | une phrase qui nomme un concept, un objet, un verdict | bottes usées ; cadenas ; balance « ANTAGONISTIC PLEIOTROPY » ; « CELLS ARE IMMORTAL » |
| **Scène avec personnage** | 25 % | l'ouverture, les analogies, les scientifiques, le retour final | grand-père et nouveau-né ; Gompertz à sa lampe à huile ; une femme devant un frigo ouvert |
| **Schéma ou comparaison** | 20 % | un mécanisme, un avant/après, deux cas côte à côte | chromosome et télomère annotés ; « MAINLAND · SHORTER LIFE / ISLAND · LONGER LIFE » ; frise « 4 BILLION YEARS » |
| **Graphique de données** | 15 % | chaque chiffre important du script | barres « AGE 30 / 38 / 46 » ; jauge « 122 YEARS · 164 DAYS » ; courbe « WEEK 8 – WEEK 12 » |
| **Carte-titre** | 5 % | début de chapitre, question-relance | « MYSTERY SOLVED : COUNTING THE CYCLE » ; « UNKNOWN ? CELL » |

Viser la part de la vidéo à 542 k vues (plus de schémas) plutôt que celle à 10 k (plus de scènes).

## 4. Préfixe de style (à placer devant chaque prompt d'image)

Préfixe **maison**, validé sur 65 images Flow (personnage récurrent à tête d'œuf et casque orange) : voir `flow-automation.md`, section « Préfixe de style maison ». C'est celui à utiliser par défaut pour la chaîne. Le préfixe ci-dessous est la variante « trait fin » générique, pour une autre chaîne ou un autre style.

```
Minimal hand-drawn explainer illustration, thin black ink outline, flat pastel fills
(sand, sage green, dusty blue, terracotta, soft orange), plain cream paper background,
hand-lettered capital labels, simple round-headed white characters with dot eyes and
thin stick limbs, no gradients, no photorealism, no text other than the labels given,
16:9, centered composition, generous empty space
```

Prompt négatif : `photo, 3D render, gradient, shadow, watermark, extra text, logo, realistic face, cluttered background`.

Pour un personnage récurrent, décrire la **fiche** une fois et la recopier dans chaque prompt où il apparaît : « a pregnant woman with a short dark bob, mustard yellow dress, white round face ».

## 5. Modèle de prompt par famille

```
[PRÉFIXE DE STYLE] + [FAMILLE] + [SUJET] + [LABELS EXACTS ENTRE GUILLEMETS] + [FOND : cream / dark slate]
```

Exemples :
- Icône : `… single icon of a worn pair of leather work boots, label "STRAIGHT LINE" below, cream background`
- Scène : `… an elderly bald man in an armchair cradling a newborn wrapped in pink, a window with soft daylight, no labels`
- Schéma : `… a horizontal timeline with eight dated circular icons from "ORIGIN OF LIFE" to "HUMAN CIVILIZATION", an orange glowing thread running through all of them, title "4 BILLION YEARS"`
- Graphique : préférer le code (section 6)
- Carte-titre : `… a rounded rectangle card with the title "THE DIVISION PUZZLE" and a small cell icon, nothing else`

## 6. Graphiques et frises par code, pas par IA

Les générateurs d'images écrivent des chiffres faux et des labels aberrants (la référence affiche « SIMPLE EXPLAINER: 229 » et « LARGE CALM CLOCK FACE » à l'écran). Pour tout plan qui porte un chiffre, générer l'image par code :

```python
import matplotlib.pyplot as plt
with plt.xkcd(scale=1, length=100, randomness=2):   # trait manuscrit
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#F5EFE0"); ax.set_facecolor("#F5EFE0")
    ax.bar(["AGE 30", "AGE 38", "AGE 46"], [1, 2, 4], color=["#8FA9BF", "#9DB89A", "#C77B58"])
    ax.set_title("RISK OF DYING THIS YEAR", fontsize=28)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    plt.savefig("shot_025.png", facecolor=fig.get_facecolor())
```

Police : une sans-serif manuscrite (Patrick Hand, Architects Daughter) pour rester cohérent avec les images IA. Même palette, même fond.

## 7. Format de la liste d'images à livrer

Un tableau, une ligne par phrase du script :

| # | Temps | Phrase (début) | Famille | Texte à l'écran | Prompt ou code |
|---|---|---|---|---|---|
| 1 | 0:00 | Look at an 80-year-old grandfather… | Scène | — | [préfixe] + elderly bald man in armchair cradling a newborn… |
| 2 | 0:05 | His joints ache, his skin has thinned… | Scène | — | [préfixe] + close-up of the same man's wrinkled hand on the armrest… |
| 25 | 1:53 | Starting around the age of 30… | Graphique | AGE 30 / 38 / 46 | code : barres doublant à chaque âge |

Ajouter en fin de liste : la miniature (voir `publication-seo.md`) et la carte finale « NEXT : [titre de l'épisode suivant] ».


### Outils de production (dans `scripts/`)
- `prompts.py shots.json` : construit `prompts.json` pour Flow à partir de la shot list (préfixe maison, fiche personnage, décor, gabarit par famille, cadrage en rotation, variante sombre, suffixe anti-texte) et **lint** la liste : mots interdits qui déclenchent des bulles, 4 scènes de suite, deux visuels de données de suite, quasi-doublons, plus de 14 images sans visuel de données, carte sans icône. Corriger les erreurs avant de générer.
- `cards.py` : cartes de chiffres avec icône. `charts.py` : 24 patrons de graphiques, jauges, frises et schémas.
- `build_slideshow.py shots.json voice.wav timing.json out.mp4 --flow flow/<video>` : monte la vidéo, chaque image tenue jusqu'à la phrase suivante ; cartes, graphiques et titres rendus par code, images Flow chargées par nom, carte de secours si une image manque.
- `scripts/flow/` : génération automatique des images Flow (`references/flow-automation.md`).
Le format de `shots.json` est documenté en tête de `prompts.py` et `build_slideshow.py` : une seule liste sert aux prompts, au lint et au montage.

## 8. Assemblage

Le script de montage lit, pour chaque phrase, l'image `flow/<NNNN>.png` (ou `flow/<video>/<Fxx>.png` pour un plan par moment) si elle existe et sinon rend l'image par code : on peut donc générer les images Flow après coup et remonter sans toucher à la voix. Chaque image reste à l'écran jusqu'à la phrase suivante ; les horodatages viennent du fichier de minutage de la voix. Toujours produire une planche contact (4 × N vignettes) pour vérifier la cohérence avant de livrer.

Voix IA (une piste par temps), puis pour chaque phrase : image affichée de la fin de la phrase précédente à la fin de la phrase courante. Export 1080p. Avec ffmpeg : un fichier de concaténation `file 'shot_001.png' / duration 4.8`, puis la piste audio. Pas de musique forte : un lit sonore discret suffit, la voix porte tout.

## 9. Erreurs vues dans la référence, à ne pas reproduire
- Labels qui décrivent l'image au lieu de nommer la chose (« SHELF OF BRIGHT NEW TUBES », « Evenly Divided Start Point (Unlabeled) »).
- Mots dédoublés dans l'image (« FREE RADICAL THEORY » deux fois).
- Deux images quasi identiques à la suite.
- Titres de chapitres générés avec des trous (« The Anatomical Cost of Thousand »).
- Relire chaque label généré ; régénérer toute image dont le texte n'est pas exactement celui demandé.
