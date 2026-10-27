# Agents de production

Un seul rédacteur qui écrit, dessine, vérifie et publie finit par se répéter : mêmes cartes, mêmes cadrages, mêmes erreurs non vues. Le skill répartit donc la production entre des agents spécialisés lancés avec l'outil Agent (type `general-purpose`, ou un agent défini dans `agents/` du repo s'il existe). Chaque agent reçoit un brief complet, travaille seul, et rend un résultat court que l'orchestrateur applique. Les agents indépendants sont lancés **dans le même message**, en parallèle.

## Orchestration (qui lance quoi, quand)

| Étape | Agents en parallèle | Entrée | Sortie attendue |
|---|---|---|---|
| Après le brouillon du script | **Fact-checker** + **Script critic** | le script | liste de corrections, chacune avec la phrase visée |
| Après la liste d'images | **Visual director** + **Prompt auditor** | shot list + préfixe de style | shot list corrigée, prompts réécrits |
| Après la génération des images | **Image QC** (vision) | planche contact + shot list | liste des images à régénérer avec le nouveau prompt |
| Avant livraison | **Publication checker** | fiche de publication + voice.json | fiche corrigée ou « OK » |

L'orchestrateur ne refait pas le travail des agents : il applique leurs corrections, relance ce qui doit l'être (régénération Flow des rejets), et passe la checklist finale.

## Briefs (à copier dans le prompt de l'agent, puis compléter les crochets)

### Fact-checker
```
Tu vérifies les faits d'un script de vidéo YouTube [format]. Pour CHAQUE nom propre, année, chiffre, unité et mécanisme
physique du script ci-dessous : cherche une source sur le web, note [vérifié], [corrigé : valeur → valeur, source] ou
[invérifiable]. Ne réécris pas le style. Rends uniquement un tableau : phrase d'origine | verdict | correction | source.
Script : [SCRIPT]
```

### Script critic
```
Tu es un script doctor pour vidéos YouTube [format]. Lis le script et signale, avec la phrase exacte : (1) les répétitions
de structure ou de mot (même tournure deux fois en moins de 60 s), (2) les passages sans image mentale (abstraits), (3) les
chiffres ronds suspects, (4) les ruptures de point de vue (2ᵉ personne, présent), (5) les boucles ouvertes résolues trop tôt,
(6) les phrases trop longues pour une voix IA (> 25 mots). Pour chaque point, propose la réécriture. Maximum 25 points,
du plus grave au plus léger. Rends un tableau : phrase | problème | réécriture.
Script : [SCRIPT]
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
revient au milieu et à la fin. Rends la shot list complète corrigée dans le même format, puis 5 lignes de changements.
Shot list : [SHOT LIST]
```

### Prompt auditor
```
Tu relis des prompts d'images pour un générateur (Google Flow) qui dessine TOUT ce qu'on lui décrit. Pour chaque prompt :
(1) supprime ou reformule tout ce qui déclenche une bulle de dialogue, un panneau, un écran avec du texte, un cadran avec
des chiffres, un livre ouvert, une étiquette : « talking », « calling », « says », « sign », « label », « screen showing »,
« reads », « written » sont interdits ; décrire la posture à la place (« handset held to the head, mouth closed ») ;
(2) vérifie que la fiche du personnage récurrent est présente mot pour mot ; (3) vérifie la mention du décor ;
(4) vérifie que la phrase de fin est « no text, no letters, no numbers, no speech bubbles, no signs » ; (5) signale deux
prompts trop proches (même scène) et propose une variante de cadrage. Rends le tableau : fichier | prompt corrigé | motif.
Préfixe de style : [PRÉFIXE]
Prompts : [PROMPTS]
```

### Image QC (vision)
```
Tu contrôles des images générées pour un diaporama. Regarde la planche contact jointe (chaque vignette porte son nom de
fichier). Rejette toute image qui a : une bulle de dialogue (vide ou non), du texte ou des lettres, des chiffres, un
personnage différent de la fiche (tête ronde blanche, casque orange, t-shirt bleu gris), un cadrage vertical ou une bande
noire, un objet absurde (membres en trop, objet fondu), ou une scène qui ne correspond pas à la phrase. Pour chaque rejet :
fichier | défaut | prompt réécrit pour l'éviter. Rends aussi la liste des fichiers acceptés. Ne commente pas le style.
Planche : [CHEMIN]  Shot list : [SHOT LIST]
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
- Un agent reçoit **tout** ce dont il a besoin dans son brief (le script, la liste, le préfixe) : il ne voit pas la conversation.
- Les sorties sont des tableaux courts ; l'orchestrateur applique, il ne discute pas.
- Image QC tourne après chaque lot Flow ; les rejets sont régénérés avec le prompt réécrit (supprimer le `.jpg` et le `.png`, relancer `batch.mjs`), puis Image QC repasse sur les nouvelles vignettes seulement. Deux passes maximum, ensuite remplacer par une carte par code.
- Pour une vidéo courte (pilote < 5 min), Fact-checker et Image QC suffisent.
