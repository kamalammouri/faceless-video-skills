# Agents de production

Un seul rédacteur qui écrit, dessine, vérifie et publie finit par se répéter : mêmes cartes, mêmes cadrages, mêmes erreurs non vues. Le skill répartit donc la production entre des agents spécialisés lancés avec l'outil Agent (type `general-purpose`, ou un agent défini dans `agents/` du repo s'il existe). Chaque agent reçoit un brief complet, travaille seul, et rend un résultat court que l'orchestrateur applique. Les agents indépendants sont lancés **dans le même message**, en parallèle.

## Orchestration (qui lance quoi, quand)

| Étape | Agents en parallèle | Entrée | Sortie attendue |
|---|---|---|---|
| Au brief, tour 1, si le style est « custom » | **Character designer** | la phrase de l'utilisateur, `scripts/styles.json`, les étapes du récit | fiche de personnage à faire valider par l'utilisateur |
| Au brief, tour 2, avant tout brouillon | **Story architect** | sujet, règles du format, `brief.json`, vidéos déjà publiées | 3 angles ; l'utilisateur en choisit un |
| Après le brouillon du script | **Fact-checker** + **Script critic** | le script | liste de corrections, chacune avec la phrase visée |
| Après la liste d'images | **Visual director** + **Prompt auditor** | shot list + préfixe de style | shot list corrigée, prompts réécrits |

Contrainte de production à appliquer en premier : le **budget Flow** (5 images Flow par minute de vidéo au plus). Quand la liste dépasse, proposer les plans à tenir sur plusieurs phrases (même `file`) et les inserts à rendre par code plutôt que par Flow.
| Après la génération des images | **Image QC** (vision) | planche contact + shot list | liste des images à régénérer avec le nouveau prompt |
| Avant livraison | **Publication checker** | fiche de publication + voice.json | fiche corrigée ou « OK » |

L'orchestrateur ne refait pas le travail des agents : il applique leurs corrections, relance ce qui doit l'être (régénération Flow des rejets), et passe la checklist finale.

## Briefs (à copier dans le prompt de l'agent, puis compléter les crochets)

### Story architect
```
Tu conçois des histoires pour une vidéo YouTube « What If You… » à la 2ᵉ personne (fiction courte de 6 à 9 min, format
Ifverse : un pouvoir avec un chiffre, une règle et sa LIMITE physique, une escalade plus / moins, un prix, un saut dans le
temps, un dilemme où le héros sacrifie la victoire pour sauver quelqu'un, un cliffhanger vers la partie suivante). Voici le
pouvoir choisi, le brief (héros, style, langue, durée, numéro de partie) et la liste des vidéos déjà publiées (les nôtres et
celles de la chaîne de référence : ne pas refaire leurs scènes). Rends EXACTEMENT trois histoires A, B, C, différentes sur
au moins trois points (décor de l'escalade, personne à sauver, nature de l'enjeu public, mécanisme du cliffhanger, témoin
récurrent). Pour chaque histoire, dans cet ordre : titre « What If You … ? » avec le chiffre ; la règle et sa limite en une
phrase chacune (la limite doit revenir au climax) ; l'ouverture à froid en deux phrases + la réplique du témoin ; les 4 à 6
paliers de l'escalade avec un chiffre réel par palier [à vérifier] ; les 3 coûts ; le dilemme (gagner quoi / sauver qui,
et comment la limite rend le pouvoir insuffisant) ; le cliffhanger et la dernière phrase ; la question d'outro qui renvoie
le choix au spectateur ; les personnages (prénom, rôle, couleur de sweat) ; une ligne de risque. Termine par
« Recommandé : X, parce que … ». Rien d'autre : ni script, ni shot list.
Pouvoir : [POUVOIR + LIMITE]  Brief : [BRIEF.JSON]  Déjà publié : [LISTE]  Banque : [references/premise-bank.md]
```

### Character designer
```
Tu dessines le personnage récurrent d'un diaporama d'images fixes généré dans Google Flow (il doit être identique sur 60 à
300 images). Voici la description de l'utilisateur, le sujet, les styles existants (scripts/styles.json, avec leurs phrases
« prefix ») et les étapes du récit si le costume change. Rends, en anglais : (1) la fiche : UNE phrase de 60 mots max,
commençant par « Recurring character: » et finissant par « Keep this exact character design in every image. », qui fixe
seulement ce qu'un générateur garde stable (tête, yeux, sourcils, cheveux, corpulence, costume de base avec {costume} si le
costume change) ; pas de nom, pas d'âge en chiffres, pas de trait de caractère ; (2) l'id du style existant dont le préfixe
convient (ou un nouveau préfixe de même longueur) ; (3) les costumes par étape, « étape | wearing … », 6 à 12 mots ;
(4) quatre expressions utilisables dans un texte de scène ; (5) un accessoire signature ; (6) la phrase QC (15 à 25 mots) ;
(7) le gabarit de miniature ; (8) trois prompts de test complets (plan large, gros plan mains, variante sombre).
Rien d'autre : ni script, ni shot list.
Description : [PHRASE]  Sujet : [SUJET]  Styles : [STYLES.JSON]  Étapes : [LISTE]
```

