# E6 — poids log-normaux : l'hypothèse est RÉFUTÉE, et le témoin dit pourquoi ce n'est pas un artefact

> Campagne : **biologie** · expérience : E6 (`docs/biologie-pour-drave.md`), poids tirés d'une
> log-normale (`w = signe · e^θ`, principe de Dale) au lieu d'une gaussienne
> Question : la biologie corticale a des efficacités synaptiques **log-normales** ; nos modèles
> sont quasi gaussiens ; une distribution **multiplicative** devrait donc être **élagable par
> construction** — c'est SA raison d'être. Le variant vaut-il mieux **sous élagage** ?
> Verdict : **NON — et de loin.** À 50 % de poids gardés, le témoin dense passe de **7,3429** à
> **7,5680** (+3,1 %) quand le log-normal passe de **7,5666** à **13,0622** (**+72,6 %**). À 25 % :
> **9,0164** (+22,8 %) contre **17,5009** (**+131 %**). L'hypothèse est **renversée** : le variant
> log-normal n'est pas plus élagable, il l'est **beaucoup moins**.
> Date réelle : **2026-10-10 23 h 38 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py` (`--elagage`, `--plancher-elagage`) · export
> `tools/exporter_gguf.py` · moteur `drave --ppl`.

## 1. Ce qui bloquait, et ce qui a été corrigé avant de mesurer

Le variant était **inutilisable** : le fichier sauvé ne reproduisait pas le modèle entraîné
(perplexité **436,6** au lieu de ~7,6). Cause trouvée et corrigée — `tie_word_embeddings` fait que
`lm_head.weight` **est** `model.embed_tokens.weight`, et reparamétrer la tête cassait ce partage
([`rapport-m8-log-normal.md`](rapport-m8-log-normal.md) § 3 ter). **Deux autres défauts de la même
famille** ont été trouvés en préparant cette mesure, et corrigés :

1. **écrire dans un poids reparamétré n'écrivait rien** : `mod.weight` est une valeur *calculée*,
   donc `mod.weight.mul_(...)` remplissait un temporaire — l'élagage d'un modèle log-normal ne
   faisait **rien**, en silence. Tout passe par `ecrire_poids`, qui écrit dans le paramètre et
   **vérifie** l'effet ;
2. **l'élagage ne couvrait que 5,8 % du modèle** : il ne parcourait que les `nn.Linear`
   (442 368 poids sur 7 575 552). Les experts fusionnés de `Qwen3MoeExperts` — 83 % des poids — et
   le routeur n'étaient **jamais** élagués. La règle du moteur (`Proj::load` → `prune_rows`)
   s'applique maintenant à **tout tenseur ≥ 2D sauf la table d'entrée**, et la couverture est
   **annoncée** :

```
# élagage à 50% gardé : 28 tenseurs · 7 526 400 poids sur 7 526 400 (100.0 % des poids de projection)
```

*Les deux premiers chiffres d'E6, mesurés avant ces corrections (dense **7,3028** contre log-normal
**7,5372** à 50 %), sont **périmés** : ils portaient sur 5,8 % des poids et un élagage inopérant sur
le variant. Ils restent ici pour mémoire, comme le veut la règle du dépôt — à côté, jamais à la
place.*

## 2. La mesure, à couverture complète

Même entraînement des deux côtés (`--dim 192 --couches 4 --tetes 4 --experts 8 --k 2 --pas 3000
--lr 3e-4 --graine 1`), mêmes 28 tenseurs élagués, même export, même texte.

| poids gardés | témoin dense | log-normal | écart |
|---|---:|---:|---:|
| 100 % (aucun élagage) | **7,3429** | **7,5666** | +3,0 % |
| 50 % | **7,5680** (+3,1 %) | **13,0622** (+72,6 %) | **+72,6 %** |
| 25 % | **9,0164** (+22,8 %) | **17,5009** (+131 %) | **+94 %** |

**L'hypothèse biologique est réfutée** : à budget de poids égal, le modèle à poids log-normaux
perd **beaucoup plus** de qualité que le modèle gaussien. La distribution multiplicative n'est pas
un avantage pour l'élagage — dans cette implémentation, c'est un handicap.

## 3. Le témoin, et pourquoi il était nécessaire

Un poids log-normal **ne peut pas être nul** : `|w| = e^θ ≥ e^−12 = 6,1e-6`. Un poids « élagué »
n'est donc pas annulé, il est **écrasé à 6,1e-6** — et il continue de contribuer. Le harnais le
compte et l'annonce (`221 184 poids NON représentables` à 50 %). Sans témoin, on aurait pu accuser
la **distribution** alors que la cause serait le **plancher**.

Le témoin sépare les deux : le **même élagage** sur le **témoin dense**, mais avec un **plancher**
de 6,1e-6 au lieu de zéro (signe conservé).

| poids gardés | dense, zéros exacts | **dense, plancher 6,1e-6** | log-normal (plancher subi) |
|---|---:|---:|---:|
| 50 % | 7,5680 | **7,5434** | 13,0622 |
| 25 % | 9,0164 | **8,9254** | 17,5009 |

**Le plancher n'est pas la cause** : le dense avec plancher dégrade *moins* que le dense avec des
zéros exacts (7,5434 contre 7,5680, et 8,9254 contre 9,0164). C'est la **distribution
log-normale** qui rend le modèle fragile à l'élagage, pas l'impossibilité d'atteindre zéro.
Le témoin ne sauve pas le variant — il rend la réfutation **propre**.

## 4. Ce que cette fiche NE dit PAS

- **elle ne dit pas que la biologie a tort** : elle dit qu'**une** façon de paramétrer des poids
  log-normaux (`w = signe · e^θ` avec signes figés et θ borné) échoue à l'élagage. Une autre
  paramétrisation (θ non borné, magnitudes renormalisées par ligne, seuil appris) n'est pas testée ;
- **elle ne sépare pas les deux rôles du variant** : les signes figés (Dale) sont peut-être la
  vraie cause de la fragilité, pas la loi log-normale. Le test qui trancherait : un modèle
  log-normal à **signes libres**, élagué au même taux ;
- **une seule échelle, une seule graine, un seul corpus** : le « +72,6 % » est un point ;
- **elle ne dit rien des PAIRES, et c'est un résultat en soi** : sur un GGUF dense, **aucun** chemin
  d'exécution ne voit l'élagage dans le compte de paires. Mesuré sur le témoin dense, élagué à 50 %
  de **tous** ses tenseurs de projection :

  | chemin | non élagué | élagué à 50 % |
  |---|---:|---:|
  | `--flux` (f32 dense) | 2,3 M | **2,3 M** |
  | `--flux-listes` | 2,3 M | **2,3 M** |
  | `--lot 4 --flux-blocs` | 2,2 M | **2,2 M** |
  | `--keep 0.5` du moteur lui-même | 2,3 M | **2,3 M** (perplexité 4,56 → 5,82) |

  La raison est dans le code : `self.paires[0] += (d8.n_in as u64) * (d8.n_out as u64) * t as u64`
  (et `*paires += (q.n_in as u64) * (q.n_out as u64)` dans `matvec`). Le compteur mesure le travail
  d'un noyau **dense** — `n_in × n_out` quelle que soit la densité — ce qui est **fidèle** à ce que
  le moteur fait vraiment, et **muet** sur ce qui est stocké.

  Le harnais d'entraînement n'est pas mieux loti : sa ligne de coût est **la même pour les huit
  modèles** entraînés ici (dense et log-normal, à 100 %, 50 % et 25 % de poids gardés, avec et sans
  plancher) — `0,59 M poids LUS par jeton et par couche · 1,92 M stockés`. Elle décrit
  l'**architecture**, pas l'occupation.

  **Conclusion de méthode** : aujourd'hui, **aucun instrument du dépôt ne voit la sparsité des
  poids dans un chiffre de coût**. Tout « ÷N de paires » doit donc **nommer son instrument**, et
  les chiffres du dessin B (`docs/modele-pour-drave.md` § 3 B : « ÷7,9 ») viennent d'un comptage qui
  n'est plus reproduit par le code actuel — c'est écrit à côté d'eux, et c'est le manque **M9**.
