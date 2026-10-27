# Titre, miniature, description, série : la fiche de publication

## 0. Fiche de publication : toujours livrée, dans cet ordre

| Champ | Valeur |
|---|---|
| Titre | un seul titre retenu + 2 alternatives |
| Description | bloc complet au gabarit du §3 |
| **Catégorie** | **écrite explicitement** : « Film et animation » pour une chaîne de fiction, ou « Éducation » si la chaîne mélange explainers et fictions (une seule catégorie par chaîne) |
| Tags | 15 à 20, **500 caractères au total maximum**, vérifiés par code |
| Langue de la vidéo | anglais |
| Public | « Non, pas conçu pour les enfants » |
| Contenu modifié ou synthétique | **oui** (voix et images générées par IA) |
| Miniature | 1280 × 720, < 2 Mo, texte et badge par code |
| Écran de fin | 5 dernières secondes : bouton Abonnement + « vidéo suivante » = la partie suivante (ou la partie 1 pour un film) |
| Commentaire à épingler | la question du choix du héros, en une ligne |
| Playlist | la série (« What If You Had 500 IQ », 3 parties + film) |
| Série | numéro de partie, liens des autres parties mis à jour dans **chaque** description quand une partie sort |

## 1. Titre

Gabarit observé sur 12 titres sur 12 :

```
What If You [Had / Were / Could / Woke Up / Used] [chiffre + pouvoir] ?
```

- Toujours « What If You… ? » (« What If Your Reaction Time Was 10x Faster? », « What If You Had 500 IQ? », « What If You Woke Up in Kindergarten With All Your Memories? »).
- Un chiffre dès que possible : 10x, 500 IQ, 5x ; sinon une unité de temps (« One Second Felt Like Ten », « … Forever »).
- Les suites gardent le pouvoir dans le titre et ajoutent l'enjeu : « What If You Used 500 IQ to Disappear? », « … to Save Your Sister? ».
- Le film : « … (FULL MOVIE) ». Les titres font 6 à 9 mots (le film peut monter à 12).

## 2. Miniature (12 sur 12)

| Élément | Règle |
|---|---|
| Fond | bleu nuit ou violet sombre, lueur chaude derrière la tête |
| Personnage | le visage noir du héros en **gros plan à droite**, yeux blancs, un reflet en étoile, expression nette (sourire en coin ou choc) |
| Accessoire | un seul objet qui résume l'épisode : balle, jauge de QI, éclair, horloge 01:00, tours de la ville |
| Texte | **2 ou 3 mots** en capitales grasses, jaune (242,196,70) ou blanc avec contour noir, en haut à gauche : « TOO SLOW. », « TOO FAST. », « I KNEW. », « 500 IQ », « LOOP BROKE. », « TEST BROKE. » |
| Badge | rectangle rouge « PART 2 » / « FINAL PART » / « FULL MOVIE » dans un coin |
| Chiffre | parfois en rouge dans un cadre (« 09.11 », « 10/10 ») |

Produire l'image dans Flow avec le gabarit `thumbnail` du style, puis le texte et le badge par code (`thumb.py` : police Impact, contour noir 10 px, badge rouge 214,72,48).

## 3. Description (gabarit)

```
[Accroche de 2 lignes avec le chiffre et la limite]
What if your brain reacted 10 times faster than everyone else's? 0.025 seconds instead of 0.25. Flies are easy to catch,
bullets look slow, and every sport turns into a joke... until one split second asks you to make a choice nobody else can.

This is Part 1 of 3.
▶ PART 2: [titre] https://youtu.be/...      (ajouté quand elle sort)
▶ PART 3 (FINAL): [titre] https://youtu.be/...

[La question du choix] Which sport would YOU dominate with 10x reflexes? Tell us in the comments.

Chapters:
0:00 The fly and the coffee cup
1:11 Everyday life in slow motion
2:13 Sports genius: table tennis, baseball, boxing
3:28 The goalkeeper nobody can beat
4:45 The World Cup final
6:10 Three days later...

Science notes: an average human reacts to what they see in about 0.25 s; elite sprinters react in about 0.13 s;
World Athletics counts any start reaction under 0.100 s as a false start.

Subscribe to [chaîne] for more what-ifs. Every what if becomes a story.
#whatif #animation #stickman #[pouvoir]
```

- 6 à 8 chapitres aux **noms de scène** (« Mom », « The call », « The bullet »), jamais « Chapter 1 » ; horodatages pris sur la voix réelle (`timing.json`).
- Trois science notes vérifiées, les mêmes que le bloc « is any of this real? » du script.
- Hashtags : `#whatif #animation` + un hashtag du pouvoir (`#500iq`, `#superpower`, `#timeloop`).

## 4. Tags (≤ 500 caractères)

`what if you, what if, [pouvoir] story, superpower story, what if animation, stickman animation, second person story, sci-fi short story, what if you had [pouvoir], [chiffre] [pouvoir], animated story, what would you do, part 1 of 3, [nom du héros], [chaîne]`

## 5. Série et commentaires

- Publier la partie 2 trois à sept jours après la partie 1, la partie 3 deux à quatre jours plus tard, le film une semaine après.
- Mettre à jour la description et l'écran de fin de chaque partie précédente avec le lien de la nouvelle.
- Commentaire épinglé : la question du choix (« If you were the keeper: the ball or the boy? Be honest. ») ; répondre aux théories, elles nourrissent la partie suivante.
