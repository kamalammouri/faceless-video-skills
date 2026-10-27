# Publication, checklists d'export, erreurs à éviter

## 9.3 Avant l'export
- [ ] Voix off nettoyée
- [ ] Marqueurs posés
- [ ] Style et personnage cohérents
- [ ] Étalonnage unifié
- [ ] Transitions appliquées
- [ ] Textes animés (2 s max)
- [ ] Deux silences respectés
- [ ] Mixage vérifié
- [ ] Sous-titres ajoutés

## 10. PUBLICATION

### 10.0 Fiche de publication : toujours livrée, dans cet ordre

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

**Titre :** court, nominal, cherchable. La référence s'appelle « Bunker Survival 1 Year » : 4 mots, lieu + survie + durée. Proposer 3 titres :
1. `[LIEU] Survival [DURÉE]` (ex. « Polar Station Survival 1 Year »)
2. `[DURÉE] Alone in a [LIEU]`
3. `You're Trapped in a [LIEU] for [DURÉE] (Day by Day)`

Éviter les majuscules partout, les points d'exclamation et les promesses (« INSANE », « SHOCKING »). Le format vend le calme.

**Description :**

```
[1 phrase de hook : l'heure, l'événement, la durée]
[1 phrase sur ce qu'on apprend : faits réels, urgences, limites humaines]

00:00 The alarm
00:30 What you prepared
02:30 The three rules
04:15 Day [X] — [Crise 1]
08:10 Day [Y] — [Mystère]
09:00 Day [Z] — [Crise 2]
10:30 Day 365

[Lien vers l'épisode suivant ou la playlist]
#survival #bunker #[décor]
```

Mettre les chapitres aux jours-repères : ils servent de mini-hooks dans la barre de lecture. **Les horodatages viennent du minutage réel de la voix** (début de chaque scène dans le fichier de minutage), jamais des estimations du script : l'écart atteint 40 s. Règles YouTube : premier chapitre à `00:00`, au moins 3 chapitres, chacun d'au moins 10 s, ordre croissant. Les tags : 15 à 20, 500 caractères au total maximum, longueur vérifiée par code.

**Fin de vidéo (fin ouverte) :** pas de call-to-action parlé. Une carte « Day 366 » ou le titre de l'épisode 2 sur fond noir, 5 secondes.

**Miniature :**
- En mode diaporama (défaut de la chaîne) : le gabarit `thumbnail` du style choisi au brief (`scripts/styles.json`) : pour `stickman-meme`, composition coupée en deux, le personnage perdant à gauche et gagnant à droite dans le même décor ; pour les autres styles, le personnage récurrent en gros plan sur la moitié droite, moitié gauche vide, une seule lueur chaude.
- En style documentaire : gros plan sur les mains ou un objet-clé, dans le noir, une seule lueur chaude.
- Texte par code, jamais par le générateur : 2 à 4 mots en jaune (242,196,70) Impact contour noir, le motif récurrent (l'heure, le jour) en rouge (214,72,48), image 1280 × 720.
- Une image du lot avec de l'espace vide fait une miniature provisoire acceptable en attendant l'image dédiée.

## 11. ERREURS À ÉVITER

- Commencer par du contexte au lieu d'une heure et d'une alarme.
- Décrire une crise sans la résoudre en 3 actions et sans leçon.

- Expliquer le mystère.
- Utiliser trop d'adjectifs dramatiques.
- Donner des chiffres vagues ou faux.
- Mettre deux crises du même type.
- Montrer le visage du personnage.
- Mettre de la musique pendant les silences clés.
- Faire des plans de plus de 8 secondes sans mouvement.
- Terminer par une morale ou une explication.
