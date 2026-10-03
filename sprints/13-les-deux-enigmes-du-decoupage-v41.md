# Sprint 13 — Les deux énigmes du découpage V4.1 : la couture, et l'instrument

- **Début** : 20:35 · **Fin** : 21:20 (45 min utiles — l'enquête était ouverte à la
  fin du bloc 12 ; les heures sont celles des commits, pas une estimation)
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
seulement absent — à trois conditions que la relecture adverse a fait ajouter : le
`take()` est en **tête** de `norme_finale` (et non dans une seule branche), un nœud
moteur qui reprend à `debut = 0` avec une `pre` reçue est **refusé** au lieu de
l'ignorer, et le chemin des LOTS **refuse** une `pre` reçue (il ne saurait pas
l'appliquer).

## La vérification, par tenseur et pas par perplexité

| mesure | avant | après |
|---|---|---|
| V4.1 découpé à la couche 20, référence locale | 1 743 713,6243 | 1 743 713,6243 |
| V4.1 découpé, deux nœuds | **514 722,0611** | **1 743 713,6243** |
| écart | 7,05e-01 | **0,00e0** |
| tenseurs de la passe RÉPARTIE du pilote (couches 0-19, positions 0-2, **953** fichiers) | 629 différents, tous aux positions 1 et 2 | **0 sur 953** |
| tenseurs du nœud moteur (couches 20-39, positions 0-2, 945 fichiers) | — | **0 sur 945** |
| tenseurs de la passe de RÉFÉRENCE du pilote contre un autre processus (1 591 fichiers) | — | **0 sur 1 591** |

Le troisième point est celui qui compte : les 20 couches locales, le transport
aller, les 20 couches distantes, le pré-mix au retour et la réduction finale
donnent, ensemble, **le même état au bit près** qu'une passe complète à un seul
nœud.

