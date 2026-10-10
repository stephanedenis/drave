> Campagne : **toutes-langues** · expérience **06**
> Titre : 6. Deux erreurs de méthode, et ce qu'elles ont coûté
> Date réelle : **2026-10-05 23:50 HAE** (source : commit `1424c5d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 6. Deux erreurs de méthode, et ce qu'elles ont coûté

**Un « gain de 1,33× » qui n'existait pas.** J'avais lancé un second traçage en
parallèle et mesuré 28,6 s par langue au lieu de 38. En réalité ce second traçage
**n'avait jamais tourné** : `bash -n` vérifie la syntaxe, pas le droit d'exécution,
et `nohup` échouait sur `Permission denied` avec la sortie redirigée vers
`/dev/null`. Le rythme était simplement revenu à la normale après la fin d'une
contention. **Mesuré après correction** : deux traçages = **50 s par langue**, un
seul = **28 s**. La charge montait à 44 sur 40 threads — drave occupe déjà les cœurs
physiques. **Un traçage à la fois est l'optimum sur cette machine.**

**Un guetteur qui aurait attendu indéfiniment.** En modifiant les scripts d'attente
pour exiger la fin des deux traçages, puis en arrêtant le second, je les aurais
bloqués pour toujours. Réparé et vérifié.


---
