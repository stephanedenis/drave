# Le chargement construisait 2,7 Go de « listes » que personne ne lisait

> Campagne : **machine et moteur** · expérience 01 — le coût du chargement
> Question : une passe `--ppl` sur Qwen3-30B passe **27 s** à charger avant de calculer 1 s par
> jeton. Que fait le chargeur pendant ces 27 s, et le faut-il ?
> Verdict : **non, il ne le faut pas.** Le chargeur construisait **par défaut** la représentation
> « listes » des projections (`PushMat`), **2,69 Go** pour Qwen3-30B et **0,71 Go** pour
> Qwen2.5-0.5B — alors que le chemin qui l'utilise n'est choisi que si la densité d'activation
> passe sous `seuil_push` (0,22), et que les passes mesurées ne l'utilisent **jamais**
> (« dont en listes : 0,0 M », dit le moteur lui-même). Rendre cette construction **paresseuse**
> (au premier usage réel) fait passer le chargement de **26,95 s à 7,36 s** (Qwen3-30B) et de
> **6,85 s à 0,60 s** (Qwen2.5-0.5B), **sans déplacer un chiffre**.
> Date réelle : 2026-10-12, 22 h 30-22 h 47 HAE (heure lue sur la machine ; source : git, commits `2bbecc86`)
> Protocole : `--ppl … --limit 2`, cache évincé avant chaque essai ; mesure du chargement lue
> dans la ligne du moteur (`[modele] … couches chargées en …s — listes … Go`)

## 1. Les mesures

| modèle | mode | chargement | « listes » construites |
|---|---|---|---|
| Qwen2.5-0.5B | défaut (auto) | **6,85 s** | 0,71 Go |
| Qwen2.5-0.5B | `--dense` | 0,77 s | 0,00 Go |
| Qwen2.5-0.5B | défaut, **après** la paresse | **0,60 s** | 0,00 Go |
| Qwen3-30B-A3B | défaut (auto) | **26,95 s** | 2,69 Go |
| Qwen3-30B-A3B | `--dense` | 7,58 s | 0,91 Go |
| Qwen3-30B-A3B | `--q4` | **2,63 s** | 0,00 Go |
| Qwen3-30B-A3B | défaut, **après** la paresse | **7,36 s** | 0,91 Go |

Ce que ça dit :

* **la forme « listes » était construite pour rien** : 0,71 Go / 6,1 s sur le petit modèle,
  2,69 Go / 19,3 s sur le gros. Les deux passes mesurées affichent « dont en listes : 0,0 M » —
  le chemin push n'a pas servi une seule fois ;
* **le chargement est CPU, pas E/S** : à froid 26,80 s, à chaud **26,03 s** (mêmes pages), et
  26,82 s avec un seul fil ; optimiser la lecture ne le touche pas, c'est la construction qu'il
  fallait éviter ;
* **il reste 7,36 s** (Qwen3-30B) : c'est la déquantification en f32 (`g.dequant`) plus la
  reconstruction Q8 des tenseurs « denses » — le `--q4` les évite (**2,10 s**) en **empruntant les
  blocs Q4_K du fichier**.

  **Correction d'une affirmation de la première version de cette fiche.** Elle disait, sur une
  paire de jetons à froid, que l'emprunt était « plus fidèle » (93228 contre 95592). C'était un
  artefact de départ à froid : mesuré sur **32 jetons**, l'ordre s'inverse et il est net —

  | chemin | perplexité (32 jetons) | chargement |
  |---|---:|---:|
  | défaut (`auto`) | **33,6967** | 7,58 s |
  | `--dense` | **33,6967** | 7,67 s |
  | `--q4` (blocs du fichier) | **33,9093** | **2,10 s** |

  L'emprunt est donc **0,63 % moins précis** (33,9093 contre 33,6967) — c'est attendu : la
  reconstruction Q8 lit des poids déquantifiés en f32 à 8 bits, l'emprunt lit les blocs Q4_K du
  fichier tels quels. Le défaut et `--dense` rendent **exactement** le même chiffre (la forme
  paresseuse ne change pas le chemin choisi).

  **La décision, chiffrée** : `--q4` échange **0,63 % de perplexité contre 5,5 s de chargement par
  passe**. Sur une passe courte, ces 5,5 s dominent (7,6 s de chargement pour ~1 s de calcul) ;
  sur une passe longue, elles disparaissent. Ce n'est pas au moteur de trancher à la place de
  l'utilisateur : le défaut reste `auto`, et le drapeau est là.

## 2. L'anecdote qui compte : la porte du flux a attrapé ma paresse trop large

La première version rendait la forme paresseuse disponible **partout**, y compris en mode
`--dense` — où le chargement ne l'avait **pas** chargée, ce qui faisait valoir `use_dense = true`
à chaque couche. Résultat : les couches creuses basculaient sur le chemin **push**, et
`tools/porte-flux.sh` l'a vu tout de suite — **61,9920 → 58,8636**, et le mode « listes par
blocs » **rouge** (1,02e-1 contre un plafond de 6e-2). La correction tient en une condition
(`auto && !dense`) et la porte est revenue **exactement** à ses valeurs.

**La leçon, à ne pas réintroduire** : *une paresse ne doit pas élargir ce que le chargement avait
décidé.* Rendre une forme « disponible à la demande » change le **choix** du chemin si le choix
dépend de sa présence (`use_dense` en dépendait) — la paresse doit donc reproduire exactement la
disponibilité, pas la dépasser.

## 2bis. Une troisième erreur de banc, attrapée par la PASSE : un nombre qui change d'unité

`porte-push-paresseux.sh` lisait `chargées en [0-9.]+s` — et le moteur imprime une durée `{:?}` :
**`601.034622ms`** quand le chargement est rapide, `7.36s` sinon. La porte **passait sur une machine
lente** (le premier essai donnait 1,42 s) et rendait une chaîne **vide** sur une machine rapide
(0,6 s) — d'où un `float("")` en pleine passe, à 02 h 18. C'est la passe complète qui l'a vue, pas
une relecture : **une porte qui n'a tourné que dans les conditions de son auteur n'a pas tourné.**

Corrigé : l'unité est **lue** (`µs`/`ms`/`s`) et normalisée, et la porte **refuse de mesurer sur du
vide** — elle imprime la sortie brute du moteur au lieu d'un `float("")`. Mesure après correction :
**0,68 s en paresseux contre 6,53 s en avance (9,6×)**.

## 3. Ce qui reste ouvert

* `DRAVE_PUSH_TOT=1` rend l'ancien comportement, pour refaire la mesure ;
* ~~la construction paresseuse n'a été déclenchée par aucune des passes mesurées~~ — **trouvé, et
  la porte existe** : c'est l'**inférence** (génération, conversation) qui prend le chemin push —
  **93 tenseurs** construits à la demande sur Qwen2.5-0.5B —, alors que `--ppl` et ses variantes
  (`--flux 1..4`, `--lot`, `--episodique`) n'en construisent **aucun**. `tools/porte-push-paresseux.sh`
  le verrouille : même texte gourmand en paresseux et en avance (ids identiques), aucune
  construction sur une passe `--ppl`, chargement **1,42 s contre 7,40 s** (5,2×), et la porte est
  **vue ROUGE** avec `DRAVE_PUSH_FAUX=1` (forme construite depuis des zéros) ;
* le reste du chargement (déquantification + reconstruction Q8, 7,4 s) est le prochain candidat
  mesuré — mais son remplacement (`--q4`, emprunt des blocs) **change la représentation**.
