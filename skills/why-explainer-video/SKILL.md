---
name: why-explainer-video
description: Use when the user wants a faceless animated explainer for YouTube about the human body, evolution or a "what if" question (« Why Evolution… », « Why do humans… », « The real reason… », « Can 2 people… »), a new episode for the channel The Hidden Bargain, a script plus a one-image-per-sentence slideshow, a « WHY … ? » thumbnail, or wants to copy channels like Apefully, Afterimath, Day One Films, Monk Mode Films or Last Soul, even without naming a skill. Also use to grow or audit that channel: more views or subscribers, the YouTube algorithm, CTR, retention, targeting a US audience, publishing hours, thumbnails and titles that do not click, Pinterest promotion, « pourquoi ma vidéo ne décolle pas », « analyse ma chaîne », « booster ma chaîne ». Triggers FR/EN : vidéo explicative, pourquoi l'évolution, chaîne faceless science, diaporama image par phrase, miniature WHY, court-métrage animé explicatif, audit YouTube, audience américaine.
---

# Why Explainer Video (format « Why Evolution Made… », chaîne The Hidden Bargain)

Un paradoxe que le spectateur porte sur lui, expliqué en **4 à 7 minutes** par un diaporama d'images fixes avec un duo de mascottes préhistoriques. Le skill contient la logique et la chaîne de production, pas un sujet : chaque demande = un nouveau sujet.

Le format vient de deux mesures : la chaîne Apefully (19 k abonnés, 2,8 M de vues en 5 semaines, vidéos de 20 min) pour la **mécanique du récit** (paradoxe, fausse croyance, chiffres, marché, question finale), et cinq chaînes de courts animés mesurées le 28 octobre 2026 pour le **format qui perce aujourd'hui** (section 0). Sur The Hidden Bargain elle-même (mesure du 29 octobre 2026, 5 vidéos en 3 jours) : Goosebumps, la seule vidéo courte (3 min 57), à miniature caveman-duo, publiée à 13 h ET, a fait **269 vues** ; les quatre autres, plus longues (8 à 16 min), publiées entre 18 h et 20 h ET, deux avec une miniature egg-headphones et une hors format (histoire de survie « You're Trapped Alone… »), ont fait **4 à 37 vues**. Les normes de la section 0 viennent de cet écart.

## Langue et sortie
- Répondre dans la langue de l'utilisateur. **Script en anglais** (audience anglophone, doublage automatique pour le reste), orthographe **américaine** quand la voix est en-US (diarrhea, hospitalized, centimeters).
- Livrer dans le dossier de travail : `brief.json`, `script.md` (une phrase par ligne), `shots.json`, `publication.md`, `chapters.md`, la vidéo et la miniature.

## 0. Ce que font les chaînes de référence (mesuré le 28 octobre 2026)

| Chaîne | Abonnés | Format | Durée | Meilleure vidéo | Ce qu'on garde |
|---|---|---|---|---|---|
| **Afterimath** (le plus proche de nous) | 7,5 k, 3 vidéos | explainer animé « What if », sources listées en description | 7 min | 2,6 M en 7 jours | titre-question, 12 chapitres de 35 s, hook = une scène (0:00–0:29), sources, « Tell us in the comments », une vidéo tous les deux jours |
| **Day One Films** | 77 k | court animé sur la discipline | 2:40–4:30 | DISCIPLINE 5,2 M | titre d'un mot ou phrase à point (« Lust Is Killing You. »), chapitres nommés comme des temps forts (« The mirror », « Rock bottom », « Day 1 »), description = logline + une maxime |
| **Monk Mode Films** | 22 k | même format, en séries | 3–4 min | LUST VS LOVE 2,1 M | série en 6 parties en 9 jours quand une vidéo décolle, liens vers les parties précédentes |
| **Last Soul** | 12 k | court animé sur les habitudes | 3–5 min | 1 MINUTE 794 k | logline de 3 phrases, 5 chapitres, un chiffre dans la miniature |
| **Chris Gu** | 3,7 k | court animé en huis clos | 4:40 | Sugar or Salt 613 k | question au spectateur en fin de description, série « One Room » |

### Les normes de la chaîne (non négociables sans demande explicite de l'utilisateur)

