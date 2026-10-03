# Sprint 13 — Les deux énigmes du découpage V4.1 : la couture, et l'instrument

- **Début** : 21:00 · **Fin** : 23:00 (bloc de 120 min)
- **Objectif** : fermer les deux questions laissées ouvertes par le sprint 12 —
  (1) pourquoi un V4.1 découpé à la couche 20 donnait 514 722,06 contre 1 743
  713,62 de référence locale ; (2) pourquoi cette référence locale (1 743 713,62)
  n'était pas celle de `--ppl` (208 411,867) sur les mêmes jetons.
- **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.

## Le résultat

Les deux énigmes sont fermées, et **l'instrument n'était pas en cause** : il
mentait par omission — deux modes qui ne règlent pas la même quantification
d'activation, comparés comme s'ils la réglaient pareil. Le vrai défaut était dans
la couture, et il rendait le découpage V4.1 **faux et muet** à partir du deuxième
jeton.

| question | réponse |
|---|---|
| Pourquoi 514 722,06 au lieu de 1 743 713,62 ? | la `pre` reçue du pair pour le jeton *p* était encore en place au `forward` du jeton *p+1* : le nœud qui commence à la couche 0 amorçait sa chaîne retardée sur les coefficients de la **dernière FFN du pair au jeton précédent**. Mesuré par tenseur : **629 tenseurs divergents, tous aux positions 1 et 2, aucun à la position 0** |
| Pourquoi la référence du harnais n'était-elle pas celle de `--ppl` ? | les deux modes ne quantifient pas les activations pareil : `--ppl` prend **16 bits** (32 767 niveaux, sa référence de non-régression) et les modes flux **8 bits** (127 niveaux, `appliquer_quantification`). Preuve : `--ppl --abits 8` donne **1 743 713,6243** et ses **2 544 tenseurs sont identiques au bit près** à ceux du harnais |
| `--dense` était-il en cause ? | **non** : `--ppl --dense` et `--ppl` sont identiques au bit près (2 544 tenseurs, 0 différent) et donnent le même 208 411,8674 |
| Pourquoi le premier écart apparaît-il à la couche 0 si c'est la quantification ? | l'attention V4 est en **f32** (`matvec_f32`), non quantifiée : `attn_brut-0-*`, `q_norm-0-*`, `kv_rope-0-*` sont identiques entre 127 et 32 767 niveaux. Ce qui diverge d'abord, c'est `l_last-0-*` — le **MoE**, seul chemin quantifié à ce niveau |

## Le correctif

Deux endroits, parce que deux invariants différents étaient faux :

1. **`Model::forward`** ne consomme la `pre` reçue que si CE nœud reprend au
   milieu du modèle (`couche_debut > 0`) : lui seul a besoin d'un chaînon
   précédent pour son premier raccord, qui n'est pas celui du modèle. Un nœud qui
   commence à la couche 0 voit un jeton neuf entrer par l'embarquement : sa
   chaîne repart de la copie 0, comme la référence.
2. **`Model::norme_finale`** prend `&mut self` et **consomme** cette `pre` : elle
   appartient à la réduction de ce flux-là et à lui seul. La laisser en place,
   c'était se fier à ce que le prochain appel veuille bien ne pas la prendre.

La conjonction des deux rend le défaut impossible par construction, et pas
seulement absent.

## La vérification, par tenseur et pas par perplexité

| mesure | avant | après |
|---|---|---|
| V4.1 découpé à la couche 20, référence locale | 1 743 713,6243 | 1 743 713,6243 |
| V4.1 découpé, deux nœuds | **514 722,0611** | **1 743 713,6243** |
| écart | 7,05e-01 | **0,00e0** |
| tenseurs du pilote (couches 0-19, positions 0-3) contre la référence | 629 différents, tous aux positions 1 et 2 | **0 sur 2 544** |
| tenseurs du nœud moteur (couches 20-39) contre la passe complète | — | **0 sur 945** |

Le dernier point est celui qui compte : les 20 couches locales, le transport
aller, les 20 couches distantes, le pré-mix au retour et la réduction finale
donnent, ensemble, **le même état au bit près** qu'une passe complète à un seul
nœud. Le flux aller fait 82 016 octets (79 d'en-tête + 1 de compte + 16 de
pré-mix + 20 480 canaux f32), le retour 81 999.

## Pourquoi le V4-Flash ne le voyait pas

Sa réduction finale est **apprise** (`output_hc_*`) : il n'a pas de chaîne
retardée, donc `hc_porte_imposee` n'est jamais posé chez lui (`np = 0` sur le
fil) et le défaut ne pouvait pas s'exprimer. C'est exactement ce qui a rendu
l'énigme longue : le même harnais, le même découpage, un écart **0,00e0** sur
V4-Flash et 7,05e-1 sur V4.1. Le modèle qui échouait était le seul dont la
réduction finale dépend d'un état porté par le fil.

## Le deuxième correctif : les modes 3 et 4 n'écrivaient pas le préfixe v6

