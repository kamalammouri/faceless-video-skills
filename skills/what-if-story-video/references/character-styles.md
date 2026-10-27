# Catalogue des styles de personnage

Un style = un préfixe de dessin + une fiche de personnage récurrent + les fonds (scène, insert, variante sombre) + un gabarit de miniature + une phrase de contrôle pour Image QC. Les valeurs exactes sont dans `scripts/styles.json` (une entrée par id) ; ce fichier dit **d'où vient chaque style, quand le choisir et ce qu'il impose**. Le style est choisi par l'utilisateur au brief (`references/brief.md`), jamais par le rédacteur.

Pour ajouter un style : une entrée dans `styles.json` (copier la plus proche), une section ici, puis 3 prompts de test dans Flow et une planche contact avant tout lot.

| id | Observé sur | Personnage | Dessin | À choisir pour |
|---|---|---|---|---|
| `stickman-meme` | miniatures de Galon Zéro (18 vidéos, 1,6 M de vues) | grosse tête ronde blanche, visage rage-comic (yeux simples, sourcils expressifs, bouche dessinée), corps blanc fin, costume par étape | trait noir épais, couleurs saturées, décor peint détaillé avec profondeur | récits où le personnage **change de statut** (grades, années, avant/après) ; ton ironique ou dramatique ; l'émotion se lit à 100 px |
| `egg-headphones` | 65 images Flow validées (style maison d'origine) | tête d'œuf blanche, casque orange, t-shirt bleu gris, mitaines | storybook crème, crayon doux, beaucoup de vide | explainers calmes, scènes intimes, tout sujet « science du quotidien » |
| `storybook-human` | intérieur des vidéos Galon Zéro | un humain réaliste (jeune homme, cheveux noirs courts), costume d'époque | film d'animation japonais années 90, fonds peints, lumière chaude | récits historiques ou d'organisation où le décor d'époque compte ; public qui veut de l'immersion, pas du meme |
| `caveman-duo` | miniatures Apefully / The Hidden Bargain | deux mascottes préhistoriques (homme et femme), gros yeux, membres en bâtons | cartoon saturé | explainers « évolution » ; miniature expressive (choc, sueur, larmes) |
| `thin-line` | explainers Apefully anciens | tête ronde blanche à yeux-points, membres fins | encre fine, pastels, fond crème | icônes et schémas nombreux, personnage secondaire |
| custom | fiche écrite par l'agent Character designer | ce que l'utilisateur décrit | à choisir parmi les préfixes ci-dessus | tout le reste |

## Ce que montrent les deux chaînes de référence

**Galon Zéro** sépare deux styles : la **miniature** est en `stickman-meme` (composition coupée en deux, le même personnage perdant à gauche et gagnant à droite, sans texte), et **l'intérieur** de la vidéo est en `storybook-human` (un protagoniste humain peint, scènes de groupe, sous-titres blancs incrustés en bas, barre de progression des grades au début). Le contraste miniature / intérieur ne gêne pas l'audience : la miniature vend l'émotion, l'intérieur vend l'immersion. Détail des mesures dans `examples/galonzero/analysis.md` du dépôt.

**Apefully / The Hidden Bargain** font pareil : duo de cavemen cartoon en miniature, personnage crème à l'intérieur.

Le skill laisse les deux choix ouverts : le brief demande le style de **l'intérieur** ; la miniature prend par défaut le gabarit `thumbnail` du même style, et l'utilisateur peut demander un style de miniature différent (clé `thumbnail` du brief, valeur = un id de style).

## Règles communes à tous les styles

- La fiche du personnage est recopiée **mot pour mot dans chaque prompt** où il apparaît (`prompts.py` s'en charge) ; Flow n'a pas de mémoire.
- Les autres personnages d'une scène sont **moins détaillés** que le récurrent (gris, sans visage pour `stickman-meme` ; au second plan pour les autres), sinon Image QC ne sait plus lequel est le héros.
- Le **costume** porte le récit : il change par grade, par saison, par état (neuf → déchiré). Le brief liste les costumes par étape et `shots.json` les pose plan par plan (`costume`). La tête et le corps ne changent jamais.
- Jamais de texte, de bulle, de panneau, de cadran chiffré dans l'image : les chiffres sont des cartes par code (`cards.py`, `charts.py`).
- Variante sombre (`dark`) pour la nuit et le danger, jamais plus de 3 de suite.

## Fiches détaillées

### `stickman-meme`
- **Fiche** : voir `styles.json`. Le mot « rage-comic » et « meme stick figure » suffisent à Flow pour le visage ; ne pas nommer de meme précis (trollface, etc.) : le générateur ajoute alors du texte ou déforme la bouche.
- **Émotions utiles** (à écrire dans `scene`) : sweating and worried · smug half-closed eyes · wide shocked eyes · tears streaming · blank stare · gritted teeth. Une émotion par plan, jamais deux personnages avec la même.
- **Costume par étape** : « wearing a torn grey tunic » (bas) → « wearing a tailored black suit » (haut). Le contraste des costumes fait la miniature.
- **Miniature** : gabarit `thumbnail` = split vertical, perdant à gauche (sueur, bouche tremblante), gagnant à droite (yeux mi-clos, sourire en coin), même décor, bande vide en haut pour le texte par code. Pas de texte dans l'image.
- **QC** : rejeter toute image où la tête n'est pas ronde et blanche, où le visage a des traits réalistes, où un second personnage est aussi détaillé que le héros, ou où apparaît une bulle.

### `egg-headphones`
- La fiche d'origine du dépôt ; validée sur 65 images. Composition : personnage petit à moyen, beaucoup de vide, fond crème ; variante ardoise pour la nuit.
- **Miniature** : gros plan du personnage sur la moitié droite, moitié gauche vide, une seule lueur chaude.

### `storybook-human`
- Le personnage est **un humain**, donc la fiche doit fixer : coupe et couleur des cheveux, forme du visage, sourcils, costume. Modifier `character` dans `styles.json` ou passer une fiche custom pour un autre héros (femme, âge différent).
- Ce style tolère les scènes de groupe détaillées (tablées, rangs de soldats) : c'est son avantage pour les récits d'organisation.
- Pas de trait épais, pas de couleurs saturées : si Flow renvoie du cartoon, ajouter « soft painterly, no thick outlines » dans `scene`.

### `caveman-duo` et `thin-line`
- Styles conservés pour les explainers « évolution » et les vidéos très « icône » ; fiches dans `styles.json`.

### custom
- L'utilisateur décrit le personnage en une phrase ; l'agent **Character designer** (`references/agents.md`) rend : la fiche de prompt en anglais (≤ 60 mots, une seule phrase, terminée par « Keep this exact character design in every image. »), le préfixe de dessin choisi parmi les styles existants, 3 costumes par étape si le récit en a, 4 expressions, un accessoire signature, la phrase QC, le gabarit de miniature, et 3 prompts de test. La fiche validée va dans `brief.json` → `character.sheet`, et `style` prend l'id du préfixe choisi.

## stickman-dark : silhouette noire, yeux blancs, sweat à capuche (style Ifverse Tales)

Le style de la chaîne de référence du skill `what-if-story-video` : stick figure en silhouette noire pleine, grande tête ronde noire, deux yeux blancs ovales avec un reflet en étoile, sweat à capuche de couleur (héros rouge, rival bleu, figurants gris, vert, jaune), décors peints au crépuscule violet-orange, nuit bleu marine avec une lumière chaude. Les émotions passent par les yeux. Convient aux fictions « What If », aux histoires de pouvoir, aux séries avec plusieurs personnages récurrents. Miniature : visage en gros plan à droite, un accessoire, moitié gauche vide pour le texte.
