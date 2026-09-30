# Plan — le préremplissage par lots sur le fil (phase 3.4)

**En une ligne** : aujourd'hui un flux = un jeton, donc un préremplissage de N
jetons paie N allers-retours ; on ajoute un **mode 3** qui transporte N états
dans **un seul** message, et le banc réparti doit rendre **0,00e0**.

Ce document est une spécification d'implémentation : chaque étape dit le fichier,
le point d'insertion et le critère de succès. Les numéros de ligne cités sont
ceux du commit `2184fc5` ; l'arbre de travail contient déjà une implémentation
partielle non commitée (`Model::emb_imposee_lot`, `MODE_LOT`, `envoyer_lot`) —
**la relire avant d'éditer**, elle bouge. Deux écarts connus à corriger en
priorité : `envoyer_lot` écrit **40** octets d'en-tête pour un `TAILLE_TETE` de
**39** (le dernier `tete.push(0)` décale tout le corps d'un octet, §2.3 et §6.2),
et `VERSION_FLUX` vaut encore **2** (§1.3).

## 0. Décisions d'architecture (à ne pas rediscuter)

| question | décision | pourquoi |
|---|---|---|
| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête reste **39 octets**, tous les offsets existants sont stables |
| quels modes dans le lot ? | **dense f32 seulement** | c'est le seul transport **sans perte**, donc le seul qui puisse exiger 0,00e0 ; un lot de listes est un mode 4 (voir §7) |
| la version change ? | **oui, 2 → 3** | un nœud v2 lirait `n×4` octets d'un corps qui en fait `n×hidden×4` avant de répondre « mode inconnu » : erreur exacte mais tardive, et qui ne dit pas que c'est une VERSION. Le critère 3.5 est « pas de silence, pas de devinette » |
| la dimension voyage ? | non | chaque nœud la connaît par son modèle ; les deux nœuds DOIVENT charger le même GGUF (limite déjà écrite dans `docs/colab-reparti.md`) |
| le décodage ? | reste séquentiel, un flux par jeton | hors sujet ; le mode 3 ne concerne que le préremplissage |

## 1. Le protocole v3

### 1.1 En-tête (39 octets, identique à l'aller et au retour)

| off | octets | champ | type | mode 0 dense | mode 1 liste | mode 2 blocs | **mode 3 lot** |
|---|---|---|---|---|---|---|---|
| 0 | 4 | magie | u32 | `0x44525631` | idem | idem | idem |
| 4 | 1 | version | u8 | **3** | 3 | 3 | **3** |
| 5 | 1 | mode | u8 | 0 | 1 | 2 | **3** |
| 6 | 4 | couche_debut | u32 | | | | |
| 10 | 4 | couche_fin | u32 | exclue | | | |
| 14 | 4 | position | u32 | jeton | jeton | jeton | **premier jeton du lot** |
| 18 | 4 | n | u32 | dimension | actifs | actifs | **nombre d'états `t`** |
| 22 | 4 | échelle | f32 | 0 | échelle | 0 | 0 |
| 26 | 4 | act.levels | f32 | niveaux de quantification des activations | | | |
| 30 | 4 | act.thresh | f32 | seuil | | | |
| 34 | 4 | act.topk | u32 | k-WTA | | | |
| 38 | 1 | act.renorm | u8 | 0/1 | | | |

Tout est en **little-endian**. Les modes 0, 1 et 2 sont **inchangés à l'octet
près** : seul le numéro de version change. Le mode 3 est le seul ajout.

### 1.2 Corps du mode 3

```
corps = t × hidden × f32 LE, dans l'ordre des jetons
        l'état du jeton (position + j) commence à l'offset j × hidden × 4
```

Règles du corps :

* **R1** — `t = n ≥ 1`. Un lot d'un seul état est **accepté en réception**, mais
  l'émetteur DOIT utiliser le mode 0 pour un jeton seul : le chemin séquentiel de
  la génération reste ainsi intact, octet pour octet.
* **R2** — les positions sont **contiguës** : `position .. position + t`. Seule la
  base voyage ; c'est le contrat, et il est vérifié (§3).
* **R3** — la dimension n'est pas transmise : le récepteur lit `n × hidden × 4`
  octets avec SON `hidden`. Deux GGUF différents ne donnent pas une erreur au
  premier lot mais une désynchronisation (le message suivant échoue sur
  « magie de flux absente ») — le dire dans le message d'erreur.
* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**
  l'allocation (`vec![0u8; …]` sur un en-tête corrompu est un OOM, pas une
  erreur de protocole).
