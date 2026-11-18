# A2.6 — la bande des experts : 7,0 Go/s à 8 fils, saturation à 8, PPL 37,2013 invariante

> **Ligne de roadmap** : A2.6 (les experts et la tête) · **Date** : 2026-11-18 · **Verdict** : ✅
> mesuré — sur `qwen3-30b-a3b-Q4_K_M` à `--limit 32` (31 jetons notés), `proj+mlp` vaut
> **156,95 ms/jeton à 8 fils** (bande implicite **6,99 Go/s**), **165,40 à 16** (aucun gain),
> 222,45 à 4 ; les deux chemins « optimisés » sont **plus lents** (cache RAM 314,36 ; tampons
> 231,32). La perplexité est **37,2013 sur tous les chemins** — un placement change le temps,
> jamais le chiffre.
>
> **Dispositif** : protocole du [rapport de reconnaissance A2.6](rapport-a2.6-reconnaissance.md) §3.2 ·
> `drave --ppl <ids> --ctx 512 --limit 32 --threads T` · machine **dédiée** · 2 passes par réglage
> (la seconde est la lecture chaude, seule citée) · données
> [`a2.6-bande-experts.json`](a2.6-bande-experts.json).

## Les points

| réglage | `proj+mlp` (ms/jeton) | bande implicite (1,097 Go/jeton) |
|---|---:|---:|
| 4 fils | 222,45 | 4,93 Go/s |
| **8 fils** | **156,95** | **6,99 Go/s** |
| 16 fils | 165,40 | 6,63 Go/s |
| `DRAVE_EXPERTS_RAM=4096`, 8 fils | 314,36 | 3,49 Go/s |
| `DRAVE_TAMPONS=1`, 8 fils | 231,32 | 4,74 Go/s |

*Perplexité : 37,2013 partout. Première passe plus lente (lecture froide) — non citée.*

## Lecture

1. **L'opérateur experts est borné par UN lecteur, ~7 Go/s** : ni la RAM (22,5 Go/s), ni le NVMe
   (3,5), ni les 31 Go/s des 16 lecteurs séquentiels. C'est la mesure de lecteur unique
   (`mesurer_lecture_experts.py`) qui gouverne, pas la bande du support.
2. **La saturation est à 8 fils** : 16 fils fait **moins bien** (165,40 contre 156,95) — le chemin
   n'est pas borné par le calcul, il est borné par la lecture, et 16 fils ajoutent de la contention.
3. **Les chemins « optimisés » perdent** : cache RAM 314 ms, tampons 231 ms, contre 157 ms pour le
   mmap par défaut. Le défaut est le bon chemin — et les deux contrôles sont plus lents, comme la
   règle l'exigeait.
4. **Conséquence pour `placement.rs`** : la bande à porter est **~7 Go/s pour les experts** (pas
   22,5 ni 3,5), le coût doit compter **un lecteur** et non la bande agrégée, et `choisir` doit
   **refuser nommément** au lieu de retomber sur NVMe en silence.

## Ce qui pourrait le rendre faux

- **31 jetons** : petit échantillon ; 13 s par point, la variance n'est pas calculée.
- **La page cache est chaude** après la première passe : un vrai run à froid (18,5 Go à lire) serait
  plus lent — c'est le régime des campagnes, pas celui de cette mesure.
- **1,097 Go/jeton** vient de la reconnaissance, pas d'un compteur du run ; une erreur sur ce
  chiffre déplace toute la bande implicite.
- **Q4_K_M seulement** : à une autre quantification, la bande de l'opérateur peut changer.
- **La machine est dédiée aujourd'hui** : la reconnaissance avait mesuré 194,8 ms à 8 fils sous
  charge ; ici 156,95. Le chiffre à citer est celui de la machine au repos, et l'écart est le prix
  de la charge.

## Ce que ça change

La prochaine étape d'A2.6 n'est plus une mesure : c'est **le code** (~200 lignes sur `placement.rs`,
`model.rs`, `materiel.rs`) qui porte le coût « experts » (un lecteur, ~7 Go/s, réutilisation),
le **refus nommé**, la trace du classement et une `Precision` de tête à perte 0. Le risque est le
**chemin de chargement et le défaut**, pas la taille du diff : opt-in `DRAVE_PERTE_MAX`, portes
`flux`/`pont`/`coupe`/`echange-experts` + `cargo test placement`.

## Voir aussi

- [la reconnaissance A2.6](rapport-a2.6-reconnaissance.md) · [les données](a2.6-bande-experts.json) ·
  [placement](../drave-core/src/placement.rs) · [le programme A](../docs/pilotage/roadmap.md)

## La règle sait chiffrer les experts (18/11, après la mesure)

`placement.rs` porte désormais les constantes mesurées et la règle :

- `BANDE_EXPERTS_8 = 6,99 Go/s`, `BANDE_EXPERTS_4 = 4,93`, `LECTEURS_SATURATION = 8` ;
- `bande_experts(lecteurs)` : linéaire de 0 à 4 puis de 4 à 8, **plate** au-delà (16 < 8, mesuré) ;
- `cout_experts(octets, lecteurs)` : octets ÷ bande du **lecteur** ;
- `choisir_experts(...) -> Result<Support, String>` : VRAM, sinon RAM, sinon **refus nommé** — le
  message porte les Go/jeton, la bande, le budget et le coût NVMe qu'on refuse (313,4 ms).

**Tests** (5 nouveaux, `cargo test placement` **14/14**, crate **145/145**) :

- la bande reproduit les deux points mesurés (4 et 8 fils) et la saturation ;
- le coût reproduit la mesure : 1,097 Go/jeton à 8 fils → **156,9 ms** (mesuré 156,95) ;
- le refus est nommé (contient « REFUSÉS », la bande et le coût NVMe) ;
- VRAM si elle tient, RAM sinon ;
- la **trace** (`trace_experts`) dit les chiffres — `1.10 Go/jeton · 6.99 Go/s · 156.9 ms → VRAM` — et
  le refus passe par la même ligne.

**Ce qui reste** : brancher `choisir_experts` dans `model.rs` (les trois sites : tête, cache VRAM,
cache RAM), en opt-in `DRAVE_PERTE_MAX` — le défaut ne doit pas bouger — et ramener les trois tables
de bandes de `materiel.rs` à une. C'est la tâche A2.6 suivante, et c'est celle qui a le plus de
risque : le chemin de chargement.
