# La voix : Gemini TTS ou edge-tts, au choix de l'utilisateur

Le moteur de voix est **demandé au brief** (`references/brief.md`, question « Voix : moteur et langue ») et écrit dans `brief.json` → `voice`. Le script `scripts/tts.py` lit ce choix et produit `voice.wav` + `timing.json`, les deux fichiers que `build_slideshow.py` attend. Ne jamais décider du moteur à la place de l'utilisateur : les deux ont un coût différent (clé et quota d'un côté, voix moins dirigeable de l'autre).

| | **Gemini TTS** (AI Studio « Generate speech », API Gemini) | **edge-tts** (voix Microsoft Edge) |
|---|---|---|
| Qualité | voix studio, **style dirigé par une phrase** (« calm, slow, documentary »), plus de 130 langues dont le français | voix neurales correctes, pas de consigne de style, le nom de la voix fait le ton |
| Coût | clé API Gemini (`GEMINI_API_KEY`), quota gratuit par minute et par jour puis payant | gratuit, sans compte ni clé |
| Installation | `pip install "google-genai>=2.25"` | `pip install edge-tts` |
| Voix par défaut | `Kore` (30 voix studio : Kore, Puck, Zephyr… et une bibliothèque étendue ; voix sur mesure possibles) | `en-US-GuyNeural` en anglais, `fr-FR-HenriNeural` en français (`edge-tts --list-voices`) |
| Sortie | WAV 24 kHz mono | mp3 converti en WAV 24 kHz mono par ffmpeg |
| Horodatage | aucun fourni par l'API | fourni mais inutile ici |
| Quand le choisir | vidéo à publier, ton précis (sombre, lent) | pilote, test de montage, pas de clé sous la main |

Dans les deux cas, **le minutage vient du script, pas du moteur** : `tts.py` génère un clip par plan de `shots.json`, les colle bout à bout avec un silence de 0,35 s, et écrit les temps de début exacts. C'est pour cela que le horodatage absent de Gemini ne gêne pas, et que le montage tombe exactement sur chaque phrase.

## Procédure

1. Vérifier `brief.json` → `voice` (`engine`, `name`, `style`, `rate`, `model`) et `voice_language`. Les flags `--engine`, `--voice`, `--style`, `--rate`, `--model` passent devant.
2. Pour Gemini : mettre `GEMINI_API_KEY=…` dans un `.env` du dossier de travail (jamais dans le dépôt, `.gitignore` l'exclut). `tts.py` le lit lui-même.
3. **Tester sur trois plans** : `python scripts/tts.py shots.json --only 1,2,3`, écouter `voice.wav`. Changer la voix ou le style si le ton ne va pas ; les clips sont dans `tts/<moteur>/` et ne sont régénérés que si la phrase change.
4. Lancer la liste complète : `python scripts/tts.py shots.json`. Gemini : 2 s de pause entre les appels par défaut (`--pace`), les erreurs de quota sont réessayées avec attente croissante ; compter 5 à 10 min pour 70 plans, 20 à 30 min pour 300.
5. Monter : `python scripts/build_slideshow.py shots.json voice.wav timing.json out.mp4 --flow flow/<video>`.
6. Après une correction du script : modifier la phrase dans `shots.json`, relancer `tts.py` (seuls les plans changés sont régénérés), puis le montage.

## Écrire pour les deux moteurs

- Une phrase par plan, 25 mots maximum : un clip trop long se désynchronise de l'image.
- Nombres en lettres quand la voix doit les dire ; pas de symboles, pas d'abréviations, pas de parenthèses (règle du Script critic).
- Gemini : la **même phrase de style sur chaque clip** (`voice.style`), sinon le débit change d'un plan à l'autre. Style par défaut : « calm, slow, low-pitched documentary narration, no enthusiasm ». Pour un passage de crise, mettre `"style"` sur le plan lui-même n'est pas prévu : garder un seul style par vidéo.
- edge-tts : le débit se règle avec `rate` (« -5% » pour une narration lente), la hauteur avec la voix elle-même.
- Les silences-armes du format survie (fondus au noir) se font au montage, pas dans la voix : ne pas écrire de « … » dans la phrase.

## Dépannage

- `GEMINI_API_KEY missing` : clé absente de l'environnement et du `.env`.
- Erreur 429 ou « quota » répétée : augmenter `--pace 5000`, ou passer en `--engine edge` pour le pilote.
- `ffmpeg not found` : `pip install imageio-ffmpeg` (déjà requis par le montage).
- Un clip sonne différemment des autres : supprimer son `.wav` dans `tts/<moteur>/` et relancer, ou reformuler la phrase.
- Modèle Gemini refusé : `--model gemini-2.5-flash-preview-tts` passe par l'ancienne voie (`generate_content`), le script la gère.
