> Campagne : **toutes-langues** · expérience **68**
> Titre : 68. Sixième remède écarté : imposer la covariance de la cible
> Date réelle : **2026-10-06 23:16 HAE** (source : commit `7c3413d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 68. Sixième remède écarté : imposer la covariance de la cible

Si le rapport ne dépend que des directions, la **matrice de covariance** du professeur
les contient. On construit donc une transformation linéaire `A` qui donne à notre sortie
la covariance de la cible :

```
A = C_Y^(1/2) · C_O^(-1/2)        (apprise sur l'apprentissage, matrice fixe de 896×896)
sortie corrigée = (O − m_O)·Aᵀ + m_Y
```

Purement linéaire, en forme fermée, déployable, sans étiquette ni regroupement.

| mélange | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0,00 | **0,4704** | 42,4 | 82,1 | **1,934** |
| 0,25 | 0,4486 | 139,6 | 254,7 | 1,825 |
| 0,50 | 0,4107 | 329,2 | 596,0 | 1,810 |
| 0,75 | 0,3725 | 611,4 | 1 105,9 | 1,809 |
| 1,00 | 0,3395 | 986,1 | 1 784,5 | **1,810** |
| | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport BAISSE (1,934 → 1,810) au lieu de monter vers 10,912**, et la fidélité
s'effondre (0,4704 → 0,3395).

### 68.1 Pourquoi — et c'est une distinction importante

**La covariance TOTALE ne détermine pas le partage contenu/langue.** `P_cont` et
`P_lang` sont construits sur les **moyennes par entrée** — donc sur la façon dont les
entrées se regroupent, information qui n'est **pas** contenue dans la covariance
globale. Deux corpus différents peuvent avoir la même covariance et des partages
contenu/langue opposés.

Imposer la covariance de la cible fixe donc l'**enveloppe** de second ordre sans fixer
la **structure de groupes** — et c'est cette dernière qui fait le rapport.

### 68.2 Un chiffre au passage, qui confirme le §61

**Trace de la covariance : notre sortie 18 285, la cible 248 429 — un rapport de
13,59.** Notre sortie porte 13,6 fois moins d'énergie totale que sa cible. C'est une
**troisième mesure indépendante** du même défaut, après le rapport
`‖écart‖/‖moyenne‖` du §60.1 (0,291) et la décomposition du §61 (`P_cont` 13,7× plus
faible). Les trois concordent.

### 68.3 Un point de méthode sur la régularisation

`C_O` est mal conditionnée (nos sorties sont très corrélées) : `C_O^(-1/2)` peut
amplifier du bruit. Un plancher de `1e-3 × trace/ncanaux` a été posé, et **il est
affiché** — un résultat obtenu avec une régularisation non déclarée n'est pas un
résultat. Le plancher vaut ici `2,04e-02`.

### 68.4 La série, après neuf moyens

| § | moyen | rapport obtenu | verdict |
|---|---|---:|---|
| — | rien | 1,460 | référence |
| 58 | objectif à deux curseurs | (cible atteinte) | non convexe, non monotone |
| 59 | pondération de la cible | ≈ 1,0 | **écarté** |
| 60 | amplification uniforme | 1,46 (constant) | **écarté** — §67 l'explique |
| 62 | amplification par entrée | 1,46 (constant) | **écarté** — §67 l'explique |
| 62 | `μ_lang` | 0,91 | **écarté** |
| 63 | sous-espace du contenu | 1,50 | **écarté** |
| 64 | **centrage de l'entrée** | **1,871** | **retenu** |
| 65-66 | **+ retrait du sous-espace de langue dans les états** | **3,064** | **retenu** |
| 68 | covariance de la cible | 1,810 | **écarté** |
| | *professeur* | *10,912* | *la cible* |

**Neuf moyens, sept écartés, deux retenus et combinés.** Le rapport est passé de 1,46 à
3,06 — **28 % de la cible** — et l'on sait maintenant *pourquoi* les amplifications ne
peuvent pas faire mieux : c'est une identité mathématique, pas une limite d'essai.


---
