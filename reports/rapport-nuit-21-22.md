# La nuit du 21 au 22 novembre — ce qui a été mesuré, écrit, committé

> **Ce que ce document est.** La **synthèse** de la session de nuit (21/11 20 h → 22/11 08 h) :
> les tranches, les chiffres, les verdicts, et ce qui reste ouvert. Chaque tranche a sa **fiche**
> (le lien) et son **commit**. Le récit daté est dans [`journal/`](../journal/).

## 1. Les tranches (18 commits)

| # | tranche | le résultat | la fiche |
|---|---|---|---|
| 1 | **le moteur de pensée — l'anti-boucle** | 5 gardes (visited, nouveauté, échecs, 3 terminaisons, trace), **5/5 invariants** | [`rapport-anti-boucle.md`](rapport-anti-boucle.md) |
| 2 | **les stratégies** | BFS, DFS, glouton ; **6/6 invariants** | — |
| 3 | **le branchement sur l'interface RSN** | 13 nouveaux, 11 répétitions évitées | — |
| 4 | **le branchement testé** | 2 paradigmes, la même structure — **7/7** | — |
| 5 | **la passerelle annotation → interface** | 51 affirmations typées, 0,796 de degré moyen | — |
| 6 | **le banc du 100 M (3 k)** | 0,882 mots, répétition 6 | [`rapport-banc-generation.md`](rapport-banc-generation.md) |
| 7 | **le run du 100 M (30 k)** | PPL 2,944, **hypothèses écrites d'avance** | [`rapport-100m-30k.md`](rapport-100m-30k.md) |
| 8 | **le résultat du 30 k** | 0,501 mots (l'hypothèse était ≥ 0,90) — **le sur-apprentissage** | idem |
| 9 | **la passe des portes** | **89 portes, 87 vertes**, 2 rouges structurelles | [`rapport-portes-rouges.md`](rapport-portes-rouges.md) |
| 10 | **le diagnostic des 2 rouges** | `melange` ne calibre pas, `indice` ne conclut pas | idem |
| 11 | **la cause commune** | les deux testent **Qwen2.5-0.5B** — un modèle de démonstration | idem |
| 12 | **le terrain** | `models/` n'a que le 0,5 B — rouge par construction | idem |
| 13 | **la leçon opérationnelle** | le **3 k** est la référence, le **30 k** le témoin | [`rapport-100m-30k.md`](rapport-100m-30k.md) |
| 14 | **le banc 612** | 602 phrases du gold gelé, 0,755 mots | [`rapport-banc-612.md`](rapport-banc-612.md) |
| 15 | **le témoin 30 k** | 0,763 (la continuité) mais 29 non-UTF-8 (la dérive) | idem |
| 16 | **le 34 M** | 0,666 (le classement : 100 M bat le 34 M de 9 points) | idem |
| 17 | **la RSN à 3 niveaux** | le noyau, les faits, les affirmations (Nipada) | [`rsn-3-niveaux.md`](../docs/theorie/rsn-3-niveaux.md) |
| 18 | **l'interface RSN** | 5 verbes, 6 paradigmes, **3 adaptateurs conformes** | [`rsn-interface.md`](../docs/theorie/rsn-interface.md) |

## 2. Les trois résultats mesurés qui comptent

**A. L'échelle paie par jeton vu, pas par taille.** Sur le **même banc** (602 phrases du gold
gelé), le 100 M à 3 000 pas (0,755) **bat le 34 M à 30 000 pas** (0,666) — avec **30× moins de
jetons vus** (0,24 jeton/paramètre contre 7,2).

**B. La dérive est un problème de données, pas de taille.** Le 100 M à 3 000 pas est **propre**
(0 octet non-UTF-8) ; à 30 000 pas il **dérive** (29). Le ratio données/paramètres (30 tokens/param
au lieu de 7) est la cause, pas le modèle.

**C. Deux bancs, deux vérités.** Le banc de style (20 prompts) mesure la **créativité** — le 3 k
gagne (0,882 contre 0,501). Le banc 612 mesure la **continuité** — le 30 k gagne (0,763 contre
0,755). **Un banc unique mentirait.**

## 3. Les deux portes rouges — closes, comprises

`porte-melange` et `porte-indice` testent **Qwen2.5-0.5B** : aucune position ne porte le code, la
mémoire ne conclut pas. **Ce n'est pas un bug, c'est un modèle trop petit.** Les rendre vertes
demande de **télécharger un modèle** — une décision humaine (règle 11).

## 4. Ce qui reste ouvert (le prochain chantier)

1. **La donnée du natif** : le palier 1 (100 M) reste plafonné par le corpus (1 Go, ~30
   tokens/paramètre au 30 k). Le **même 100 M avec 10× plus de données** est le test décisif — la
   prédiction est écrite (mots > 0,90, répétition ≤ 5, PPL < 2,0).
2. **Le gold de pensée** : toujours absent (le bloc « Pensée » est en pause pour cette raison).
3. **La promotion RSN** : le noyau (`Noyau`) et le vérificateur de dérivations restent à écrire —
   l'interface est prête, le noyau non.

## 5. Les limites de la nuit

- **Aucun appel API** : tout a été local (GPU + CPU), conformément au mode nuit.
- **Les bancs sont des débits et des dérives**, pas des jugements de qualité linguistique.
- **Le 100 M reste un modèle de 96,7 M** : il ne compose pas de phrase, même au 3 k (le défaut
  connu du natif, mesuré le 16/11).
## 6. La tranche du palier 1 (ajoutée en fin de nuit)

Le **100 M sur le corpus `corpus_wiki_fr_palier1` (3,44 Go)** — le test de la donnée — est lancé
à 02 h 15, fini à 04 h 42 (**2 h 25**, PPL 3,073), et **mesuré** sur le gold 612 :

| modèle | corpus | mots valides | répétition | non-UTF-8 |
|---|---|---:|---:|---:|
| 34 M | 1 Go (mix) | 0,666 | 3 | 3 |
| 100 M, 3 k | 1 Go (mix) | 0,755 | 3 | 0 |
| 100 M, 30 k | 1 Go (mix) | 0,763 | 3 | 29 |
| **100 M, 30 k** | **3,44 Go (wiki brut)** | **0,854** | **2** | **13** |

**Le palier 1 est franchi** : le **meilleur résultat du natif** (0,854) vient du **plus gros
corpus** — la donnée était le verrou, comme le diagnostic du 16/11 le prédisait. La réserve : la
PPL (3,073) n'est pas comparable (le corpus brut est plus dur que le mix), et les 13 non-UTF-8
montrent que la dérive recule mais ne disparaît pas.
