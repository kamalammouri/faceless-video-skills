---
name: what-if-story-video
description: Écrit et produit des vidéos YouTube de fiction « What If You… » à la 2ᵉ personne (tu reçois un pouvoir ou une condition impossible : réflexes dix fois plus rapides, 500 de QI, une seconde vie, une boucle temporelle, lire dans les pensées, une gravité cinq fois plus faible), format mesuré sur la chaîne Ifverse Tales (12 vidéos, 8,5 M de vues en 3 semaines) — épisodes de 6 à 9 min en séries de 3 parties plus compilation, narrateur lent et répliques de personnages, une règle avec sa limite, une escalade plus/moins, un dilemme moral, un cliffhanger. Produit le brief, le script avec répliques, la shot list, les voix par personnage, les images Flow au style stickman sombre, le montage avec mouvement léger, la miniature et la fiche de publication. Use whenever the user wants a "what if you had / could / were…" story, a superpower or thought-experiment fiction video, a second-person sci-fi short, a stickman animated story, a 3-part series with cliffhangers, or says "comme Ifverse", "what if", "et si tu avais…", "pouvoir", "histoire à la deuxième personne", even if they don't say "skill".
---

# What If Story Video (format « What If You… », chaîne Ifverse Tales)

Fiction courte à la 2ᵉ personne : **tu** reçois un pouvoir, la vidéo te fait vivre ce que ça change, puis te met devant un choix. Mesuré sur les 12 vidéos de la chaîne de référence (étude dans `references/reference-ifverse.md`) : 6 à 9 min, 85 à 125 mots par minute, 6 à 8 « you » pour 100 mots, un plan toutes les 3 à 4 s dont deux sur trois en mouvement, des répliques jouées par plusieurs voix, des séries en trois parties puis un film. Le skill contient la méthode, pas une histoire : chaque demande = un pouvoir, un héros, un dilemme nouveaux.

## Langue et sortie
- Répondre dans la langue de l'utilisateur. **Script en anglais par défaut** (le doublage automatique fait le reste), répliques comprises.
- Livrable par défaut : `script.md` (script avec répliques marquées), `shots.json`, `brief.json`, fiche de publication ; en production complète : `voice.wav`, `flow/`, `out.mp4`, `thumb.jpg`.

## La formule

```
UN POUVOIR QUE LE SPECTATEUR A DÉJÀ RÊVÉ D'AVOIR, AVEC UN CHIFFRE (10x, 500 IQ, 5x)
+ OUVERTURE À FROID : LE POUVOIR EN ACTION DANS UNE MICRO-SCÈNE + UNE RÉPLIQUE DE TÉMOIN
+ LA RÈGLE ET SA LIMITE (« your brain got faster, your muscles did not »)
+ L'ESCALADE PLUS / MOINS : quotidien → jeux → sport ou école → célébrité, un chiffre et une réplique par palier
+ LE PRIX (ennui, faim, solitude, le monde trop lent)
+ SAUT DANS LE TEMPS → LE DILEMME : LE HÉROS SACRIFIE LA VICTOIRE POUR SAUVER QUELQU'UN
+ L'ACCROCHE DE LA SUITE (une voiture noire, un écran qui s'allume seul) → PARTIE 2, PARTIE 3, FILM
+ « SO WHAT WOULD YOU DO WITH… ? » + « IF YOU'D HAVE [FAIT CE CHOIX] TOO, HIT LIKE »
```

Pourquoi ça marche : la fiction bat l'explication (même sujet « réflexes humains » : 4,6 M de vues contre 150 k pour l'explainer) ; la limite posée à la minute 1 devient le problème du climax ; le dilemme moral donne l'émotion, pas la victoire ; la question finale renvoie le choix au spectateur ; la trilogie multiplie les vues d'une seule écriture.

