# Style visuel, animation et méthode de fabrication

> Ce plan visuel est une direction artistique proposée pour le format. Le montage réel de la vidéo de référence n'a pas été analysé image par image : si l'utilisateur fournit des captures ou une analyse visuelle, aligner la palette et le rythme de coupe dessus.

## 7. STYLE VISUEL ET D'ANIMATION

## 7.1 Direction artistique
- **Documentaire sombre, réaliste, claustrophobe.**
- **Vue subjective (POV)** : jamais de visage, seulement les mains et ce que le personnage regarde.
- Contraste fort entre l'intérieur (lumière chaude faible) et l'extérieur (lumière froide).
- Léger grain de pellicule et vignette douce sur toute la vidéo.

## 7.2 Palette
| Usage | Couleur |
|---|---|
| Extérieur / froid | Bleu acier `#5B7C99` |
| Ombres | Noir bleuté `#0A1118` |
| Intérieur chaud | Orange sourd `#C98A3D` |
| Danger | Rouge `#B3261E` |
| Texte | Blanc cassé `#F2F2F0` |
| Motif mystère | Rouge discret `#D1453B` |

## 7.3 Étalonnage
1. Contraste +25, ombres -20, hautes lumières -15, saturation 85.
2. Ombres froides, hautes lumières intérieures légèrement chaudes.
3. Courbe en S douce.
4. Vignette -1.2, grain 12–18 %.
5. Scènes de crise : désaturation à 60 % et léger flou de bougé.

## 7.4 Mouvements
- **Pousse lente** (zoom 100→108 % sur 4–6 s) sur presque tous les plans.
- **Tremblement** (wiggle) uniquement en crise.
- **Respiration** (zoom pulsé de 1 %) sur les moments de peur.
- **Ralenti 50–70 %** sur les gestes clés.
- **Accéléré 400–800 %** sur les montages de routine.
- **Overlays** neige, poussière, brume en mode Screen.

## 7.5 Transitions
| Moment | Transition |
|---|---|
| Normal | Fondu enchaîné 12–18 images |
| Tension | Coupe franche |
| Panne / silence | Fondu au noir 6 images + 1–2 s de noir |
| Retour de la lumière | Flash blanc doux 4 images |
| Fin de scène forte | Dip to black 12 images |
| Routine | Coupes très rapides 4–8 images |

## 7.6 Textes et infographies
- Police sans-serif condensée, majuscules, blanc cassé, ombre légère.
- Apparition : fondu + glissement vertical 20 px sur 6 images.
- **Maximum 2 secondes** à l'écran.
- Chiffres animés en **count-up** (de 0 à la valeur en 1 s).
- Icônes en traits fins, apparition par tracé.
- Jours (`DAY X`) : petit, en bas à gauche.
- Motif récurrent : toujours en rouge discret avec glitch de 3 images.

## 7.7 Audio
| Couche | Niveau |
|---|---|
| Voix off | -12 dB (peak -6) |
| Musique | -24 à -20 dB sous la voix |
| Ambiances | -30 dB |
| SFX | -18 à -10 dB |

- **Musique :** drones graves continus, sans mélodie. Un seul moment chaleureux, bref, à l'espoir.
- **Silence :** utilisé **deux fois** comme arme (début de la crise n°1 et fin).
- **Sidechain :** la musique baisse de 4 dB sous la voix.
- **Son signature :** un SFX court lié au motif récurrent, joué à chaque apparition.

## 8. MÉTHODE DE FABRICATION

## 8.1 Pipeline en 7 étapes

1. **Écrire** le script avec le template (section 5).
2. **Vérifier** chaque fait réel (chiffres, procédures, explications).
3. **Voix off** : enregistrer ou générer, puis nettoyer (réduction de bruit, compresseur léger, EQ chaleureux).
4. **Découper** : un marqueur par scène sur la timeline.
5. **Shot list** : un plan de 3 à 6 s par idée importante.
6. **Créer les plans** (section 8.3), monter, étalonner, ajouter textes et sons.
7. **Mixer et exporter** : H.264 1080p, 16–20 Mbps.

## 8.2 Structure des pistes (Premiere)

