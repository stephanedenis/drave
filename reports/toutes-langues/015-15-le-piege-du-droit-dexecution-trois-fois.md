> Campagne : **toutes-langues** · expérience **15**
> Titre : 15. Le piège du droit d'exécution, trois fois de suite
> Date réelle : **2026-10-06 04:00 HAE** (source : commit `43adee1`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 15. Le piège du droit d'exécution, trois fois de suite

**Ce qui s'est passé.** Romeo a terminé ses 48 scènes (24 anglais + 24 français,
appariement parfait vérifié). Mais Wikipedia **n'a pas démarré**, et son guetteur
n'était plus vivant.

**La cause** : trois scripts créés par l'outil d'écriture avaient le mode
`-rw-------` — donc **non exécutables** : `trace_wiki.sh`, `trace_unites.sh`,
`analyse_final.sh`. Or `wiki_apres.sh` faisait `exec /tmp/trace_wiki.sh`, qui exige
le droit d'exécution. L'échec est **silencieux** : le guetteur meurt, la phase ne
démarre jamais, et rien ne le signale.

**Pourquoi je ne l'avais pas vu** : j'avais vérifié la **syntaxe** de ces scripts
avec `bash -n`. Or `bash -n` teste la syntaxe, **pas** le droit d'exécution. C'est
exactement la même confusion que deux tours plus tôt, avec `nohup` et
`Permission denied` redirigé vers `/dev/null`.

**C'est la troisième fois** qu'un défaut de plomberie me coûte du temps dans ce
parcours — après le `chmod +x` manquant et le drapeau sans effet. Les trois avaient
la même signature : **ça a l'air de tourner, donc je crois que ça marche.**

**Corrigé à la racine**, pas au cas par cas :

1. les huit scripts sont maintenant exécutables (`chmod +x`) ;
2. **et** les `exec /tmp/x.sh` sont devenus `exec bash /tmp/x.sh` — passer par
   `bash` rend le droit d'exécution **inutile**, donc le piège ne peut plus se
   reproduire même si un script est recréé par l'outil d'écriture.

C'est la différence entre réparer un symptôme et supprimer la cause. La première
correction aurait suffi aujourd'hui ; la seconde protège les prochains scripts.


---
