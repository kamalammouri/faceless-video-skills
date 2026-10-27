---
name: why-explainer-video
description: Écrit et prépare des vidéos YouTube explicatives de 20 minutes au format « Why Evolution Made… » (style Apefully) : un paradoxe sur le corps ou le comportement humain, ouvert par une scène du quotidien à la 2ᵉ personne, résolu par des chapitres « scientifique + année + chiffre + analogie », retourné en « ce n'était pas un défaut mais un marché », fermé par un retour à la scène et une question aux commentaires. Produit le script complet (3 300–3 600 mots), la liste d'images une par phrase pour un diaporama 2D sans animation (prompts avec préfixe de style, familles de plans, graphiques par code), le titre, la miniature « WHY … ? », les chapitres, la description, les tags et la catégorie, et génère les images automatiquement dans Google Flow (Chrome piloté par Playwright, scripts inclus) puis la miniature par code. Use whenever the user wants a faceless educational video, a science or evolution explainer, a "why do humans…", "why did evolution…", "the real reason…" video, a 2D stickman or whiteboard-style explainer, or wants to copy a channel like Apefully, Kurzgesagt-lite or Stickman explainers, even without saying "skill". Triggers FR/EN : vidéo explicative, pourquoi l'évolution, script éducatif 20 minutes, diaporama image par phrase, miniature WHY, chaîne faceless science.
---

# Why Explainer Video (format « Why Evolution Made… »)

Reproduit le format mesuré sur la chaîne Apefully (19 k abonnés, 2,8 M de vues en 5 semaines, une vidéo par jour) : un paradoxe humain expliqué en 20 minutes par un diaporama d'images fixes. Le skill contient la logique, pas un sujet : chaque demande = un nouveau sujet.

## Langue et sortie
- Répondre dans la langue de l'utilisateur. **Script en anglais par défaut** (le format vit sur l'audience anglophone et le doublage automatique fait le reste).
- Livrer un seul fichier `.md` dans le dossier courant : script, puis liste d'images, puis publication.

## La formule

```
UN PARADOXE QUE LE SPECTATEUR PORTE SUR LUI (calvitie, yeux bleus, nausées, vieillissement)
+ OUVERTURE : UNE SCÈNE PHYSIQUE DU QUOTIDIEN À LA 2ᵉ PERSONNE
+ LA FAUSSE CROYANCE, PUIS LA PROMESSE D'UN TWIST POUR LA FIN
+ 8 À 11 CHAPITRES : UN CONCEPT NOMMÉ = UN SCIENTIFIQUE + UNE ANNÉE + UN CHIFFRE + UNE ANALOGIE
+ LE RETOURNEMENT : « CE N'ÉTAIT PAS UN DÉFAUT, C'ÉTAIT UN MARCHÉ » (trade-off)
+ RETOUR À LA SCÈNE D'OUVERTURE, SENS INVERSÉ, PUIS UNE QUESTION AUX COMMENTAIRES
```

Pourquoi ça marche : le titre promet que la réponse connue est fausse ; la scène d'ouverture fait du spectateur le sujet ; les noms, dates et chiffres donnent la crédibilité qui compense le titre racoleur ; le retournement donne une émotion (« tu n'es pas cassé ») ; la question finale remplit les commentaires.

## Workflow
1. **Choisir le sujet** avec le test du miroir (section 1). Si l'utilisateur n'en donne pas, en proposer 3 et prendre le premier. `references/topic-bank.md` pour les idées et les sujets à éviter.
2. **Rassembler les faits** : 3 à 5 études ou scientifiques nommés, avec année, institution et un chiffre chacun. Chercher sur le web ; ne jamais inventer un nom, une année ou un chiffre. Marquer `[vérifié]` dans le brouillon.
3. **Écrire le script** avec `references/script-template.md` (mécanique de chaque temps, budgets de mots) et les règles de la section 3.
4. **Construire la liste d'images** avec `references/visual-pipeline.md` : une image par phrase, famille de plan, prompt complet ; cartes de chiffres par `scripts/cards.py` (icône obligatoire, mises en page en rotation) ; puis audit par les agents Visual director et Prompt auditor.
5. **Générer les images** : scènes avec personnage par Google Flow, en automatique avec `references/flow-automation.md` (scripts dans `scripts/flow/`) ; icônes, schémas, graphiques et cartes par code. Puis assembler (voix + images) et vérifier sur une planche contact.
6. **Publication** : la fiche complète de `references/publication-seo.md` §0, avec la **catégorie Éducation** toujours écrite, la miniature texte par code, les chapitres calés sur la voix.
7. **Contrôle qualité** (section 5) puis livraison.


