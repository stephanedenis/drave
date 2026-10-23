# Spécification — mode 4 : le **lot en listes** (protocole v5)

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> **État : ÉCRIT, mesuré et relu** (voir `reports/rapport-mode4-lot-listes.md`) — ce plan
> reste la référence de conception, et les écarts constatés à la mise en œuvre sont
> consignés dans ce rapport (version 5, borne des actifs, garde cumulatif).
> **L'implémentation est faite** : `--lot > 1 --flux-blocs` produit le mode 4
> (`drave-core/src/main.rs`, `envoyer_lot_listes`). Le corps de spécification
> ci-dessous est conservé tel quel — c'est le document de conception, pas un
> reste-à-faire. Il suppose connus
> `docs/format-flux.md` (protocole **v5**, modes 0–**4**) et `docs/plan-prefill-reparti.md`
> (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
> l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
> `MODE_LOT = 3` — la version est passée à 5 depuis).

**En une ligne** : le mode 3 transporte `t` états en f32 dense — 3 589 octets par
jeton à `t = 16` pour Qwen2.5-0.5B ; le mode 4 transporte **les mêmes `t` états
encodés en listes à échelle par bloc de 32 canaux**, soit ≈ 1 530 octets par état
au seuil 0,01, **÷2,3 sur le fil**, au prix exact que le mode 2 paie déjà
(2,7e-2 d'écart à 256 jetons, 1,3e-2 à 1 024). Le mode 4 ne touche ni au calcul,
ni au cache KV, ni à la norme finale : il s'arrête au transport — le flux
transporté est aussi le journal que relisent les outils d'analyse
(`docs/vision.md` §2).

## 0. Décisions d'architecture (à ne pas rediscuter)

| question | décision | pourquoi |
|---|---|---|
| nouveau mode ou nouveau champ ? | **mode 4** (`MODE_LOT_LISTES`), en-tête **inchangé** (79 octets) | le corps est variable par construction (chaque état a son nombre d'actifs) ; `n` (offset 18) porte déjà le nombre d'ÉTATS, comme en mode 3 |
| quel encodage dans le lot ? | **listes à échelle par bloc de 32, valeurs i8 — le mode 2, tel quel** | c'est le mode qui gagne en régime creux (mesuré : ÷2,3 sur le fil ; à sparsité égale, 22× plus fidèle que l'i16 à 60 % d'activité) ; un lot i16 serait un second encodage à maintenir pour rien |
| la version change ? | **oui, 4 → 5** | dans `recevoir_flux`, un mode inconnu n'est refusé qu'APRÈS la lecture de `n × 4` octets (repli `_ => {}` puis `autre => Err`) : un pair v4 lirait `4·t` octets d'un corps qui en fait ≈ 1 500·t, se désynchroniserait, puis dirait « mode inconnu » — exact, tardif, muet sur la cause |
| l'encodage des paires ? | **`encoder_paires_blocs` / `decoder_paires_blocs`, appelés tels quels** | ce couple a déjà été désaccordé une fois (quatre octets écrits, deux lus, invisible tant qu'aucun écart n'atteint 255) : on ne l'ouvre pas, on l'appelle |
| la dimension voyage ? | non, et `n_blocs_j` doit valoir **exactement** ⌈hidden/32⌉ | garde nouvelle : deux GGUF différents sont refusés **au premier état**, au lieu de se voir au flux suivant sous forme de « magie absente » |
| où est l'échelle ? | **une par état, dans l'état** (§2) | la dynamique d'un résidu change à chaque jeton ; un tableau partagé ferait dépendre les états l'un de l'autre |
| la représentation en mémoire ? | **celle du mode 3** : `ChargeFlux::Lot(Vec<f32>)` | `plat()`, `emb_imposee_lot`, `forward_lot(&vec![0;t], pos)`, le cache KV, `flux_brut` et la norme finale fonctionnent déjà : le mode 4 ne change QUE les octets sur le fil |
| le décodage par lots ? | **hors sujet** | la génération reste séquentielle, un jeton par flux (mode 2). Le mode 4 sert au préremplissage, comme le mode 3 |

## 1. Le corps du message

### 1.1 En-tête : 79 octets, identique aux modes 0–3

| off | octets | champ | mode 4 |
|---|---|---|---|
| 0 | 4 | magie `0x44525631` | inchangée |
| 4 | 1 | version | **5** |
| 5 | 1 | mode | **4** |
| 6 | 4 | couche_debut | inchangé |
| 10 | 4 | couche_fin | inchangée (exclue) |
| 14 | 4 | position | **premier jeton du lot** (positions contiguës) |
| 18 | 4 | `n` | **nombre d'ÉTATS `t`** — pas le nombre d'actifs |
| 22 | 4 | échelle | **0** : sans objet (chaque état porte les siennes) |
| 26…38 | 13 | levels · thresh · topk · renorm | le contrat d'activation, appliqué par le récepteur |
| 39…78 | 40 | 7 top-k de projection · attn · q·k · moe | idem |

`TAILLE_TETE` ne bouge pas : les deux émetteurs gardent leur
`assert_eq!(tete.len(), TAILLE_TETE)`.

### 1.2 Corps : `t` états **auto-délimités** par un préfixe de 12 octets

```
corps = état 0 ‖ état 1 ‖ … ‖ état t−1        (dans l'ordre des positions)

état j, à partir de l'offset courant :
  +0              a_j         u32 LE   nombre de paires (canaux actifs) de l'état j
  +4              n_blocs_j   u32 LE   nombre d'échelles ; DOIT valoir ⌈hidden/32⌉
  +8              longueur_j  u32 LE   octets de paires (les échelles ne comptent pas)
  +12             n_blocs_j × f32 LE   échelle du bloc b = canaux 32b … 32b+31
  +12+4·n_blocs_j longueur_j × u8      paires, telles que les écrit `encoder_paires_blocs` :
                                       écart u8 · valeur i8, et 255 = échappement :
                                       écart u8=255 puis indice ABSOLU u16 LE puis valeur i8

taille de l'état j  = 12 + 4·n_blocs_j + longueur_j
taille du corps     = Σ_j (12 + 4·n_blocs_j + longueur_j)
taille du message   = 79 + taille du corps
```

L'ordre des champs est **délibérément** `a_j · n_blocs_j · longueur_j` avant les
données, et non `n_blocs_j · échelles · longueur_j · paires` comme l'esquisse de
`docs/plan-prefill-reparti.md` §7 : les trois tailles annoncées sont alors lisibles
d'un seul `read_exact` de 12 octets, **avant toute allocation**, et un état peut
être sauté sans lire son contenu. Le contenu lui-même (échelles puis paires) est
l'octet pour octet celui du mode 2. L'esquisse du plan n'est pas un contrat : elle
a été écrite avant que la règle R4 ne descende dans le code.

### 1.3 Règles du corps

* **R1** — `t = n ≥ 1`. Un lot d'un seul état est accepté en réception ;
  l'émetteur DOIT utiliser le mode 2 pour un jeton seul (le chemin séquentiel de
  la génération reste intact, octet pour octet).
* **R2** — positions contiguës `position .. position + t`; seule la base voyage.
* **R3** — la dimension ne voyage pas ; `n_blocs_j == hidden.div_ceil(32)` est
  **vérifié** à chaque état, et un écart est refusé en nommant la cause probable
  (deux GGUF de dimensions différentes). C'est plus strict que le mode 2, où
  `n_blocs` n'est qu'une borne ; c'est voulu, parce qu'un lot n'a pas de
  resynchronisation par jeton.
* **R4** — toute taille annoncée passe par `verifier_taille` avant l'allocation
  correspondante (§4) ; le cumul du corps aussi.
* **R5** — la réponse est encodée **comme la demande** : mode 4, même `t`, même
  `position`, même `couche_debut`/`couche_fin`, mêmes réglages.
* **R6** — le préfixe est la seule frontière d'état : il n'y a **pas** de
  sentinelle, pas de séparateur, pas de table de fin. Un état est exactement
  `12 + 4·n_blocs_j + longueur_j` octets.
* **R7** — `longueur_j` est la seule autorité pour la lecture socket, `a_j` la
  seule autorité pour le décodage. L'émetteur écrit `longueur_j = paires.len()`
  et ne dérive JAMAIS `longueur_j` de `a_j` (les échappements font que
  `longueur_j ≠ 2·a_j`). Contrôle gratuit et exact : `2·a_j ≤ longueur_j ≤ 4·a_j`.

### 1.4 Bilan d'octets (Qwen2.5-0.5B : hidden = 896, ⌈896/32⌉ = 28)

| envoi | formule | octets | par jeton |
|---|---|---|---|
| un jeton, mode 0 | `79 + 4·hidden` | 3 663 | 3 663 |
| un jeton, mode 2 (seuil 0,01, 78,6 % d'actifs) | `79 + 8 + 112 + 2a` | 1 607 | 1 607 |
| lot de `t`, mode 3 | `79 + 4·t·hidden` | `79 + 3 584t` | 3 589 à `t = 16` |
| **lot de `t`, mode 4** | `79 + t·(12 + 112) + 2·Σa_j` | ≈ `79 + 1 532t` | **≈ 1 537 à `t = 16`** |

**÷2,34** sur le fil à seuil 0,01, et le lot est même un peu moins cher que le
mode 2 par jeton : l'en-tête de 79 octets est amorti et le corps du mode 2
(8 octets de préfixe) est remplacé par 12 octets par état. À 1 024 jetons, où la
mesure du mode 2 donne 1 589 octets par flux, le mode 4 donne ≈ 1 554 par état
(≈ 1 560 par jeton à `t = 16`).
Les échelles coûtent 112 octets par état (4 × 28), soit ~7 % du message : elles
sont conservées telles quelles (§2).

## 2. Où vit l'échelle d'état — et pourquoi là

**Décision : à l'intérieur de l'état, à l'offset +12, une f32 par bloc de 32
canaux, exactement comme le mode 2.** Quatre raisons, dans l'ordre :

1. **Un seul codec, donc une seule classe de bug.** Le contenu de l'état j est le
   corps du mode 2 à l'octet près ; `flux_en_liste_blocs` (model.rs:3638) produit
   les échelles, `encoder_paires_blocs` produit les paires, `decoder_paires_blocs`
   les relit. Aucun nouvel encodage n'est introduit.
2. **La dynamique est par jeton.** `flux_en_liste_blocs` calcule une échelle par
   bloc à partir du maximum DU VECTEUR ; partager une table entre états
   reviendrait à quantifier des colonnes, pas des états, et ferait dépendre la
   précision d'un jeton de ses voisins du lot.
3. **L'état reste autonome.** Le lecteur valide, alloue, décode et déquantifie un
   état sans connaître les autres ; un état forgé ou corrompu ne peut pas
   contaminer les suivants, et le cumul (§4) est vérifiable état par état.
4. **Le coût est déjà payé et il est petit.** 112 octets sur ~1 530 (~7 %) ; les
   supprimer (une échelle globale par état) ferait retomber sur l'erreur absolue
   constante du mode 1, mesurée 22× moins fidèle en régime creux. Les passer en
   f16 ferait gagner 56 octets par état au prix d'un **nouvel** encodage
   d'échelle : refusé, ce n'est pas là qu'est le ÷2,3.

Alternatives écartées : table d'échelles partagée par le lot (perte
d'indépendance, gain ~112t octets) ; table en fin de message (interdit la
validation en flux et impose de relire le corps deux fois).

## 3. Compatibilité : le protocole passe en **version 5**

**Oui, il faut une version 5**, et c'est le critère 3.5 (« pas de silence, pas de
devinette ») qui l'impose. Ce qui se passerait sans elle :

