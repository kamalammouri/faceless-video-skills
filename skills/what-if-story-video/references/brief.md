# Brief de pré-production : les questions à poser AVANT d'écrire

Le skill ne choisit plus seul le personnage ni le scénario. Avant le premier mot du script, il fait valider trois choses par l'utilisateur : **le style de personnage, le scénario, et les paramètres de la vidéo**. Les réponses sont écrites dans `brief.json` (dossier de travail), que `scripts/prompts.py` et tous les agents lisent ensuite. Sans `brief.json` validé, on ne passe pas à l'écriture.

Pourquoi : sans brief, chaque vidéo sortait avec le même personnage (la fiche était codée en dur dans `prompts.py`) et le rédacteur prenait le premier scénario venu. Le brief coûte deux tours de conversation et évite une vidéo entière à refaire.

## Règles de conduite

- **Deux tours maximum**, jamais plus. Tour 1 : cadrage (une seule salve de questions). Tour 2 : choix de l'histoire (le dilemme) parmi trois propositions.
- Ne poser **que** ce que l'utilisateur n'a pas déjà dit. S'il a donné le sujet, le style et la langue dans sa demande, le tour 1 se réduit à une ligne de confirmation (« Sujet X, style stickman-meme, voix EN, livrable complet : je lance les 3 scénarios »), et on passe au tour 2.
- Dans Claude Code, poser les questions du tour avec l'outil **AskUserQuestion** (un seul appel, jusqu'à 4 questions, l'option recommandée en premier avec « (Recommandé) »). Ailleurs (claude.ai, autre client), poser les mêmes questions en **une liste numérotée dans un seul message** et attendre la réponse.
- Chaque question porte une valeur par défaut : si l'utilisateur répond « comme tu veux » ou ne répond pas à une question, prendre la valeur par défaut et l'écrire dans le brief.
- Le brief est **relu à voix haute** en 3 lignes avant de commencer l'écriture (style, scénario, paramètres) : c'est la dernière chance de corriger à bas coût.

## Tour 1 : cadrage

| # | Question | Options (la première = défaut) | Clé `brief.json` |
|---|---|---|---|
| 1 | **Le pouvoir et sa limite** (seulement s'il manque) | question libre : « réflexes 10x, mais le corps reste normal » ; `references/premise-bank.md` pour les pistes ; si l'utilisateur donne le pouvoir sans la limite, en proposer une | `subject`, `limit` |
| 2 | **Style de personnage** (`references/character-styles.md`, ids de `scripts/styles.json`) | `stickman-dark` (Recommandé : silhouette noire, yeux blancs, sweat à capuche de couleur, crépuscule ; le style de la chaîne de référence) · `stickman-meme` (grosse tête ronde blanche, visage meme, décor saturé) · `egg-headphones` (tête d'œuf, casque orange, storybook crème) · `storybook-human` (humain peint, film d'animation 90s) · `caveman-duo` · `thin-line` · **custom** (décrire en une phrase : l'agent Character designer fait la fiche) | `style`, `character` |
| 3 | **Voix : moteur et langue** (`references/voice.md`) | `Gemini TTS, anglais` (Recommandé : voix studio, style dirigé par une phrase ; clé API Gemini et quota) · `Gemini TTS, français` · `edge-tts, anglais` (gratuit, sans clé, moins dirigeable) · `edge-tts, français` ; autre langue en « autre » | `voice.engine`, `voice_language` |
| 4 | **Livrable** | script + plan de production (défaut) · script seul · production complète (script, voix, images Flow, montage, fiche de publication) | `deliverable` |
| 5 | **Série** | partie 1 de 3 (défaut : chaque partie a son cliffhanger, le film réunit les trois) · épisode unique · partie 2 ou 3 d'une série existante (donner le script de la partie précédente) | `series` |

Paramètres annoncés avec leur défaut, **sans question** (l'utilisateur les change s'il veut, dans la même réponse) :

| Paramètre | Défaut | Clé |
|---|---|---|
| Durée | 8 min (6 à 9 ; le film = les trois parties) | `duration_min` |
| Ton | fiction chaleureuse, narrateur lent et amusé, jamais moqueur ; 100 mots par minute | `tone` |
| Héros et personnages | prénom du héros (défaut Max), sweat rouge ; rival ou second héros en bleu ; témoin récurrent (ami, mère, coach) ; les personnages déjà créés dans `universe` reviennent | `character.name`, `character.costume`, `universe` |
| Décor en une phrase | déduit du sujet, recopié dans chaque prompt | `setting` |
| Voix : narrateur et personnages | narrateur edge-tts `en-US-GuyNeural` à `-8%` (ou Gemini `Kore`, style « warm, slow, amused storyteller ») ; une voix par personnage dans `voices` : {"MOM": "en-US-JennyNeural", "JAKE": "en-US-ChristopherNeural", "COACH": "en-US-DavisNeural", "ZOE": "en-US-AnaNeural"} ; `tts.py` signale tout personnage sans voix | `voice.name`, `voice.rate`, `voices` |
| Miniature | `character-prop` : visage du héros à droite, un accessoire, 2 ou 3 mots jaunes à gauche, badge « PART n » (`scripts/thumb.py`) | `thumbnail` |

Si le style est **custom** : lancer l'agent **Character designer** (`references/agents.md`) avec la phrase de l'utilisateur, montrer la fiche obtenue (fiche de prompt en anglais, 3 expressions, accessoire signature, phrase QC), la faire valider dans le tour 2 en même temps que le scénario.

## Tour 2 : choix du scénario

1. Lancer l'agent **Story architect** (`references/agents.md`) avec le pouvoir et sa limite, le format (tableau de structure et paramètres du `SKILL.md`), le brief du tour 1 et, si l'utilisateur en a, la liste de ses vidéos déjà publiées (pour ne pas refaire un angle).
2. Présenter ses **3 angles** sous forme compacte : titre au gabarit de la chaîne, logline en une ligne, hook en deux phrases, type de twist (ou de retournement), un fait vérifiable. Une ligne de recommandation.
3. Poser **une** question : « Quel scénario ? » avec les options A (Recommandé), B, C, et « autre » (l'utilisateur décrit le sien ou mélange deux angles). Si le style est custom, ajouter la question « Fiche du personnage : OK / à modifier ».
4. Écrire `brief.json`, relire le brief en 3 lignes, puis passer à l'étape « Choisir les faits » du workflow.

## Format de `brief.json`

```json
{
  "format": "survival-story-video",
  "subject": "a Soviet polar station cut off after a radio blackout",
  "style": "stickman-meme",
  "character": {
    "costume": "wearing a torn orange parka and a grey wool hat",
    "costumes_by_stage": null,
    "sheet": null,
    "name": null
  },
  "setting": "a small Antarctic research station of three plywood modules on a white plateau",
  "voice_language": "en",
  "voice": { "engine": "gemini", "name": "Kore", "style": "calm, slow, low-pitched documentary narration, no enthusiasm", "rate": "+0%", "model": "gemini-3.8-flash-tts" },
  "duration_min": 11.5,
  "tone": "dark-documentary",
  "thumbnail": "split-before-after",
  "deliverable": "script+production",
  "scenario": {
    "choice": "A",
    "title": "365 Days Alone at the Bottom of the World",
    "logline": "...",
    "hook": "...",
    "twist_type": "fausse sécurité",
    "motif": "the 4:17 a.m. radio tone"
  },
  "series": { "episode": 1, "previous_videos": [] },
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
