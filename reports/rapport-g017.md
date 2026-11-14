# B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
> **Verdict** : ❌ **règle rejetée**.
> La règle demandée — **l'adverbe final de temps hors de la SUB** — corrige bien `g017`
> (`that she would come` au lieu de `that she would come yesterday`) et retire un faux positif
> de `g005`, mais elle **casse `r264`** (`qu'il vient demain`) et **`r288`**
> (`that he comes tomorrow`) : **F1 0,7902 → 0,7901 (−0,0001)**, **dev +0,0011**, **test
> −0,0028**, **attachement 237/238 → 236/237**, **couverture 0,9958 → 0,9916**. Les deux cas
> favorables sont en **dev**, les deux cas défavorables en **test** : le gain est in-sample, la
> perte est hors échantillon. **Aucun code de production n'est modifié** ; la porte du bloc
> reste verte, et l'état reste à **237/238**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (lecture seule),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; copies locales dans
> `/tmp/g017/` (`bloc_g017.py` pour la règle, `bloc_adv_large.py`, `bloc_garde.py`,
> `bloc_placebo.py` pour les contrôles) ; **0 fichier du dépôt modifié pour la mesure**.
> JSON : [`pensee-g017.json`](pensee-g017.json).

## 1. Le span et la règle

`g017` — « She said that she would come yesterday. » (hand, anglais). Le gold attend :

| segment | span |
|---|---|
| GN « She » | 0:3 |
| GV « said » | 4:8 |
| **SUB « that she would come »** | **9:28** |

Le bloc prédit la même SUB **avec l'adverbe** : `SUB 9:38` = « that she would come yesterday ».
C'est le **seul label manquant** des 239 cibles (`g017` n'est pas dans `labels`) ; la cible
d'attachement est déjà juste (`said`), donc le défaut est **le span, pas l'attachement**.

**La règle mesurée** : quand le dernier token d'une SUB est un adverbe de `ADVERBES_TEMPS`
(`hier`, `demain`, `aujourd'hui`, `maintenant`, `yesterday`, `tomorrow`, `today`, `now`,
`later`, `soon`, `tonight`) et qu'il est suivi d'une ponctuation ou de la fin, il est retiré du
span. Elle s'applique à **toutes les SUB**, dans toutes les langues, après la boucle de
frontière et avant `segments.append` :

```python
while (j - 1 > i
       and _normaliser(mots[j - 1][2]) in ADVERBES_TEMPS
       and (j >= len(mots) or mots[j][3] != "mot")):
    j -= 1
```

C'est la même classe d'adverbes que la règle du **GV** (`rapport-convention-gv.md` § 3.2), mais
appliquée à la **SUB**. Le gold ne l'entend pas de la même oreille (§ 6).

## 2. La mesure

Gold vivant : **612 phrases**, **239 cibles**. Split déterministe `crc32(id) % 3` : **dev 422
phrases / 163 cibles**, **test 190 / 76**. Base = le bloc courant, sans modification ; règle =
copie locale avec le retrait ci-dessus.

| mesure | base | règle | Δ |
|---|---:|---:|---:|
| **F1 all** | **0,7902** | **0,7901** | **−0,0001** |
| F1 dev | 0,7875 | 0,7886 | **+0,0011** |
| F1 test | 0,7962 | 0,7934 | **−0,0028** |
| précision / rappel (all) | 0,7860 / 0,7944 | 0,7863 / 0,7939 | +0,0003 / −0,0005 |
| tp / fp / fn (all) | 1480 / 403 / 383 | 1479 / 402 / 384 | **−1 / −1 / +1** |
| tête (F1) | 0,9029 | 0,9029 | 0 |
| POS | 0,8625 | 0,8625 | **0 token** (0/3749) |
| **attachement exact / labels** | **237 / 238** | **236 / 237** | **−1 / −1** |
| exact / cibles | 237/239 (0,9916) | 236/239 (0,9874) | −1 |
| **couverture** | **0,9958** | **0,9916** | **−0,0042** |

Par source :

| source | n | F1 base | F1 règle | Δ F1 | attachement base | attachement règle |
|---|---:|---:|---:|---:|---:|---:|
| hand | 20 | 0,9016 | **0,9256** | **+0,0240** | 12/12 (13 cibles) | **13/13** |
| reel | 432 | 0,7857 | 0,7846 | **−0,0011** | 171/171 | **169/169** |
| synthétique | 160 | 0,7888 | 0,7888 | 0 | 54/55 | 54/55 |

Le gain hand vient de `g017` (label gagné) et de `g005` (faux positif retiré) ; la perte reel
vient de `r264` et `r288`, tous deux dans le gold réel.

## 3. Les quatre phrases changées

