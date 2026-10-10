> Campagne : **toutes-langues** · expérience **03**
> Titre : 3. Le découpage : stratifié par écriture, déduit du texte
> Date réelle : **2026-10-05 23:50 HAE** (source : commit `1424c5d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 3. Le découpage : stratifié par écriture, déduit du texte

`tools/decoupe_langues.py` déduit l'écriture des **points de code** du texte
lui-même — pas un choix à la main, donc reproductible et vérifiable.

**22 écritures trouvées, toutes représentées dans le TEST.**

| | langues |
|---|---:|
| **TEST** | **41** (les 22 écritures) |
| VALIDATION | 50 |
| APPRENTISSAGE | **301** |

C'est la réponse directe au biais découvert précédemment : un test **uniquement non
latin** mesurait surtout la **distance typologique**. L'écart de transfert s'était
révélé **2,6× plus grand** sur le test que sur la validation, et cette différence
était entièrement attribuable à l'écriture et à la famille linguistique.

---
