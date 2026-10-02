# P0 — Le harnais de flux : compter ce qu'on paie, par provenance

**En une ligne** : les chemins **MLA** et **experts-IQ** annonçaient « 0
événement » alors qu'ils calculent des dizaines de milliards de produits par
jeton — le compteur manquait, pas le travail ; le moteur compte maintenant les
**paires** (poids × activation) par provenance (**attention / experts /
partagé**), et la première mesure dit une chose que la suite du plan doit
entendre : **sur ces deux chemins, le flux est dense** — 0 événement en listes,
la totalité des matrices est payée.

## 1. Ce qui était muet, et pourquoi

`events_total()` ne comptait que le chemin **push** de `matvec` : `Σ row_ev[i]`
sur les sources actives, c'est-à-dire les poids **non nuls** réellement
multipliés. Trois chemins ne passaient jamais par là :

| chemin | ce qu'il fait | ce qu'il comptait |
|---|---|---|
| MLA (`attn_mla`) | projections de rang faible en **f32 plein** (`matvec_f32`) | rien — aucune liste n'est construite |
| experts **IQ** (`Source::Dequant`) | **déquantification** du super-bloc puis produit f32 | rien |
| tête de sortie, FFN dense en mode pull | produit scalaire complet sur la ligne | rien (par conception : « pas d'événement » sur le dense) |

Un modèle MLA (GLM-5.3, Kimi-K2.7) ou à experts IQ annonçait donc
« **0 événement** » — un chiffre faux, pas un chiffre nul. Et c'est le chiffre qui
sert à décider ce qu'on déporte, ce qu'on découpe et ce qu'on simplifie.

## 2. La mesure ajoutée : les **paires**, par provenance

Une **paire** est un (poids, activation) effectivement multiplié — ce qui est
**payé**. Elle se distingue de l'**événement**, qui est la paire dont le poids
est non nul : sur un chemin en listes, les deux coïncident (on ne paie que les
poids non nuls, et l'identité est testée :
`list::tests_grille::une_paire_est_un_evenement_en_listes`) ; sur un chemin
dense, on paie la matrice entière.

`Model::paires: [u64; 3]` — 0 = attention, 1 = experts routés, 2 = partagé (FFN
dense, expert partagé, tête). Compté là où le travail se fait : `matvec` (toutes
branches : push, int8 dense, 4 bits, GPU), `matvec4_ou_iq` (déquantification IQ
et 4 bits), `attn_mla` (projections + remontées `k_b`/`v_b` + scores),
`logits` (la tête, toujours dense). Les scores MLA alimentent en plus
`attn_events`, comme le chemin dense, pour que les deux familles se comparent.

## 3. La vérification : le compte doit être juste, pas seulement non nul

| modèle | provenance | paires/token mesurées | calcul analytique |
|---|---|---|---|
| Qwen2.5-0.5B Q8_0 | attention | **44,2 M** | 24 couches × (896×896 + 896×128 + 896×128 + 896×896) = **44,04 M** ✅ |
| Qwen2.5-0.5B Q8_0 | partagé | **451,2 M** | 24 × 3×896×4864 = 313,7 M (FFN) + 896×151 936 = 136,1 M (tête) = 449,8 M ✅ (l'écart de 0,3 % est le jeton de tête non noté) |
| Qwen2.5-0.5B Q8_0 | experts | 0 | pas de MoE ✅ |

Et la porte du dépôt ne bouge pas : **Qwen2.5-0.5B ctx 256 = 19,3885**, la même
valeur qu'avant l'instrumentation — un compteur ne change pas un calcul, et
c'est ce qu'il fallait prouver.

Sur **GLM-5.3** (79 couches, MLA, 256 experts top-8, 216,7 Go), un jeton froid
donne :

| provenance | paires/token | part |
|---|---|---|
| attention (MLA) | **21,9 G** | 37,7 % |
| experts routés | **30,6 G** | 52,6 % |
| partagé | **5,6 G** | 9,7 % |
| **total** | **58,2 G** | 100 % |
| dont en **listes** | **0** | **0 %** |

## 4. Ce que cette mesure dit (et qui commande la suite)

1. **Le flux de ces deux chemins est dense.** 58 G paires payées, 0 événement :
   sur MLA et sur IQ, Drave ne conduit **aucune liste** aujourd'hui. La vision
   (« le coût suit l'activité ») n'est pas réalisée là — elle l'est sur les
   modèles dont les projections ont un noyau en listes. Le dire est le premier
   pas pour que P1–P6 changent quelque chose.
2. **Les experts dominent** (52,6 %) alors qu'ils sont **routés** : 8 experts sur
   256, soit 3 % du modèle — la sélection fonctionne, mais chaque expert
   sélectionné est payé **entier**, déquantifié en f32. C'est le poste où une
   forme en listes rapporterait le plus.
3. **L'attention MLA coûte 21,9 G paires pour 4 positions de contexte** : elle
   ne dépend pas de la taille du modèle mais de `nh × (kvl × qkn + vd × kvl)`,
   payé à **chaque** jeton. C'est structurel (le cache est latent, la remontée
   ne l'est pas).
4. **Un calcul mort dans la boucle de scores — trouvé, mesuré, supprimé.**
   `attn_mla` calculait la remontée `v_b` (`vd × kvl` par tête et par position)
   dans la boucle de scores… et la jetait : la variable `vv` n'était relue nulle
   part, la sortie refaisant le calcul. Supprimé (§4.bis), sans changer un
   chiffre — et le compteur le prouve.

## 4.bis Le compteur comme instrument : un delta prédit, un delta mesuré

Le calcul mort a été retiré, puis la même passe GLM-5.3 rejouée. Prédiction
**avant** la mesure, à partir des dimensions réelles des tenseurs
(`attn_k_b [64, 512, 192]`, `attn_v_b [64, 256, 512]`, `nh = 64`, 79 couches) :
le travail retiré vaut `vd × kvl` par (tête, position), soit **662,7 M paires**
par passe avant, et **1 988,1 M** pour la passe complète d'un jeton noté
(trois passes avant).

| | avant (avec le calcul mort) | après (calcul retiré) |
|---|---|---|
| perplexité | 14533,9920 | **14533,9920** — identique |
| paires d'attention / token | **29 224,8 M** | **27 236,7 M** |
| écart | — | **−1 988,1 M**, exactement la prédiction |
| total / token | 83 104,0 M | 81 115,9 M |

Trois choses sont établies par ce tableau : le compteur suit le code **au
millier de millions près** (le delta prédit est le delta mesuré), la suppression
**ne change aucun chiffre** (même perplexité), et le travail retiré n'était pas
une hypothèse — il était payé.

**Ce que le chronomètre ne dit pas** : la seconde passe était **chaude**
(41,8 s contre 215,7 s pour la première, page cache), donc comparer
« attention 14 024 ms → 12 256 ms » serait malhonnête — c'est le compteur, pas
l'horloge, qui mesure ici. Le gain attendu est de l'ordre de 1 % du temps d'un
jeton sur ce chemin, sous le bruit d'une passe froide.

## 5. Portes de la phase

| porte du plan | état |
|---|---|
| `--config` annonce la bonne liste de manques | ✅ **franchie** — elle ne l'était pas : `attn_sinks` était compté comme un manque V4, donc gpt-oss répondait « calculable : NON » alors que sa porte (15,6017) tourne. Corrigé, et la porte est désormais **exécutée par `tools/portes.sh`** |
| les deux côtés produisent les mêmes tenseurs nommés | ✅ `ref_logits --tensors` (llama.cpp) et `DRAVE_DEBUG_MLA` / `DRAVE_DEBUG_ETAT` existent et ont servi à la validation MLA (corrélation 0,999024) |
| **un jeton affiche un flux non nul avec sa provenance et son coût** | ⚠️ **franchie sur GLM-5.3, pas encore sur V4-Flash** : le forward de V4-Flash est refusé (hyper-connexions, sortie à rang faible) — c'est P1/P2. GLM-5.3 exerce **les deux mêmes chemins** (MLA à rang faible + experts IQ), c'est donc lui qui porte la preuve aujourd'hui |

## 6. Réserves de méthode

- Les chiffres GLM-5.3 viennent d'un **jeton froid** (216,7 Go lus depuis le
  disque mécanique, 190 s de chargement, 147 s/jeton) : ils mesurent un **flux**,
  pas une performance. Aucun débit n'est publié ici.
- L'A/B du calcul mort de `v_b` est **fait** (§4.bis) — et il est concluant sur
  le **travail** (delta prédit = delta mesuré), pas sur le **temps** (seconde
  passe chaude, donc incomparable).
- Le compteur de paires du chemin `forward_lot` (préremplissage par lots) est
  branché sur les projections q/k/v ; le reste du chemin par lots (experts,
  FFN, tête) n'est pas encore compté. Le total annoncé vaut donc pour le
  décodage jeton par jeton, qui est le régime des mesures ci-dessus.