* **R5** — la réponse est encodée **comme la demande** : même mode, même `n`,
  même `position`, mêmes `couche_debut`/`couche_fin`.

### 1.3 Compatibilité

* Un pair v2 et un pair v3 se refusent **au premier message**, sur le champ
  version (offset 4), avec le message existant qui nomme les deux versions :
  `[flux] arrêt : flux en version 2, cette build parle la 3 (pair incompatible :
  rien n'a été interprété)`.
* L'ordre de lecture compte : `recevoir_flux` lit les **39 octets** de l'en-tête
  puis teste la version. C'est ce qui rend le refus sûr (aucun octet du corps
  n'est interprété). Ne pas déplacer ce test.
* Les deux nœuds doivent donc être reconstruits ensemble : la recette Colab
  impose déjà le même commit des deux côtés.

### 1.4 Ce que le mode 3 change au bilan d'octets

| envoi | formule | Qwen2.5-0.5B (`hidden` 896) |
|---|---|---|
| un jeton, mode 0 | 39 + 4·hidden | 3 623 octets, 3 623 par jeton |
| lot de 8, mode 3 | 39 + 4·t·hidden | 28 711 octets, **3 589 par jeton** |
| lot de 16, mode 3 | 39 + 4·t·hidden | 57 383 octets, **3 586 par jeton** |

L'en-tête est amorti (39 → 5,4 octets par jeton à `t = 8`), et surtout le nombre
d'**allers-retours** passe de N−1 à `⌈(N−1)/t⌉` : c'est là que se gagne la phase
3.4, pas dans le débit (cf. `docs/colab-reparti.md` : à 60 ms d'aller-retour,
8 jetons/s en séquentiel).

## 2. Côté serveur

### 2.1 Constantes et types — `drave-core/src/main.rs`

| point | ligne (HEAD) | quoi |
|---|---|---|
| `VERSION_FLUX` | 1231 | `2` → **`3`** |
| constantes de mode | 1233–1242 | ajouter `const MODE_LOT: u8 = 3;` |
| `TAILLE_TETE` | 1251 | **inchangée** (39) |
| `struct Flux` | 1277 | ajouter `n: usize` (le compte du mode : canaux, actifs ou états) |
| `enum ChargeFlux` | 1292 | ajouter `Lot(Vec<f32>)` (aplati `t × hidden`) |
| `ChargeFlux::en_dense` | 1301 | bras `Lot(_)` → **panique nommée** : « un lot d'états n'est pas un vecteur dense ; c'est `plat()` qui le sert » |
| `ChargeFlux::plat` | — | nouveau, rend `&[f32]` pour `Lot`, `&[]` sinon |

### 2.2 Réception — `recevoir_flux` (main.rs:1400)

Le corps est lu **avant** le `match mode` (ligne 1468 : `vec![0u8; n*4]`). Le mode 3
doit donc **retourner tôt**, comme le fait déjà `MODE_BLOCS` (ligne 1426) :

```rust
MODE_LOT => {
    if n == 0 || n * hidden * 4 > PLAFOND_LOT { return Err(/* InvalidData, message nommé */); }
    let mut corps = vec![0u8; n * hidden * 4];
    s.read_exact(&mut corps)?;
    let etats = (0..n * hidden).map(|k| f32::from_le_bytes(
        [corps[k*4], corps[k*4+1], corps[k*4+2], corps[k*4+3]])).collect();
    return Ok(Flux { n, debut, fin, pos, mode, act, octets_corps: corps.len(),
                     charge: ChargeFlux::Lot(etats) });
}
```

D'où la signature `recevoir_flux(s, hidden)` : la dimension vient du modèle du
récepteur, elle n'a pas à voyager. Les **deux** appelants doivent être mis à jour :
la boucle serveur (`recevoir_flux(&mut sock, hidden)`, main.rs:1520) et le pilote
(`recevoir_flux(&mut sock, mdl.cfg.hidden)`, main.rs:1626).

### 2.3 Émission — `envoyer_lot` (nouvelle, à côté d'`envoyer_flux`, main.rs:1330)

```rust
fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
               etats: &[f32], t: usize, mdl: &model::Model) -> std::io::Result<usize>
```