## Agents de production
Le rédacteur seul se répète ; la production passe par des agents spécialisés lancés en parallèle avec l'outil Agent, chacun avec un brief complet (`references/agents.md`) : **Fact-checker** et **Script critic** après le brouillon ; **Visual director** et **Prompt auditor** après la shot list ; **Image QC** (vision) après chaque lot d'images ; **Publication checker** avant livraison. L'orchestrateur applique leurs tableaux de corrections et relance ce qui doit l'être. Ne jamais sauter Visual director et Image QC : ce sont eux qui empêchent les cartes nues, les bulles vides et les doublons.

## 1. Le test du miroir (choix du sujet)

Un sujet marche quand le spectateur peut **se regarder dans un miroir et se reconnaître** : calvitie, yeux bleus, barbe, courbes, taille, vieillissement, mort. Sur 29 vidéos de la chaîne de référence, ces sujets font 146 000 vues médianes ; les sujets médicaux sans auto-identification (nausées de grossesse, perte de cheveux féminine, accouchement) et les émotions abstraites (chagrin, amour) font 7 000 à 14 000.

Avant d'écrire, vérifier : (a) une personne sur trois peut dire « c'est moi » ; (b) il existe une réponse évidente que la vidéo va contredire ; (c) il existe au moins 3 études nommables.

## 2. Structure calibrée (cible 20 à 24 min, 3 300 à 3 600 mots à 155–170 mots/min)

| # | Temps | Part | Mots | Contenu |
|---|---|---|---|---|
| 1 | **Scène d'ouverture** | 0–4 % | 120–170 | 2ᵉ personne, un geste, un lieu, une heure, des sensations. Jamais d'abstraction en premier. |
| 2 | **Fausse croyance + promesse** | 4–8 % | 120–160 | « Society tells you… » / « the version you learned in ninth grade… » ; puis « it is not a flaw, it is a… » ; puis **la promesse** : « near the end, we will see why… » |
| 3 | **Chapitres 1 à 4 : le contexte ancestral** | 8–35 % | 900–1 000 | Le monde d'avant (savane, 200 000 ans), le mécanisme, le premier scientifique, le premier chiffre |
| 4 | **Chapitres 5 à 7 : les preuves** | 35–60 % | 800–900 | 2 ou 3 études avec nom + institution + année + échantillon + résultat chiffré |
| 5 | **CTA abonnement intégré** | ≈ 60 % | 40–60 | Une phrase qui joue avec le sujet (« clicking subscribe contains zero bitter alkaloids »), puis relance : « because we are about to uncover… » |
| 6 | **Chapitres 8 à 10 : le twist promis** | 60–88 % | 700–800 | La découverte récente, le mécanisme caché, le paradoxe résolu |
| 7 | **Retournement** | 88–95 % | 200–250 | « You were never broken » ; le défaut est un marché ; lever la culpabilité |
| 8 | **Retour à la scène + question** | 95–100 % | 120–160 | Même lieu, même geste qu'à l'ouverture, sens inversé ; une question précise aux commentaires |

Chapitres YouTube : 8 à 11, de 2 à 3 minutes, nommés « The [Nom] of [Chose] » (The Riddle of…, The Hidden Cost of…, The … Mechanism, The Final Verdict).

## 3. Règles d'écriture