| phrase | gold | avant | après | effet |
|---|---|---|---|---|
| **g005** « Elle a dit qu'elle viendrait hier. » | SUB 11:28 | SUB 11:28 (exact) + **SUB 11:33** (FP) + GP 29:33 (FP) | SUB 11:28 + GP 29:33 | **−1 FP**, 0 exact |
| **g017** « She said that she would come yesterday. » | SUB 9:28 | **SUB 9:38** (FP) | **SUB 9:28** | **+1 exact, −1 FP, −1 FN** |
| **r264** « Je sais qu'il vient demain. » | SUB 8:26 | **SUB 8:26** (exact) + SUB 8:19 (FP) + GP 20:26 (FP) | SUB 8:19 + GP 20:26 | **−1 exact, +1 FN** |
| **r288** « I know that he comes tomorrow. » | SUB 7:29 | **SUB 7:29** (exact) | **SUB 7:20** (FP) | **−1 exact, +1 FP, +1 FN** |

Bilan : **+1 span gagné** (`g017`), **−2 spans perdus** (`r264`, `r288`), **−1 FP** (`g005`,
`g017`) et **+1 FP** (`r288`). Net : **−1 tp, −1 fp, +1 fn**, exact **−1**.

`g005` mérite une lecture séparée : le bloc produisait **deux** SUB, la courte (11:28, exacte)
et la longue (11:33, avec « hier »). La règle retire la longue et **laisse la courte exacte** :
elle ne change pas le nombre d'exacts, elle retire un faux positif. Le GP « hier » (29:33)
reste un faux positif, que la règle ne touche pas.

## 4. Le test tranche

| moitié | phrases concernées | F1 base → règle | attachement base → règle | couverture |
|---|---|---|---:|---:|
| **dev** | `g005`, `g017` | 0,7875 → **0,7886** (+0,0011) | 161/162 → **162/163** | 0,9939 → **1,0** |
| **test** | `r264`, `r288` | 0,7962 → **0,7934** (−0,0028) | 76/76 → **74/74** | 1,0 → **0,9737** |

Les **deux cas favorables sont en dev** et les **deux cas défavorables sont en test**. Le test
n'a pas servi à régler la règle : le split est un hash déterministe, et la règle a été écrite
pour `g017` seule. Mais le test dit ce que le dev ne peut pas dire : **la règle ne généralise
pas**. C'est le contrôle négatif décisif de cette fiche.

## 5. Contrôles négatifs

| contrôle | F1 | tp / fp / fn | attachement | couverture | lecture |
|---|---:|---:|---:|---:|---|
| **placebo** : retirer le dernier token de toute SUB, sans condition | **0,7107** | 1372 / 626 / 491 | 159/160 | 0,6695 | tronquer au hasard détruit des SUB ; le gain de la règle n'est pas un artefact de troncature |
| **ADV large** : retirer tout `ADV` final, pas seulement les adverbes de temps | **0,7885** | 1476 / 405 / 387 | 233/234 | 0,9791 | la règle large coupe aussi des attributs (« late » sur `r218`/`r313`, « tard » sur `r303`) et, comme la règle demandée, `r264`/`r288` ; `r210` n'est pas coupé (POS de « tard » non `ADV`) : la restriction aux adverbes de temps est nécessaire, mais pas suffisante |
| **variante gardée** : retirer l'adverbe final seulement s'il est passé (`hier`/`yesterday`) et que la SUB est modale/conditionnelle (`would`, `-rait`) | **0,7909** | 1481 / 401 / 382 | **238/239** | **1,0** | elle corrige `g017` et `g005` **sans toucher** `r264`/`r288` ; **non retenue** : c'est une autre règle, réglée sur 2 cas de dev, sans aucun cas de confirmation en test |

La variante gardée est la seule mesurée qui ne casse rien. Elle n'est pas la règle demandée :
elle ajoute une condition sémantique (compatibilité du temps de l'adverbe avec le temps de la
SUB) qui n'est attestée que par **deux** phrases, toutes deux en dev. L'intégrer reviendrait à
choisir une convention sur deux exemples, puis à la faire passer pour une règle. C'est
exactement ce que le dépôt reproche aux règles dessinées sur le gold.

## 6. La convention du gold

Le gold contient **quatre** SUB dont le dernier token est un adverbe de temps, et il ne les
annote pas de la même façon :

| phrase | source | SUB du gold | adverbe final | convention |
|---|---|---|---|---|
| `g005` | hand | « qu'elle viendrait » | `hier` | **exclu** |
| `g017` | hand | « that she would come » | `yesterday` | **exclu** |
| `r264` | reel | « qu'il vient demain » | `demain` | **inclus** |
| `r288` | reel | « that he comes tomorrow » | `tomorrow` | **inclus** |