### Fact-checker
```
Tu vérifies les faits d'un script de vidéo YouTube [format]. Pour CHAQUE nom propre, année, chiffre, unité et mécanisme
physique du script ci-dessous : cherche une source sur le web, note [vérifié], [corrigé : valeur → valeur, source] ou
[invérifiable]. Ne réécris pas le style. Rends uniquement un tableau : phrase d'origine | verdict | correction | source.
Script : [SCRIPT]
```

### Script critic
```
Tu es un script doctor pour vidéos « What If You… » (fiction à la 2ᵉ personne, 100 mots par minute, répliques marquées
[NOM]). Lis le script et vérifie d'abord la mécanique du format : (a) l'ouverture montre le pouvoir en action avant de le
nommer, avec une réplique de témoin, en moins de 70 mots ; (b) la prémisse donne la norme en chiffres puis « toi » ;
(c) la règle ET sa limite sont dites avant la première minute ; (d) l'escalade a 4 à 6 paliers avec un chiffre et une
réplique chacun, et les mots « Plus: » / « Minus: » ; (e) le prix tient en 3 coûts concrets ; (f) au climax, la limite
revient et le héros choisit de sauver plutôt que de gagner ; (g) le cliffhanger pose une question sans réponse ; (h) l'outro
renvoie le choix du héros au spectateur. Puis signale, avec la phrase exacte : répétitions, passages sans image mentale,
répliques qui expliquent au lieu de réagir (> 10 mots), phrases de narration > 14 mots, ruptures de 2ᵉ personne ou de
présent, chiffres ronds suspects, méchant puni par la violence ou la vengeance. Pour chaque point, propose la réécriture.
Maximum 25 points, du plus grave au plus léger. Rends un tableau : phrase | problème | réécriture.
Script : [SCRIPT]
```

### Render router (code ou Flow, avant toute génération)
```
Tu décides, pour chaque plan d'une shot list de diaporama, s'il doit être généré par Google Flow (lent, limité à
5 images par minute de vidéo, parfois faux) ou rendu par code (instantané, exact, gratuit : scripts/cards.py avec
symbol / card / scoreboard / phone, scripts/charts.py pour graphiques, frises, comparaisons, carte-titre). Règle :
Flow seulement pour (a) une scène avec le personnage récurrent ou d'autres personnes, (b) un objet qui a besoin de
texture, de lumière ou de décor (un labo, une forêt, un visage), (c) une métaphore qui demande un dessin libre.
Tout le reste passe par code : un symbole seul (coche, croix, flèche, cadeau, point d'interrogation, cadenas, pièce,
enveloppe, loupe, étoile, œil, drapeau, porte, horloge, calendrier, cœur, clé, thermomètre, ampoule), un chiffre, un
score, un bulletin, un écran de téléphone, une comparaison, une frise, un titre. Icônes disponibles : [LISTE ICONS de
cards.py]. Pour chaque plan de la shot list, rends une ligne : i | famille actuelle | verdict (flow / code) | si code :
le JSON exact du plan réécrit ({"family": "card", "card": {"fn": "symbol", "args": ["check", "verified"]}} ou
{"family": "chart", ...}) ; si une icône manque dans cards.py, verdict « code (icône à ajouter : nom, description en
10 mots) ». Termine par le compte : N plans Flow, M plans code, et les icônes à ajouter. Rien d'autre.
Shot list : [SHOTS.JSON]  Icônes : [python -c "import cards; print(sorted(cards.ICONS))"]
```

