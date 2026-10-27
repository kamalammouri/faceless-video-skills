# Titre, miniature, chapitres, description, tags, doublage

## 0. Fiche de publication : toujours livrée, dans cet ordre

Chaque livraison se termine par un bloc « Publication » prêt à coller dans YouTube Studio. Les oublis coûtent une relance : ne jamais omettre une ligne, même évidente.

| Champ | Valeur |
|---|---|
| Titre | un seul titre retenu + 2 alternatives |
| Description | bloc complet (hook, promesse, chapitres, suite, hashtags) |
| **Catégorie** | **Éducation** (Education), pour toutes les vidéos de la chaîne : la même catégorie partout aide YouTube à relier les vidéos entre elles et aux chaînes voisines |
| Tags | 15 à 20, **500 caractères au total maximum**, vérifier la longueur par code |
| Langue de la vidéo | anglais |
| Public | « Non, pas conçu pour les enfants » |
| Contenu modifié ou synthétique | **oui** (voix et images générées par IA) : YouTube l'exige pour une voix réaliste |
| Miniature | fichier 1280 × 720, < 2 Mo, texte ajouté par code |
| Écran de fin | 5 dernières secondes : bouton Abonnement + emplacement « vidéo suivante » |
| Commentaire épinglé | la question posée à la fin de la vidéo, reformulée en une ligne |
| Playlist | la série du format |

## 1. Titre

Gabarit observé sur 28 titres sur 29 :

```
Why Evolution [verbe fort] [trait humain visible] ([parenthèse qui nie la réponse évidente])
```

- Verbes : Made, Gave, Let, Forced, Insisted on, Refused to, Allowed, Took Away, Invented, Ruined.
- Variante : « The [Real / Creepy / Strange / Shocking / Brilliant] Reason Evolution … ».
- Parenthèses qui marchent : « It's Not What You Think », « It Was Never A Beauty Trend », « You Won't Believe This », « The Reason is Crazy », « Every Blue Eyed Person Shares One Ancestor », « Doctors Still Won't Admit This ».
- Le format se transpose à d'autres forces : « Why Your Brain… », « Why Your Body… », « Why History… ».
- Proposer 3 titres et classer par force de la négation.

## 2. Miniature

Gabarit unique sur les 29 miniatures de la référence :

| Élément | Règle |
|---|---|
| Texte | 2 à 4 mots, majuscules, jaune vif avec contour noir épais, en haut du cadre, terminé par `?` ou `?!` |
| Formule | « WHY … ? » (WHY BALD?!, WHY BLUE EYES?, WHY SO PALE?, WHY DO WE DIE?) |
| Personnages | un duo de mascottes récurrentes, expressives (choc, sueur, larmes), visage visible, style cartoon saturé, différent du style intérieur de la vidéo |
| Accessoire | un seul objet qui dit le sujet sans texte (banane, carte, bol, feu) |
| Décor | savane, coucher de soleil, nuit avec feu ; couleurs saturées |

Prompt de miniature :

```
Bold cartoon YouTube thumbnail, two expressive caveman mascots (man and woman in fur tunics,
messy brown hair, big eyes, stick limbs), [ÉMOTION], [ACCESSOIRE], [DÉCOR] at [MOMENT],
saturated colors, large empty area at the top for text, 16:9
```

Puis ajouter le texte « WHY … ? » en jaune (242,196,70) à contour noir par code (PIL, police Impact, contour 10 px, image 1280 × 720), jamais par le générateur d'images. Le personnage choisi au brief (gabarit `thumbnail` de son style dans `scripts/styles.json`) peut remplacer le duo de mascottes : il relie la miniature au contenu ; pour `stickman-meme`, composition coupée en deux, perdant à gauche, gagnant à droite. Laisser une moitié du cadre vide pour le texte.

## 3. Chapitres

8 à 11 chapitres pour 20 minutes (5 à 8 pour un pilote court), 2 à 3 minutes chacun, nommés sur le modèle « The [Nom] of [Chose] » :
The Riddle of…, The Hidden Cost of…, The … Dilemma, What the Data Revealed, The … Mechanism, The Survival Trigger, The Rise of…, The Final Verdict.

Règles YouTube, sinon les chapitres ne s'affichent pas : le premier commence à `00:00`, au moins 3 chapitres, chacun d'au moins 10 secondes, dans l'ordre croissant. Format `mm:ss` suffisant sous une heure.

**Les horodatages viennent du minutage réel de la voix**, jamais d'une estimation : quand le fichier `voice.json` (fin de chaque caractère) existe, prendre le temps de fin de la phrase qui précède le début du chapitre. Sans voix générée, écrire « à caler après la voix » plutôt qu'un chiffre inventé. Les chapitres servent de mini-hooks dans la barre de lecture.

## 4. Description

```
#[Hashtag1] #[Hashtag2] #[Hashtag3]

[1 phrase qui reprend la question du titre et promet la réponse cachée.]

[Paragraphe de 120 à 180 mots, dense en mots-clés : reprendre le titre, nommer 4 à 6 concepts
scientifiques du script (noms de théories, d'hormones, de chercheurs), 2 ou 3 chiffres, et le
retournement final. Terminer par : « Your [organe] is not broken, it is… »]

[Question finale du script, mot pour mot, suivie de « Share your answer in the comments. »]

Subscribe for more animated documentaries on human evolution, prehistoric life and the mysteries of the human body.

CHAPTERS:
00:00:00 - [Chapitre 1]
00:02:36 - [Chapitre 2]
…

#[Hashtag1] #[Hashtag2] #[Hashtag3]
```

Catégorie YouTube : **Education**. Cocher la mention « contenu modifié ou généré par IA ».

## 5. Tags (15 à 20, **500 caractères au total maximum**)

YouTube refuse la sauvegarde au-delà de 500 caractères, virgules comprises : compter avant de livrer (`len(", ".join(tags))`) et retirer les tags les plus longs, jamais les génériques de niche. Trois familles, dans cet ordre :
1. **Génériques de niche avec « documentary »** (5) : human evolution documentary, evolutionary biology documentary, anthropology documentary, science documentary, evolutionary psychology.
2. **Questions en longue traîne** (8) reprises du script : why do so many people need glasses, why is childbirth so painful, why do men go bald.
3. **Concepts nommés** (4 à 6) : obstetric dilemma, antagonistic pleiotropy, inverted retina explained, GDF-15 pregnancy.

## 6. Doublage automatique et titres traduits

Activer dans YouTube Studio le doublage automatique et la traduction des titres et descriptions. La référence est servie en arabe, français, hindi, japonais, portugais, espagnol et plus de 15 autres langues : un spectateur français voit « La vraie raison pour laquelle l'évolution veut votre mort » et entend une voix française. C'est gratuit et invisible dans les statistiques publiques, mais c'est une part réelle de l'audience.

## 7. Cadence et série
- Une vidéo par jour pendant 30 jours avant de juger : la référence a percé à la 6ᵉ vidéo, après la reprise quotidienne.
- Carte finale « NEXT : [titre suivant] » 5 secondes ; une chaîne associée en collaboration (fonction « collab » de YouTube) partage les vues entre deux chaînes.