* un pair **v4** lit l'en-tête, ne connaît pas le mode 4, tombe dans le repli
  `_ => {}` de `recevoir_flux`, lit `n × 4` octets (soit `4t` : quelques dizaines
  d'octets d'un corps qui en fait ~1 500 par état), puis répond
  `mode de flux inconnu : 4`. Le refus est exact mais **tardif** (le corps est
  déjà consommé, la connexion est désynchronisée) et **muet sur la cause** (ce
  n'est pas le mode qui manque, c'est la version).
* Avec la version 5 : le test de version est à l'offset 4, **avant tout octet de
  corps**. Un pair v4 refuse le message au premier échange avec le message déjà
  en place :

```
[flux] arrêt : flux en version 5, cette build parle la 5 (pair incompatible : rien n'a été interprété)
```

et un pair v5 recevant un flux v4 dit la réciproque. Les deux nœuds doivent être
reconstruits ensemble, comme la recette Colab l'impose déjà
(`docs/colab-reparti.md` : même commit des deux côtés).

**Règle à écrire dans le code** : un nouveau mode ⇒ une nouvelle version. Un mode
est un contrat de corps ; le champ version est le seul endroit d'où un refus peut
partir sans avoir rien interprété.

**Durcissement fait dans le même passage** (indépendant du mode 4, mais c'était
le même défaut) : dans `recevoir_flux`, un mode inconnu est désormais refusé
**juste après l'en-tête**, avant la lecture du corps. Un mode 7 forgé en v5 est
refusé sans qu'un seul
octet de corps soit lu, et le prochain mode ajouté héritera de la même sûreté.

