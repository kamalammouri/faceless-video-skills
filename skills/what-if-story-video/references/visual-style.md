# Le style visuel : stickman sombre, un plan toutes les 3 à 4 s, deux plans sur trois en mouvement

Mesuré sur 6 vidéos de la chaîne de référence (720 plans) : 94 à 152 plans par épisode, **3,2 à 4,2 s par plan**, 2 plans sur 3 avec un mouvement (caméra ou personnage), 1 sur 3 fixe ; texte à l'écran fréquent (chiffres, scores, bulletins, écrans de téléphone, panneaux) ; palette crépuscule violet-orange pour le jour, bleu marine avec une lumière chaude pour la nuit. La chaîne est un vrai film d'animation 2D ; ce skill reproduit la **sensation** avec des images fixes, un zoom lent et des cartes par code, à coût nul.

## Le personnage (`stickman-dark` dans `scripts/styles.json`)

- Silhouette **noire pleine**, grande tête ronde noire, deux yeux blancs ovales avec un petit reflet en étoile, bras et jambes fins ; **sweat à capuche de couleur** : le héros en rouge, le rival ou l'autre héros en bleu, les figurants en gris, vert, jaune.
- Expressions par les yeux seulement (ouverts, plissés, en larmes, étoile plus grande) ; pas de bouche sauf sourire fin.
- Les autres personnages gardent la même silhouette avec une autre couleur de sweat et un accessoire (casquette, lunettes rondes, blouse blanche, chapeau noir).
- La fiche du personnage est dans **chaque** prompt (`prompts.py` l'ajoute) ; le costume change par série via `character.costume`.

## Les plans

| Famille | Part cible | Quand | Rendu |
|---|---|---|---|
| Scène avec personnage | 55 % | chaque action, chaque réplique | Flow, tenue sur 2 ou 3 phrases (même `file`), budget 5 par minute |
| Insert objet ou gros plan | 15 % | la main, la tasse, la balle, le téléphone | Flow, fond bleu marine, sans personnage (`nochar`) |
| Carte chiffre | 10 % | la prémisse, chaque palier chiffré | `cards.card` avec icône (clock, people, heart…) |
| Score / bulletin / téléphone | 10 % | victoires, examens, appels, messages | `cards.scoreboard`, `cards.phone`, `card(layout="stamp")` |
| Carte-titre | 5 % | la question du titre, « Two years later », « PART 2 » | `title` |
| Graphique | 5 % | une comparaison (0,25 s / 0,025 s), une courbe de progression | `charts.bar_ratio`, `charts.line` |

Règles de rythme : jamais plus de 3 scènes Flow de suite sans insert ; une carte par palier de l'escalade ; la carte-titre de la question à la fin du temps 2 ; le plan de l'ouverture revient au climax (même décor, autre lumière).

## Le mouvement (`build_slideshow.py --motion`)

- Deux images Flow sur trois reçoivent un zoom lent de 7 % (avant, puis arrière, en alternance) ; la troisième et toutes les cartes restent fixes : c'est l'alternance mobile / fixe qui donne le rythme, pas le mouvement continu.
- Coupes franches, aucune transition, aucun fondu sauf au noir avant « Two years later ».
- Durée des plans : celle des phrases (3 à 4 s) ; une carte chiffre tient 1 s de plus que sa phrase si la suivante est courte (`start` manuel dans `shots.json`).

## Les prompts Flow

- Décor **au crépuscule** par défaut (ciel violet-orange, fenêtres allumées), nuit bleu marine avec une seule lumière chaude pour `dark: true` (danger, solitude, labo la nuit).
- Compositions en rotation (`prompts.py`) : large, moyen, gros plan, vue de dessus, POV mains. Pour les répliques, un plan moyen sur celui qui parle, bouche fermée, jamais de bulle.
- Mots interdits et suffixe anti-texte : `flow-automation.md`. Les scores, bulletins et écrans sont **toujours** par code : Flow écrit des chiffres faux.
- Miniature : gabarit `thumbnail` du style (visage en gros plan à droite, accessoire unique, moitié gauche vide) ; le texte et le badge « PART n » par `thumb.py`.
