# La PPL du natif n'est pas reproductible — le 2,40 annoncé ne se retrouve pas

> **Ligne de roadmap** : **N4** (la mesure du natif) · **Date** : 2026-11-16 · **Verdict** :
> ❌ **le `ppl_val` 2,40 du checkpoint `mix1024-60k` n'est pas reproductible** avec le corpus
> actuel : les mêmes 1 024 octets de `data/wiki_mix/propre/val.txt` donnent **17,3** (la tête,
> avec le canal) à **22,6** (un autre morceau), et le gold linguistique **18,55**.
>
> **Ce que ce document est.** Une **alerte de reproductibilité**, pas un réquisitoire : le
> chiffre annoncé et le chiffre mesuré diffèrent d'un facteur ~7, et la cause la plus probable
> est que **le corpus a changé** après l'entraînement (le fichier `val.txt` actuel commence
> au milieu d'un mot : « minisation et de l'humanité… »).

## 1. Les chiffres

| mesure | valeur | protocole |
|---|---:|---|
| **le `ppl_val` annoncé** (le `.pt.json`) | **2,4038** | 65 536 jetons, 8 lots × 8 × 1 024, avec le canal |
| la tête du `val.txt` (1 024 octets) | **17,32** | le même fichier, le canal du fichier (`val.canal`) |
| la tête du `val.txt` (sans canal) | **21,63** | le même, sans le canal |
| un autre morceau (les 1 025 derniers d'un bloc de 4 096) | **22,62** | le banc `banc_perplexite_gold.py` |
| **le gold linguistique 612** (avec le canal) | **18,55** (fr **16,03**, en **24,52**) | les phrases du gold, le canal calculé |
| le gold 612 (sans canal) | 18,93 | le même, sans le canal |

**Le facteur** : 17,32 / 2,40 = **7,2×** (la PPL) — soit **4,1 bits/octet** contre 1,26.

## 2. L'enquête

- **Le corpus a-t-il changé ?** Le `val.txt` actuel commence au **milieu d'un mot** (« minisation »
  = « humanisation » sans « hu ») : c'est une **tranche** d'un texte plus grand, pas un début
  propre. La date du fichier et la date de l'entraînement ne sont pas dans le `.pt.json` — **le
  corpus n'est pas épinglé** (ni son sha256 ni sa version).
- **Le canal ?** Il aide (21,63 → 17,32) mais **ne comble pas** l'écart.
- **Le chargement ?** Le checkpoint (127 tenseurs, le `pos.weight` présent, le `NativeModel`) se
  charge **strictement** ; la génération est cohérente avec le banc (les mêmes octets) — ce n'est
  pas un problème de classe.
- **La tête du val** est un morceau **atypique** (la phrase tronquée) ; les autres morceaux sont
  **pires** (22,6), pas meilleurs. Aucun morceau ne donne 2,40.

## 3. La conclusion

**Le 2,40 est invérifiable dans l'état actuel** : le corpus n'est pas versionné, le checkpoint ne
dit pas son sha256 de données, et aucun morceau du fichier actuel ne le reproduit. Ce n'est pas
la faute du modèle : c'est **la faute du protocole de mesure** — un chiffre sans ses données
n'est pas un résultat (la règle 2 du dépôt).

**Ce que ça change pour le plan** ([`natif-plan.md`](../docs/pilotage/natif-plan.md)) : le
**palier 1** doit **épingler le corpus** (le sha256 du train et du val, la date, la version du
nettoyage) **avant** d'entraîner — sinon chaque PPL sera une anecdote. Le banc de génération, lui,
est reproductible : il ne dépend pas du corpus d'entraînement, seulement des prompts et du modèle.

## 4. Ce que cette fiche ne dit pas

- Elle ne dit pas que le modèle est **mauvais** : la PPL annoncée a peut-être été mesurée sur un
  val **différent** (le même corpus, une autre tranche) — c'est probable, et c'est précisément le
  problème : on ne peut pas savoir.
- Elle ne dit pas que **toutes** les PPL du dépôt sont invérifiables : celles des fiches qui
  donnent leur protocole et leurs données le sont (le gold, les bancs).

## 5. La leçon

**Un résultat sans ses données est une rumeur.** Le natif a des chiffres (2,40, 0,87, 6,9 GV) ;
les deux derniers se reproduisent (le banc), le premier non. Le premier pas du palier 1 n'est pas
un modèle plus gros : c'est **un corpus épinglé**.