## 4. Le garde-fou de taille (R4) : champs et ordre exact

`PLAFOND_FLUX` vaut 256 Mo et `verifier_taille` est la seule porte. En mode 4,
**l'en-tête ne borne plus le corps** : `t` états peuvent annoncer chacun une
taille licite et faire, ensemble, n'importe quoi. Il faut donc deux niveaux.

Ordre de réception, **aucune allocation avant la vérification qui la couvre** :

1. Lire les 79 octets d'en-tête ; magie ; **version == 5** (refus immédiat,
   nommé) ; **mode == 4** (refus immédiat si inconnu, cf. §3).
2. `t = n` (offset 18). Refuser `t == 0` (« lot de listes vide »).
3. `verifier_taille(t·hidden·4, "lot de {t} états × {hidden} canaux")` — calculé
   avec `checked_mul(...).unwrap_or(usize::MAX)`, exactement comme le mode 3
   (main.rs:1743). C'est **la** borne de la mémoire vivante : le lot décodé est
   un `Vec<f32>` de `t·hidden`, alloué une seule fois juste après.
4. Allouer le lot plat `vec![0f32; t·hidden]` (remis à zéro : un état sans actif
   doit valoir zéro, pas du hasard).
5. Pour chaque état `j` de `0..t`, lire le préfixe de 12 octets puis, dans cet
   ordre :
   * `verifier_taille(a_j · 2, "état {j} : {a_j} paires")` — avant tout `Vec`
     d'indices/valeurs ; `saturating_mul` (un `a_j` de 4 milliards ne doit pas
     boucler en silence). Le garde propre de `decoder_paires_blocs` reste en
     seconde ligne, mais c'est celui-ci qui nomme l'état.
   * `verifier_taille(n_blocs_j · 4, "état {j} : {n_blocs_j} blocs d'échelles")` —
     avant le tampon d'échelles.
   * `verifier_taille(longueur_j, "état {j} : {longueur_j} octets de paires")` —
     avant le tampon de paires.
   * **contrôles de cohérence, avant lecture** : `n_blocs_j == hidden.div_ceil(32)`
     (R3) et `2·a_j ≤ longueur_j ≤ 4·a_j` (R7) ; refus nommés.
   * **cumul** : `cumul += 12 + 4·n_blocs_j + longueur_j` puis
     `verifier_taille(cumul, "corps du lot en listes (cumul)")`. Sans lui, un pair
     peut annoncer `t × 256 Mo` de corps licites un par un : la mémoire resterait
     bornée (on décode état par état) mais le temps, non.
   * lire les `n_blocs_j × f32` puis les `longueur_j` octets, appeler
     `decoder_paires_blocs(&paires, a_j)`, déquantifier dans
     `lot[j·hidden .. (j+1)·hidden]`.
