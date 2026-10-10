> Campagne : **campagne-benefices** · expérience **09**
> Titre : 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs
> Date réelle : **2026-10-08 22:04 HAE** (source : commit `2d57177`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs

La perplexité moyenne ne dit pas si un modèle **retrouve** un fait précis. Test :
un code unique planté dans une botte de foin, à trois profondeurs (10 %, 50 %,
90 %), et une question à la fin. Qwen2.5-0.5B Q8_0, `--infer`, 12 jetons, `temp 0` :

| longueur | profondeur 10 % | 50 % | 90 % |
|---|---:|---:|---:|
| 512 jetons | ✅ | ✅ | ✅ |
| 1 024 | ✅ | ✅ | ✅ |
| 2 048 | ✅ | ✅ | ✅ |
| 4 096 | ✅ | ✅ | ✅ |

**12 configurations sur 12 retrouvent le code**, y compris à 4 096 jetons avec un
modèle de 0,5 B.

**Étendu à 8 192 puis 12 288 jetons le 9 octobre** (`--n 24`, lot de
préremplissage 256, `temp 0`, remplissage `wikitext2_test.txt`, fenêtres décalées,
l'outil confirme « 2 fenêtres distinctes sur 2 sondes ») :

| longueur | profondeur 10 % | 50 % | 90 % | durées |
|---|---:|---:|---:|---:|
| 8 192 jetons | ✅ (7 963 j.) | ✅ (9 224 j.) | ✅ (8 033 j.) | 935 / 1 199 / 954 s |
| 12 288 jetons | ✅ (11 857 j.) | ✅ (12 474 j.) | ✅ (12 601 j.) | 1 815 / 1 964 / 2 055 s |

**18 sondes sur 18 retrouvent le code**, et la portée **triple** (12 288 au lieu de
4 096) sans qu'une seule échoue. C'est la mesure de tâche qui porte la
revendication « contexte long » — la perplexité moyenne, elle, ne dit rien de la
mémoire (§ 20), et le cache KV ne détruit pas l'information jusqu'à 12 288 jetons.

**Réserve, et elle est sérieuse sur les temps** : cette série a tourné **en
parallèle de la campagne** (un défaut d'enchaînement corrigé depuis), donc deux
gros modèles lisaient le disque en même temps. Les **verdicts** (retrouvé/perdu)
n'en dépendent pas ; les **durées** oui — de 26 s à 609 s pour la même taille,
selon ce que le disque faisait à ce moment-là.

---