Même contrat qu'`envoyer_flux` : construit l'en-tête de 39 octets (mode 3, `n = t`,
échelle 0, réglages `Act::du_modele`), **un seul `write_all` pour l'en-tête et un
seul pour le corps** (pas 2t petites écritures : c'est la même classe de coût que
Nagle, cf. §6.1). Rend le nombre d'octets écrits, en-tête compris.

Garde-fou obligatoire avant l'écriture :

```rust
debug_assert_eq!(tete.len(), TAILLE_TETE, "en-tête de {} octets, il en faut {TAILLE_TETE}", tete.len());
```

C'est ce `debug_assert` qui attrape l'erreur la plus coûteuse de ce chantier : un
`push` de trop décale **tout** le corps d'un octet et les états arrivent
silencieusement faux (des f32 valides, jamais les bons — l'écart de perplexité
ressemblerait à un bogue de calcul).

### 2.4 Boucle serveur — `run_serveur_flux` (main.rs:1491)

Le préambule existant reste **le même** et doit s'appliquer aussi au lot :
`f.act.appliquer(&mut mdl)`, `mdl.couche_debut/couche_fin` depuis l'en-tête,
`mdl.flux_brut = true`. Puis, avant le chemin « un jeton » (ligne 1532) :

```rust
if f.mode == MODE_LOT {
    let t = f.n;
    if f.pos as usize + t > mdl.ctx {
        println!("[flux] arrêt : lot de {t} jetons à la position {} au-delà du contexte {}",
                 f.pos, mdl.ctx);
        break;
    }
    let hs = mdl.forward_lot_impose(f.pos as usize, f.charge.plat().to_vec());
    let plat: Vec<f32> = hs.concat();
    if envoyer_lot(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl).is_err() { break; }
    servis += 1;
    continue;
}
```

Le nœud moteur **rend toujours un flux brut** : il ne norme pas, même quand sa
plage va jusqu'à la dernière couche (`flux_brut`). La norme appartient au nœud qui
a la tête de sortie, et à lui seul.

### 2.5 Côté modèle — `Model::forward_lot_impose` (nouveau, model.rs:2091)

`forward_lot` part aujourd'hui des identifiants de jetons (lignes 2107–2111 :
`self.g.row_f32("token_embd.weight", tok, h)`). Le lot imposé est le pendant
exact de `emb_imposee` (model.rs:728) pour un jeton :

```rust
// champ, à côté de emb_imposee (model.rs:728), initialisé à None (model.rs:1546)
pub emb_imposee_lot: Option<Vec<f32>>,      // t × hidden, aplati

// au début de forward_lot (model.rs:2091), AVANT le raccourci `t == 1`
let impose = self.emb_imposee_lot.take();
if t == 1 {
    if let Some(v) = impose { self.emb_imposee = Some(v); }
    // le jeton n'est PAS lu quand un état est imposé : `forward` prend `emb_imposee`
    return vec![self.forward(toks.first().copied().unwrap_or(0), pos0)];
}
// puis, à la place de la boucle d'embeddings :
match impose {
    Some(v) => { assert_eq!(v.len(), t * h, "lot imposé de {} valeurs pour {t} jetons de {h} canaux", v.len()); x.copy_from_slice(&v); }
    None => { /* boucle token_embd inchangée */ }
}
```

et la variante qui évite au serveur d'inventer des jetons :

```rust
pub fn forward_lot_impose(&mut self, pos0: usize, etats: Vec<f32>) -> Vec<Vec<f32>> {
    let h = self.cfg.hidden;
    assert!(h > 0 && etats.len() % h == 0, "lot imposé de {} valeurs, pas un multiple de {h}", etats.len());
    let t = etats.len() / h;
    assert!(t > 0, "lot imposé vide");
    assert!(pos0 + t <= self.ctx, "lot imposé : positions {pos0}..{} au-delà du contexte {}", pos0 + t, self.ctx);
    self.emb_imposee_lot = Some(etats);
    self.forward_lot(&vec![0u32; t], pos0)   // le vecteur ne sert QUE de porteur de longueur
}
```

**Rien d'autre ne change dans `forward_lot`** : la boucle de couches
`couche_debut..couche_fin` (model.rs:2167), la sortie brute (model.rs:2544) et la
norme finale (model.rs:2548) sont déjà correctes et déjà partagées avec le chemin
par jetons. C'est le point qui a coûté le plus cher en phase 3 (`forward` bouclait
sur `0..n_layer`, perplexité répartie 798,3) : on ne réintroduit pas une seconde
boucle.

