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
  reconstructions Q8 des tenseurs « denses » — le `--q4` les évite (**2,63 s**) en **empruntant
  les blocs Q4_K du fichier**, au prix d'une représentation différente (perplexité 93228,4793
  contre 95592,5272 sur une paire de jetons à froid : l'emprunt est **plus fidèle**, il ne
  requantifie pas). Changer le défaut est une **décision**, pas une évidence : elle déplace des
  chiffres et doit se mesurer sur une passe complète.

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

## 3. Ce qui reste ouvert

* `DRAVE_PUSH_TOT=1` rend l'ancien comportement, pour refaire la mesure ;
* la construction paresseuse **n'a été déclenchée par aucune** des passes mesurées — il reste à
  trouver le mode qui l'utilise vraiment (le chemin push existe : `PushMat`, `seuil_push`,
  `reports/rapport-croisement-push-pull.md`) et à vérifier qu'elle rend alors **le même** chiffre
  que la construction d'avance : c'est la porte qui manque, et elle s'écrit avec
  `DRAVE_PUSH_TOT=1` comme témoin ;
* le reste du chargement (déquantification + reconstruction Q8, 7,4 s) est le prochain candidat
  mesuré — mais son remplacement (`--q4`, emprunt des blocs) **change la représentation**.
