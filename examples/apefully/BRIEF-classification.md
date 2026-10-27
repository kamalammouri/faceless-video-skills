# Brief : classer les plans d'une vidéo Apefully

Tu reçois les planches contact d'une ou plusieurs vidéos (`ape_shots/<id>/sheets/NN.jpg`, 48 vignettes par planche, chaque vignette porte en haut à gauche son numéro de plan et son minutage). Regarde chaque planche avec l'outil Read et classe CHAQUE vignette.

Familles (une seule par plan) :
- `scene` : personnage(s) dans un décor (savane, maison, labo, bureau, hôpital…)
- `icon` : un objet ou organe isolé sur fond uni, avec ou sans 1 à 3 mots
- `schema` : coupe anatomique, mécanisme, comparaison côte à côte, flèches
- `chart-bar`, `chart-pie`, `chart-line`, `chart-dots` (grille de points qui compte), `gauge` (thermomètre, jauge, compteur), `timeline` (frise, barre de durée, chronologie), `map` (carte), `table` (tableau ou liste)
- `title` : carte-titre ou texte seul
- `other`

Pour chaque vidéo, écris `ape_shots/<id>/classes.json` : une liste d'objets `{"n": <numéro>, "family": "<famille>", "text": "<texte lisible dans l'image, sinon vide>", "note": "<5 mots max : ce qu'on voit>"}`.

Puis écris `ape_shots/<id>/patterns.md` (15 lignes max) : pour chaque plan des familles chart-*, gauge, timeline, map, table, schema, décris le PATRON visuel réutilisable (pas le sujet) : disposition, nombre d'éléments, couleur mise en avant, où est le texte, fond. Exemple : « barre unique très haute à côté d'une barre minuscule, étiquette de ratio "100x" au-dessus, fond crème, cadre arrondi ». Signale aussi le style général de la vidéo (fonds unis crème / décors colorés complets / personnages à cheveux ou têtes blanches rondes).

Ne saute aucune planche. Ne décris pas le contenu scientifique. Rends à la fin un résumé de 5 lignes : nombre de plans par famille.