6. Déquantification : réutiliser **la garde du mode 2** (main.rs:1513-1525) —
   un indice ≥ hidden ou un bloc ≥ n_blocs_j est ignoré, compté, et le total est
   imprimé **une fois** en fin de message (une ligne par état ferait t lignes de
   bruit sur une trame forgée). Un indice hors dimension ne doit jamais être un
   `index out of bounds` : c'était un SIGABRT, déjà payé.
7. Le contrôle de contexte (`pos + t ≤ mdl.ctx`) reste dans la boucle serveur,
   sur la branche commune aux modes 3 et 4 : sans lui, `KvCache::assurer`
   (model.rs:1117 — noté 907 dans le plan du mode 3, l'arbre a bougé depuis)
   boucle indéfiniment.

Borne structurelle gratuite, à défaut d'un champ de longueur totale : un corps de
mode 4 **ne peut pas** dépasser `t · (4·hidden + 4·⌈hidden/32⌉ + 12)` — c'est le
cas où chaque paire échappe. Dès que le cumul la dépasse, la trame est forgée :
refuser sans lire l'état fautif.

## 5. Les deux côtés

### 5.1 Le pilote (`run_ppl_reparti`) — encoder N états

1. La référence locale ne change pas : `forward_lot(&ids[pos..pos+t], pos)` puis
   `logits_lot`, avec **le même découpage** que le chemin réparti.
2. Sélection du mode : `--lot > 1 && --flux-blocs` → **mode 4** ;
   `--lot > 1` seul → mode 3 dense (inchangé) ; `--flux-liste` (i16) reste
   **non défini** pour un lot : message nommé, et le lot part en mode 3 — pas de
   repli silencieux. Le message « mode 4 non écrit » a bien été remplacé par le
   branchement du mode 4 (`envoyer_lot_listes`).
3. Nouvelle fonction `envoyer_lot_listes(s, debut, fin, pos0, etats, t, mdl)` :
   en-tête de 79 octets (mode 4, `n = t`, échelle 0, `Act::du_modele`), puis
   **un seul** `Vec<u8>` de corps construit ainsi :

   ```rust
   let h = mdl.cfg.hidden;
   let mut corps = Vec::new();
   for j in 0..t {
       let (idx, val, ech) = mdl.flux_en_liste_blocs(&etats[j*h..(j+1)*h]);
       let paires = encoder_paires_blocs(&idx, &val);
       corps.extend_from_slice(&(idx.len() as u32).to_le_bytes());
       corps.extend_from_slice(&(ech.len() as u32).to_le_bytes());
       corps.extend_from_slice(&(paires.len() as u32).to_le_bytes());
       for e in &ech { corps.extend_from_slice(&e.to_le_bytes()); }
       corps.extend_from_slice(&paires);
   }
   ```

4. Garde-fous d'émetteur, les deux, avant d'écrire :
   `assert_eq!(tete.len(), TAILLE_TETE, …)` (le bug d'un octet de trop, déjà
   payé) et `debug_assert_eq!(corps.len(), 12*t + 4*Σn_blocs + Σlongueur, …)`.
5. **Deux `write_all`** (en-tête, corps), jamais t+1 ; `TCP_NODELAY` reste.
   Rend `(octets, Σa_j)` : la comptabilité doit être mesurée, pas déduite.
6. Ligne de transport : `mode 4 · listes à échelle par bloc · t états · X octets
   par lot · Y par jeton · N lots (au lieu de M flux)`.

### 5.2 Le nœud moteur (`run_serveur_flux`) — décoder N états

* La branche existante `if f.mode == MODE_LOT` devient
  `if f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES`. Rien d'autre ne bouge :
  `f.act.appliquer(&mut mdl)`, `couche_debut/fin`, `mdl.flux_brut = true`, le
  contrôle `pos + t ≤ ctx`, puis
  `mdl.emb_imposee_lot = Some(f.charge.plat().to_vec())` et
  `mdl.forward_lot(&vec![0u32; t], f.pos as usize)` — `ChargeFlux::Lot` est
  produit par le décodeur du mode 4 exactement comme par celui du mode 3.
* Aucune ligne de `model.rs` ne change. `emb_imposee_lot` (model.rs:928),
  `forward_lot` (model.rs:2320), le cache KV et `flux_brut` sont déjà corrects et
  partagés : c'est le point qui a coûté le plus cher en phase 3, on n'y touche
  pas.
* Le nœud moteur **ne connaît pas le texte** : il reçoit des états, pas des
  jetons.

### 5.3 La réponse

Encodée **comme la demande** (R5) : `envoyer_lot_listes` sur les `t` états
rendus par `forward_lot` (résidu brut, jamais normé), mêmes `t`, `position`,
plage et réglages. Le pilote la décode par le même `recevoir_flux`, retrouve un
`ChargeFlux::Lot` plat, garde son `assert_eq!(etats.len(), t*hidden)`, applique
`norme_finale` **une fois par état** puis `logits_lot`. Le coût du retour est du
même ordre que l'aller (÷2,3) ; c'est la ligne `octets_recus` qui le prouvera.

## 6. La vérification

### 6.1 Commande exacte (localhost, Qwen2.5-0.5B, 12 couches par nœud ; la même
campagne entre **deux machines** reste à faire — `docs/colab-reparti.md`)

