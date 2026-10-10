> Campagne : **toutes-langues** · expérience **28**
> Titre : 28. Réservoir multi-échelle : gain réel, mais ce n'était pas la cause
> Date réelle : **2026-10-06 08:20 HAE** (source : commit `482240c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 28. Réservoir multi-échelle : gain réel, mais ce n'était pas la cause

### 28.1 L'idée

La quantité de contenu par jeton varie de **6×** selon la langue (1,578 jeton/caractère
en pular contre 0,271 en allemand, §27). Le réservoir n'avait qu'**une** constante de
temps `a = 0,2`, donc **une** échelle de mémoire : la même en jetons, donc jusqu'à 6×
différente en contenu. Je lui ai donné des constantes **étalées logarithmiquement**
de 0,02 à 0,80 (médiane 0,127), une par neurone — même nombre de neurones, coût nul.

### 28.2 Prédiction, écrite avant la mesure

Si la mémoire mono-échelle était la limite, **l'apport propre du pont
(`fidélité − témoin`) devait augmenter préférentiellement sur les langues FAIBLEMENT
fragmentées** — celles où le pont n'apporte rien aujourd'hui (`deu` 0,271,
`pam` 0,332, `tpi` 0,352).

### 28.3 Mesure

| | mono-échelle | multi-échelle |
|---|---:|---:|
| fidélité TEST | 0,5972 | **0,5998** |
| **apport propre** | **+0,0294** | **+0,0320** (+8,8 %) |
| oracle par langue | 0,6935 | **0,6994** |
| apport ↔ fragmentation | +0,8206 | +0,7973 |
| oracle ↔ norme | −0,8368 | −0,8314 |

**37 langues sur 41 s'améliorent**, 4 régressent (`khm` −0,0046, `ell` −0,0025,
`mal` −0,0017, `tam` −0,0006).

Par quartile de fragmentation, le gain est bien plus grand là où le tokeniseur est
**efficace** :

| quartile | fragmentation | gain de l'apport |
|---|---:|---:|
| Q1 (la plus efficace) | 0,37 | **+0,0039** |
| Q4 (la plus hachée) | 1,30 | +0,0017 |

**La direction de la prédiction est confirmée, son amplitude non** : corrélation
(effet ↔ fragmentation) = **−0,2103**, faible. Et le plus gros gain individuel est
`fuf` (+0,0100), qui est la langue **la plus** fragmentée — l'inverse de la
prédiction.

### 28.4 Et surtout : les langues non servies ne sont pas servies

| langue | apport mono | apport multi | effet |
|---|---:|---:|---:|
| **deu** | +0,0133 | +0,0143 | **+0,0010** |
| **heb** | +0,0014 | +0,0023 | **+0,0009** |
| srp | +0,0128 | +0,0144 | +0,0016 |
| jpn | +0,0216 | +0,0219 | +0,0003 |
| kor | +0,0192 | +0,0215 | +0,0023 |

**L'écart entre Q1 (+0,019) et Q4 (+0,055) reste d'un facteur 3.** Le multi-échelle
est un gain général modeste, **pas** le correctif des langues que le pont ignore.
L'hypothèse de la constante de temps unique est donc **écartée comme cause
principale** — mesure faite, pas supposée.

### 28.5 Ce qui est retenu

Le réservoir multi-échelle est **conservé** : +8,8 % sur l'apport propre et +0,0059
sur l'oracle, à nombre de neurones constant et sans apprentissage. C'est un gain
gratuit et vérifié sur 37 langues. Mais il ne dispense pas de chercher la vraie
cause pour `deu`, `heb`, `jpn`, `kor`, `srp`.

Implémentation : `Pont.a_min` / `Pont.a_max` / `Pont.a_neur` (`tools/pont_generatif.py`),
propagés dans `nait`, `recalcule` et `compacte` — une constante de temps qui ne
suivrait pas le neurone à l'attrition changerait silencieusement la dynamique de
tous les survivants.


---
