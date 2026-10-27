---
name: survival-story-video
description: Écrit et prépare des vidéos YouTube de survie / isolement racontées à la 2ᵉ personne ("you"), jour par jour, style documentaire sombre, avec faits réels vérifiés, crises techniques, mystère jamais expliqué et twist final (format "Bunker Survival 1 Year", 10–12 min). Produit le script complet calibré à la minute, le plan visuel (shot list, prompts IA, animation, étalonnage, audio), le titre, la description, la catégorie, la miniature par code, et génère les images automatiquement dans Google Flow (Chrome piloté par Playwright, scripts inclus) en mode diaporama. Use whenever the user wants a script, scenario, storytelling or faceless video about survival, bunker, shelter, isolation, apocalypse, nuclear winter, polar station, submarine, space station, lifeboat, lockdown, blackout, "365 days in", "one year alone", "what if you were trapped/alone", or wants to copy/adapt the style of a viral second-person survival video, even if they don't say "skill" or "template". Triggers FR/EN - script vidéo survie, histoire à la 2ème personne, scénario d'isolement, vidéo faceless, shot list, prompts vidéo IA, montage Premiere, titre et miniature YouTube pour ce format.
---

# Survival Story Video (2ᵉ personne)

Génère des vidéos longues (10–12 min) de survie/isolement à la 2ᵉ personne, calibrées sur le format qui marche (référence : "Bunker Survival 1 Year", 2 M de vues en un mois). Le skill contient la **logique** (structure, rythme, règles, faits), pas une histoire : chaque demande = un nouveau scénario.

## Langue et sortie
- Répondre dans la langue de l'utilisateur.
- **Script / voix off en anglais par défaut**, sauf demande contraire.
- Livrer un seul fichier `.md` dans le dossier de travail courant, puis le présenter.

## La formule

```
FICTION À LA 2ᵉ PERSONNE ("you"), JOUR PAR JOUR
+ FAITS RÉELS VÉRIFIÉS, CHIFFRÉS, INTÉGRÉS AU RÉCIT
+ 2 CRISES TECHNIQUES → CHAQUE CRISE ENSEIGNE UNE LEÇON RÉELLE
+ MYSTÈRE JAMAIS EXPLIQUÉ (boucles ouvertes)
+ DOUBLE TENSION : extérieure (menace inconnue) + intérieure (santé mentale)
+ FIN OUVERTE AVEC TWIST EN UNE PHRASE
```

Pourquoi ça marche : le spectateur **est** le personnage ; les chiffres donnent de la valeur et de la crédibilité ; les crises donnent une tension concrète ; le mystère retient jusqu'au bout ; le twist pousse au commentaire et appelle une suite.

## Workflow
1. **Cadrer** : si le thème est absent, poser UNE question courte (lieu ou thème). Sinon choisir soi-même les paramètres (section 1) et les annoncer en une ligne.
2. **Choisir les faits** : ouvrir `references/fact-bank.md` pour le décor choisi. Chercher sur le web tout chiffre absent ou douteux. Ne jamais inventer un chiffre présenté comme réel.
3. **Caler le rythme** : lire `references/reference-beat-sheet.md` (la feuille de rythme de la vidéo cible, minute par minute) et le tableau de la section 2. C'est la jauge : même densité de chiffres, mêmes jours-repères, même alternance scène/fait.
4. **Écrire le script** avec `references/script-template.md` (mécanique de phrase par scène) et les règles de la section 3.
5. **Construire le plan visuel** si l'utilisateur veut produire la vidéo : `references/style-et-production.md` (§8.9 pour le mode diaporama, qui est le mode par défaut de la chaîne).
6. **Générer les images** : un plan par moment (60 à 70 images pour 11 min) par Google Flow en automatique avec `references/flow-automation.md` (scripts dans `scripts/flow/`) ; cartes de chiffres et jours par code. Shot list en `shots.json` (format en tête de `scripts/prompts.py`), règles de rythme de `references/scene-catalogue.md` ; cartes par `scripts/cards.py`, graphiques et frises par `scripts/charts.py` ; `python scripts/prompts.py shots.json` produit les prompts Flow et lint la liste ; audit par Visual director et Prompt auditor avant génération, planche contact par Image QC après ; montage par `python scripts/build_slideshow.py shots.json voice.wav timing.json out.mp4 --flow flow/<video>`.
7. **Livrer** : script complet + shot list + la fiche de publication complète de `references/publication.md` (titre, description avec chapitres calés sur la voix, tags ≤ 500 caractères, **catégorie Éducation** toujours écrite, miniature texte par code). Passer la checklist de la section 4 avant de livrer.

