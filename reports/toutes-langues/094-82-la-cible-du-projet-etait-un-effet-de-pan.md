> Campagne : **toutes-langues** · expérience **82**
> Titre : 82. LA CIBLE DU PROJET ÉTAIT UN EFFET DE PANEL
> Date réelle : **2026-10-07 11:08 HAE** (source : commit `207ef67`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 82. LA CIBLE DU PROJET ÉTAIT UN EFFET DE PANEL

### 82.1 Ce qui a mis la puce à l'oreille

Le §70 puis le §79 ont fait du **12,001** le chiffre-cible du projet : *« le professeur a un
rapport contenu/langue de 12,001, notre pont est à 2,487 »*. Ce chiffre a servi de boussole
à une dizaine de paragraphes, et il a été recopié dans le bilan et dans la clôture.

En construisant `profil_couches.py` — la sonde qui regarde **par-dessus l'épaule** du
professeur, couche par couche — le même professeur, à la même couche, sur le même corpus,
donnait **1,697**. Un facteur 7. L'un des deux chiffres était faux, ou bien ils ne
mesuraient pas la même chose.

Ils ne mesuraient pas la même chose. Rien dans le chiffre « 12,001 » ne disait **sur quelles
langues** il était mesuré.

### 82.2 Le même professeur, trois panels

482 articles, couche 8, moyenne sur les positions, 896 canaux. **Seul le panel de langues
change** :

| panel | P_lang | P_cont | **RAPPORT** | dim. eff. |
|---|---:|---:|---:|---:|
| **6 langues** (de, en, es, fr, it, pt) | 2 381,8 | 4 041,9 | **1,697** | 49,1 |
| **de/en/fr** (2 germaniques + 1 romane) | 3 347,7 | 4 405,3 | **1,316** | 35,4 |
| **es/it/pt** (3 romanes — le panel du §70) | 387,9 | 4 655,4 | **12,001** | 60,8 |

La ligne `es/it/pt` **reproduit le 12,001 du §70 à la décimale** (387,9 · 4 655,4 · 12,001)
depuis le cache `cache_vf_test.npz` et depuis les traces elles-mêmes. Le chiffre n'était
donc pas faux : il était **muet sur son panel**, et son panel était le plus facile des trois.

**Ce que `P_cont` fait pendant ce temps est instructif** : 4 041,9 · 4 405,3 · 4 655,4 — il
varie de **15 %** à peine. Toute la variation du rapport vient de `P_lang`, c'est-à-dire du
choix des langues. Le contenu, lui, est stable.

### 82.3 Pourquoi les langues romanes gonflent le rapport

`P_lang` est la dispersion des moyennes par langue. Entre l'espagnol et le portugais, cette
dispersion est petite : les deux langues se ressemblent. Entre l'allemand et l'anglais, elle
est grande. En ne gardant que es/it/pt, on divise le dénominateur par 6 sans toucher au
numérateur — et le rapport paraît six fois meilleur.

**Le 12,001 est donc la valeur qu'on obtient en ne comparant que des langues proches.** Ce
n'est pas une propriété du professeur, c'est une propriété de la question posée.

### 82.4 Et la couche 0, pour situer

| panel | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|
| 6 langues | 4 103,5 | 1 221,4 | **0,298** |
| es/it/pt | 1 186,1 | 1 575,3 | **1,328** |
| de/en/fr | 5 564,9 | 1 594,5 | **0,287** |

**L'entrée est dominée par la langue partout** — y compris sur le panel roman, où elle est
seulement à 1,328 contre 12,001 en couche 8. Le professeur, lui, a bien construit la
séparation : c'est le seul point que le panel ne discute pas.

---