YouTube associe une chaîne à un groupe de spectateurs à partir de ce qui se répète : format, durée, miniature. Chaque vidéo qui s'écarte brouille ce signal pour toutes les autres. Ces normes s'appliquent donc à **chaque** vidéo, et le Publication checker les vérifie toutes.

1. **Un seul format : le paradoxe du corps humain expliqué par l'évolution** (« Why Evolution [verbe] Your [trait] »). Une question « What if » n'est acceptée que si elle porte sur le corps ou l'évolution humaine (« Can 2 People Really Restart Humanity? »). Les histoires de survie à la 2ᵉ personne, jour par jour (« You're Trapped Alone in… »), sont le format de la chaîne Ifverse Tales (skill `what-if-story-video`) : jamais sur The Hidden Bargain. Si l'utilisateur en demande une pour cette chaîne, le dire et proposer l'autre chaîne.
2. **4 à 7 minutes, 5 par défaut.** Aucune vidéo de référence ne dépasse 8 min 14 ; sur la chaîne, 8 à 16 min = 4 à 37 vues. Le format long Apefully (20 min) n'existe plus pour cette chaîne.
3. **Un seul univers visuel, une seule miniature.** Intérieur en `thin-line` (papier crème, trait fin, pastels, personnage à tête ronde blanche, étiquettes manuscrites), **miniature toujours en `caveman-duo`** (le duo homme-femme des cavernes, nuit, feu de camp), avec le bandeau bleu nuit et le texte jaune de `scripts/thumb.py`. Jamais de miniature egg-headphones, thin-line ou autre. Le style n'est pas une question du brief : `brief.json` porte `style: thin-line` et `thumbnail_style: caveman-duo`.
4. **Texte de miniature : 2 à 4 mots, en anglais grammatical**, un chiffre ou une question. Trois formes correctes : la vraie question (« WHY DO WE SNORE? », « WHY DO YOU BLUSH? »), le titre sans point d'interrogation (« WHY WE SNORE »), ou « WHY + nom pluriel » (« WHY GOOSEBUMPS? »). Fautes interdites : « WHY + verbe en -ing » (« WHY SNORING? »), « WHY + nom singulier sans article » (« WHY APPENDIX? »), « WHY WE/YOU + verbe » suivi d'un point d'interrogation (« WHY YOU BLUSH? »). Jamais de nombre au format durée (« 3:47 »), qui se confond avec le minuteur de YouTube ; le chiffre affiché est vrai. `thumb.py` refuse celles qu'un code sait repérer (-ing, « WHY WE/YOU + verbe ? », format durée, nombre de mots), et tout texte anglais visible passe par l'agent **English copy editor** (section 3.7).
5. **Titre ≤ 60 caractères, compté par code** (`len(title)`), gabarit « Why Evolution [verbe] Your [trait] (négation) » ou une question. Au-delà, il est coupé sur mobile.
6. **Hook : le mot du titre (snore, blush, appendix) est dit dans les deux premières phrases, et la question du titre est posée avant 0:30.** La rétention à 30 s est le premier signal testé.
7. **Publication entre 12 h et 14 h heure de l'Est (ET), de préférence du jeudi au samedi, programmée dans Studio** (« Planifier ») et jamais après 16 h ET : publiée le soir, la vidéo est encore en test quand le pic américain (18 h–23 h ET) est passé. Convertir l'heure par code dans le fuseau de l'utilisateur (`zoneinfo`, `America/New_York` → `Europe/Paris` ou autre) : l'écart change deux fois par an et diffère selon les pays. **Pour The Hidden Bargain, l'heure retenue par l'utilisateur est 18 h heure du Maroc, toute l'année** : selon la saison américaine et l'heure marocaine (UTC+1, ou UTC+0 pendant le ramadan), elle tombe toujours entre 12 h et 14 h ET, donc pas de conversion à refaire.
8. **Un Short par vidéo longue** (étape 10 du workflow), relié à la vidéo longue par « Vidéo associée ».
9. **Références américaines** : orthographe et vocabulaire US, unités US (miles, feet, pounds, °F), et dans le temps 2 un chiffre à l'échelle des États-Unis quand il existe (« about 90 million Americans snore »), vérifié par le Fact-checker.
10. **Réglages Studio identiques partout** : « Non, pas conçue pour les enfants » (sinon commentaires, écran de fin et une grande partie des recommandations sont coupés), commentaires activés, catégorie Éducation, langue English (United States), playlist « Why Evolution Made You… », écran de fin vers la vidéo suivante.
11. **Chapitres de 30 à 60 secondes**, nommés comme des temps forts, le premier à 00:00.
12. **Cadence** : une vidéo tous les deux jours en régime normal (c'est ce que la production à 5 images Flow par minute permet) ; quotidienne pendant les deux premières semaines d'une vague de format ; quand une vidéo décolle, une suite (« part 2 », même sujet, autre angle) sous 24 à 48 h. La règle la plus exigeante que la production permet prime.

## La formule

```
UN PARADOXE QUE LE SPECTATEUR PORTE SUR LUI (calvitie, yeux bleus, appendice, chair de poule)
+ OUVERTURE : UNE SCÈNE PHYSIQUE DU QUOTIDIEN À LA 2ᵉ PERSONNE (lieu, heure, geste)
+ LA FAUSSE CROYANCE, PUIS LA PROMESSE D'UN TWIST POUR LA FIN
+ 7 À 10 CHAPITRES DE 30 À 60 S : UN CONCEPT NOMMÉ = UN SCIENTIFIQUE + UNE ANNÉE + UN CHIFFRE + UNE ANALOGIE
+ LE RETOURNEMENT : « CE N'ÉTAIT PAS UN DÉFAUT, C'ÉTAIT UN MARCHÉ » (trade-off)
+ RETOUR À LA SCÈNE D'OUVERTURE, SENS INVERSÉ, PUIS UNE QUESTION AUX COMMENTAIRES
```

Pourquoi ça marche : le titre promet que la réponse connue est fausse ; la scène d'ouverture fait du spectateur le sujet ; les noms, dates et chiffres donnent la crédibilité qui compense le titre racoleur ; le retournement donne une émotion (« tu n'es pas cassé ») ; la question finale remplit les commentaires.