Par défaut, livrer **script + plan de production** ; si l'utilisateur ne veut que le texte, livrer le script seul.


## Agents de production
Le rédacteur seul se répète ; la production passe par des agents spécialisés lancés en parallèle avec l'outil Agent, chacun avec un brief complet (`references/agents.md`) : **Fact-checker** et **Script critic** après le brouillon ; **Visual director** et **Prompt auditor** après la shot list ; **Image QC** (vision) après chaque lot d'images ; **Publication checker** avant livraison. L'orchestrateur applique leurs tableaux de corrections et relance ce qui doit l'être. Ne jamais sauter Visual director et Image QC : ce sont eux qui empêchent les cartes nues, les bulles vides et les doublons.

## 1. Paramètres à choisir avant d'écrire

| Paramètre | À remplir | Contrainte |
|---|---|---|
| Lieu isolé | `[LIEU]` | fermé, dépendant de systèmes (air, eau, énergie, chaleur) |
| Événement déclencheur | `[ÉVÉNEMENT]` | une cause claire, datée à l'heure près |
| Durée | `[DURÉE]` | 365 jours par défaut ; sinon un nombre précis |
| Menace extérieure | `[MENACE]` | jamais vue, jamais expliquée |
| Motif récurrent | `[HEURE/CHIFFRE]` | une heure ou un nombre qui revient (scènes 1, 3, 6, 9) |
| Ressources | `[RESSOURCES]` | eau, nourriture, air, énergie, médical, communication |
| Crise n°1 | `[CRISE 1]` | panne d'un système vital (énergie, air, chaleur) |
| Crise n°2 | `[CRISE 2]` | danger physique différent (fuite, feu, maladie, intrusion) |
| Mystère | `[MYSTÈRE]` | un signal, un bruit, une présence, un objet déplacé |
| Menace intérieure | `[MENACE INTÉRIEURE]` | solitude → hallucinations → somnambulisme / acte contre soi |
| Twist | `[TWIST]` | un seul type (section 3.7) |

Règle : plus le lieu a de systèmes, plus il y a de crises possibles. Les 7 décors prêts à l'emploi (chalet, appartement, canot, station polaire, ferme, sous-marin, station spatiale) sont pré-remplis dans `references/reference-beat-sheet.md`.

## 2. Structure calibrée (cible 11 min 30, ≈ 1 600 mots à 140 mots/min)

| # | Scène | Timecode | Mots | Jour-repère | Fonction |
|---|---|---|---|---|---|
| 1 | **Hook** | 0:00–0:30 | 70 | Jour 0 | Heure précise + alarme + compte à rebours + action + annonce coupée |
| 2 | **Inventaire** | 0:30–2:30 | 280 | Jour 0 | Visite des systèmes avec 6 à 8 chiffres concrets |
| 2b | **Les 3 règles** | 2:30 | 30 | Jour 0 | Sécurité / vérification / routine |
| 3 | **Premières semaines** | 2:30–4:15 | 240 | Jours 1–14 | Danger scientifique + 1 détail étrange noté + silence |
| 4 | **Crise n°1** | 4:15–6:30 | 310 | ≈ Jour 70 | Panne, action en 3 temps, durée exacte, leçon « X est la clé » |
| 5 | **Routine et solitude** | 6:30–8:10 | 230 | Mois 4–6 | Maintenance (3 règles réelles), début du déclin |
| 6 | **Mystère** | 8:10–9:00 | 115 | ≈ Jour 180 | Événement impossible, vérification, déclin accéléré |
| 7 | **Crise n°2** | 9:00–9:50 | 115 | ≈ Jour 260 | Danger rapide, geste à ne pas faire, ressource perdue |
| 8 | **Escalade psychologique** | 10:00–10:30 | 70 | ≈ Jour 300 | Le personnage devient la menace ; mesure contre soi-même |
| 9 | **Climax et twist** | 10:30–11:30 | 140 | Jour 365 | Bilan chiffré, message, choix, twist en une phrase |

