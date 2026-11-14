# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne

> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
> le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
> le seul gold réel 432 : lire le chiffre avec sa source.

## 1. Ce qui est livré

```bash
python3 tools/drave.py analyser "Le chat dort." --tagger          # POS par l'API, syntagmes heuristiques
python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
python3 tools/drave.py evaluer --tagger                            # heuristique + cascade API + Δ
python3 tools/drave.py evaluer --tagger --par-langue --json
```

- **La clé** est lue dans `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`, puis
  `DEEPSEEK_API_KEY` (`DSH_KEY_FILE` / `DSH_API_KEY` en repli). **La clé n'est jamais affichée**,
  ni dans le message d'erreur, ni dans le JSON, ni dans le cache.
- **Sans clé** : message clair sur `stderr`, **code 4**, rien sur `stdout`. Le défaut reste
  l'heuristique hors ligne.
- **Le cache** : chaque tagger a un cache mémoire par `(texte, langue)` ; le client a son cache
  disque (`modèle + messages + température + max_tokens`, jamais la clé). Deux analyses du même
  texte **ne refont pas d'appel** — vérifié par un test et par la seconde passe du CLI
  (40 appels transport, **0 réseau**, **0 token**).
- **La fusion** : `pos → neuronal`, `syntagme → heuristique`, `pragmatique → heuristique`,
  `seuil 0,6`. Le tagger ne rend ni rôle ni cible ; forcer ses syntagmes ferait perdre
  l'attachement mesuré du produit. Le gain porte sur le **POS**, pas sur les syntagmes.

## 2. Le dispositif

- **20 phrases** : les 20 premières de `tools/tests/linguistique/gold.json` (source `hand`),
  **105 tokens** ; le même gold pour les deux lectures.
- **API DeepSeek** (`deepseek-chat`, température 0), via `tools/llm/deepseek.py` ; **cache neuf**
  (`/tmp/drave-tagger-option-cache`) : aucun rejeu des réponses du 2026-11-13.
- **Deux appels par phrase** : `NeuronalLLMPOS` + `NeuronalLLMChunks` dans
  `NeuronalLLMCompose`, puis `Cascade(heuristique, compose, seuil=0,6)`.
- **La mesure de référence** est [`reports/tagger-612.json`](tagger-612.json) (612 phrases,
  3 179 tokens, 2026-11-13 22:21) : elle donne le chiffre publié et sa ventilation par source.
- **Les contrôles négatifs** : classe POS tirée au hasard (graine 0) et classe majoritaire, sur
  les 105 tokens ; plus le **défaut** comparé octet pour octet à l'heuristique.

## 3. Les résultats

### 3.1 Les 20 phrases `hand`

| mesure | heuristique | cascade `--tagger` | Δ |
|---|---:|---:|---:|
| **POS** (105 tokens) | 0,8857 | **0,9714** | **+8,57 pts** |
| POS fermé | 0,8772 | 0,9474 | +7,02 pts |
| POS ouvert | 0,8958 | 1,0000 | +10,42 pts |
| SYNTAGMES F1 | 0,9016 | 0,9016 | 0 |
| tête F1 | 0,9739 | 0,9739 | 0 |
| attachement exact | 0,9231 | 0,9231 | 0 |
| acte | 1,0000 | 1,0000 | 0 |

**Lecture.** La cascade ne remplace que le POS : les syntagmes, la tête, l'attachement et la
pragmatique sont **identiques** à l'heuristique. Le POS fermé gagne **+7,02**, l'ouvert
**+10,42**. La ponctuation (`PONCT`) n'est pas rendue par le tagger (il ne reçoit que les mots et
les nombres) : elle sort du POS de l'option, mais elle est **hors gold** et ne change pas le
score.

### 3.2 Le coût

| passage | appels | réseau | cache | tokens | durée | modèle renvoyé |
|---|---:|---:|---:|---:|---:|---|
| 20 phrases, **cache neuf** | 40 | 40 | 0 | **11 868** | **39,49 s** (0,99 s/appel) | `deepseek-flash` |
| 20 phrases, **cache chaud** | 40 | **0** | 40 | **0** | 0,05 s | — |
| 612 phrases (référence) | 1 218 | 1 218 | 0 | **358 962** | **1 257,96 s** (~21 min) | `deepseek-flash` |

**Le prix.** ~**0,04 $** pour les 612 phrases (chiffre de la décision) ; au prorata des tokens,
les 20 phrases valent ~**0,0013 $**. Le coût est dominé par les **2 appels/phrase** (~593
tokens/phrase) : le tagger de syntagmes du composite est appelé, mais sa sortie n'est **pas**
utilisée par la fusion (voir § 6).

### 3.3 La référence 612, par source

| source | phrases | heuristique | tagger | Δ |
|---|---:|---:|---:|---:|
| `hand` | 20 | 0,8857 | 0,9714 | +8,57 pts |
| `reel` | 432 | 0,8893 | 0,9360 | **+4,67 pts** |
| `synth` | 160 | 0,7682 | 0,9828 | +21,46 pts |
| **tous** | **612** | **0,8625** | **0,9475** | **+8,49 pts** |

**Lecture.** Le 20 phrases `hand` reproduit **exactement** la ligne `hand` du 612 — même
heuristique, même tagger. C'est une **cohérence**, pas une réplication indépendante : le 20
`hand` est le sous-ensemble le plus facile, et le **+8,49** agrégé est porté par le synthétique
(**+21,46**). Le seul gold **réel 432** ne vaut que **+4,67**. Ne pas annoncer +8,49 sans sa
source.