## Workflow
1. **Brief** (`references/brief.md`, deux tours) : le pouvoir **et sa limite**, le héros (prénom, couleur du sweat), style de personnage (défaut `stickman-dark`), voix (moteur, narrateur, personnages), durée (défaut 8 min), livrable, et la **série** (épisode 1 de 3 : chaque partie a son cliffhanger). Tour 2 : l'agent **Story architect** propose **3 dilemmes** ; l'utilisateur en choisit un.
2. **Faits** : 4 à 8 chiffres réels pour la prémisse et les « science notes » (temps de réaction 0,25 s, faux départ sous 0,1 s, QI 100 / 140 / 160). Chercher sur le web, ne jamais inventer. `references/premise-bank.md` pour les pouvoirs, limites et dilemmes déjà cartographiés.
3. **Script** avec `references/story-template.md` : 8 temps, 700 à 1 000 mots, répliques marquées `[MOM]`, `[JAKE]`, narration sans marque. Puis **Fact-checker** et **Script critic** (qui vérifie règle → limite → dilemme → cliffhanger).
4. **Shot list** `shots.json` (format en tête de `scripts/prompts.py`) : un plan par phrase ou réplique, `speaker` sur les répliques, familles scène / icône / schéma / carte / titre ; cartes score, bulletin et téléphone par `scripts/cards.py` (`scoreboard`, `phone`, `card`) ; **budget Flow de 5 images par minute** (une scène tenue sur 2 ou 3 phrases avec le même `file`), vérifié par `python scripts/prompts.py shots.json`. Puis **Visual director** et **Prompt auditor**.
5. **Voix** : `python scripts/tts.py shots.json` (edge-tts ou Gemini selon le brief, `references/voice.md`) avec la table `voices` du brief : une voix par personnage, le narrateur lent (`-8%`), silences de 0,5 s. Tester trois plans avant le lot.
6. **Images** : Flow en automatique (`references/flow-automation.md`, style `stickman-dark` de `scripts/styles.json`), contrôle par **Image QC**, rejets régénérés ; cartes et graphiques par code.
7. **Montage** : `python scripts/build_slideshow.py shots.json voice.wav timing.json out.mp4 --flow flow/<video> --motion` (zoom lent sur deux images sur trois, coupes franches). Planche contact par `scripts/sheets.py`.
8. **Miniature et publication** : `references/publication.md` (titre « What If You… ? », visage du héros à droite + 2 ou 3 mots jaunes à gauche + badge « PART n », description au gabarit avec science notes, **catégorie écrite**), puis **Publication checker**.

## Agents de production
Lancés en parallèle avec l'outil Agent, briefs dans `references/agents.md` : **Story architect** (3 dilemmes) et **Character designer** (style custom) avant le script ; **Fact-checker** et **Script critic** après le brouillon ; **Render router** (plan par plan : code ou Flow ; un symbole seul, un chiffre, un score ou une frise ne vont jamais à Flow), puis **Visual director** et **Prompt auditor** après la shot list ; **Image QC** (vision) après chaque lot ; **Publication checker** avant livraison. Ne jamais sauter Story architect (c'est le dilemme qui fait la vidéo), Visual director et Image QC. Quand le skill **hand-drawn-visuals** est installé, les inserts par code (symbole, chiffre, score, graphique, frise, titre) passent par lui (`family: "html"` + spec, rendu dans le navigateur avec rough.js et les icônes Lucide, bien plus proche du dessin à la main que `cards.py`) ; `cards.py` et `charts.py` restent le secours sans navigateur.

## 1. Choisir le pouvoir (test du rêve)

Un sujet marche quand le spectateur **a déjà imaginé l'avoir** : plus rapide, plus intelligent, recommencer sa vie, lire les gens, voler. Sur la chaîne de référence, les pouvoirs « corps et cerveau » (réflexes, QI, temps) font 400 k à 4,6 M ; les pouvoirs sociaux (mentaliste) 80 k ; les mondes imaginaires (planète à faible gravité) 40 k. Trois conditions : (a) un chiffre dans le titre ; (b) une **limite physique** évidente qui crée l'intrigue ; (c) un dilemme où le pouvoir ne suffit pas et où il faut **choisir**.

## 2. Structure calibrée (8 min ≈ 800 mots à 100 mots/min ; 6 min = 650, 9 min = 1 000)

| # | Temps | Durée | Mots | Contenu |
|---|---|---|---|---|
| 1 | **Ouverture à froid** | 10–30 s | 40–70 | Le pouvoir en action dans une micro-scène concrète, 2ᵉ personne, présent ; une réplique de témoin (« How did you do that? ») |
| 2 | **Prémisse chiffrée** | 20 s | 40–60 | La norme en chiffres → toi ; la question-titre « So what if… ? » ; carte-titre |
| 3 | **La règle et sa limite** | 15–20 s | 40–60 | « Here's how it works » : un mécanisme en une phrase, et ce que le pouvoir **ne** fait **pas** |
| 4 | **Escalade plus / moins** | 3–4 min | 300–400 | 4 à 6 paliers, chacun avec un chiffre, une réplique courte, un « Plus: » ou « Minus: » dit à voix haute ; un surnom public (« The Wall », « The Boy Who Knows ») |
| 5 | **Le prix** | 30–45 s | 60–90 | 3 coûts concrets (maux de tête, faim, ennui, solitude, ne rien pouvoir montrer) ; « the world feels slow » |
| 6 | **Saut dans le temps + dilemme** | 1,5–2 min | 150–220 | « Two years later. » Le grand enjeu ; au moment décisif, la limite du temps 3 revient ; le héros sacrifie la victoire pour sauver quelqu'un ; la foule applaudit ; « you just won something bigger » |
| 7 | **Accroche de la suite** | 20–30 s | 40–60 | Un inconnu, une voiture noire, « We've been watching you » ; ou un écran qui s'allume seul ; dernière phrase = question ouverte |
| 8 | **Outro** | ≤ 20 s | 30–40 | « So what would you do with… ? Tell us in the comments. And if you'd have [fait le choix du héros] too… hit like, and subscribe for Part Two. » |

