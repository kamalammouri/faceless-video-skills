# Génération automatique des images avec Google Flow

Google Flow n'a pas d'API. Ce qui marche, mesuré sur un lot de 65 images (27 min, ≈ 25 s par image) : un vrai Chrome piloté par Playwright, ouvert sur Flow avec un profil persistant, et un script qui colle chaque prompt, lance la génération et télécharge le résultat. Les scripts sont dans `scripts/flow/`.

## Prérequis (une fois)

- Node 18+ et le paquet `playwright` installé quelque part (`npm i playwright` dans un dossier) ; indiquer ce dossier par la variable `PLAYWRIGHT_DIR` si ce n'est pas celui du script. Chrome déjà installé suffit (`channel: 'chrome'`).
- Un compte Google avec Flow actif (plan AI Pro ou Ultra : les crédits Flow limitent le nombre d'images par mois).
- Le MCP Playwright, s'il est configuré, sert pour les étapes interactives (ouvrir le projet, régler le format, vérifier une image) ; pour un lot, utiliser les scripts : le MCP ne récupère pas les octets d'une image et relancerait un appel par image.

## Procédure

1. **Ouvrir Chrome** : `node scripts/flow/browser.mjs` en arrière-plan, et le laisser tourner. Le profil (`~/.flow-profile` ou `FLOW_PROFILE`) garde la session Google d'une fois sur l'autre.
2. **Connexion** : `node scripts/flow/login.mjs` clique « Créer avec Google Flow » puis attend jusqu'à 20 min que l'utilisateur se connecte lui-même dans la fenêtre. Ne jamais saisir un mot de passe soi-même : le demander à l'utilisateur.
3. **Préparer le projet** : dans la fenêtre, créer un projet Flow, passer en mode image, régler le format 16:9 une fois (il reste réglé pour le projet). Vérifier que la zone « Que voulez-vous créer ? » est visible.
4. **Générer `prompts.json`** avec `python scripts/prompts.py shots.json` : il assemble préfixe, fiche personnage, décor, gabarit de famille, cadrage et suffixe anti-texte pour chaque plan, et refuse les prompts à risque (mots qui déclenchent des bulles). Ne pas écrire les prompts à la main : le préfixe complet doit être dans **chaque** prompt, Flow n'a pas de mémoire entre deux générations. Le `STYLE` en tête de `prompts.py` se règle une fois par chaîne (`setting` = le décor en une phrase).
5. **Lancer le lot** : `PACE=12000 node scripts/flow/batch.mjs prompts.json flow/<video>`. Un fichier déjà présent est sauté, donc relancer la même commande reprend après une coupure. Rediriger la sortie dans un log et le surveiller en arrière-plan. **Toujours tester sur 3 prompts d'abord** (un `p3.json` extrait de la liste), faire la planche contact et vérifier que chaque image correspond bien à son prompt avant de lancer les 160 autres.
6. **Convertir** : `python scripts/flow/convert.py flow/<video>` produit les PNG attendus par le script de montage.
7. **Contrôler** : `python scripts/sheets.py flow/<video> sheets` fait les planches contact étiquetées (12 images par planche), chercher les trois défauts fréquents : texte ou lettres dans l'image, personnage différent, cadrage vertical. Supprimer le `.jpg` et le `.png` fautifs puis relancer le lot : seuls ceux-là sont régénérés.
8. **Monter** la vidéo avec les images, puis la miniature par code.

## Ce qu'il faut savoir

- Sélecteurs de l'interface (FR / EN) : zone `Que voulez-vous créer ?` / `What do you want to create?`, bouton `Lancer la génération` / `Generate`, images `img[alt*="Vignette"]` / `Thumbnail`. Si Google change l'interface, relire `page.locator('body').ariaSnapshot()` pour retrouver les rôles et noms, et corriger les trois expressions régulières de `batch.mjs`.
- **Détection du résultat** : Flow insère la nouvelle génération en **première tuile** de la grille (`flow-grid-tile-container`), avec le prompt complet en `aria-label` pendant le chargement, puis l'image et une légende courte. `batch.mjs` ne lit que cette première tuile. L'ancienne méthode (« toute image dont l'URL n'était pas là avant ») a produit un lot entier décalé : la grille est virtualisée et des vignettes **anciennes** du projet se chargent tardivement, prises pour le résultat (les 12 premières images du blush étaient des scènes polaires du projet précédent). Si le libellé de la première tuile n'est pas le prompt 15 s après le clic, le script note `NOT QUEUED` et passe.
- **Cadence** : à plus de 6 images par minute Flow affiche « Nous avons remarqué une activité inhabituelle » et refuse tout pendant deux à trois heures (64 échecs sur le premier lot blush, soumis à 7 s d'intervalle). `PACE` (ms de pause après chaque image, 12 000 par défaut) tient le lot à 2 images par minute ; une carte « Échec » fait pauser le script 2 min. Compter ≈ 27 s par image, 75 min pour 160.
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

## Préfixe de style maison (validé par l'utilisateur sur 65 images)

```
Modern storybook illustration, soft textured pencil shading, gentle ambient lighting, clean minimalist composition, generous empty space, no text, no letters, no words, 16:9 wide format. Plain cream-colored paper background. Recurring character: a whimsical figure with a smooth matte white egg for a head, small dark dot eyes and thin expressive eyebrows, thin stick-figure arms and legs, wearing a simple dusty-blue t-shirt and dark mittens, with large vintage over-ear headphones in warm orange-brown leather tones around the egg head. Keep this exact character design in every image. Setting: [DÉCOR EN UNE PHRASE, IDENTIQUE DANS TOUS LES PROMPTS]. [SCÈNE] no text, no letters, no numbers, no speech bubbles, no signs, no labels.
```

Variante sombre, à ajouter aux scènes de nuit ou de danger : `Dark variant: same drawing style, but a dark slate-blue background instead of cream, with a single warm orange light source.`

## Miniature

Générer la scène dans Flow avec le même personnage en gros plan sur la moitié droite, moitié gauche vide ; le texte (2 à 4 mots, jaune 242,196,70, police Impact, contour noir 10 px ; chiffre-motif en rouge 214,72,48) est ajouté par code (PIL) en 1280 × 720, jamais par le générateur. En attendant l'image dédiée, une image du lot avec de l'espace vide fait une miniature provisoire acceptable.
