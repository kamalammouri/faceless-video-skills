# Brief de pré-production : les questions à poser AVANT d'écrire

Le skill ne choisit plus seul le personnage ni le scénario. Avant le premier mot du script, il fait valider trois choses par l'utilisateur : **le style de personnage, le scénario, et les paramètres de la vidéo**. Les réponses sont écrites dans `brief.json` (dossier de travail), que `scripts/prompts.py` et tous les agents lisent ensuite. Sans `brief.json` validé, on ne passe pas à l'écriture.

Pourquoi : sans brief, chaque vidéo sortait avec le même personnage (la fiche était codée en dur dans `prompts.py`) et le rédacteur prenait le premier scénario venu. Le brief coûte deux tours de conversation et évite une vidéo entière à refaire.

## Règles de conduite

- **Deux tours maximum**, jamais plus. Tour 1 : cadrage (une seule salve de questions). Tour 2 : choix du scénario parmi trois propositions.
- Ne poser **que** ce que l'utilisateur n'a pas déjà dit. S'il a donné le sujet, le style et la langue dans sa demande, le tour 1 se réduit à une ligne de confirmation (« Sujet X, style stickman-meme, voix EN, livrable complet : je lance les 3 scénarios »), et on passe au tour 2.
- Dans Claude Code, poser les questions du tour avec l'outil **AskUserQuestion** (un seul appel, jusqu'à 4 questions, l'option recommandée en premier avec « (Recommandé) »). Ailleurs (claude.ai, autre client), poser les mêmes questions en **une liste numérotée dans un seul message** et attendre la réponse.
- Chaque question porte une valeur par défaut : si l'utilisateur répond « comme tu veux » ou ne répond pas à une question, prendre la valeur par défaut et l'écrire dans le brief.
- Le brief est **relu à voix haute** en 3 lignes avant de commencer l'écriture (style, scénario, paramètres) : c'est la dernière chance de corriger à bas coût.

## Tour 1 : cadrage