**Pourquoi 953 et pas 2 544** (correction de la relecture adverse) : `--ppl-reparti`
écrit **deux** passes dans le même `DRAVE_DUMP_COUCHES` — la référence locale
(toutes les couches, toutes les positions) puis la passe répartie, qui écrase les
mêmes noms pour les couches 0-19 aux positions 0-2 (le dernier jeton n'est pas
envoyé : il n'a rien à prédire). Sur les 2 544 fichiers, **1 591 sont donc la
passe de référence du pilote**, et seuls 953 peuvent échouer sur la couture. La
version initiale de ce sprint annonçait « 0 sur 2 544 » : le verdict était juste,
le chiffre ne l'était pas — 62 % de ce qui était publié ne pouvait pas échouer.
Le sous-ensemble est séparé par les dates de modification (au-delà du dernier vide
de la passe de référence).

Le flux aller fait **82 016 octets** (79 d'en-tête + 1 de compte + 16 de pré-mix +
20 480 canaux f32), le retour **82 016** aussi. Le chiffre de 81 999 publié
initialement venait d'un compteur qui n'incluait pas le préfixe de corps côté
réception (17 octets) : corrigé, et remesuré (voir la revue adverse).

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
état comme un compte de pré-mix, et le corps entier se décalait de **1 + 4·np**
octets.

**Ce que ça faisait exactement** (mesuré par la relecture adverse, qui a rejoué
une trame d'avant correctif contre un vrai nœud moteur) : le premier octet d'un
état f32 est presque toujours non nul, donc le décodeur attendait `np × hc × 4`
octets qui ne venaient pas et **restait bloqué dans `read_exact`** — sans délai de
lecture en production, c'est un **interblocage**, pas un chiffre faux, et le nœud
ne se plaint qu'à la fermeture du client (« 0 flux servis »). Si ce premier octet
avait valu zéro, le corps aurait été lu **décalé d'un octet**, silencieusement
faux. Les deux issues étaient mauvaises ; la formulation « faux et muet » de la
première version de ce sprint était trop vague.

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

## La relecture adverse du bloc (et ce qu'elle a corrigé)

Une relecture adverse en lecture seule (aucune modification du dépôt) a repris le
commit `ac80e7e` pièce par pièce : elle a recalculé les comparaisons de tenseurs,
rejoué une trame d'avant correctif contre un vrai nœud moteur, exercé la porte
neuve et démoli trois affirmations publiées. Son verdict sur le fond : le
diagnostic et le correctif tiennent ; ce qui ne tenait pas, c'était la comptabilité.

| trouvaille | gravité | correctif |
|---|---|---|
| « tenseurs du pilote : 0 sur 2 544 » : 1 591 de ces fichiers viennent de la **passe de référence** du pilote (mêmes noms écrasés), seuls 953 peuvent échouer sur la couture | **faux** (chiffre) | chiffres corrigés partout (953 + 945 + 1 591, séparés par les dates de modification) ; le verdict était juste |
| « mode entier, faux et muet » / « décalé de quatre octets » : en réalité le pair **bloque dans `read_exact`** (aucun délai de lecture en production), et le décalage vaut `1 + 4·np` octets | **faux** (formulation) | reformulé dans `docs/format-flux.md`, ici et dans le rapport, avec les deux issues possibles |
| « 81 999 au retour » : le compteur des octets REÇUS n'incluait pas le préfixe de corps (17 octets), alors que l'émission le compte | **faux** (chiffre) | compteur corrigé aux quatre sites de décodage + test mis à jour ; remesuré : **82 016 / 82 016** |
| `portes.sh` ne lisait que « ❌ » et ignorait le code retour de la porte : un modèle absent rendait « toutes les portes sont vertes » | trou | code retour lu, sortie vide traitée comme un échec (démontré avant/après) |
| aucun délai sur le pilote dans la porte : un interblocage (le défaut ci-dessus) l'aurait laissée tourner jusqu'au `timeout` externe | trou | `timeout 180` sur le pilote, code retour vérifié |
| `norme_finale` ne `take()` que dans la branche `hc_retarde` : deux chemins laissaient la `pre` en place | trou | `take()` en **tête** de fonction (la conjonction des invariants devient structurelle) |
| un nœud moteur qui reprend à `debut = 0` avec une `pre` reçue l'ignorait en silence | trou | trame **refusée** en le disant |
| le chemin des LOTS n'applique jamais la `pre` reçue et ne la refuse pas non plus | trou | refus explicite |
| plafond du mode 4 à 11× le mesuré, et identique à celui du mode 2 : ne distinguait pas « correct » de « dégradé » | faible | plafonds resserrés (6e-2 / 1e-2) **et** contrôle « mode 4 ≤ mode 2 » (même codec) |
| « réduction finale comprise » dans les tenseurs : la sortie de `norme_finale` n'est jamais vidée ; seule l'égalité de perplexité la couvre | faible | affirmation corrigée (voir plus bas) |
| la recette du digeste écrivait `--ppl` sans `--abits 8`, donc ne reproduisait pas sa propre référence | faible | recette corrigée, avec la provenance réelle de la référence (port mort) |
| `np = 1` n'est exercé par **aucun** test : le décodeur des tests écrit `np = 0` en dur, la porte tourne sans hyper-connexions | trou (assumé) | écrit dans « ce qui reste » : le pré-mix n'est couvert que par un run V4.1 manuel de 4 minutes |
| chemins `/tmp` partagés et port tiré au hasard dans la porte : deux exécutions pouvaient se tronquer le journal | trou | répertoire `mktemp -d` par exécution |

**Ce qu'elle n'a pas pu casser** : le diagnostic de la fuite (629 → 0, 7,05e-1 →
0,00e0), l'encodage v6 des cinq modes (encodeur ↔ décodeur), l'absence d'autre
écrivain ou lecteur de `hc_porte_imposee`, les 62 tests de l'époque (63 depuis
l'ajout du test `np = 1` au bloc 14), et le `trap` de la porte
(son soupçon initial). Elle a aussi produit une mesure que je n'avais pas faite et
que j'ai revérifiée : l'`etat_impose` du nœud moteur est **identique au bit près**
au `l_last-19` du pilote — le transport aller est exact octet par octet,
indépendamment de la perplexité.

**Ce que la réduction finale a vraiment comme preuve** (correction de la
formulation initiale) : les 953 + 945 tenseurs couvrent les 40 couches et le
transport, mais **aucun vide ne porte la sortie de `norme_finale`** — la réduction
finale n'est établie que par l'égalité de perplexité (1 743 713,6243 des deux
côtés). C'est une preuve plus faible qu'un tenseur, et elle est dite ici plutôt que
sous-entendue.

## Ce que la relecture adverse avait raison de soupçonner

Le sprint 12 concluait : « l'instrument qui mesure l'écart est suspect, pas
(encore) le découpage ». C'était **à moitié faux** : l'instrument était exact, et
c'est la comparaison entre deux modes réglés différemment qui ne valait rien.
La leçon est dans le code, pas seulement ici : `run_ppl_reparti` imprime sa
quantification, `--ppl` imprime la sienne quand `--options-actives` est demandé —
et le chiffre de 16 bits n'apparaît nulle part sans lui. La prochaine fois, la
comparaison portera le réglage à côté du chiffre.

## Retro — introspection (garder / changer / doute)

**Garder.**

- **Le tenseur plutôt que la perplexité.** Une perplexité sur trois prédictions à
  froid amplifie chaotiquement (1,8e-3 sur `l_last-0` devient 8,4× de
  perplexité) : comparer 2 544 fichiers en numpy a donné la réponse nette —
  position 0 exacte, positions 1 et 2 fausses — là où le scalaire ne disait que
  « c'est faux ».
- **La porte écrite dans le même bloc que le correctif.** Le défaut a vécu parce
  qu'aucun test n'exerçait un couple de nœuds ; la porte existe maintenant, et
  elle a coûté vingt minutes.

**Changer.**

- **Vérifier les réglages des deux choses comparées AVANT de chercher une
  divergence numérique.** J'ai dépensé trois runs de 4 minutes (365 Go) à traquer
  un état résiduel imaginaire, alors que `--ppl --abits 8` (2 min) tranchait. La
  question la moins chère était posée en dernier. Action du bloc suivant : quand
  deux passes donnent deux chiffres, la première ligne du protocole est « quels
  réglages ? » — et je le consigne dans le rapport avant de courir.
- **Un commentaire ne doit pas justifier un état.** Le bloc précédent portait
  « elle est lue par `norme_finale`, qui ne la consomme pas » : écrit comme une
  intention, c'était la description exacte du défaut, et cela l'a protégé de la
  relecture. Là où `take()` et `&mut self` suffisent, le commentaire est de trop.

**Doute.**

- Les **2 544 tenseurs identiques** prouvent la couture sur *ce* découpage (couche
  20), *ce* modèle et *quatre* jetons. Rien ne dit qu'un découpage à la couche 8
  ou 32, ou un contexte long, tiendrait : la porte rapide attrape la classe de
  défaut, pas le cas.
- Le `--ppl-reparti` compare **deux passes dans le même processus**, et la passe
  répartie **saute le dernier jeton** (par construction : il n'a rien à prédire).
  C'est correct, mais c'est une asymétrie que seule la lecture du code montre —
  un futur mode « deux processus » ne l'aurait pas.

## Planning du bloc suivant (14) — l'engram est-il vivant ?

Le plan P8 n'a plus qu'une question ouverte qui se mesure : l'**injection de
l'engram entre-t-elle vraiment dans le calcul** d'une passe complète ? On sait
qu'elle est branchée, vérifiée contre la référence numpy et **non nulle** dans la
passe complète (mesuré : `engram_sortie` couche 1 rms 0,058 à 0,235 ; couche 14
rms 0,53 à 0,73 sur 20 480 valeurs), mais aucun A/B ne l'établit.

1. `DRAVE_SANS_ENGRAM=1` — interrupteur de comparaison, déclaré dans `VARS_LUES`,
   **annoncé** quand il est actif (« le moteur calcule SANS l'engram : ce n'est
   pas V4.1 »).
2. A/B sur la perplexité V4.1 (ctx 8, ~55 s par passe) : le chiffre doit bouger ;
   et sur les vides : `engram_sortie` doit être exactement nul avec l'interrupteur,
   `l_last-1` et `l_last-14` doivent différer.
3. Décider du **masque des jetons d'image** (`dead_mask = image_sentinel_mask`) :
   le porter ou l'écrire comme sans objet en texte seul, avec sa condition de
   réouverture (un modèle multimodal).

## Portes

- `tools/portes.sh rapide` : **toutes vertes** — 62 tests au moment du bloc (63
  après le test `np = 1` ajouté au bloc 14), Qwen2.5-0.5B ctx 256 =
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