### 3.1 Voix
- 2ᵉ personne dans l'ouverture, le retournement et la fin ; 3ᵉ personne dans les chapitres scientifiques. Cible : **2 « you/your » pour 100 mots** (la vidéo à 542 k vues en a 2,0 ; celle à 10 k en a 1,0).
- Présent, phrases de 15 à 25 mots, une image mentale par phrase (chaque phrase devient une image à l'écran).
- Ton : documentaire chaleureux, jamais moqueur. Le titre est racoleur, le texte ne l'est pas.

### 3.2 Densité de faits
- **40 à 90 chiffres** par script (années, pourcentages, échantillons, durées).
- Chaque chapitre : au moins un **scientifique nommé + institution + année**, et un chiffre précis (« tracked nearly 800 pregnancies », « 27 traditional societies », « doubles every 8 years »).
- Chaque concept abstrait reçoit **une analogie du quotidien** en une phrase (bottes usées, siphon, ligne de côte, gardien de frontière, tour radio).

### 3.3 Les mots-clés du format
- Le pivot s'appelle toujours **trade-off / bargain / contract**.
- Les verbes de l'évolution : *made, gave, let, forced, refused, insisted, invented, traded away*. L'évolution est un personnage qui décide.
- Formules à placer : « It was never a glitch. » « You are looking at… » « Here is the strange reality… » « Pause and let that sink in. »

### 3.4 Boucles ouvertes
- Une promesse explicite dans le temps 2, tenue dans le temps 6 (« the ultimate twist we promised at the start »).
- Deux relances « and that raises a bigger riddle » entre les chapitres.

### 3.5 Écrire pour une voix IA
- Écrire les nombres en lettres quand la voix doit les dire (« number one », pas « #1 » : la référence a prononcé « hashtag one »).
- Pas de symboles, d'abréviations ni de parenthèses dans le script ; les noms propres difficiles reçoivent une graphie phonétique en commentaire.

## 4. Le diaporama (résumé ; détail dans `references/visual-pipeline.md`)

Mesuré sur deux vidéos complètes : 297 et 323 images fixes, **4,1 à 4,8 s par image, une image par phrase**, coupes franches, zéro transition, zéro mouvement de caméra, 94 % du temps strictement fixe. Le rythme vient du montage et de la voix, pas de l'animation.

Cinq familles de plans, à mélanger : icône + 1 à 3 mots (35 %), scène avec personnage (25 %), schéma ou comparaison (22 %), graphique de données (10 %), carte-titre (5 %). Style unique : fond crème, trait fin noir, pastels, lettrage manuscrit en capitales, personnages à tête ronde blanche. Un motif visuel récurrent (la scène d'ouverture) revient au milieu et à la fin.

## 5. Contrôle qualité avant livraison
- [ ] Sujet validé par le test du miroir ; titre au gabarit « Why [force] [verbe] [trait] ([négation]) »
- [ ] Ouverture = scène physique à la 2ᵉ personne, en moins de 170 mots
- [ ] Promesse d'un twist dans le temps 2, tenue dans le temps 6
- [ ] 3 à 5 scientifiques nommés avec institution, année, chiffre ; tous vérifiés
- [ ] 40 à 90 chiffres ; une analogie par concept ; 2 « you » pour 100 mots
- [ ] CTA intégré vers 60 %, lié au sujet, suivi d'une relance
- [ ] Retournement « trade-off » puis retour à la scène d'ouverture et question aux commentaires
- [ ] 3 300 à 3 600 mots ; 8 à 11 chapitres nommés « The … of … »
- [ ] Liste d'images : une par phrase, famille indiquée, prompt complet ; chiffres à l'écran identiques à la voix
- [ ] Aucun label d'image qui décrit l'image au lieu de nommer la chose (« LARGE CALM CLOCK FACE » est une erreur de la référence)
- [ ] Script sans symboles ni abréviations pour la voix IA
- [ ] Fiche de publication complète (§0 de `publication-seo.md`) : **catégorie Éducation écrite**, tags ≤ 500 caractères vérifiés, chapitres aux temps réels de la voix, contenu synthétique = oui, commentaire à épingler
- [ ] Images : planche contact passée par l'agent Image QC (aucune bulle de dialogue, aucun texte généré, même personnage partout), rejets régénérés ; aucune carte de chiffre sans icône ; jamais 3 images de même famille de suite ; miniature 1280 × 720 avec texte par code