| # | Question | Options (la première = défaut) | Clé `brief.json` |
|---|---|---|---|
| 1 | **Sujet / thème** (seulement s'il manque) | question libre : lieu, organisation, paradoxe, « comme la vidéo X » | `subject` |
| 2 | **Durée** | `5 min` (défaut : le format des chaînes de référence, 750 à 900 mots) · `4 min` · `7 min` (maximum, norme 2 du `SKILL.md`) | `duration_min` |
| 3 | **Livrable** | production complète (défaut pour The Hidden Bargain : script, images Flow, montage, miniature, fiche de publication) · script + plan de production · script seul | `deliverable` |

**Pas de question de style, de format ni de voix pour The Hidden Bargain** (normes de la section 0 du `SKILL.md`, mesurées le 29 octobre 2026 : la seule vidéo courte à miniature caveman-duo a fait 269 vues, les autres 4 à 37 ; une chaîne = un format, un univers, une miniature). Si le sujet demandé est une histoire de survie jour par jour, le signaler et proposer la chaîne Ifverse Tales (skill `what-if-story-video`). Le tour 1 confirme en une ligne : « intérieur thin-line, miniature caveman-duo, voix edge-tts en-US-GuyNeural -5 % (ou Gemini TTS Kore si une clé GEMINI_API_KEY est dans le .env), comme l'épisode précédent ». Pour une **autre chaîne**, poser en plus les deux questions d'origine : style (`stickman-meme`, `egg-headphones`, `storybook-human`, `caveman-duo`, `thin-line`, custom via l'agent Character designer) et voix (`references/voice.md`).

Paramètres annoncés avec leur défaut, **sans question** (l'utilisateur les change s'il veut, dans la même réponse) :

| Paramètre | Défaut | Clé |
|---|---|---|
| Durée | 5 min (explainer The Hidden Bargain), 7 min au plus | `duration_min` |
| Ton | documentaire chaleureux | `tone` |
| Costume du personnage | `barefoot` (le style) ; par étape si le récit change de lieu ou de moment (nuit : « a grey wool blanket over the shoulders », labo : « white lab coats over the fur tunics ») | `character.costume`, `character.costumes_by_stage` |
| Décor en une phrase | **neutre** (« each scene in its own place as described below, drawn as a full painted set with depth ») : chaque texte de scène décrit son propre lieu, sinon Flow mélange savane et salle de bain | `setting` |
| Voix : nom, style, débit | edge-tts : `en-US-GuyNeural`, débit `-5%` (≈ 150 mots/min avec les pauses) ; Gemini : `Kore`, style « calm, slow, low-pitched documentary narration, no enthusiasm » | `voice.name`, `voice.style`, `voice.rate` |
| Miniature | toujours le gabarit `thumbnail` de `caveman-duo` (duo expressif, un accessoire, nuit et feu de camp, bandeau vide en haut), quel que soit le style intérieur ; texte = 2 à 4 mots en anglais grammatical (norme 4 du `SKILL.md`), relu par l'English copy editor, posé par `scripts/thumb.py` | `thumbnail_style`, `thumbnail` |
| Série | numéro d'épisode et liste des vidéos déjà publiées (pour le Story architect) | `series` |

**Si le sujet est déjà donné** (« fais-moi une vidéo sur les dents de sagesse »), le tour 1 n'est pas une question : une seule ligne de confirmation (« Dents de sagesse, 5 min, production complète, intérieur thin-line, miniature caveman-duo, edge-tts GuyNeural -5 % : je lance les 3 angles »), et on passe au tour 2. L'utilisateur corrige dans sa réponse s'il veut autre chose.

Si le style est **custom** : lancer l'agent **Character designer** (`references/agents.md`) avec la phrase de l'utilisateur, montrer la fiche obtenue (fiche de prompt en anglais, 3 expressions, accessoire signature, phrase QC), la faire valider dans le tour 2 en même temps que le scénario.

## Tour 2 : choix du scénario

1. Lancer l'agent **Story architect** (`references/agents.md`) avec le sujet, le format (tableau de structure et paramètres du `SKILL.md`), le brief du tour 1 et, si l'utilisateur en a, la liste de ses vidéos déjà publiées (pour ne pas refaire un angle).
2. Présenter ses **3 angles** sous forme compacte : titre au gabarit de la chaîne, logline en une ligne, hook en deux phrases, type de twist (ou de retournement), un fait vérifiable. Une ligne de recommandation.
3. Poser **une** question : « Quel scénario ? » avec les options A (Recommandé), B, C, et « autre » (l'utilisateur décrit le sien ou mélange deux angles). Si le style est custom, ajouter la question « Fiche du personnage : OK / à modifier ».
4. Écrire `brief.json`, relire le brief en 3 lignes, puis passer à l'étape « Choisir les faits » du workflow.

## Format de `brief.json`

```json
{
  "format": "why-explainer-video",
  "subject": "the human appendix: Darwin called it useless in 1871; Duke 2007 showed it is a safe house of gut bacteria",
  "style": "thin-line",
  "thumbnail_style": "caveman-duo",
  "character": {
    "costume": "barefoot",
    "costumes_by_stage": [{"stage": "night", "costume": "barefoot, a grey wool blanket over the shoulders"}, {"stage": "past", "costume": "barefoot"}],
    "sheet": null,
    "name": null
  },
  "setting": "each scene in its own place as described below, drawn as a full painted set with depth",
  "voice_language": "en",
  "voice": { "engine": "edge", "name": "en-US-GuyNeural", "style": "calm, slow, low-pitched documentary narration, no enthusiasm", "rate": "-5%", "model": null },
  "duration_min": 5,
  "tone": "warm-documentary",
  "thumbnail": "character-prop",
  "deliverable": "script+production",
  "scenario": {
    "choice": "A",
    "title": "Why Evolution Refused to Delete Your Appendix (It Was Never Useless)",
    "logline": "...",
    "hook": "...",
    "twist_type": "a famous scientist was wrong + a job discovered recently",
    "motif": "tap water cupped in both hands"
  },
  "series": { "episode": 2, "previous_videos": ["Why Evolution Kept Your Goosebumps (They Were Never Useless)"] },
  "validated_by_user": true
}
```

- `character.sheet` : phrase complète de la fiche (en anglais) pour un style custom ; `null` = la fiche du style.
- `character.costumes_by_stage` : liste `[{"stage": "Day 0", "costume": "..."}, …]` quand le costume change au fil du récit (grades, saisons) ; `prompts.py` prend alors `costume` plan par plan dans `shots.json`.
- `validated_by_user` : `true` seulement après la réponse du tour 2. Les agents refusent un brief non validé.

## Ce que le brief change en aval

- `python scripts/prompts.py shots.json` lit `brief.json` : préfixe, fiche du personnage, costume et décor viennent du style choisi. Plus aucune description de personnage dans le code.
- Les briefs des agents **Prompt auditor** et **Image QC** reçoivent la phrase `qc` du style (et la fiche custom le cas échéant) à la place d'une description fixe.
- La miniature suit le gabarit `thumbnail` du style (`styles.json`) : pour `stickman-meme`, le split « avant / après » des miniatures Galon Zéro.
- `python scripts/tts.py shots.json` lit `brief.json` → `voice` : moteur (Gemini TTS ou edge-tts), voix, style, débit, langue ; il écrit `voice.wav` et `timing.json` pour le montage (`references/voice.md`).
- La fiche de publication est écrite dans la langue de la voix.
