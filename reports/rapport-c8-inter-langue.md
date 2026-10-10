# C8 — transfert inter-langue : ce que le corpus multilingue dit vraiment (et le piège du corpus PARALLÈLE)

> Campagne : **cerveau** · expérience : tête entraînée sur le français, testée sur un corpus
> multilingue — puis tête entraînée dans ce corpus
> Question : après le transfert réussi à un autre corpus de français (`÷1 730`), la lecture
> apprise traverse-t-elle une **autre langue** ?
> Verdict : **deux résultats, et le second invalide la lecture naïve du premier.**
> (1) **Le transfert depuis le français échoue** : entraînée sur le corpus de campagne, la tête ne
> gagne **rien** sur un morceau multilingue (582 361,83 avant comme après — la meilleure époque
> est l'époque 0). (2) **Dans le corpus multilingue, la tête atteint 3,1005** contre 29,9154 pour
> le modèle complet… **et ce chiffre ne veut pas dire ce qu'il a l'air de dire** : le corpus est
> l'UDHR **parallèle** — le même texte traduit en une centaine de langues —, donc les morceaux
> d'entraînement et le morceau de test **portent le même contenu**. Un adaptateur linéaire ne peut
> pas battre un modèle de 24 couches sur du texte neuf ; il le « bat » ici parce que le contenu
> du test a déjà été vu, dans d'autres langues.
> Date réelle : **2026-10-10 16:05 HAE** · graine fixée, morceau de test exclu de la liste.
> Protocole : `tools/c8_corpus.sh` sur `ids_b2_multilingue.txt` (30 morceaux), puis
> `tools/c8_entrainer_tete.py`.

## 1. Les chiffres

Test : morceau 29 du corpus multilingue (1 024 jetons).

| tête (adaptateur) | entraînée sur | perplexité TEST | modèle complet |
|---|---|---|---|
| empruntée (identité) | — | 582 361,8322 | 29,9154 |
| **entraînée** | corpus de campagne (français, 30 morceaux) | **582 361,8322** — aucun gain | 29,9154 |
| **entraînée** | multilingue, 28 morceaux | **3,1005** | 29,9154 |

Le transfert depuis le français **ne gagne rien du tout** : la meilleure époque est l'**époque 0**,
c'est-à-dire l'identité. S'entraîner sur du français ne donne pas de quoi lire un morceau
multilingue — l'adaptateur s'éloigne même de la solution à chaque époque.

## 2. Le piège : un corpus PARALLÈLE n'a pas de morceaux indépendants

Le corpus est la **Déclaration universelle des droits de l'homme** dans une centaine de langues,
concaténée. Deux morceaux pris à des endroits différents **disent la même chose** : ce ne sont pas
des échantillons indépendants, ce sont **des traductions les uns des autres**.

Conséquence directe : le 3,1005 du tableau n'est pas « le réflexe bat le modèle complet ». Un
adaptateur **linéaire** (896×896) suivi d'une tête **gelée** ne peut pas battre un modèle de
24 couches sur du texte neuf — c'est arithmétiquement exclu. Il obtient ce chiffre parce que le
**contenu** du morceau de test a été vu à l'entraînement, dans d'autres langues. Le chiffre est
donc une mesure de **recopie de contenu**, pas de lecture d'état.

**Le contrôle qui l'aurait dit d'avance** : comparer la perplexité du modèle complet sur le
morceau de test à celle d'un morceau d'entraînement. Si le corpus est parallèle, les deux se
ressemblent ; ici, le modèle complet fait 29,9 sur le test — et un simple adaptateur linéaire
fait 3,1, ce qui est **impossible sans recopie**.

## 3. Ce que ça laisse comme résultat solide

- **le transfert inter-langue, tel que mesuré, échoue** — mais l'expérience mélange deux choses :
  un changement de **langue** et un mélange de **cent langues à la fois** dans l'entraînement. Un
  adaptateur linéaire ne peut pas servir cent langues ; ce n'est pas la même question que
  « français → une autre langue » ;
- **le transfert inter-corpus, lui, tient** (`rapport-c8-transfert-corpus.md` : ÷1 730, coût de
  domaine ×2,6) parce que les deux corpus sont du **français** ;
- **la leçon de protocole est la plus utile** : avant de conclure d'un chiffre de test, vérifier
  que les morceaux sont **indépendants**. Un corpus parallèle, un corpus de paraphrases, un
  document découpé en fenêtres voisines : tous violent l'indépendance, et aucun ne le dit.

## 4. La mesure qu'il faudrait pour trancher

Trois protocoles, du plus propre au plus mêlé :

1. **français → français** : fait (÷1 730), c'est le seul transfert propre mesuré ;
2. **une langue → la même langue, autre corpus** : prendre l'UDHR **en français** d'un côté et la
   prose française de l'autre — même langue, contenus sans rapport ;
3. **français → une autre langue, seule** : entraîner sur du français et tester sur **une** langue,
   une seule (et non sur un mélange de cent) — c'est là que la question « la lecture traverse-t-elle
   une langue ? » a une réponse interprétable.

Le protocole 3 est celui qui manque, et il est faisable avec ce qui est en place : il suffit de
découper `ids_b2_multilingue.txt` **par langue** (le corpus est une langue par ligne) au lieu de le
découper en morceaux consécutifs.
