> Campagne : **campagne-benefices** · expérience **34**
> Titre : 34. La porte rouge de répartition : un DÉFAUT DE PORTE, pas un défaut du modèle
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 34. La porte rouge de répartition : un DÉFAUT DE PORTE, pas un défaut du modèle

Le tour de vérification avait laissé **une rouge non expliquée** : `porte-reparti-moteur`,
perplexité entière **321,9623** contre répartie **132,8349** (écart 58,7 %) avec un **flux
bit-exact (0,00e0)**. La porte teste « notre modèle entraîné ici est-il découpable sans
changer un chiffre ».

**Trois hypothèses éliminées par la mesure :**

| hypothèse | test | résultat |
|---|---|---|
| le **routage d'experts** ne survit pas au découpage | même porte sur la variante DENSE (`/tmp/moteur_dense.gguf`) | **échoue aussi** (37,8 %) — ce n'est pas le routage |
| le **transport** altère les états | la porte imprime l'écart de flux | **0,00e0** |
| notre modèle est **intrinsèquement** non découpable | — | contredit par le résultat final, ci-dessous |

**La cause, trouvée en comparant les deux chemins à la main** : le fichier d'identifiants
contient **255 jetons**, et la porte en annonçait **128**. Or les deux chemins fenêtrent
**différemment** :

```text
--ppl          … note les `limit` PREMIERS jetons          → 127 jetons notés (0..127)
--ppl-reparti  … « 256 jetons fournis > limite 128 (ctx 256) : troncature aux 128 derniers »
                                                            → jetons 128..255
```

**La porte comparait donc deux textes différents** — et 37 à 58 % d'« écart de perplexité »
entre deux passages sans rapport est un chiffre parfaitement normal.

**Après correction** (le nombre de jetons est **compté** dans le fichier, plus supposé) :

| modèle | référence entière | répartie | écart |
|---|---|---|---|
| `moteur_dense.gguf` | 173,0196 | **173,0196** | **0,0000 %** |
| `moteur_route.gguf` | 173,0196 | **173,0196** | **0,0000 %** |

**PORTE TENUE — et les deux variantes, dense et routée, sont découpables au chiffre près.**
C'est un résultat du sprint « cerveau » : le modèle entraîné ici (Qwen3-MoE, corpus
d'octets) **survit au découpage**, routage compris, ce que la porte rouge laissait croire
faux pendant deux jours.

**Deux leçons, et la seconde est pour le moteur** : (1) une porte qui échoue doit être
instruite jusqu'à sa cause — celle-ci accusait le modèle, et c'était la porte ; (2)
`--limit` ne veut pas dire la même chose dans les deux chemins (`N` premiers en perplexité,
`N` derniers en réparti) : c'est une **asymétrie de protocole** à connaître, et elle est
maintenant écrite dans la porte qui l'a subie.