Parties 2 et 3 : rappel en 30 s (« Your name is Max. Your brain is ten times faster. Not your body. »), un nouveau décor (le labo, la ville), un mentor et un rival, la limite poussée à l'extrême (« il ne peut pas esquiver la balle, mais il voit le doigt sur la détente »), un bloc « But is any of this real? » de 3 faits avant l'outro. Le film = les trois parties bout à bout, chapitres « PART 2 : … ».

## 3. Règles d'écriture
- **2ᵉ personne, présent**, 6 à 8 « you / your » pour 100 mots ; le narrateur parle **lentement** (100 mots/min) : phrases de 4 à 14 mots, points de suspension pour les silences (« You just... catch it. »).
- **Répliques** : 15 à 25 % des lignes, marquées `[NOM]` en tête de ligne, 3 à 10 mots chacune, jamais d'exposition ; le témoin réagit, le héros répond court (« They think I'm cheating. »). Narrateur = ligne sans marque.
- **« Plus: » / « Minus: » / « The catch? »** prononcés tels quels ; chaque palier a un chiffre vrai (« a table tennis smash crosses the table in a fifth of a second »).
- La **limite** du temps 3 doit revenir mot pour mot au climax.
- Le dilemme oppose toujours **gagner** et **sauver** ; le héros sauve. Jamais de méchant tué, jamais de vengeance : « you didn't take a cent, you just showed everyone the truth ».
- Pas de symboles ni d'abréviations (voix IA) ; chiffres en lettres quand la voix les dit ; noms propres faciles (Max, Leo, Zoe, Jake, Dr Lee).
- Univers partagé : les personnages reviennent d'une série à l'autre ; noter dans `brief.json` (`universe`) ceux déjà créés.

## 4. Les images (résumé ; détail dans `references/visual-style.md`)
Style `stickman-dark` : silhouette noire à tête ronde, yeux blancs à reflet étoilé, sweat à capuche de couleur (le héros rouge, le rival bleu), décors peints au crépuscule violet-orange, nuit bleu marine avec une lumière chaude. Un plan toutes les 3 à 4 s : scènes Flow (tenues 2 ou 3 phrases, budget 5 par minute), inserts par code (score, bulletin, écran de téléphone, chiffre de la prémisse, carte-titre). `--motion` au montage : zoom lent sur deux images sur trois. Texte à l'écran seulement par code, jamais par Flow.

## 5. Contrôle qualité avant livraison
- [ ] `brief.json` validé : pouvoir + limite, héros, style, voix (narrateur + personnages), série, dilemme choisi parmi 3
- [ ] Titre « What If You … ? » avec un chiffre, 6 à 9 mots
- [ ] Ouverture à froid = micro-scène + réplique en moins de 70 mots ; prémisse chiffrée ; règle **et** limite avant 1 min
- [ ] 4 à 6 paliers plus / moins avec chiffre et réplique ; le prix en 3 coûts
- [ ] Dilemme gagner / sauver ; la limite du temps 3 revient au climax ; cliffhanger ; outro avec la question du choix
- [ ] 650 à 1 000 mots selon la durée ; 6 à 8 « you » pour 100 mots ; répliques 15 à 25 % marquées `[NOM]` ; 4 à 8 chiffres vérifiés
- [ ] `shots.json` : `speaker` sur chaque réplique ; budget Flow respecté (lint `prompts.py` sans erreur) ; cartes par code pour tout chiffre ou texte
- [ ] Voix : une voix par personnage présente dans `brief.voices`, aucun « speaker sans voix » au rapport de `tts.py`
- [ ] Images : planche contact passée par Image QC (même silhouette, même sweat, aucune bulle ni texte) ; montage avec `--motion`
- [ ] Miniature 1280 × 720 : visage à droite, 2 ou 3 mots jaunes, badge « PART n » ; fiche de publication complète avec **catégorie écrite**, science notes, liens des autres parties, commentaire épinglé