Quatre autres SUB finissent par un `ADV`, mais ce sont des **attributs** (« il soit **tard** »,
« it is **late** »), pas des circonstants de temps : `r210`, `r218`, `r303`, `r313`. Ils ne
relèvent pas de la même règle ; la version large en casse trois (`r218`, `r303`, `r313`) et
laisse `r210`, dont le POS de « tard » n'est pas `ADV` (§ 5).

Sur la **même construction** — verbe principal + `that`/`que` + sujet + verbe + adverbe final —
le gold donne **2 exclusions contre 2 inclusions**. Aucune règle de surface ne peut satisfaire
les quatre. Ce n'est pas un défaut de l'automate : c'est une **convention non tranchée**, comme
l'adverbe final du GV (`r019`/`r186`, `r051`/`r189` ; `rapport-convention-gv.md` § 2 et § 7).
La différence de rôle (`contenu` pour `g005`/`g017`, `complément` pour `r264`/`r288`) est une
piste, mais elle est portée par deux exemples et le bloc ne produit pas encore cette distinction.

## 7. Ce qui pourrait rendre cette fiche fausse

- **Deux contre deux.** Le verdict repose sur quatre phrases. Si l'une des annotations est une
  erreur locale, la convention change de camp ; le gold doit être relu avant d'en faire une
  règle.
- **Un seul split.** `crc32(id) % 3` est déterministe ; un autre découpage pourrait mettre les
  cas favorables et défavorables du même côté. Le contraste dev/test est net, mais il n'est pas
  une validation croisée.
- **Le test n'est pas aveugle à la règle.** On a vu `g017` et `r264`/`r288` en écrivant la règle ;
  le test n'a pas choisi la règle, il a seulement refusé de la confirmer.
- **La mesure est sur copies.** Le code de production n'est pas modifié ; la règle testée est
  une copie de `_syntagmes_simple`, avec `RACINE` réécrit pour importer `generateur.py`. Une
  intégration réelle devrait être rejouée sur les 183 portes.
- **La variante gardée peut être la bonne règle.** Elle vaut **0,7909** et **238/239** sans
  perte en test, mais sur deux exemples de dev. Si un gold tenu à l'écart la confirme, le rejet
  de la version large ne condamne pas la version étroite.
- **Le compte est un compte de spans.** 237/238 est un dénominateur de labels ; une règle qui
  change un span sans changer le compte ne serait pas vue par le seul agrégat. Le diff des
  quatre phrases est joint pour cette raison.

## 8. La décision

**La règle demandée est rejetée ; elle n'est pas intégrée.** Le bloc reste inchangé, la porte
reste verte, l'attachement reste à **237/238 (0,9958)** et le F1 à **0,7902**. `g017` reste le
**dernier span** du gold, mais ce n'est plus un problème de règle : c'est une **convention à
trancher**.

La suite, dans l'ordre :

1. **Trancher la convention** : soit `g005`/`g017` sont corrigés (inclure l'adverbe final),
   soit `r264`/`r288` le sont (exclure). La décision est un choix d'annotation, pas un ajout de
   code ; elle doit être écrite dans le gold, pas devinée par une règle.
2. **Si la convention est « exclure »**, corriger `r264`/`r288` puis rejouer la règle large ;
   **si elle est « inclure »**, corriger `g005`/`g017` et fermer le span sans règle.
3. **La variante étroite** (passé + modal/conditionnel) est la seule candidate mesurée qui ne
   casse rien ; elle reste à valider sur un gold tenu à l'écart avant toute intégration.
4. **Puis J6.2** : `s065` (la cible fausse). Avec `g017` encore sans label, sa correction
   donnerait **238/239** (238 exacts sur 239 cibles) ; si la convention règle `g017` d'abord,
   elle donnerait **239/239**. Les deux comptes doivent être lus avec leur dénominateur.

## 9. Fichiers

- **Cette fiche** : `reports/rapport-g017.md`.
- **JSON** : [`pensee-g017.json`](pensee-g017.json) — reproduction, règle, mesures all/dev/test
  et par source, quatre phrases changées, convention du gold, contrôles, limites.
- **Mesure** : `/tmp/g017/mesure.py` (non commité) ; copies `/tmp/g017/bloc_g017.py`,
  `bloc_adv_large.py`, `bloc_garde.py`, `bloc_placebo.py`.
- **Lecture seule** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
  [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
  [`gold_split.py`](../tools/tests/linguistique/gold_split.py),
  [`gold.py`](../tools/tests/linguistique/gold.py).
- **Contexte** : [`rapport-convention-gv.md`](rapport-convention-gv.md) § 2–3 (l'adverbe final
  du GV, la convention contradictoire), [`rapport-semaine.md`](rapport-semaine.md) (237/238,
  `g017` et `s065` restants).