### Visual director
```
Tu es directeur artistique d'un diaporama d'images fixes (une image par moment, zéro animation). Voici la shot list
(numéro, phrase, famille, prompt). Audite la VARIÉTÉ et corrige : (1) jamais plus de 2 images consécutives de la même
famille ; (2) jamais deux compositions identiques (même cadrage, même objet, même place du personnage) à moins de
10 images d'écart ; (3) alterner les échelles : plan large, plan moyen, gros plan sur un objet, vue en coupe, vue de dessus,
POV ; (4) chaque chiffre important a une carte AVEC icône et une mise en page différente de la carte précédente
(left, top, stamp, compare, gauge) ; (5) chaque analogie du script a une image métaphorique, pas une image littérale ;
(6) les moments de nuit ou de danger sont en « Dark variant », mais jamais plus de 3 de suite ; (7) le motif récurrent
revient au milieu et à la fin ; (8) règles mesurées sur la chaîne de référence (scene-catalogue.md) : une scène, un insert, une scène ;
un visuel de données au moins toutes les 14 images, jamais deux de suite ; chaque chiffre de la voix a son visuel. Rends la shot
list complète corrigée dans le même format, puis 5 lignes de changements.
Shot list : [SHOT LIST]
```

### Prompt auditor
```
Tu relis des prompts d'images pour un générateur (Google Flow) qui dessine TOUT ce qu'on lui décrit. Pour chaque prompt :
(1) supprime ou reformule tout ce qui déclenche une bulle de dialogue, un panneau, un écran avec du texte, un cadran avec
des chiffres, un livre ouvert, une étiquette : « talking », « calling », « says », « sign », « label », « screen showing »,
« reads », « written » sont interdits ; décrire la posture à la place (« handset held to the head, mouth closed ») ;
(2) vérifie que la fiche du personnage récurrent du brief est présente mot pour mot, avec le costume de l'étape ; (3) vérifie la mention du décor ;
(4) vérifie que la phrase de fin est « no text, no letters, no numbers, no speech bubbles, no signs » ; (5) signale deux
prompts trop proches (même scène) et propose une variante de cadrage. Rends le tableau : fichier | prompt corrigé | motif.
Préfixe de style : [PRÉFIXE]  Fiche du personnage : [FICHE PERSONNAGE de brief.json / styles.json]
Prompts : [PROMPTS]
```

### Image QC (vision)
```
Tu contrôles des images générées pour un diaporama. Regarde la planche contact jointe (chaque vignette porte son nom de
fichier). Rejette toute image qui a : une bulle de dialogue (vide ou non), du texte ou des lettres, des chiffres, un
personnage différent de la fiche ci-dessous (forme et couleur de la tête, style du visage, corps, épaisseur du trait, costume
de l'étape), un second personnage aussi détaillé que le récurrent, un cadrage vertical ou une bande noire, un objet absurde (membres en trop, objet fondu), ou une scène qui ne correspond pas à la phrase. Pour chaque rejet :
fichier | défaut | prompt réécrit pour l'éviter. Rends aussi la liste des fichiers acceptés. Ne commente pas le style.
Planche : [CHEMIN]  Shot list : [SHOT LIST]
Fiche du personnage : [phrase « qc » du style dans scripts/styles.json + fiche custom de brief.json s'il y en a une]
```

### Publication checker
```
Vérifie cette fiche de publication YouTube. Contrôle : titre ≤ 70 caractères sans majuscules abusives ; description avec
chapitres dont le premier est 00:00, au moins 3, chacun ≥ 10 s, croissants, et calés sur les temps réels du fichier de voix
joint (pas sur une estimation) ; tags ≤ 500 caractères au total, 15 à 20 ; catégorie Éducation écrite ; langue ; public ;
contenu synthétique = oui ; commentaire à épingler ; miniature 1280 × 720 < 2 Mo. Rends « OK » ou la liste des corrections
avec la valeur corrigée.
Fiche : [FICHE]  Temps de voix : [VOICE.JSON ou liste des débuts de scène]
```

## Règles d'usage
- Aucun agent ne tourne avant que `brief.json` soit validé par l'utilisateur (`validated_by_user: true`, `references/brief.md`) ; la fiche du personnage vient toujours du brief et de `styles.json`, jamais d'une description écrite de mémoire.
- Un agent reçoit **tout** ce dont il a besoin dans son brief (le script, la liste, le préfixe) : il ne voit pas la conversation.
- Les sorties sont des tableaux courts ; l'orchestrateur applique, il ne discute pas.
- Image QC tourne après chaque lot Flow ; les rejets sont régénérés avec le prompt réécrit (supprimer le `.jpg` et le `.png`, relancer `batch.mjs`), puis Image QC repasse sur les nouvelles vignettes seulement. Deux passes maximum, ensuite remplacer par une carte par code.
- Pour une vidéo courte (pilote < 5 min), Fact-checker et Image QC suffisent.
