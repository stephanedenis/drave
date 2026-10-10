> Campagne : **toutes-langues** · expérience **45**
> Titre : 45. Premier corpus MULTI-DOMAINE et ALIGNÉ : 482 articles Wikipedia en 6 langues
> Date réelle : **2026-10-06 14:02 HAE** (source : commit `48aa0d9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 45. Premier corpus MULTI-DOMAINE et ALIGNÉ : 482 articles Wikipedia en 6 langues

### 45.1 Ce que la machine contenait et qui n'avait pas été utilisé

Dix bases **Wikipedia décompressées**, 30 Go au total, dans
`data/wikipedia/db/*.db` : arabe, allemand, anglais, espagnol, français, italien,
japonais, portugais, russe, chinois. Chacune porte, par article, son **résumé**
(2 000 caractères), indexé par titre.

C'est exactement le « grand corpus multilingue » que l'objectif demande, et il était
là depuis le début. Le pont n'avait travaillé que sur l'UDHR — **un seul texte**,
juridique et répétitif.

### 45.2 Comment on apparie sans être aligné

Wikipedia n'est pas aligné : les articles diffèrent d'une langue à l'autre. Mais un
article donné existe souvent **sous le même titre** dans plusieurs langues quand ce
titre est un nom propre ou un internationalisme (« Albert Einstein », « Albedo »,
« Achilles »). On garde donc les titres présents dans **toutes** les langues visées.

Rendement mesuré sur 400 titres anglais tirés au hasard :

| langue | présents | | langue | présents |
|---|---:|---|---|---:|
| fr | 173/400 | | ru | **39/400** |
| de | 179/400 | | zh | **27/400** |
| es | 142/400 | | ja | **22/400** |
| it | 182/400 | | ar | **1/400** |
| pt | 149/400 | | | |

**Les écritures non latines transcrivent les noms** : l'appariement par titre y est
stérile (1 sur 400 en arabe). Le corpus aligné est donc bâti sur les **six langues
latines** ; arabe, chinois, japonais et russe restent disponibles pour la fidélité et
le transfert, **pas** pour l'invariance.

### 45.3 Le corpus, mesuré

Sur 4 000 titres anglais candidats (résumé > 900 caractères), **483 tiennent dans les
six langues (12 %)**. Écrit dans `corpus/wiki_apparie/` :

| langue | articles | caractères | moyenne par article |
|---|---:|---:|---:|
| en | 482 | 961 174 | 1 994 |
| fr | 482 | 942 809 | 1 956 |
| de | 482 | 948 858 | 1 969 |
| es | 482 | 940 144 | 1 951 |
| it | 482 | 944 789 | 1 960 |
| pt | 482 | 923 709 | 1 916 |

**2 892 fichiers, ~5,7 millions de caractères.** Contre l'UDHR : **un** texte de
~1 300 jetons.

### 45.4 Pourquoi cela change ce qu'on peut mesurer

**1. Le multi-domaine.** L'UDHR est mono-domaine : l'hypothèse « le vocabulaire dépend
du domaine » n'y était **pas testable** (§25). Ici, 482 articles couvrent la science,
l'histoire, la géographie, les personnes — et chaque article est traduit. On peut donc
enfin séparer **ce qui vient de la langue** de **ce qui vient du domaine**.

**2. Le professeur est plus riche.** 2 000 caractères d'encyclopédie par article,
contre un texte juridique répétitif. Le vocabulaire et la syntaxe sont bien plus
variés.

**3. Six langues latines proches** — un cas de contrôle utile : si l'invariance est
déjà imparfaite entre six langues apparentées, elle ne peut pas être meilleure entre
familles éloignées.

### 45.5 Un gain de traçage, vérifié octet à octet

Puisque la couche 8 est la cible retenue (§44), il est inutile d'**exécuter** les 24
couches du professeur. `--couches 0:9` n'exécute que 0..8.

**Vérifié, et pas supposé** : sur `en_Albert_Einstein` et `de_Albert_Einstein`, la
trace produite avec `--couches 0:9` est **identique OCTET À OCTET** à celle produite
avec `--couches 0:24` — même MD5 (`400c4a1ed58700bbc59a6848d02ae757` pour l'anglais).
Et c'est **1,6× plus rapide** : 15 s contre 24 s.

C'est la troisième fois de la session qu'une optimisation est vérifiée par identité
plutôt que supposée — après `--ctx` et la vectorisation de `nait`.

### 45.6 Le traçage est lancé

**2 892 traces** à ~16 s, soit **~13 heures**. Elles sont analysables par lots au fur
et à mesure ; la chaîne écrit son journal dans `/tmp/trace_wiki_apparie.log` et se
termine par `TERMINE` (garde `grep -qx`, pas de correspondance de sous-chaîne).


---
