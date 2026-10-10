> Campagne : **campagne-benefices** · expérience **46**
> Titre : 46. Inventaire des drapeaux en chemin RÉPARTI : cinq agissent, trois sont inertes
> Date réelle : **2026-10-10 09:39 HAE** (source : commit `63203d7`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 46. Inventaire des drapeaux en chemin RÉPARTI : cinq agissent, trois sont inertes

L'audit du §39 avait produit des **candidats** sans les départager (une mesure vide, due à un port
hors bornes, ne prouvait rien). Après le v7, le v8 et les corrections des rounds 20 et 42,
l'inventaire est refait — **nœud relancé à chaque essai** (il sert UNE connexion : mon premier
banc les faisait tous échouer, et c'était encore une erreur de harnais) :

| drapeau | perplexité répartie (référence **72,0185**) | verdict |
|---|---|---|
| `--act-topk 64` | 362 333,58 | **agit** |
| `--qk-topk 64` | 4 760,07 | **agit** |
| `--attn-window 32` | 1 571,30 | **agit** (corrigé au round 42) |
| `--act-thresh 0,01` | 98,83 | **agit** |
| `--ffn-gain 0:0.75` | 76,88 | **agit** (corrigé au round 20) |
| `--attn-topk 64` | 71,47 | **agit** |
| `--swa-pattern 2` | 72,0185 | **sans effet — ATTENDU** : le motif ne décide quelles couches prennent la fenêtre ; sans `--attn-window`, il n'a rien à décider |
| `--sans-fenetre` | 72,0185 | **sans effet — ATTENDU** : désactiver une fenêtre qui n'est pas posée ne change rien |
| `--moe-topk 2` | 72,0185 | **sans effet — ATTENDU** : Qwen2.5-0.5B est **dense**, il n'a pas d'experts |
| **`--attn-sinks 4`** | 72,0185 | **INSTRUIT (§47)** : inerte **sans fenêtre**, attendu ; avec fenêtre 32, 4 puits valent 29,0206 contre **1297,5437** à 0 — et cette ligne « 0 » n'existait pas : le garde avalait le zéro |

**Six drapeaux agissent sur dix**, et **trois des quatre inertes le sont pour une raison
identifiée** (conditions non remplies : pas de fenêtre posée, pas d'experts). Reste **un seul
candidat ouvert**, nommé : `--attn-sinks`.

**Ce que cet inventaire vaut** : c'est la réponse à la question posée au §39 — « combien d'autres
drapeaux ne font rien en réparti ? » — et elle est **chiffrée**, pas estimée. Les deux vrais
défauts qu'elle a fait apparaître (`--ffn-gain`, `--attn-window`) ont été corrigés et **mesurés
avant/après** aux rounds 20 et 42.

### 46 bis. Le dernier candidat est instruit — et c'est le plus grave des cinq

> **CORRIGÉ — voir §47.** La conclusion ci-dessous (« lu nulle part ») est **FAUSSE** : le
> compteur **est** lu dans la branche à fenêtre (`model.rs:7472`, `:7490`). Le refus qui allait
> être livré sur cette base a été **retiré avant d'être committé**. Le texte est conservé comme
> trace de l'erreur : deux nombres égaux (`0` et `4`) qui ne mesuraient pas la même chose, et une
> mesure d'inertie faite dans la configuration où l'inertie est attendue.

`--attn-sinks 4` n'agit **pas** en réparti. Instruit : il n'agit **pas non plus en local**
(14,6496 dans les deux cas). La lecture du code donne la réponse, et elle est nette :

```text
main.rs:1036   --attn-sinks N   →  o.attn_sinks = N
main.rs:1227   run_infer        →  if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
main.rs:7114   run_ppl          →  if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
main.rs:4425   run_ppl_reparti  →  mdl.attn_sinks = opt.attn_sinks;      (round 42)
model.rs:2961  Act::appliquer   →  m.attn_sinks = self.attn_sinks       (protocole v7)
```

**Le champ `Model.attn_sinks` est écrit dans les trois chemins d'exécution, transporté par le
protocole v7… et LU NULLE PART.** Aucune occurrence de `self.attn_sinks` dans le calcul : ce sont
les puits **appris** (`lay.sinks`, le tenseur `attn_sinks.weight`) qui sont consommés par
l'attention (lignes 5591, 5624, 5653), pas ce compteur.

**C'est le cinquième défaut de la même famille** — après `--ffn-gain` en réparti (round 20), le
poids de greffe par défaut à zéro (round 15), `--attn-window` (rounds 23-42) et le `sys.exit` qui
sortait en 1 (round 13) — **et c'est le plus grave**, parce que le drapeau a été **transporté par
un protocole** (une modification de version, 91 → 99 octets) avant qu'on s'aperçoive qu'il ne
pouvait rien faire : le v7 a fait voyager un réglage **mort**.

**Deux issues, et le choix est un choix de conception** : (1) **implémenter** le compteur — `n`
jetons puits au début de la séquence, comme le décrit `model.rs:2435` — ce qui est un vrai
mécanisme d'attention (et différent des puits *appris*) ; ou (2) **retirer le drapeau**, car un
drapeau qui ne peut rien faire est pire qu'aucun drapeau : il donne l'illusion d'un réglage. Dans
les deux cas, la **porte** doit suivre : elle doit exiger que le drapeau **agisse**, ou qu'il
n'existe plus.