| Piste | Contenu |
|---|---|
| V5 | Textes et infographies |
| V4 | Overlays (neige, brume, poussière) |
| V3 | Grain + vignette (calque d'ajustement) |
| V2 | Inserts (mains, objets, cadrans) |
| V1 | Plans principaux |
| A1 | Voix off |
| A2 | Musique |
| A3 | Ambiances |
| A4 | SFX |

## 8.3 Sources des plans (par ordre de préférence)
1. **Clips générés par IA** (text-to-video ou image-to-video).
2. **Images IA animées** (pousse + parallaxe).
3. **B-roll de stock.**

## 8.4 Prompt de style commun (à placer au début de CHAQUE prompt)

```
Cinematic documentary realism, first-person POV, cold color palette with dim
warm interior lights, heavy contrast, fine film grain, shallow depth of field,
slight vignette, 35mm lens, moody and claustrophobic, no text, no logos,
no visible face, 16:9
```

**Prompt négatif :**

```
cartoon, illustration, text, watermark, logo, face closeup, extra fingers,
oversaturated, bright cheerful, plastic look
```

## 8.5 Modèle de prompt par plan

```
[PROMPT DE STYLE COMMUN] + [TYPE DE PLAN] + [SUJET] + [LIEU] + [LUMIÈRE] + [MOUVEMENT DE CAMÉRA]
```

**Exemples de types de plans à prévoir pour chaque scène :**
- **Plan large** (établir le lieu)
- **Plan moyen POV** (couloir, déplacement)
- **Gros plan mains** (action technique)
- **Gros plan objet** (cadran, écran, journal)
- **Plan de réaction** (respiration, mains qui tremblent)
- **Insert** (détail du motif récurrent)

## 8.6 Cohérence entre les plans
- Garder **le même décor** (matériaux, couleurs, éclairage).
- Garder **le même équipement du personnage** (gants, vêtement).
- Réutiliser une **image de référence** dans chaque génération.
- Appliquer **le même étalonnage** à tous les plans.

## 8.7 Comment animer une image fixe
1. Placer l'image sur V1.
2. Transform : échelle 100 % → 108 %.
3. Léger déplacement de position (± 20 px).
4. Overlay neige/poussière en Screen sur V4.
5. Wiggle si la scène est une crise.

## 8.8 Rythme de coupe par type de scène

| Type de scène | Durée des plans |
|---|---|
| Hook | 4–8 s |
| Inventaire | 3–6 s |
| Calme / solitude | 5–8 s |
| Crise | 2–6 s |
| Routine (montage) | 4–8 images |
| Mystère | 4–8 s |
| Climax | 4–6 s, puis plan final long |

## 8.9 Mode diaporama 2D (sans animation), variante économique

Mesuré sur deux vidéos de 20 min d'une chaîne faceless à 2,8 M de vues : 300 images fixes, une par phrase, 4 à 5 s chacune, coupes franches, zéro mouvement de caméra, 94 % du temps strictement fixe. Le rythme vient de la fréquence des coupes et de la voix, pas de l'animation.

C'est le **mode par défaut de la chaîne** : le style documentaire sombre des §7 et 8.1 à 8.8 a été testé et n'a pas plu ; le style retenu est crème, trait doux, personnage récurrent (préfixe maison dans `flow-automation.md`), avec une variante « fond ardoise, une lumière orange » pour les scènes de nuit et de danger, qui garde la tension du récit.

Pour produire une vidéo de survie à moindre coût :
- **Un plan par moment**, pas par phrase : 60 à 70 images Flow pour 11 min (5 à 15 s chacune), générées automatiquement (`flow-automation.md`), plus une vingtaine de cartes par code (heure, jour, litres, degrés, compte à rebours). Une image par phrase (230 images) coûterait 2 h de génération pour un gain invisible.
- Coupes franches ; garder seulement les deux fondus au noir des silences-armes.
- Style unique sur toutes les images, préfixe maison en tête de chaque prompt, personnage identique partout (c'est lui qui fait la cohérence) ; `Dark variant` sur les scènes de crise.
- Les chiffres (inventaire, jauges, compte à rebours, jours) en images générées par code (matplotlib style « xkcd » ou SVG), jamais par IA : chiffres exacts, labels sans erreur.
- Texte à l'écran = mot ou chiffre exact de la voix, 1 à 3 mots.
- Assemblage ffmpeg : liste de concaténation image + durée, piste voix, lit sonore discret.

Le mode diaporama renonce au grain, aux overlays et à la pousse lente des §7.4 à 7.7 ; il garde l'étalonnage et le silence.