## 3. Cache KV et positions

**Ce qui se passe.** Un lot de `t` états écrit `t` positions dans le cache KV de
**chaque** nœud : le pilote pour ses couches locales (son `forward_lot(chunk, pos0)`
écrit `pos0+i`), le nœud moteur pour les siennes (`forward_lot` calcule
`pos = pos0 + i` puis écrit `kvc.ecrire(hh, pos, …)`, model.rs:2212 et 2246, dans
la boucle de couches ouverte en 2167 ; l'attention du jeton `i` est causale sur
`pos0+i`).

**Ce qui voyage.** La seule position transmise est `position` = **base** du lot
(offset 14) ; `n` = nombre d'états (offset 18). Rien d'autre : le lot est contigu
par contrat (R2).

**Ce qui est vérifié.**

1. *Avant le calcul, côté serveur* : `pos + n ≤ mdl.ctx`, sinon arrêt nommé (§2.4).
   Sans ce test, `KvCache::assurer` (model.rs:907) **boucle indéfiniment** : il
   plafonne `cap` à `self.ctx` dans un `while cap < besoin`, donc `besoin > ctx`
   ne termine jamais. Ajouter en défense `assert!(besoin <= self.ctx, …)` dans
   `assurer` — une panique nommée vaut mieux qu'une attente active (le dépôt a
   déjà payé 27 minutes de blocage muet, cf. `reports/rapport-prefill-par-lots.md`
   §4.ter).
2. *Après réception, côté pilote* — l'**écho** : `rep.mode == MODE_LOT`,
   `rep.pos == pos0`, `rep.n == chunk.len()`, `rep.debut == couches_locales`,
   `rep.fin == n_layer`. Sans ces cinq égalités, un lot décalé corrompt le cache
   des deux nœuds **en silence** : les positions ne servent qu'à la lecture
   suivante, donc l'erreur n'apparaîtrait qu'à la génération, loin de sa cause.
   C'est la même classe que la clé `(couche, position)` de la phase 0, qui avait
   donné 356 694 de perplexité.
3. *En diagnostic* : `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1`
   des deux côtés ; deux lignes qui divergent désignent le découpage fautif.

**Dépassement de contexte.** Il n'y a pas de « continuation » implicite : si
`pos + t > ctx`, le lot est refusé (arrêt de la session, message qui nomme `pos`,
`t` et `ctx`). Un lot ne se scinde pas tout seul côté serveur — c'est le pilote
qui découpe, à la taille `--lot` (§5, étape 5).

## 4. La vérification : 0,00e0, et rien d'autre

### 4.1 Ce que le banc doit faire

`--ppl-reparti` honore `--lot N` (aujourd'hui il l'ignore : `run_ppl_reparti`,
main.rs:1557, ne lit jamais `opt.lot`). Les **deux** chemins — référence locale et
deux nœuds — doivent découper **exactement pareil** :

```rust
let lot = opt.lot.max(1);
let cible = ids.len() - 1;              // la dernière position n'a rien à prédire
assert!(cible > 0, "banc réparti : il faut au moins 2 jetons");
let mut base = 0usize;                  // position du premier jeton du lot
for chunk in ids[..cible].chunks(lot) {
    …                                   // mêmes frontières dans les deux chemins
    base += chunk.len();
}
```

et, pour le chemin réparti : `mdl.forward_lot(chunk, base)` (couches
`0..couches_locales`) → `envoyer_lot` → `recevoir_flux` → écho (§3) →
`norme_finale` **une fois par état** → `logits_lot` → notation de `ids[base+i+1]`.

### 4.2 Commande exacte (localhost, Qwen2.5-0.5B)

```bash
# terminal 1
./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 --ctx 256
# terminal 2
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
        --couches-locales 12 --limit 40 --ctx 256 --lot 8
```

Résultat attendu :

```
  référence locale  : perplexité X          <- lots de 8, mêmes frontières
  deux nœuds        : perplexité X          <- LA MÊME chaîne imprimée ({:.4})
  écart             : 0.00e0
  transport         : mode 3 · 5 lots · 28 711 octets par lot (3 589 par jeton)
  temps             : … ms par jeton en local · … ms à attendre le pair
```

* Le critère est **l'égalité des deux chaînes et l'écart 0,00e0**, pas la valeur
  de `X`. Le mode dense est sans perte (f32 sur le fil), donc le découpage ne doit
  pas changer un bit.
