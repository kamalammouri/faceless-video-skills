# Génération automatique des images avec Google Flow

Google Flow n'a pas d'API. Ce qui marche, mesuré sur un lot de 65 images (27 min, ≈ 25 s par image) : un vrai Chrome piloté par Playwright, ouvert sur Flow avec un profil persistant, et un script qui colle chaque prompt, lance la génération et télécharge le résultat. Les scripts sont dans `scripts/flow/`.

## Prérequis (une fois)

- Node 18+ et le paquet `playwright` installé quelque part (`npm i playwright` dans un dossier) ; indiquer ce dossier par la variable `PLAYWRIGHT_DIR` si ce n'est pas celui du script. Chrome déjà installé suffit (`channel: 'chrome'`).
- Un compte Google avec Flow actif (plan AI Pro ou Ultra : les crédits Flow limitent le nombre d'images par mois).
- Le MCP **Chrome DevTools** rattaché au même Chrome (`claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9222`) permet de voir la page Flow, les tuiles et les images produites sans script (capture d'écran, lecture du DOM) ; il n'est chargé qu'au démarrage d'une session, et Chrome doit déjà écouter sur 9222 (`browser.mjs`).
- Le MCP Playwright, s'il est configuré, sert pour les étapes interactives (ouvrir le projet, régler le format, vérifier une image) ; pour un lot, utiliser les scripts : le MCP ne récupère pas les octets d'une image et relancerait un appel par image.

## Procédure

1. **Ouvrir Chrome** : `node scripts/flow/browser.mjs` en arrière-plan, et le laisser tourner. Le profil (`~/.flow-profile` ou `FLOW_PROFILE`) garde la session Google d'une fois sur l'autre.
2. **Connexion** : `node scripts/flow/login.mjs` clique « Créer avec Google Flow » puis attend jusqu'à 20 min que l'utilisateur se connecte lui-même dans la fenêtre. Ne jamais saisir un mot de passe soi-même : le demander à l'utilisateur.
3. **Préparer le projet** : dans la fenêtre, créer un projet Flow, passer en mode image, régler le format 16:9 une fois (il reste réglé pour le projet). Vérifier que la zone « Que voulez-vous créer ? » est visible.
4. **Générer `prompts.json`** avec `python scripts/prompts.py shots.json` : il assemble préfixe, fiche personnage, décor, gabarit de famille, cadrage et suffixe anti-texte pour chaque plan, et refuse les prompts à risque (mots qui déclenchent des bulles). Ne pas écrire les prompts à la main : le préfixe complet doit être dans **chaque** prompt, Flow n'a pas de mémoire entre deux générations. Le style (préfixe, fiche du personnage, costume, décor) vient de `brief.json` (`references/brief.md`) et de `scripts/styles.json` ; `--style ID` force un style, `python scripts/prompts.py --styles` les liste.
5. **Lancer le lot** : `PACE=45000 node scripts/flow/batch.mjs prompts.json flow/<video>`. Un fichier déjà présent est sauté, donc relancer la même commande reprend après une coupure. Rediriger la sortie dans un log et le surveiller en arrière-plan. **Toujours tester sur 3 prompts d'abord** (un `p3.json` extrait de la liste), faire la planche contact et vérifier que chaque image correspond bien à son prompt avant de lancer les 160 autres.
6. **Convertir** : `python scripts/flow/convert.py flow/<video>` produit les PNG attendus par le script de montage.
7. **Contrôler** : `python scripts/sheets.py flow/<video> sheets` fait les planches contact étiquetées (12 images par planche), chercher les trois défauts fréquents : texte ou lettres dans l'image, personnage différent, cadrage vertical. Supprimer le `.jpg` et le `.png` fautifs puis relancer le lot : seuls ceux-là sont régénérés.
8. **Monter** la vidéo avec les images, puis la miniature par code.

## Ce qu'il faut savoir

- Interface (flow.google.com, octobre 2026) : la barre de prompt en bas porte la zone `Que voulez-vous créer ?`, un bouton **Agent** (à laisser DÉSACTIVÉ : le mode direct génère sans conversation), un déclencheur de paramètres (Image · 16:9 · modèle Nano Banana · x1, réglé une fois par projet, `batch.mjs` le vérifie) et le bouton `Lancer la génération`. Chaque résultat est un `group` dans `<main>` dont le texte contient le prompt complet et dont l'`<img>` fait 1376 × 768 ; `batch.mjs` lit la tuile qui porte SON prompt, sinon la **première** tuile de la liste (la plus récente), et n'accepte qu'une URL d'image absente avant le clic (liste remise en haut avant chaque lecture, car elle est virtualisée). Mesuré : 24 s de génération par image, 0 crédit par image Nano Banana. Si Google change l'interface, `node scripts/flow/peek.mjs out.png` donne la capture et l'arbre d'accessibilité pour corriger les sélecteurs.
- `browser.mjs` ouvre un Chrome **séparé** (profil `~/.flow-profile`, port 9222) : un Chrome déjà ouvert ne peut pas être piloté (pas de port de débogage, et Chrome refuse le CDP sur le profil par défaut). La connexion Google se fait une fois dans cette fenêtre et reste.
- **Détection du résultat** : Flow insère la nouvelle génération en **première tuile** de la grille (`flow-grid-tile-container`), avec le prompt complet en `aria-label` pendant le chargement, puis l'image et une légende courte. `batch.mjs` ne lit que cette première tuile. L'ancienne méthode (« toute image dont l'URL n'était pas là avant ») a produit un lot entier décalé : la grille est virtualisée et des vignettes **anciennes** du projet se chargent tardivement, prises pour le résultat (les 12 premières images du blush étaient des scènes polaires du projet précédent). Si le libellé de la première tuile n'est pas le prompt 15 s après le clic, le script note `NOT QUEUED` et passe.
- **Cadence** : Flow a un détecteur d'« activité inhabituelle » (carte « Échec … Cette génération ne vous a rien coûté »). Mesuré en octobre 2026 : à 7 s d'intervalle, blocage de deux à trois heures ; à `PACE=12000` (≈ 35 s par image), 30 images passent puis les refus se multiplient et le lot s'effondre. Tenir **45 à 60 s par image** (`PACE=45000` par défaut, 60000 par sécurité, ≈ 1 h 40 pour 110 images). `batch.mjs` compte les cartes « Échec » : une nouvelle carte = refus, pause 3 min puis 6 min, et le script **s'arrête de lui-même au troisième refus consécutif** (`MAXFAIL`) ; attendre au moins 30 min avant de relancer la même commande, qui reprend là où elle en était.
- **Récupération** : quand le script note `TIMEOUT` ou `NOT QUEUED`, l'image a souvent été générée quand même (la tuile a reçu sa légende avant d'être reconnue). Ne jamais régénérer à l'aveugle : `node scripts/flow/harvest.mjs flow/<video>` ouvre le filtre « Images », fait défiler toute la liste virtuelle, télécharge chaque image dans `flow/<video>/harvest/H###.jpg` et marque celles déjà présentes (mêmes octets). `python scripts/flow/harvest_sheet.py flow/<video>` fait la planche des inconnues avec la légende de Flow ; les apparier à `prompts.json` à l'œil (les tuiles sont du plus récent au plus ancien, donc l'ordre inverse du lot), puis copier chaque H-fichier sous son nom F. Sur le lot calvitie : 32 images téléchargées par le lot, 44 récupérées ainsi, 37 régénérées.
- `scripts/flow/peek.mjs out.png` : capture d'écran et texte de la page Flow, pour diagnostiquer un blocage sans toucher à la fenêtre.
- Sortie Flow : 1376 × 768 ; le montage redimensionne en 1920 × 1080 sans perte visible dans ce style.
- Bouton de génération grisé = plus de crédits ou prompt vide : le script saute l'image et continue.
- Une image par phrase (300 images pour 20 min) coûte 2 h de génération et autant de crédits : regrouper en **un plan par moment** (5 à 15 s, 60 à 70 images pour 11 min) et faire les chiffres, cartes et graphiques par code.
- Les images avec personnage sont les seules que Flow fait mieux que le code ; icônes, schémas, frises et chiffres restent par code (exacts, cohérents, gratuits).


## Ce que Flow dessine quand on ne le lui interdit pas : bulles, panneaux, cadrans

Le générateur dessine **tout** ce que le prompt évoque. « The character calls the base on the radio » donne un personnage avec deux bulles de dialogue vides, puisque le texte est interdit : c'est l'image la plus moche de la vidéo polaire. Règles pour chaque prompt :
- Mots interdits dans la scène : `talking`, `calling`, `says`, `speaks`, `conversation`, `sign`, `label`, `poster`, `screen showing`, `reads`, `written`, `clock showing`, `gauge reading`. Décrire la **posture** à la place : « handset held to the side of the head, mouth closed », « looking at a blank screen that glows », « a round dial with a single red needle, no digits ».
- Terminer chaque prompt par : `no text, no letters, no numbers, no speech bubbles, no signs, no labels`.
- Les chiffres, heures, jours, jauges, cartes et graphiques ne sont **jamais** demandés à Flow : ils sont rendus par `scripts/cards.py` et les graphiques par code (exacts, cohérents, gratuits).
- Après chaque lot, l'agent **Image QC** (`references/agents.md`) regarde la planche contact et liste les rejets (bulle, texte, personnage différent, cadrage) avec un prompt réécrit ; supprimer les fichiers rejetés et relancer `batch.mjs`, qui ne régénère que ceux-là. Deux passes maximum, puis remplacer par une carte par code.

## Préfixe de style et fiche du personnage

Ils viennent du style choisi au brief (`scripts/styles.json`, catalogue dans `references/character-styles.md`) ; `prompts.py` les assemble dans chaque prompt dans cet ordre : préfixe, fiche du personnage avec le costume de l'étape, décor, cadrage et scène, fond de la famille, variante sombre, suffixe anti-texte. Exemple assemblé avec le style `egg-headphones` (le style d'origine, validé sur 65 images) :

```
Modern storybook illustration, soft textured pencil shading, gentle ambient lighting, clean minimalist composition, generous empty space, no text, no letters, no words, 16:9 wide format. Plain cream-colored paper background. Recurring character: a whimsical figure with a smooth matte white egg for a head, small dark dot eyes and thin expressive eyebrows, thin stick-figure arms and legs, wearing a simple dusty-blue t-shirt and dark mittens, with large vintage over-ear headphones in warm orange-brown leather tones around the egg head. Keep this exact character design in every image. Setting: [DÉCOR EN UNE PHRASE, IDENTIQUE DANS TOUS LES PROMPTS]. [SCÈNE] no text, no letters, no numbers, no speech bubbles, no signs, no labels.
```

Variante sombre (clé `dark` du style), ajoutée par `prompts.py` aux plans marqués `"dark": true` : `Dark variant: same drawing style, but a dark slate-blue background instead of cream, with a single warm orange light source.`

## Miniature

Générer la scène dans Flow avec le gabarit `thumbnail` du style (`styles.json`) : pour `stickman-meme`, composition coupée en deux, le personnage perdant à gauche et gagnant à droite dans le même décor ; pour les autres styles, le personnage en gros plan sur la moitié droite, moitié gauche vide ; le texte (2 à 4 mots, jaune 242,196,70, police Impact, contour noir 10 px ; chiffre-motif en rouge 214,72,48) est ajouté par code (PIL) en 1280 × 720, jamais par le générateur. En attendant l'image dédiée, une image du lot avec de l'espace vide fait une miniature provisoire acceptable.