## Workflow
1. **Brief** (`references/brief.md`), deux tours au plus. Tour 1 : si le sujet manque, une seule salve (sujet, durée défaut **5 min**, livrable défaut production complète) ; si le sujet est donné, **pas de question**, une ligne de confirmation (sujet, 5 min, production complète, intérieur `thin-line`, miniature `caveman-duo`, voix edge-tts en-US-GuyNeural -5 % ou Gemini TTS si une clé est fournie) que l'utilisateur corrige s'il veut. Tour 2 : l'agent **Story architect** propose 3 angles, l'utilisateur en choisit un. Écrire `brief.json` avec `validated_by_user: true`.
2. **Faits** : 3 à 5 études nommées avec année, institution et un chiffre ; recherche web, jamais d'invention.
3. **Script** (`references/script-template.md`, section 2 ci-dessous) : une phrase par ligne, chaque ligne = un plan. Puis **Fact-checker** et **Script critic** en parallèle, corrections appliquées (ne pas révéler le mot du twist au temps 2 « fausse croyance », pas de citation sans source, phrases ≤ 25 mots, orthographe américaine).
4. **Shot list** : `scripts/make_shots.py` (copie de l'exemple appendice : un dictionnaire de specs par chapitre, zippé avec les lignes du script ; les fichiers Flow sont numérotés à la première apparition ; un plan `html` = insert dessiné par le skill **hand-drawn-visuals**, un plan `title` = carte-titre affichée pendant la première phrase du chapitre). Puis `python scripts/prompts.py shots.json` (prompts Flow + lint, budget 5 images Flow par minute) et les agents **Visual director** + **Prompt auditor** en parallèle ; appliquer leurs tableaux.
5. **Voix d'abord** : `python scripts/tts.py shots.json` → `voice.wav` + `timing.json` ; recopier les temps de début dans `shots.json` (`start`), c'est ce qui donne le vrai budget Flow et les chapitres.
6. **Images** : inserts par `node render.mjs shots.json flow/<video>/html --shots` (hand-drawn-visuals) ; scènes par Flow (`references/flow-automation.md`) : `browser.mjs` avec `FLOW_PROFILE`, nouveau projet depuis flow.google.com (il s'ouvre déjà en Image · 16:9 · x1), **test sur 3 prompts**, puis `PACE=25000 node batch.mjs` (mesuré le 28 octobre 2026 : 44 images, 0 refus, 50 s par image). Convertir, planche contact, agent **Image QC**, régénérer les rejets.
7. **Montage** : `python scripts/build_slideshow.py shots.json voice.wav timing.json out.mp4 --flow flow/<video>`, planche contact de la vidéo.
8. **Miniature** : une scène Flow avec le gabarit `thumbnail` de **`caveman-duo`** (`scripts/styles.json`), quel que soit le style intérieur, puis `python scripts/thumb.py scene.png thumbnail.jpg "WHY DO WE SNORE?"` (texte jaune Impact sur bandeau bleu nuit, jamais par le générateur ; le texte a d'abord été validé par l'English copy editor, et le script refuse plus de 4 mots, les nombres au format durée, « WHY + -ing » et « WHY WE/YOU + verbe ? »).
9. **Publication** (`references/publication-seo.md` §0) : chapitres aux temps réels de la voix, catégorie Éducation, sources listées, contenu synthétique = oui, date et heure de programmation en ET et dans le fuseau de l'utilisateur. Agent **Publication checker**, puis contrôle qualité (section 6).
10. **Short d'appel** : les temps 1 et 2 de la vidéo (ouverture + fausse croyance + promesse, 35 à 55 s), qui finissent sur la boucle ouverte, recadrés en 9:16 sur fond flou. `<fin>` = temps de début de la première phrase du temps 3 dans `timing.json` :
   ```
   FF=$(python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
   "$FF" -y -i out.mp4 -t <fin> -vf "split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2" -c:a aac short.mp4
   ```
   Titre du Short = la question du titre (≤ 60 caractères) + `#shorts` ; « Vidéo associée » = la vidéo longue ; publié le lendemain dans la même plage de 12 h à 14 h ET.

## Agents de production
Lancés avec l'outil Agent, en parallèle quand ils sont indépendants, chacun avec un brief complet (`references/agents.md`) : **Story architect** au brief ; **Fact-checker** + **Script critic** après le brouillon ; **Visual director** + **Prompt auditor** après la shot list ; **Image QC** (vision) après chaque lot Flow ; **English copy editor** sur tous les textes visibles avant la miniature ; **Publication checker** avant livraison. L'orchestrateur applique leurs tableaux et relance ce qui doit l'être. Pour un pilote de 3 minutes ou moins, Fact-checker, Prompt auditor et Image QC suffisent.

## 1. Le test du miroir (choix du sujet)

Un sujet marche quand le spectateur peut **se regarder dans un miroir et se reconnaître** : calvitie, yeux bleus, appendice, chair de poule, vieillissement. Sur 29 vidéos Apefully, ces sujets font 146 000 vues médianes ; les sujets médicaux sans auto-identification et les émotions abstraites font 7 000 à 14 000. Banque de sujets et test en trois questions : `references/topic-bank.md`.

Les chaînes de référence ajoutent une deuxième famille qui marche : la **question « What if » universelle** (« Can 2 People Really Restart Humanity? », 2,6 M) : même mécanique (scène, chiffres, sources), le paradoxe est remplacé par une hypothèse que tout le monde s'est déjà posée. Sur The Hidden Bargain, elle doit porter sur le corps ou l'évolution humaine (norme 1 de la section 0).

## 2. Structure calibrée

Cible par défaut **5 min = 750 à 900 mots** à 150–175 mots/min (edge-tts GuyNeural -5 % : 150 mots/min avec les pauses de 0,35 s entre phrases). Un épisode peut aller jusqu'à 7 min (1 100 mots), jamais au-delà (norme 2).

| # | Temps | Part | Mots (5 min) | Contenu |
|---|---|---|---|---|
| 1 | **Scène d'ouverture** | 0–8 % | 60–80 | 2ᵉ personne, un geste, un lieu, une heure, des sensations. Jamais d'abstraction en premier. |
| 2 | **Fausse croyance + promesse** | 8–16 % | 60–80 | « Every biology poster showed you… » ; « it is not a flaw, it is a… » (sans révéler le mot du twist) ; **la promesse** : « near the end, you will see why… » |
| 3 | **Chapitres 1 à 3 : le contexte ancestral** | 16–40 % | 180–220 | Le monde d'avant, le mécanisme, le premier scientifique, le premier chiffre |
| 4 | **Chapitres 4 à 5 : les preuves** | 40–60 % | 150–180 | 2 études avec nom + institution + année + échantillon + résultat chiffré |
| 5 | **CTA abonnement intégré** | ≈ 60 % | 25–35 | Une phrase qui joue avec le sujet, puis relance : « because we are about to uncover… » |
| 6 | **Chapitres 6 à 7 : le twist promis** | 60–85 % | 150–180 | La découverte récente, le mécanisme caché, le paradoxe résolu |
| 7 | **Retournement** | 85–93 % | 60–80 | « You were never broken » ; le défaut est un marché ; lever la culpabilité |
| 8 | **Retour à la scène + question** | 93–100 % | 50–70 | Même lieu, même geste qu'à l'ouverture, sens inversé ; une question précise aux commentaires |

Chapitres YouTube : **7 à 10, de 30 à 60 secondes** (5 min = 7 chapitres : les 8 temps du tableau moins le CTA, l'ouverture étant le chapitre 1 « The Riddle of… » ; 7 min = 10 chapitres en coupant les temps 3, 4 et 6 en deux). Noms = des temps forts : « The Riddle of… », « What Duke Revealed in 2007 », « The Final Verdict », « Tomorrow Morning ».

## 3. Règles d'écriture

### 3.1 Voix
- 2ᵉ personne dans l'ouverture, le retournement et la fin ; 3ᵉ personne dans les chapitres scientifiques. Cible : **2 « you/your » pour 100 mots**.
- Présent, phrases de 12 à 22 mots, **une phrase par ligne, une image mentale par phrase** (chaque ligne devient une image).
- Ton : documentaire chaleureux, jamais moqueur. Le titre est racoleur, le texte ne l'est pas.

### 3.2 Densité de faits
- **25 à 50 chiffres** sur 5 min (années, pourcentages, échantillons, durées) ; chaque chiffre dit est vu à l'écran (carte, comparaison, barre).
- Chaque chapitre : au moins un **scientifique nommé + institution + année**, et un chiffre précis. Varier l'attaque (« In 2007, surgeon X… » puis « Anatomist Y went through 533 species in 2017 »).
- Chaque concept abstrait reçoit **une analogie du quotidien** en une phrase (bunker, lance à incendie, gardien de frontière, banque de graines), et l'analogie a sa propre image.

### 3.3 Les mots-clés du format
- Le pivot s'appelle toujours **trade-off / bargain / contract**.
- L'évolution est un personnage qui décide : *made, gave, let, forced, refused, insisted, invented, traded away*.
- Formules à placer : « It was never a glitch. » « Here is the strange reality… » « That raises a bigger riddle. » Une seule fois chacune.

### 3.4 Boucles ouvertes
- Une promesse explicite dans le temps 2, tenue dans le temps 6 ; le mot du twist (« safe house ») n'apparaît qu'au temps 6.
- Une relance « and that raises a bigger riddle » entre deux chapitres.

### 3.5 Écrire pour une voix IA
- Nombres en lettres quand la voix doit les dire ; pas de symboles, d'abréviations ni de parenthèses ; orthographe américaine pour une voix en-US.
- Une citation n'est reprise que si le Fact-checker la retrouve mot pour mot ; sinon paraphrase sans guillemets.

### 3.6 Écrire pour un spectateur américain
- Unités US (miles, feet, pounds, °F) ; lieux, objets et habitudes familiers aux Américains dans la scène d'ouverture (kitchen counter, high school biology class, Thanksgiving dinner) quand le sujet s'y prête.
- Dans le temps 2, un chiffre à l'échelle des États-Unis quand une source fiable le donne (« about 90 million Americans snore »), sinon un chiffre mondial.

### 3.7 Relecture de l'anglais (tout texte visible ou lu)
Un Américain repère en une seconde une tournure fautive, et une miniature fautive fait passer la chaîne pour amateur avant même le clic. Exemple réel : « WHY SNORING? » (faux), puis la correction proposée « WHY WE SNORE? » (encore fausse avec le point d'interrogation) ; les bonnes formes sont « WHY DO WE SNORE? » ou « WHY WE SNORE ». Ne jamais se fier à sa propre intuition sur une formule courte : la faire relire.
- **Quoi** : titre et ses 2 alternatives, texte de miniature, noms de chapitres, cartes-titres et légendes des inserts, description, commentaire épinglé, titre du Short.
- **Qui** : l'agent **English copy editor** (`references/agents.md`), lancé avant `thumb.py` et avant le Publication checker, en parallèle d'autres agents si possible. Il rend un tableau texte | problème | correction ; appliquer toutes les corrections, puis relancer `thumb.py` si le texte de miniature a changé.
- Le script lui-même est relu par le Script critic (point 7 de son brief : grammaire et idiomes américains).

## 4. Le diaporama (détail dans `references/visual-pipeline.md` et `references/scene-catalogue.md`)

- **Une image par phrase**, tenue 3 à 6 s, coupes franches, zéro animation. Le rythme vient des coupes et de la voix.
- **Budget Flow : 5 images par minute au plus** (une scène tenue sur 2 à 3 phrases avec le même `file`) ; tout ce qui porte un chiffre, un titre, un symbole ou une comparaison est un insert `html` dessiné par code (hand-drawn-visuals), exact et gratuit.
- Rythme mesuré sur 30 vidéos : une scène, un insert, une scène ; jamais plus de 2 inserts de même famille de suite ni 3 inserts sans scène ; un visuel de données au moins toutes les 14 images, jamais deux de suite ; le motif de l'ouverture revient au milieu et à la fin ; au moins un plan `pov` et un `overhead`.
- Style unique `thin-line` à l'intérieur de la vidéo (`caveman-duo` réservé à la miniature, norme 3) : le texte de scène décrit **son propre lieu** (salle de bain, savane, labo) ; la phrase de décor du brief reste neutre. Mots interdits dans une scène Flow (bulles, texte) : `talking, sign, label, poster, map, screen showing, reads, written, number, letters`, et les objets qui portent du texte (livre ouvert, pile de papiers, flacon étiqueté, moniteur, enseigne) sont décrits « plain, blank, unmarked ».

## 5. Faire grandir la chaîne : algorithme et audience américaine (ex-skill youtube-boost-usa, fusionné)

Principe : YouTube ne pousse pas des chaînes, il teste chaque vidéo sur un petit groupe et élargit si les signaux tiennent (satisfaction, CTR sur non-abonnés, rétention des 30 premières secondes, contribution à la session). Une audience américaine vient du **contenu** (anglais US, voix US, références, sujets, heure), jamais d'un réglage de pays, d'un VPN ou de vues achetées. Détail des signaux et repères chiffrés : `references/algorithme.md` ; étude du cluster « Animated Short Films » (octobre 2026) : `references/niche-animated-short-films.md` ; ciblage : `references/ciblage-usa.md` ; trafic externe : `references/pinterest.md`.

**Quand l'utilisateur demande un audit ou « pourquoi ça ne décolle pas »** :
1. Mesurer avant de juger : `python scripts/yt/yt_scan2.py https://www.youtube.com/@handle/videos` (titres, vues, dates, durées, sans yt-dlp) et `python scripts/yt/yt_video.py <id>` (description, chapitres) ; `scripts/yt/extract_channel.py` si yt-dlp est installé (likes, commentaires). Télécharger les miniatures (`https://i.ytimg.com/vi/<ID>/maxresdefault.jpg`) et les regarder sur une planche contact. Demander en une fois ce qui manque : chiffres Studio des 28 derniers jours (impressions, CTR, durée moyenne, sources de trafic, pays, heures d'audience).
2. Un seul goulot à la fois : peu d'impressions → sujets et packaging ; CTR bas → titre et miniature ; chute avant 30 s → hook ; rétention plate → rythme et durée ; vidéos isolées → séries, playlists, écrans de fin ; audience hors USA → signaux du contenu.
3. Cohérence de la chaîne d'abord : un format, un style, une durée, un gabarit de miniature. C'est la raison des normes de la section 0.
4. Ciblage US dans chaque vidéo : orthographe et vocabulaire américains, voix en-US, langue de la vidéo et des métadonnées réglée sur English (United States), unités US quand le sujet s'y prête, publication entre 12 h et 14 h heure de l'Est convertie par code dans le fuseau de l'utilisateur (norme 7), test A/B de miniatures dans Studio quand il est disponible.
5. Vague de format : quand plusieurs chaînes neuves d'une niche font des centaines de milliers de vues en quelques semaines, entrer vite avec le packaging exact du cluster, publier quotidiennement deux semaines, enchaîner les suites à 24 h, se différencier par le thème une fois la traction venue.
6. Livrer un fichier `audit.md` dans le dossier de travail (et le résumé en chat), dans ce format : Diagnostic (goulot + chiffres) ; Ce que l'algorithme attend de cette chaîne (3 à 5 points) ; Ciblage USA ; Optimisations vidéo (3 titres, 2 miniatures, hook réécrit) ; Plan 30 jours (5 actions par semaine au plus, un indicateur par action). Ne jamais promettre de chiffres ni de délai.

Jamais recommandé : vues, abonnés ou likes achetés ; changer le pays de la chaîne ; VPN ou IP américaine ; bourrage de tags ; clickbait non tenu ; réupload de contenus d'autrui ; vidéos générées en masse quasi identiques (politique « contenu inauthentique » de juillet 2025).

## 6. Contrôle qualité avant livraison
- [ ] `brief.json` validé (angle choisi parmi 3, durée, livrable), `style: thin-line`, `thumbnail_style: caveman-duo`
- [ ] Format de la chaîne (norme 1) : paradoxe du corps ou « What if » sur l'évolution humaine, jamais une histoire de survie jour par jour
- [ ] Sujet validé par le test du miroir ; titre ≤ 60 caractères compté par code, question ou gabarit « Why Evolution … (…) »
- [ ] Ouverture = scène physique à la 2ᵉ personne ; mot du titre dit dans les 2 premières phrases, question du titre posée avant 0:30 ; promesse au temps 2 tenue au temps 6 sans fuite du mot du twist
- [ ] Durée finale de la voix entre 4 et 7 minutes (`timing.json`)
- [ ] 3 à 5 scientifiques nommés avec institution, année, chiffre ; tous `[vérifié]` par le Fact-checker ; aucune citation non sourcée
- [ ] 750 à 1 100 mots ; 2 « you » pour 100 mots ; phrases ≤ 25 mots ; une phrase par ligne ; orthographe américaine
- [ ] CTA intégré vers 60 %, lié au sujet, suivi d'une relance
- [ ] Retournement « trade-off », retour à la scène d'ouverture, question aux commentaires en dernière phrase
- [ ] Shot list : lint `prompts.py` sans erreur, Visual director et Prompt auditor appliqués, budget Flow ≤ 5/min sur les vrais temps de la voix
- [ ] Inserts html : chiffres identiques à la voix, aucun texte qui déborde (planche contact regardée)
- [ ] Images Flow : planche contact passée par Image QC (pas de bulle, pas de texte, même personnage thin-line partout), rejets régénérés
- [ ] English copy editor passé sur tous les textes visibles (titre, miniature, chapitres, cartes, description, Short) et corrections appliquées
- [ ] Miniature 1280 × 720 < 2 Mo : duo `caveman-duo`, 2 à 4 mots en anglais grammatical (norme 4) avec un chiffre ou une question, pas de nombre au format durée, texte par `thumb.py`
- [ ] Short 9:16 de 35 à 55 s produit, titre + `#shorts`, vidéo associée = la vidéo longue
- [ ] Fiche de publication complète (§0 de `publication-seo.md`) : chapitres aux temps réels, catégorie Éducation, sources, tags ≤ 500 caractères, contenu synthétique = oui, pas conçue pour les enfants, commentaires activés, playlist, commentaire à épingler, carte « NEXT », programmation entre 12 h et 14 h ET avec l'heure locale de l'utilisateur
