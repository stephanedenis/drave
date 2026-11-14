# B13 — le pronom sujet est un GN : F1 0,6519 → 0,7013, attachement préservé

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-07 · **Verdict** : ✅
> **La plus grosse erreur de segmentation** était la convention : le gold segmente le **pronom
> sujet** comme un **GN** (« Il | a couru »), le bloc le laissait dans le GV — **417 GN manquants**
> et **333 GV en trop**. La règle (un pronom sujet devant un verbe émet un GN, le GV commence
> après) fait passer la **F1 de 0,6519 à 0,7013** (+4,9), sans perdre un seul attachement :
> **236/237, couverture 0,9916**. **dev 0,6986 / test 0,7073** ; **183/183**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> branche GV), [`autotest.py`](../tools/pensee/autotest.py) (7 assertions) ; JSON
> [`pensee-gn-pronom-sujet.json`](pensee-gn-pronom-sujet.json).

## 1. La règle

```python
# un pronom sujet devant le verbe est un GN (« Il | a couru ») — convention du gold
if (typ == "mot" and langue == "fr" and n in SUJETS and i + 1 < len(mots)
        and (est_verbe(mots[i+1][0], mots[i+1][2])
             or _normaliser(mots[i+1][2]) in lex.get("AUX", set())
             or _normaliser(mots[i+1][2]) in {"ne", "n'", "n’"})):
    segments.append({"type": "GN", "role": "agent", ...})
```

La **garde de langue** est essentielle : sans elle, le « on » anglais (« We leave on vacation »)
devenait un GN et le GP était perdu (r070).

## 2. Avant / après

| mesure | avant | français seul | **+ anglais** |
|---|---:|---:|---:|
| F1 syntagmes | 0,6519 | 0,7013 | **0,7438** |
| F1 dev / test | 0,6482 / 0,6601 | 0,6986 / 0,7073 | **0,7438** |
| exact / labels | 236/237 | 236/237 | **236/237** |
| couverture | 0,9916 | 0,9916 | **0,9916** |
| tête | 0,7709 | 0,8141 | **0,8561** |

**L'anglais** a ses propres pronoms sujets (`i, you, he, she, it, we, they`) : la même règle lui
donne **+4,25 points de F1** (0,7013 → 0,7438) sans perdre un attachement.

**Le nom propre sujet** (« Marie lit », « Paris brille ») suit la même convention : un mot à
majuscule initiale devant un verbe émet un GN — **F1 0,7438 → 0,7535**. Total de la règle :
**0,6519 → 0,7535** (+10,2 points), attachement toujours **236/237 (0,9916)**.

**Ce que ça dit** :

- **La convention de segmentation** (le pronom sujet est un GN) valait **4,9 points de F1** et
  **+4,3 de tête** : c'était la plus grosse erreur, pas une règle de reconnaissance.
- **L'attachement ne bouge pas** : les cibles du gold qui portaient sur le GV restent trouvées.
- **Le GP anglais** est protégé par la garde de langue.

## 3. Contrôles

- **183/183** portes, **7 assertions** recalées.
- **Test sur dev et test** : les deux montent (0,6986 / 0,7073), pas de surapprentissage.
- **Le cas r264** (SUB « qu'il vient demain ») reste trouvé.

## 4. Ce que ce banc ne dit pas

- **L'anglais** n'a pas la règle (ses pronoms sujets ne sont pas dans `SUJETS`) : à mesurer.
- **Les GN sans pronom** (« Marie lit ») restent manquants (le gold les segmente).
- **La F1** est mesurée sur le gold templaté.

## 4 bis. Les règles **rejetées** (mesurées puis non intégrées)

| règle | effet | décision |
|---|---|---|
| GV arrêté à l'**adverbe final** (« viens ∣ demain ») | F1 0,7535 → **0,7505** | rejetée |
| **rogner le sujet** des GV du générateur S | F1 0,7533 | rejetée (neutre) |
| **ADJ/ADV attributs** (65 segments du gold) | F1 0,7535 → **0,7464** | rejetée (trop de faux) |

## 5. Ce qui pourrait rendre cette fiche fausse

- **la garde fr** : un pronom sujet anglais reste dans le GV ;
- **`SUJETS`** est une liste ;
- **la règle** suppose un verbe à droite.

## 6. La suite

1. **Les GN sujets non pronominaux** (« Marie lit un livre ») : la même convention.
2. **L'anglais** : ses pronoms sujets.
3. **Les GV en trop** (333) : la règle en supprime une part.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — la règle et la garde.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-gn-pronom-sujet.json`](pensee-gn-pronom-sujet.json).