```bash
# terminal 1 — le nœud moteur : inchangé
./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 --ctx 256

# terminal 2a — la référence PERDANTE : le mode 2, un flux par jeton (mêmes ids)
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
        --couches-locales 12 --limit 256 --ctx 256 --flux-blocs --act-thresh 0.01

# terminal 2b — le mode 4 : mêmes ids, même seuil, par lots
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
        --couches-locales 12 --limit 256 --ctx 256 --lot 16 --flux-blocs --act-thresh 0.01
```

Résultat attendu (le chiffre exact dépend du corpus ; les identifiants par défaut
`1..256` donnent une perplexité bien plus haute que WikiText-2, l'écart seul
compte) :

```
  référence locale  : perplexité X          <- identique au run mode 3 à mêmes ids et --lot
  deux nœuds        : perplexité Y          <- Y ≠ X : c'est le prix des listes, pas un bug
  écart             : 2,7e-2                <- du même ordre que 2a (critère : ≤ 1,5×)
  transport         : mode 4 · listes à échelle par bloc · 16 états ·
                      ≈ 24 500 octets par lot (≈ 1 530 par jeton) · 16 lots (au lieu de 255 flux)
```

### 6.2 Ce qui est acceptable, et par rapport à quoi

* Le mode 4 est **avec perte** : `0,00e0` est impossible et le chercher est une
  erreur de critère. Le mode 2 coûte déjà **2,7e-2 à 256 jetons** (1,3e-2 à
  1 024, 1,4e-1 à 64) au seuil 0,01. Le mode 4 quantifie **chaque état
  exactement comme le mode 2 quantifie un jeton**, avec la même fonction et les
  mêmes réglages.
