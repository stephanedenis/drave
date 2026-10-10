> Campagne : **campagne-benefices** · expérience **47**
> Titre : 47. `--attn-sinks` : le drapeau VIT, mais seulement avec une fenêtre — et « 0 » n'existait pas
> Date réelle : **2026-10-10 10:07 HAE** (source : commit `85cf49c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 47. `--attn-sinks` : le drapeau VIT, mais seulement avec une fenêtre — et « 0 » n'existait pas

Le §46 bis concluait « écrit partout, transporté par le v7… et **lu nulle part** », et un
**refus** (`code 2`) allait être livré sur cette base. Il a été écrit, vérifié… puis **retiré
avant d'être committé** : la lecture du code le contredisait. `self.attn_sinks` **est lu**, dans la
**branche à fenêtre** de `forward()` (`model.rs:7472`, `:7490`) :

```rust
let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
for t in (0..ns).chain(lo..nw) { sc[t] = point(qh, &kd) * scale; }  // les puits sont NOTÉS
for t in ns..lo { sc[t] = f32::NEG_INFINITY; }                       // le reste est masqué
```

Les `n` premiers jetons restent notés en plus de la fenêtre : c'est le **drain** de l'attention —
à ne pas confondre avec les puits **appris** (`lay.sinks`), qui entrent au dénominateur du
softmax. L'inertie mesurée au §46 avait donc **deux** causes :

1. la mesure avait été faite **sans fenêtre**, la seule configuration où l'inertie est
   **attendue** (`lo` vaut toujours 0, donc `ns` aussi) ;
2. l'égalité `0 ≡ 4` qui semblait la confirmer venait d'un **garde** :
   `if attn_sinks > 0 { mdl.attn_sinks = attn_sinks }` **avalait le zéro**. « 0 » mesurait donc
   **4**, le défaut (`model.rs:4492` : `if fenetre > 0 { 0 } else { 4 }`) — le zéro était
   **inexprimable**.

**Courbe de dose mesurée** (Qwen2.5-0.5B-Q8_0, `ids_0.5B-Q8`, fenêtre 32) :

| puits | perplexité (`--limit 64`) | perplexité (`--limit 128`) |
|---|---|---|
| **0** | **1297,5437** | — |
| 1 · 2 · 8 · 12 | 28,7244 · 28,7682 · 28,8308 · 28,9700 | — |
| **4** (défaut) | **29,0206** | **18,1141** |
| 16 | 28,5286 | 16,3812 |
| **24** | **27,4439** | **15,4339** |
| 32 | 27,4964 | 15,4499 |

Trois résultats qui comptent :

- **zéro puits avec une fenêtre n'est pas un réglage neutre, c'est un modèle cassé**
  (1297,5437 contre 29,0206, ×45) : une attention à fenêtre **sans drain** ne perd pas un peu de
  qualité, elle s'effondre. C'est pour cela que le défaut vaut 4 ;
- **le défaut n'est pas l'optimum** : 24 puits rendent **15,4339** contre **18,1141**, soit
  **−14,8 %** à 128 jetons. Le levier existait, il était **indicible** ;
- **sans fenêtre** : `--attn-sinks 24` → **27,4964**, identique à l'absence de drapeau — inerte,
  **attendu**, et désormais **annoncé** par le moteur (`INERTE ici`).

**Correctif** : `attn_sinks_impose` (l'idiome de `--ctx`/`--threads`/`--abits` — appliquer si le
drapeau a été **donné**, pas si la valeur est `> 0`), aux trois sites d'exécution ; la valeur
**effective** et son origine au tableau de bord (`puits d'attention 4 (défaut)` /
`0 (imposé)`, plus `· INERTES : aucune fenêtre active`) ; un **avertissement** quand le réglage
est imposé sans fenêtre. Après correctif, `--attn-sinks 0` rend **enfin** autre chose que 4 :
1297,5437.

**En réparti** (transporté par le v7, `Act`, offset 87), la porte §9 de `tools/porte-gain.sh` le
vérifie par un test **décisif pour les deux côtés à la fois** : le découpage étant exact, deux
découpages différents sous les mêmes drapeaux doivent rendre le **même** chiffre — mesuré
**65,6625 = 65,6625** (fenêtre 32, 64 jetons, `0-11|12-23` contre `0-3|4-23`), avec la garde
« la fenêtre mord d'abord » (59,0790 sans fenêtre, **+11,1 %** avec). Si le pilote n'appliquait
pas la fenêtre (défaut du round 28) **ou** si le nœud ne la recevait pas (ce que le v7 a corrigé),
les deux découpages fenêtreraient des couches différentes — et divergeraient.
