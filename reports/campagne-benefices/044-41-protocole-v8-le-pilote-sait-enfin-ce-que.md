> Campagne : **campagne-benefices** · expérience **41**
> Titre : 41. Protocole v8 : le pilote sait enfin ce que coûte la moitié distante
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 41. Protocole v8 : le pilote sait enfin ce que coûte la moitié distante

Les paires sont calculées par **le nœud** ; le pilote ne pouvait donc rien borner sans qu'elles
lui soient transportées. Le v8 ajoute **un `u64` à l'en-tête** (91 → **99 octets**, version
**8**), que le nœud remplit avec son compte cumulé et que le pilote lit.

**Ce que le pilote affiche maintenant** (12 couches locales, 12 distantes, 48 pas) :

```text
paires du pair    : 8408924160 au total, 178.9 M par pas (annoncées par le nœud dans chaque trame)
```

**178,9 M paires par pas pour la moitié distante** — cohérent avec les **358 M par jeton** du
modèle entier mesurés pendant la campagne (§21) : la moitié des couches, la moitié des paires.
C'est la première fois que le pilote sait ce que coûte la moitié distante **sans le déduire de
son propre travail**.

**Et le chiffre a attrapé mon propre bug.** Première implémentation : j'**additionnais** le
compte de chaque trame. Or le compteur du nœud est **cumulatif depuis le premier pas** — la
somme des cumuls vaut N²/2, et le pilote annonçait **4 293,9 M par pas**, soit ~24× trop (47
pas). C'est **la comparaison avec le chiffre connu** (358 M pour le modèle entier) qui l'a rendu
visible : un nombre 12× supérieur à celui du modèle COMPLET, pour la moitié de ses couches, ne
pouvait pas être juste. Corrigé (`fetch_max` au lieu de `fetch_add`) : 178,9 M par pas.

**La leçon est celle du sprint** : un chiffre nouveau n'est pas vérifié par sa propre cohérence,
il l'est par **comparaison à ce qu'on sait déjà**. Sans les 358 M de la campagne, 4 293,9 M
serait passé pour une mesure.

**Vérifications** : `porte-flux.sh` **vert** (les deux côtés, cinq modes), **122 tests verts**.