* **Critère** : `écart(mode 4) ≤ 1,5 × écart(mode 2 par jeton)` à mêmes ids,
  même `--limit`, même `--act-thresh` — en pratique ≈ 2,7e-2. Si le mode 4
  s'écarte de 10×, c'est le placement des échelles ou l'ordre des états qui est
  faux, pas la quantification.
* **Contrôle gratuit** : la ligne `référence locale` du run 2b doit être
  **identique** (à 4 décimales) à celle d'un run mode 3 à mêmes ids et mêmes
  frontières de lots — le chemin de référence ne touche pas au fil. Une
  différence signale un découpage changé, pas un problème de transport.
* **Contrôle de taille** : si la ligne de transport affiche ~3 590 octets par
  jeton, le mode 4 n'a pas été utilisé (repli dense) ; si elle affiche ≈ 1 530,
  la formule du §1.4 est vérifiée et l'écart attendu est celui du mode 2.
* Comparer l'écart à celui d'un run `--lot 1` n'a de sens qu'à seuil et corpus
  égaux ; comparer la perplexité absolue à celle d'un autre corpus n'en a aucun
  (le corpus pèse plus que le mode : 0,2 % sur identifiants synthétiques à
  40 jetons contre 2,7 % sur WikiText-2 à 256).

### 6.3 Les portes sans modèle (avant toute campagne)

```bash
cargo test -p drave-core tests_flux      # protocole et codec
cargo test -p drave-core tests_plafond   # règle R4 : refus avant allocation
```

Doivent exister et passer : aller-retour `encoder_etat_blocs` → `lire_etat_blocs`
sur 3 états aux nombres d'actifs différents, **identique** (idx, val, échelles,
tampon décodé), y compris un état vide et un état avec échappement ; un lot
tronqué au milieu d'un état rend une **erreur**, pas une panique ni une attente ;
un état annonçant 100 millions de paires, de blocs ou d'octets est refusé en
nommant le plafond **avant** d'allouer ; un en-tête v5 de mode inconnu est refusé
sans lire le corps ; `assert_eq!(VERSION_FLUX, 5)` et `assert_eq!(TAILLE_TETE, 79)`.

## 7. Les pièges (ceux déjà payés, et ceux que le mode 4 ajoute)

1. **Un octet d'en-tête en trop** décale tout le corps, ne lève aucune erreur, et
   ne se voit qu'au flux suivant (« magie de flux absente »). Déjà payé (40 pour
   39). Les trois émetteurs (`envoyer_flux`, `envoyer_lot`, `envoyer_lot_listes`)
   gardent leur `assert_eq!(tete.len(), TAILLE_TETE)`.
2. **Le décalage propre au mode 4** : une erreur d'un octet dans un préfixe
   d'état décale les états SUIVANTS dans le même message, et peut produire des
   préfixes plausibles — donc des états faux sans erreur. C'est le même bug, une
   couche plus bas. Réponse : R6 (frontières exactes), le `debug_assert` de
   longueur de corps à l'émission, et le test d'aller-retour multi-états.