## 4. Le contrôle négatif

- **Classe tirée au hasard** (12 classes, graine 0) : **10,48 %** ; **classe majoritaire**
  (`VERB`) : **22,86 %**. Le tagger (97,14 %) et l'heuristique (88,57 %) sont très au-dessus :
  le score n'est pas un effet de la distribution des classes.
- **Le défaut est inchangé** : `drave analyser "Le chat dort." --json` sans `--tagger` rend
  **exactement** le JSON de `Heuristique().analyser` (test) ; aucun `--tagger` ne change le
  chemin hors ligne.
- **Le cache** : deux analyses du même texte rendent le même JSON et **un seul** appel par
  tagger (`pos.appels == 1`, `chunks.appels == 1`) — test.
- **La cohérence 612** : le `hand` du 20 vaut 0,8857 → 0,9714, comme la ligne `hand` du 612
  (0,8857 → 0,9714).

## 5. Ce qui pourrait rendre ce résultat faux

- **L'échantillon** : 20 phrases, 105 tokens. Trois erreurs séparent 0,9714 de 0,9429 ;
  l'intervalle est large, et `hand` n'est pas le réel.
- **Le modèle** : `deepseek-chat` demandé, `deepseek-flash` renvoyé sur les 40 appels ; l'API
  peut changer de routage ou de modèle. Le 612 du 2026-11-13 avait le même renvoi.
- **Le cache** : la mesure exige un cache **neuf**. Un cache chaud rejoue les réponses d'un
  ancien modèle — la seconde passe du CLI (0 réseau, 0 token) le montre. Le chiffre mesure donc
  le modèle du jour du cache, pas nécessairement celui de demain.
- **La température 0** n'est pas une garantie de déterminisme de l'API ; le cache disque fige
  chaque réponse, et le rejeu hors ligne est exact.
- **La fusion** : le choix `pos → neuronal, syntagme → heuristique` est **le nôtre**. La
  cascade mesurée du harnais forçait aussi les syntagmes du neuronal ; ici on garde
  l'attachement. Le POS, lui, est le même dans les deux cas.
- **La ponctuation** : le tagger ne reçoit pas `PONCT` ; le POS de l'option a une étiquette de
  moins par ponctuation. Le gold ne la compte pas, le JSON la perd.
- **Un refus du tagger** (le 612 en a **1**, `s015`) rend une annotation sans POS pour cette
  phrase : `analyser --tagger` sort **1** plutôt que de rendre un JSON muet ; `evaluer --tagger`
  le compte (`refus`). La mesure ne masque pas l'échec.

## 6. Les tests et les portes

- [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) : **14 tests**, **aucun
  réseau**. Transport factice (un JSON de POS valide) ; ils verrouillent la substitution des POS,
  la validité **v2** et la lecture **v1**, le cache, le défaut inchangé, le **code 4**, l'ordre
  de la clé et `evaluer --tagger`. `Ran 14 tests … OK`.
- [`tools/tests/test_produit.py`](../tools/tests/test_produit.py) : **18 tests**, défaut
  inchangé, `Ran 18 tests … OK`.
- Portes : `python3 tools/revue_documentation.py`, `python3 tools/taille_documents.py`,
  `python3 tools/tests/test_produit.py` — vertes (voir § 8).
- **Aucune porte ne fait d'appel API** : le chemin réseau réel est couvert par la mesure du
  § 3 et par le harnais `qualifier_tagger_612.py`, pas par la porte. C'est le prix de la règle
  « hors ligne par défaut ».

## 7. Les limites et la suite

- Le gain est **conditionnel** à la clé et au réseau ; le défaut reste l'heuristique.
- Le tagger est **français** (prompt), même s'il étiquette l'anglais du gold ; la ventilation
  par langue du 612 n'est pas faite ici.
- Les **2 appels/phrase** incluent le tagger de syntagmes dont la sortie est ignorée. Si l'on
  ne veut que le POS, un appel suffirait : ~0,02 $ pour 612 et ~590 tokens/phrase en moins.
  C'est une optimisation **non mesurée** ; on ne l'a pas prise pour rester sur le câblage du
  harnais.
- La **mesure 612 via le CLI** (`evaluer --tagger` complet) n'a pas été refaite : elle coûterait
  un second ~0,04 $ et ~21 min. Le CLI a été validé sur 20 phrases avec le même cache ; le
  chiffre 612 est celui du harnais, déjà publié.
- **Suite** : mesurer le 612 par le CLI (mêmes réponses en cache), puis trancher l'appel de
  syntagmes inutile. La décision 1A est **livrée** ; la ligne R0.7 garde le split réel et le
  gold 200+.

## 8. Les liens

- [`tools/drave.py`](../tools/drave.py) — la CLI (`--tagger`, la clé, le cache, le code 4).
- [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) — 14 tests sans réseau.
- [`reports/tagger-612.json`](tagger-612.json) — la mesure de référence.
- [`reports/rapport-coordination-r.md`](rapport-coordination-r.md) — la fiche du tagger 612.
- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — la notice d'usage de l'option.
- [`reports/pensee-tagger-option.json`](pensee-tagger-option.json) — les chiffres bruts de cette
  fiche.
