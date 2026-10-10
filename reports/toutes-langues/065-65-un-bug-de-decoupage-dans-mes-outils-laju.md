> Campagne : **toutes-langues** · expérience **65**
> Titre : 65. Un bug de découpage dans MES outils : l'ajustement ne portait que sur DEUX langues
> Date réelle : **2026-10-06 22:24 HAE** (source : commit `1f6dc82`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 65. Un bug de découpage dans MES outils : l'ajustement ne portait que sur DEUX langues

### 65.1 Le bug

Les outils de diagnostic des §57 à §64 découpaient ainsi :

```python
itr = np.arange(len(cltr))
nt = max(1, len(itr) // 3)
iap, ival = itr[nt:], itr[:nt]      # ajustement = dernier tiers
```

Or **les entrées d'un cache sont ORDONNÉES PAR LANGUE** — `de_*` (85), `en_*` (85),
`fr_*` (85). Prendre le **dernier tiers** revient donc à prendre **`en_*` et `fr_*`
seulement** : le bloc entier de la première langue est supprimé.

**L'ajustement portait sur deux langues au lieu de trois**, dans six outils. Le signe
qui aurait dû alerter était dans la sortie du §64 : *« SOUS-ESPACE DE LANGUE : **2
langues** d'apprentissage · la 1re porte **100,0 %** de l'énergie de langue »*. Avec
deux groupes, une covariance inter-langue est de **rang 1** — elle ne peut rien
séparer. J'ai lu ce chiffre, je l'ai rapporté, et je n'en ai pas tiré la conclusion
évidente.

### 65.2 Corrigé, et re-mesuré

On ajuste désormais sur **toutes** les entrées d'apprentissage : le panneau *hors
vivier* est le **cache de test**, pas un sous-ensemble de l'apprentissage. Re-mesure du
diagnostic central (§61) :

| | avant correction | **après correction** |
|---|---:|---:|
| **TEST** notre `P_lang` | 232,0 | **247,1** |
| **TEST** notre `P_cont` | 338,7 | **318,7** |
| **TEST** notre rapport | 1,460 | **1,290** |
| **TEST** professeur (rappel) | 399,2 / 4 356,4 | idem · rapport 10,912 |
| **APPRENTISSAGE** notre `P_lang` | 1 834,7 | **2 161,7** |
| **APPRENTISSAGE** notre `P_cont` | 493,9 | **342,9** |
| **APPRENTISSAGE** notre rapport | 0,269 | **0,159** |
| **APPRENTISSAGE** professeur | 2 405,1 / 5 219,9 → 2,170 | **3 402,5 / 4 205,5 → 1,236** |

### 65.3 Aucune conclusion ne change — et c'est ce qu'il faut vérifier

| conclusion | tient-elle ? |
|---|---|
| Le défaut est la **famine de contenu**, pas l'excès de langue | **oui** — notre `P_cont` reste **13,7× sous** celui du professeur (318,7 contre 4 356,4), notre `P_lang` du même ordre (247,1 contre 399,2) |
| L'énergie de contenu est **récupérable par mise à l'échelle** | **oui** — β=3 donne `P_cont` **5 099,9** pour une fidélité de 0,4711 (coût 0,0055) |
| L'amplification **déployable** ne change pas le rapport | **oui** — 1,290 **exactement** à tout γ |
| Le défaut existe aussi **dans le vivier** | **oui** — rapport 0,159 à l'apprentissage contre 1,236 pour le professeur |

**Les quatre conclusions du diagnostic survivent à la correction.** C'est la raison
pour laquelle la correction est rapportée en détail plutôt que discrètement : un
chiffre faux qui ne change aucune conclusion reste un chiffre faux, et la prochaine
mesure qui s'appuiera dessus n'aura pas la même chance.

### 65.4 Ce que cela change pour la suite

Le **rapport du professeur lui-même** passe de 2,170 à **1,236** sur le panneau
d'apprentissage selon que celui-ci compte deux ou trois langues. **La cible dépend donc
aussi du nombre de langues**, pas seulement de leur identité (§60.3). Toute comparaison
« notre rapport contre celui du professeur » doit nommer **le panel et sa composition**
— c'est la troisième fois dans cette série qu'un chiffre de référence se révèle
dépendre du périmètre.

### 65.5 La règle que j'aurais dû appliquer

**Un découpage par position n'est un découpage aléatoire que si l'ordre est
aléatoire.** Les caches sont triés par langue ; prendre « le dernier tiers » n'est pas
prendre « un tiers au hasard », c'est prendre **deux langues sur trois**. Un `ival` par
**stride** (`itr[::7]`, comme le fait `profil_langues.py`) aurait été correct ; un
`ival` par **bloc contigu** ne l'était pas.

C'est la quatrième fois de la session qu'une hypothèse de forme régulière — ici, que
l'ordre des entrées est indifférent — se glisse dans un outil de mesure.


---