3. **Ne pas dériver `longueur_j` de `a_j`** : les échappements (255 + 2 octets)
   font que `longueur_j` n'est pas `2·a_j`. Le mode 2 a déjà payé ce couple
   (écrit sur quatre octets, lu sur deux) ; ici l'erreur ne casserait rien tant
   qu'aucun écart n'atteint 255 — donc resterait invisible jusqu'au jour où.
4. **Chaque état a son propre `prev`** : `encoder_paires_blocs` repart de 0 à
   chaque appel, donc le premier écart d'un état est son indice absolu. Un
   décodeur qui réutilise `prev` d'un état à l'autre décale tous les indices du
   lot.
5. **Les réglages d'activation voyagent et s'appliquent** : le seuil décide de la
   sparsité (donc de la taille) et il est appliqué au serveur par
   `f.act.appliquer(&mut mdl)` avant tout calcul — la ligne doit rester dans la
   branche commune 3/4. Mesuré : 0,69 d'écart de perplexité entre deux nœuds à
   seuils différents.
6. **La clé de trace est un compteur global**, pas la position : `forward_lot`
   l'avance **une fois pour tout le lot** (`j0 = jeton_trace + 1`, puis `+= t`).
   Le décodeur du mode 4 ne touche pas au compteur ; ne pas ajouter d'avance par
   état, et ne pas casser le raccourci `t == 1` de `forward_lot` (model.rs:2330),
   qui délègue à `forward` et avance le sien.
7. **`n` change de sens selon le mode** : 0/1 = canaux, 2 = actifs, 3 = états,
   **4 = états aussi** — et le nombre d'actifs d'un lot est `Σ a_j`, jamais `n`.
   Un lecteur qui réutilise `n` comme nombre d'actifs lira des octets qui ne
   veulent rien dire ; la ligne de statistiques doit afficher `Σ a_j`.
8. **Le dernier jeton n'a rien à prédire** : la boucle du pilote s'arrête à
   `pos + 1 < ids.len()` ; ne pas envoyer un lot final d'un seul état pour
   « finir proprement », ce serait un aller-retour pour un état que personne ne
   lit (c'est aussi pourquoi R1 interdit le mode 4 à `t = 1` à l'émission).
9. **Le contexte qui déborde ne s'arrête pas, il boucle** : `KvCache::assurer`
   plafonne à `self.ctx` ; le contrôle `pos + t ≤ mdl.ctx` doit couvrir les
   modes 3 **et** 4.
10. **Un indice hors dimension ne doit pas tuer le nœud** : la garde du mode 2
    (indice ignoré, compté, message une fois) s'applique à la déquantification du
    mode 4 ; une trame forgée donnait un SIGABRT.
11. **`TCP_NODELAY` et le nombre d'écritures** : l'en-tête puis le corps en deux
    `write_all`, jamais une écriture par état (Nagle retient les petites
    écritures ; mesuré 97,6 ms contre 15,6 ms de calcul).
12. **La mémoire ne baisse pas** : le mode 4 économise le fil, pas la RAM — le
    lot décodé est un `Vec<f32>` de `t·hidden`, identique au mode 3. Le plafond
    de l'étape 3 de §4 est donc exactement celui du mode 3.

## 8. Plan d'implémentation (7 étapes, dans l'ordre)

