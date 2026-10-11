# E6 — poids log-normaux : le variant est enfin MESURABLE, et il est très légèrement derrière le témoin

> Campagne : **biologie** · expérience : E6 (`docs/biologie-pour-drave.md`), poids tirés d'une
> log-normale (`w = signe · e^θ`, principe de Dale) au lieu d'une gaussienne
> Question : la biologie corticale a des efficacités synaptiques **log-normales** ; nos modèles
> sont quasi gaussiens ; une distribution multiplicative devrait être **élagable par
> construction**. Le variant vaut-il mieux ?
> Verdict : **on ne peut pas encore répondre à cette question — mais on peut enfin mesurer le
> variant.** M8 (le fichier sauvé ne reproduisait pas le modèle entraîné) est **corrigé** : le
> modèle log-normal passe de **436,6** de perplexité dans le moteur à **7,5666**, contre
> **7,3429** pour le témoin dense au même entraînement. À qualité d'entraînement égale, le variant
> est donc **+3,0 %** derrière — et l'élagabilité, qui est SA raison d'être, reste à mesurer.
> Date réelle : **2026-10-10 23 h 00 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py` (+ `--verifier-sauvegarde`) · export
> `tools/exporter_gguf.py` · moteur `drave --ppl` · porte : `tools/porte-sauvegarde-modele.sh`.

## 1. Ce qui bloquait, et ce qui est corrigé

Le variant était **inutilisable** : le fichier sauvé ne reproduisait pas le modèle entraîné
(perplexité **436,6** au lieu de ~5,6). La cause est trouvée et corrigée — elle n'était ni dans les
poids, ni dans la quantification, ni dans le moteur : `tie_word_embeddings` fait que
`lm_head.weight` **est** `model.embed_tokens.weight`, et reparamétrer la tête **cassait ce
partage** (la table d'entrée restait figée pendant l'entraînement, puis recevait les poids de la
tête à la matérialisation). Détail et preuves : [`rapport-m8-log-normal.md`](rapport-m8-log-normal.md)
§ 3 ter. Les poids **partagés** sont désormais exclus de la reparamétrisation, et une vérification
recalcule la **même** perte de validation à **quatre moments** (boucle, restauration,
matérialisation, disque) : les quatre coïncident.

## 2. La mesure, après correctif

Même protocole des deux côtés (`--famille route --dim 192 --couches 4 --tetes 4 --cache 768
--experts 8 --k 2 --seq 128 --lot 32 --pas 3000 --lr 3e-4 --graine 1`), même corpus, même export
(Q8_0 pour les tenseurs ordinaires, Q4_0 pour les experts), même texte d'évaluation.

| | val (bits/octet) | perplexité PyTorch, poids relus | export simulé | **moteur** |
|---|---:|---:|---:|---:|
| **dense** (témoin) | 2,3533 | 7,1504 | 7,3429 | **7,3429** |
| **log-normal** | 2,4874 | 7,2712 | 7,5666 | **7,5666** |

- le **moteur reproduit au chiffre près** l'export simulé en PyTorch (7,3429 = 7,3429 et
  7,5666 = 7,5666) : la chaîne entraînement → export → moteur est vérifiée de bout en bout ;
- le variant log-normal est **+3,0 %** de perplexité derrière le témoin dans le moteur, et sa
  validation d'entraînement est **+5,7 %** derrière (2,4874 contre 2,3533 bits/octet) : il apprend
  un peu moins bien, ce qui n'est pas la question posée ;
- l'écart de **×1,44** qui figurait dans la fiche M8 entre la validation du harnais (5,11 de
  perplexité) et le moteur (7,34) n'était **pas un défaut** : ce sont **deux dispositifs** (8 lots
  de 32 × 128 jetons sur 32 ko contre un seul contexte de 512 jetons en tête de fichier), et
  PyTorch reproduit exactement chacun des deux.

## 3. Ce que cette fiche ne dit PAS — et c'est la question d'E6

**L'élagabilité n'est pas mesurée ici.** C'est pourtant la raison d'être du variant : une
distribution log-normale doit survivre à l'élagage là où une gaussienne s'effondre à 25 % de poids
gardés. La suite est donc : entraîner les deux variants, les **élaguer** aux mêmes taux (50 %, 25 %)
avec la règle exacte du moteur (`prune_rows`, par ligne de sortie), et comparer les perplexités.
Le variant est maintenant **mesurable**, donc la question redevient posable — c'est tout ce que ce
verdict affirme.

**Et une limite de protocole** : une seule échelle (7,58 M paramètres), un seul taux
d'apprentissage, une seule graine. Le « +3,0 % » du § 2 est un point, pas une courbe.