* `X` vaudra « autour de 144,8289 » (la valeur mesurée du chemin jeton par jeton
  à 40 jetons) mais **peut différer aux derniers chiffres** : un lot change
  l'ordre des accumulations flottantes (mesuré 6e-5 à 4e-4 dans
  `reports/rapport-prefill-par-lots.md` §2). Comparer un run `--lot 8` à un run
  `--lot 1` **n'est pas** le critère : c'est une fausse alerte.
* Non-régression : `--lot 1` doit redonner **exactement** la sortie d'aujourd'hui
  (144,8289 et 0,00e0) — le découpage `ids[..cible].chunks(1)` est le chemin
  jeton par jeton actuel.

### 4.3 Les deux autres portes

```bash
# 199 positions en 13 lots au lieu de 199 messages (÷15,3 d'allers-retours)
./drave … --ppl-reparti 127.0.0.1:45733 --couches-locales 12 --limit 200 --ctx 256 --lot 16
# doit afficher : écart 0.00e0 et « 13 lots »
```

```bash
# test unitaire du codec, sans modèle : l'aller-retour est identique à l'octet
cargo test -p drave-core tests_flux_lot
```

Les deux premiers critères sont **exacts** ; en mode listes (hors de ce plan),
l'écart serait au contraire du même ordre que le chemin par jeton (2,7e-2 pour
`--flux-blocs --act-thresh 0.01`) : ne pas confondre les deux régimes.

## 5. Plan d'implémentation ordonné

| # | fichier | quoi | critère de succès vérifiable |
|---|---|---|---|
| 1 | `main.rs:1231-1251` | `VERSION_FLUX = 3`, `MODE_LOT = 3` | un binaire v3 et un binaire v2 se refusent au 1er message en nommant les deux versions ; deux v3 en mode 0 dense : écart 0,00e0 inchangé |
| 2 | `main.rs:1277-1345, 1400-1486` | `Flux.n`, `ChargeFlux::Lot`, `plat()`, bras `MODE_LOT` de `recevoir_flux`, `envoyer_lot` | `tests_flux_lot` : encode→décode rend les mêmes f32 à l'octet près, taille `39 + 4·t·hidden` ; un corps tronqué rend une erreur, pas une panique |
| 3 | `model.rs:728, 1546, 2091-2111` | `emb_imposee_lot` + `forward_lot_impose` | test unitaire : `forward_lot_impose(pos, embeddings_du_lot)` == `forward_lot(jetons, pos)` **exactement** |
| 4 | `main.rs:1491-1552` | branche lot de la boucle serveur (§2.4) | 40 jetons, lot 8 : le serveur imprime « 5 flux servis », pas 39 |
| 5 | `main.rs:1557-1661` | pilote par lots + référence locale au **même** découpage (§4.1) | la commande §4.2 rend `écart 0.00e0` |
| 6 | `main.rs` (sortie du banc) | comptabilité : lots, octets par lot **et par jeton**, ms/jeton local et distant | 3 589 ± 1 octet par jeton à `t = 8`, 5 lots pour 39 positions |
| 7 | `reports/rapport-prefill-reparti.md`, `docs/format-flux.md` | chiffres mesurés, tableau du protocole v3 (mode 3) | les nombres du rapport sont ceux de l'étape 5, commande recopiée telle quelle |
| 8 | `docs/colab-reparti.md` | répétition réelle (nœud moteur local, pilote Colab) | 200 jetons, `--lot 16`, écart **0,00e0** avec 60 ms d'aller-retour, et le tableau ms/jeton lots vs séquentiel |

Étapes 1 à 3 sont indépendantes et testables sans réseau ; les étapes 4 et 5 se
rejoignent à l'étape 5. Ne pas commencer par 8.

## 6. Pièges connus (tous déjà payés une fois dans ce dépôt)

1. **`TCP_NODELAY`** — sans lui, Nagle retient une petite écriture et l'ACK
   différé du pair la retarde : **97,6 ms d'attente contre 15,6 ms de calcul**,
   six fois le calcul (main.rs:1511-1516 côté serveur, 1597 côté pilote). Le
   lot réduit le nombre de messages, donc le nombre d'occasions de payer Nagle :
   ne pas en profiter pour retirer le réglage. Et écrire l'en-tête puis le corps
   en **deux** `write_all`, pas 2t.