Les jours-repères sont **inégaux et précis** (71, 183, 264, 301 plutôt que 60, 180, 270, 300). Chaque jour-repère = un événement.

## 3. Règles d'écriture

### 3.1 Voix
- **2ᵉ personne** ("you"), **présent de narration**, du début à la fin.
- **Phrases courtes.** Une idée par phrase. Peu d'adjectifs : la tension vient des faits.
- **Aucun nom propre** pour le personnage. Pas d'humour, pas de morale.

### 3.2 Le hook en 6 temps (30 secondes)
1. Heure exacte (« 6:14 a.m. »).
2. Signal d'alerte (sirènes, alarme, message).
3. Fausse explication rassurante écartée (« Not a drill. »).
4. Compte à rebours court (« 8 minutes »).
5. Action physique immédiate (fermer l'écoutille, couper l'arrivée).
6. Annonce coupée au milieu + durée de l'isolement + premier doute.

### 3.3 Le rythme interne : scène → fait → scène
Chaque crise suit : **problème → action logique en 3 étapes → explication réelle → leçon en une phrase → nouvelle règle**.
La leçon est courte et mémorisable : « Power is the key. » « Propane doesn't expire. » « CO₂ rises without ventilation. »

### 3.4 Densité de chiffres
- Inventaire : 6 à 8 chiffres (quantité → calcul → durée couverte).
- Chaque crise : 2 à 3 chiffres (seuil, durée, perte).
- Bilan final : 3 à 5 chiffres (jours, ressources restantes, crises survécues).
- Jamais « beaucoup », toujours un nombre. Donner l'ordre de grandeur puis la conséquence.

### 3.5 Le motif récurrent
Une heure, un chiffre ou un son qui revient dans les scènes 1, 3, 6 et 9, et qui **change de sens** à la fin.

### 3.6 Les boucles ouvertes
Poser au moins **3 éléments jamais expliqués** (un détail physique, un signal, un son). Ne jamais les résoudre : le twist les relie ou les aggrave.

### 3.7 Le twist final
Un seul type :
1. **Retournement de source** : la cause supposée était autre chose.
2. **Fausse sécurité** : la délivrance révèle un problème plus grand (ex. : « N'ouvrez pas » à la radio, puis des coups qui viennent de l'intérieur).
3. **Menace intérieure confirmée** : la menace était le personnage.
4. **Boucle** : retour au début avec un détail changé.

Dernière phrase : **une seule phrase courte, concrète, sans explication.** Elle doit laisser la porte ouverte à un épisode 2.

## 4. Contrôle qualité avant livraison
- [ ] Lieu fermé, dépendant de systèmes ; événement daté à l'heure près
- [ ] Hook en 6 temps en 70 mots max
- [ ] 2ᵉ personne et présent du début à la fin
- [ ] Deux crises de types différents, chacune avec action en 3 temps + leçon en une phrase
- [ ] Chaque chiffre vérifié (fact-bank ou web) ; aucun chiffre rond gratuit
- [ ] Jours-repères inégaux et précis ; motif dans les scènes 1, 3, 6, 9
- [ ] Au moins 3 boucles ouvertes, aucune résolue
- [ ] Dernière phrase courte, sans explication, ouverte sur une suite
- [ ] Longueur 1 500–1 700 mots (10–12 min)
- [ ] Fiche de publication complète (§10.0 de `publication.md`) : **catégorie Éducation écrite**, tags ≤ 500 caractères vérifiés, chapitres aux temps réels de la voix, contenu synthétique = oui, commentaire à épingler
- [ ] Images : planche contact passée par l'agent Image QC (aucune bulle de dialogue, aucun texte généré, même personnage partout), rejets régénérés ; aucune carte de chiffre sans icône ; jamais 3 images de même famille de suite ; miniature 1280 × 720 avec texte par code

Export, publication, erreurs à éviter : `references/publication.md`.