| # | fichier | quoi | critère de succès |
|---|---|---|---|
| 1 | `drave-core/src/main.rs` : 1376, 1387-1393, 3344-3345 | `VERSION_FLUX = 5`, `MODE_LOT_LISTES = 4` ; mettre à jour le test qui affirme 4 | `cargo test -p drave-core tests_flux` passe ; deux binaires v4/v5 se refusent au premier message en nommant les deux versions ; deux v5 en mode 0 dense gardent 0,00e0 |
| 2 | `main.rs` : 1446-1485, 1548-1598 | `Flux.actifs` (comptabilité), `encoder_etat_blocs(idx, val, ech)`, `lire_etat_blocs<R: Read>(s, j, hidden, dst, cumul)` avec les contrôles du §4 dans l'ordre | test unitaire sans modèle : 3 états aux actifs différents, aller-retour identique ; un lot tronqué rend une erreur, pas une panique |
| 3 | `main.rs` : 1739-1801 | bras `MODE_LOT_LISTES` de `recevoir_flux` (en-tête, `t`, plafond, boucle sur les états, `ChargeFlux::Lot`) + refus immédiat des modes inconnus après l'en-tête | une trame forgée annonçant 100 M de paires/blocs/octets est refusée en nommant le plafond **avant** d'allouer ; un mode 7 est refusé sans lire le corps (envoi d'un en-tête seul, pas de blocage) |
| 4 | `main.rs` : 1666-1704 | `envoyer_lot_listes` (en-tête + corps par état) avec les deux garde-fous d'émetteur | test aller-retour par socket : le message relu par `recevoir_flux` rend le lot attendu ; `octets == 79 + corps` et `corps` conforme à la formule du §1.4 |
| 5 | `main.rs` : 1849-1886, 1920-1939, 1982-2039 | branchement : `--lot > 1 && --flux-blocs` → mode 4 côté pilote ; branche serveur `MODE_LOT \|\| MODE_LOT_LISTES`, réponse en mode 4 ; message `--flux-liste` corrigé ; ligne de transport | les deux nœuds s'échangent des mode 4 ; le serveur annonce le bon nombre de lots ; `octets_recus ≈ octets_envoyes` |
| 6 | campagne locale | la commande §6.1, plus le contrôle `--lot 1 --flux-blocs` pour la référence perdante, plus un run mode 3 à mêmes ids pour l'égalité de la référence locale | `écart(mode 4) ≤ 1,5 × écart(mode 2)` ; référence locale identique au run mode 3 ; ≈ 1 530 octets par jeton là où le mode 3 en met 3 589 |
| 7 | `reports/rapport-mode4-lot-listes.md`, `docs/format-flux.md`, `docs/plan-prefill-reparti.md` §7, `docs/roadmap.md` 3.4/3.5 | consigner les chiffres **mesurés**, le tableau du mode 4 et la version 5 ; retirer « mode 4 non écrit » partout où c'est écrit | chaque nombre du rapport est recopié de la sortie de l'étape 6, commande incluse ; aucune mention de mode 4 « à écrire » ne subsiste |

Étapes 2 et 3 sont testables sans modèle ni campagne ; l'étape 4 aussi (socket
locale). Ne pas commencer par 6.

## Résumé (10 lignes)

1. Le mode 4 est le mode 2 répété par état : `t` états dans un seul flux, chacun
   auto-délimité par un préfixe de 12 octets (`a_j`, `n_blocs_j`, `longueur_j`),
   puis les échelles f32 par bloc de 32, puis les paires d'`encoder_paires_blocs`.
2. Aucun encodage nouveau : le contenu d'un état est l'octet pour octet du mode 2.
3. L'échelle vit dans l'état, pas dans une table du lot : indépendance des états,
   dynamique par jeton, et 112 octets sur ~1 530 ne justifient pas un second codec.
4. Le protocole passe en version 5, sinon un pair v4 consommerait `4·t` octets
   avant de dire « mode inconnu » ; la règle « nouveau mode ⇒ nouvelle version »
   est écrite, et le refus des modes inconnus devient immédiat.
5. Le corps n'est plus borné par l'en-tête : `a_j·2`, `n_blocs_j·4`, `longueur_j`
   et leur cumul passent par `verifier_taille` avant chaque allocation, dans cet
   ordre, après `t·hidden·4` validé en tête.
6. Le mode 4 s'arrête au transport : `ChargeFlux::Lot`, `emb_imposee_lot`,
   `forward_lot`, le cache KV et la norme finale ne changent pas.
7. La réponse est encodée comme la demande ; le pilote norme chaque état une fois.
8. Le critère est `écart(mode 4) ≤ 1,5 × écart(mode 2 par jeton)` (≈ 2,7e-2 à
   256 jetons, seuil 0,01), jamais 0,00e0 : le mode est avec perte par décision.
9. **Laissé à l'implémenteur** : le nom et la forme exacte des deux helpers
   (`encoder_etat_blocs` / `lire_etat_blocs`, générique sur `Read` ou non) et le
   portage de `Flux.actifs` sur les autres modes.
10. **Laissé à l'implémenteur** : le seuil de bascule par défaut entre mode 3 et
    mode 4 (aujourd'hui `--flux-blocs` décide) et la borne structurelle
    facultative du §4, à poser seulement si elle ne rejette aucune trame réelle.