2. **Un octet de trop dans l'en-tête** — 39 octets lus, 39 à écrire. Le
   `debug_assert_eq!(tete.len(), TAILLE_TETE)` de §2.3 est le seul garde-fou :
   sans lui, le corps entier glisse d'un octet et les états sont faux **sans
   jamais lever d'erreur**.
3. **Le raccourci `t == 1` de `forward_lot`** (model.rs:2094) — `emb_imposee_lot`
   doit être lu **avant** lui, sinon un lot d'un état repasse par `token_embd` et
   calcule le jeton 0 au lieu de l'état reçu.
4. **`forward_lot(&[], pos)`** — `toks.len() == 0` rend un vec vide (model.rs:2093)
   **et laisse `emb_imposee_lot` en place** pour l'appel suivant : l'état fuit sur
   le lot d'après. Toujours passer une tranche de longueur `t` (c'est ce que fait
   `forward_lot_impose`).
5. **Les réglages d'activation doivent voyager et s'appliquer** — `f.act.appliquer(&mut mdl)`
   dans la branche lot comme dans l'autre, **avant** le `forward_lot` (le serveur
   quantifie aussi sa réponse avec ces réglages). Mesuré : 0,69 d'écart de
   perplexité entre un nœud à `--act-thresh 0,05` et un nœud à 0,00.
6. **La norme finale, une seule fois** — le serveur garde `flux_brut = true` ; le
   pilote applique `norme_finale` à chaque état reçu, puis `logits_lot`. Oublier
   `flux_brut` dans la branche lot, c'est refaire 798,3 au lieu de 18,2.
7. **La plage de couches** — `forward_lot` boucle déjà sur
   `couche_debut..couche_fin` (model.rs:2167) et rend le brut si
   `flux_brut || couche_fin < n_layer` (model.rs:2544). Ne pas ajouter de boucle
   `0..n_layer` dans la variante « lot imposé » : c'est l'erreur exacte qui a
   donné la perplexité répartie 798,3.
8. **Un découpage différent entre référence et mesure** — les deux chemins du banc
   doivent utiliser les mêmes frontières de lots (`ids[..cible].chunks(lot)`), sans
   quoi l'ordre des accumulations diffère et l'écart vaut ~1e-4 pour un
   non-bug. Corollaire : le pilote ne « rogne » pas le dernier lot d'un jeton de
   son côté.
9. **Le contexte qui déborde ne s'arrête pas, il boucle** — `KvCache::assurer`
   (model.rs:907) plafonne à `self.ctx` : `besoin > ctx` = attente infinie.
   Vérifier `pos + t ≤ ctx` **avant** l'appel et poser l'assert dans `assurer`.
10. **La mémoire du lot** — `forward_lot` alloue par lot `gate`, `up` et `yl`
    (`t × largeur × 4` chacun, `largeur` valant `ffn` ou `n_têtes × dim_tête`),
    plus les tampons d'attention (`sc2 = vec![f32; nh × ctx]`,
    model.rs:2143). À `t = 512` sur un FFN de 18 944, c'est ~39 Mo par tampon et
    il y en a trois : garder le découpage en lots côté pilote et un défaut
    raisonnable (`--lot` 8 à 16, 64 au maximum pour la démonstration).
11. **Deux GGUF identiques** — la dimension ne voyage pas (R3) ; un `hidden`
    différent ne provoque pas une erreur au premier lot mais une
    désynchronisation du flux d'octets. Le message d'erreur de la lecture
    suivante doit le suggérer.

## 7. Ce que ce plan ne fait pas

* **Le lot en listes** : c'est le mode 4, à écrire quand le débit gênera. Corps
  prévu, un préfixe auto-délimité par état — `u32 a_j · u32 n_blocs_j ·
  n_blocs_j × f32 · u32 longueur_j · paires (écart u8, échappement 255 → u16,
  valeur i8)` — c'est-à-dire le corps du mode 2 répété `t` fois, avec le compte
  d'actifs en tête. Gain attendu : ÷2,3 sur le fil pour ~2,7e-2 d'écart
  (`reports/rapport-transport-liste.md`) ; le critère de la phase 3.4 (0,00e0)
  reste celui du mode 3 dense.
* **Le décodage par lots** : la génération reste séquentielle, un jeton par flux
  (c'est écrit dans la vision). Le mode 3 ne sert qu'au préremplissage.
* **Le chargement partiel** : les deux nœuds chargent le modèle entier ; le
  découpage porte sur le calcul. Limite déjà assumée dans `docs/colab-reparti.md`.
