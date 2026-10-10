> Campagne : **toutes-langues** · expérience **08**
> Titre : 8. La courbe de dose complète : elle NE sature PAS
> Date réelle : **2026-10-06 00:22 HAE** (source : commit `0613445`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 8. La courbe de dose complète : elle NE sature PAS

Troisième point ajouté (60 langues, sous-ensemble strict de la dose 112 — même
graine). Même validation, même test, seul le nombre de langues d'apprentissage
change.

| langues | fid TEST | constante | **écart à la constante** | écart oracle TEST | écart oracle VAL |
|---:|---:|---:|---:|---:|---:|
| 30 | 0,7029 | 0,6907 | **+0,0122** | +0,0347 | +0,0240 |
| 60 | 0,7058 | 0,6928 | **+0,0130** | +0,0343 | +0,0237 |
| 112 | 0,7105 | 0,6955 | **+0,0150** | +0,0299 | +0,0231 |

### Ce que la courbe dit

**Le gain marginal par langue AUGMENTE au lieu de diminuer** :
2,7·10⁻⁵ par langue de 30 à 60, puis **3,8·10⁻⁵** de 60 à 112. Une courbe qui
sature ferait l'inverse. **Pousser jusqu'à 392 langues devrait donc continuer de
payer** — ce qui justifie la phase en cours.

**Et l'écart de transfert se réduit régulièrement** : oracle TEST +0,0347 → +0,0343
→ **+0,0299**, oracle VALIDATION +0,0240 → +0,0237 → +0,0231. Plus de langues
réduisent donc aussi la distance entre ce que nos caractéristiques contiennent et
ce que la lecture en extrait.

**Ce que cela corrige** : j'avais conclu, sur la plage 20-30-36 langues, que le
nombre de langues **ne comptait pas**. C'était vrai *dans cette plage* — l'effet y
est sous le bruit — et faux au-delà. Une conclusion tirée d'une plage trop étroite
ne vaut que pour cette plage.

### Réserve, toujours la même

Le test ne compte que **9 langues** à ce stade (41 quand les 392 seront tracées).
C'est pourquoi l'**écart à la constante** est le chiffre à regarder : il corrige la
difficulté du panel, qui varie d'une dose à l'autre (la constante passe de 0,6907
à 0,6955 sans que le modèle change).


---