Le protocole v6 a ajouté un octet `np` (compte de pré-mix) en tête de **corps**.
Le chemin « un jeton » (modes 0-2) l'écrivait ; les deux émetteurs de **lots**
(modes 3 et 4) non — le décodeur du pair lisait donc le premier octet du premier
état comme un compte, et tout le reste était décalé de quatre octets. Un mode
entier, faux et muet.

Un seul encodeur désormais (`prefixe_premix`), utilisé par les trois émetteurs,
avec l'invariant qui manquait : **une `pre` appartient à UN état**, donc un flux
de plus d'un état n'en porte pas.

Mesuré, deux nœuds sur Qwen2.5-0.5B Q8_0 (24 jetons, `--lot 4`) :

| mode | écart |
|---|---|
| 3 — lot dense f32 | **0,00e0** |
| 4 — lot en listes | 4,45e-3 |
| 2 — un jeton en listes, pour comparaison | 3,65e-2 |

Le mode 4 n'est pas exact, et ne peut pas l'être : il encode chaque état avec le
codec quantifié du mode 2 (les mêmes 4 à 8 octets par actif). Son écart est
**plus petit** que celui du mode 2 sur le même modèle, ce qui est le sens
attendu — et c'est ce qui distingue « quantifié » de « mal lu ».

## Les hypothèses tuées en chemin (et par quoi)

| hypothèse | ce qui la tue |
|---|---|
| l'état résiduel laissé par la passe de référence du harnais | la position 0 est **exacte au bit près** : un état résiduel l'aurait touchée aussi |
| le transport, ou le pré-mix sur le fil | les 945 tenseurs du nœud moteur (couches 20-39) sont identiques à la passe complète |
| `--dense` (chargement dense des projections) | `--ppl --dense` = `--ppl`, 2 544 tenseurs identiques |
| le cache compressé partagé / le compresseur | les couches 0 et 1 n'ont pas de compresseur (les sources sont 2, 8, 14, 20) et la divergence commence à la couche 0 |
| l'engram | il est aux couches 1 et 14, et la divergence à la position 0 est nulle alors que l'engram s'y exerce aussi |
| un décalage de jetons (`--ids` tronqué) | les deux passes utilisent les mêmes quatre jetons (`270,15301,6605,223`) et la position 0 est identique |

## Ce que la relecture adverse avait raison de soupçonner

Le sprint 12 concluait : « l'instrument qui mesure l'écart est suspect, pas
(encore) le découpage ». C'était **à moitié faux** : l'instrument était exact, et
c'est la comparaison entre deux modes réglés différemment qui ne valait rien.
La leçon est dans le code, pas seulement ici : `run_ppl_reparti` imprime sa
quantification, `--ppl` imprime la sienne quand `--options-actives` est demandé —
et le chiffre de 16 bits n'apparaît nulle part sans lui. La prochaine fois, la
comparaison portera le réglage à côté du chiffre.

## Portes

- `tools/portes.sh rapide` : **toutes vertes** — 62 tests, Qwen2.5-0.5B ctx 256 =
  19,3885, clusters Qwen3-30B = 799,8557, threads 20, les quatre routages,
  **V4-Flash 43 couches ctx 32 = 8430,4966**, engram V4.1 (rangées distinctes).
- **Porte NOUVELLE : `tools/porte-flux.sh`**, branchée dans `tools/portes.sh`.
  Deux nœuds, cinq modes de flux, Qwen2.5-0.5B, ~20 s — mesuré :

  | mode | écart | plafond de la porte |
  |---|---|---|
  | 0 — f32 dense | 0,00e0 | 0 |
  | 1 — listes quantifiées | 0,00e0 | 0 |
  | 2 — listes à échelle par bloc | 3,65e-2 | 5e-2 |
  | 3 — lot dense f32 | 0,00e0 | 0 |
  | 4 — lot en listes | 4,45e-3 | 5e-2 |

  C'est elle qui manquait : le défaut de la `pre` reçue a vécu jusqu'à ce qu'on
  compare des tenseurs à la main sur un modèle de 365 Go. Le nœud moteur servant
  **une seule connexion**, la porte en relance un par mode — un détail qui a
  coûté un premier essai (quatre modes sur cinq refusés par « connexion
  refusée », et le message du serveur le disait : « 23 flux servis · arrêt »).
- `cargo build --release` : 43 avertissements (aucun nouveau).

## Ce qui reste, nommé

- **La porte V4-Flash** est repassée verte (8430,4966) avec le correctif YaRN :
  c'était la dernière valeur publiée à revérifier après le 03/10.
- **Le pré-mix est désormais couvert** par `tools/porte-flux.sh` (modes 0 à 4 sur
  deux nœuds réels) — mais **pas** par un test sur V4.1, qui coûte 4 minutes et
  365 Go : la porte rapide attrape la *classe* de défaut, pas le modèle.
- La **sélection à deux niveaux** de l'indexeur reste non portée (refusée au bon
  seuil).
- Le **masque des jetons d'image** de l'engram reste un no-op (texte seulement).
