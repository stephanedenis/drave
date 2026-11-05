# B13 — le cache du chunker appliqué : ×139 en chunker, ×1 en défaut (S domine)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **181/181 portes** : le **O(n²)** du chunker est supprimé (1+2S → **1**, dans **les deux chemins** depuis le hoisting complet : T178) — `_syntagmes_simple` était appelé
> **1+2S fois** par analyse (3,21/phrase sur le corpus, 193 fois à 320 tokens), il l'est **une
> fois** ; les verbes de GV sont **mémoïsés par span** (`_verbe_gv`). Résultat mesuré : **×139 à
> 160 répétitions** sur le chemin chunker, sortie **identique** (0 différence sur 612 phrases).
> Sur le chemin par défaut, le gain est **×5,8 à 20 répétitions puis ×1,0** : le coût restant est
> chez **S** (`_segmente` appelé deux fois par phrase), pas dans le chunker.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_gv`,
> `cache_gv`, branche chunker hoistée), [`autotest.py`](../tools/pensee/autotest.py) (T178),
> bancs hors dépôt ; fiche amont [coût du chunker](rapport-cout-chunker.md) (A6, cache simulé) ;
> JSON [`pensee-cache-chunker-applique.json`](pensee-cache-chunker-applique.json).

> **Validation indépendante (A11, `rapport-cache-chunker.md`)** : sur l'instantané `6e8430…`,
> le cache complet donne **×11,0 à 160 tokens** (×12,2 en re-mesure), **×18,1–19,5 à 320**,
> **×29–37 à 640–1 280** en chunker ; **×2,06 à 160** en défaut ; l'**égalité est vérifiée**
> 612/612 et 42/42 (7 longueurs × 2 chemins), et un **cache falsifié** est détecté (113/612
> chunker, 290/612 défaut) — le comparateur est sensible. La mémoïsation seule vaut ×5,1 ;
> c'est le cache des verbes de GV qui apporte le second facteur.

## 1. Temps (base de 16 tokens répétée, chemin chunker `segmenter_s=False`)

| répétitions | avant (ms) | **après (ms)** | facteur |
|---:|---:|---:|---:|
| 10 | 47,8 | **4,9** | ×9,8 |
| 20 | 152,9 | **9,8** | ×15,6 |
| 40 | 617,8 | **17,9** | ×34,5 |
| 80 | 2 609,5 | **34,5** | ×75,6 |
| **160** | **9 817,7** | **70,8** | **×138,7** |

## 2. Temps (chemin par défaut, avec le générateur S)

| répétitions | avant (ms) | après (ms) | facteur |
|---:|---:|---:|---:|
| 20 | 157,5 | **27,1** | ×5,8 |
| 80 | 157,3 | 151,2 | ×1,0 |
| 160 | 426,3 | 419,6 | ×1,0 |

**Ce que ça dit** :

- **Le O(n²) du chunker est éliminé** : 1+2S appels → 1, et `_verbe_dans` n'est plus relu pour
  chaque segment (`_verbe_gv` mémoïse par span). À 160 répétitions, ×139.
- **La sortie est identique** : 0 différence sur les 612 phrases, **tous champs** comparés
  (niveau, type, span, valeur, confiance, candidats, meta) — le cache ne change pas une mesure.
- **En défaut, S domine** : `_cibles_s` rappelle `generateur._segmente` après `_syntagmes_s` —
  deux passes S par phrase. Le cache du chunker ne peut pas le réduire ; c'est le prochain levier
  (une seule passe S par analyse).
- **La négative est explicite** : ×1,0 à 80 et 160 en défaut ; annoncer un gain global serait faux.

## 3. Ce que ce banc ne dit pas

- **Le coût de S** : non mesuré ici (A6 le chiffre à part) ; `_segmente` deux fois par phrase.
- **Les phrases réelles** : le corpus (6,13 tokens/phrase) ne gagne que ×1,2 environ.
- **La mémoire** : le cache est local à l'analyse, libéré à chaque phrase.
- **Le tri** `sorted(gvs, key=ecart)` par segment reste O(S·G log G).

## 4. Ce qui pourrait rendre cette fiche fausse

- **le banc** utilise des phrases répétées (même contenu) : le cache y est idéal ;
- **les temps** sont CPU, machine partagée (3 passes, minimum retenu) ;
- **l'égalité** est vérifiée sur le gold, pas sur un corpus arbitraire ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Une seule passe S par analyse** (`_cibles_s` réutilise `_segmente` de `_syntagmes_s`).
2. **Les 8 échecs d'attachement** (vague 3, A9).
3. **Les 94 spans** : demander à S les REL/SUB (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_verbe_gv`, `cache_gv`, hoisting.
- [`autotest.py`](../tools/pensee/autotest.py) — T178, 181/181.
- [`pensee-cache-chunker-applique.json`](pensee-cache-chunker-applique.json) — les temps.
