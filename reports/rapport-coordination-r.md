# R — le tagger POS sur le gold 612 : **+8,49 pts**, la règle dit **intégrer**

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) · **Date** : 2026-11-13 · **HEAD mesuré** :
> `ced21933` · **Verdict** : le tagger POS par **API DeepSeek** mesure **0,9475** (**3012/3179**)
> sur le gold **612**, contre **0,8625** (**2742/3179**) pour l'heuristique du HEAD : **+8,49 pts**,
> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle
> de décision (**≥ +5 pts → intégrer**) donne : **intégrer via l'API**, jamais le 7B local
> (règle 11). La prémisse « clé absente » est **fausse** : la clé est dans
> `~/.config/drave/deepseek.key` (0600) et l'API répond **200** ; c'est `DEEPSEEK_API_KEY` qui
> manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.

**En trois lignes.** (1) La mesure est **réelle**, faite le 2026-11-13 avec un **cache neuf** :
`deepseek-chat` est servi par `deepseek-flash` (DeepSeek-V4.1-Flash-1017), 1 218 appels,
358 962 tokens, 20 min 59 s, **0 refus POS**. (2) La baseline publiée **0,8500** est **datée** :
elle reproduit exactement au commit `97256b8f`, mais trois commits POS du 2026-11-06 l'ont portée
à **0,8625** ; comparer à 0,8500 **surestime** le gain de **1,26 pt**. (3) La règle appliquée au
**612** donne **intégrer** ; la ventilation impose une réserve : sur le **réel 432 seul**, le gain
est **+4,67 pts** **[+3,45 ; +6,01]**, et le **synthétique 160** porte **+21,46 pts**.

## Ce que cette fiche est, et n'est pas

- **Est** : une coordination R **avec sa mesure**. Elle exécute le tagger sur le gold 612, publie
  les chiffres, applique la règle de décision et donne la **commande exacte avec la clé**.
- **N'est pas** : un patch de `tools/bloc_linguistique.py`, de `qualifier_quatre_modes.py` ou de
  `qualifier_cascade.py` ; le tagger **n'est pas branché** dans la production par cette fiche.
  Aucun fichier existant de R n'est modifié. Le banc ajouté
  (`tools/tests/linguistique/qualifier_tagger_612.py`) est **additif**.
- **N'écrit pas** `docs/pilotage/en-cours.md` ni `docs/pilotage/roadmap.md` : la session
  principale met les compteurs et l'état à jour, comme pour les coordinations N2 et S.
- **Public** : la session R (prochaine action : brancher la route API et tenir un split réel à
  l'écart) et le superviseur du chantier J4.

## 1. La prémisse, le modèle et le cache

### 1.1 « Clé absente » : vrai pour la variable, faux pour le fichier

| vérification | résultat |
|---|---|
| `DEEPSEEK_API_KEY` / `DSH_API_KEY` dans l'environnement | **absentes** |
| `~/.config/drave/deepseek.key` | **présent**, **0600**, **35 caractères** (préfixe `sk-`) |
| `GET https://api.deepseek.com/models` avec ce fichier | **HTTP 200** ; modèles `deepseek-flash` et `deepseek-v4-pro` |
| premier `chat/completions` de contrôle | **HTTP 200**, réponse `OK` |

`tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY`/`DSH_API_KEY`, puis `DEEPSEEK_KEY_FILE`/
`DSH_KEY_FILE` (première ligne, fichier 0600). La commande de § 6 utilise la **deuxième** voie :
la clé ne transite ni par le dépôt, ni par un fichier de mesure, ni par un message d'erreur.

### 1.2 `deepseek-chat` est un alias, le modèle renvoyé est `deepseek-flash`

Les 1 218 réponses du run portent `"model": "deepseek-flash"`. La documentation publique donne
`DeepSeek-V4.1-Flash-1017` et accepte encore les noms historiques ; `deepseek-chat` reste accepté
et sert ce modèle. **Conséquence** : le chiffre mesure le modèle **du 2026-11-13**, pas un modèle
figé par un identifiant de version. La fiche consigne le modèle renvoyé ; une re-mesure ultérieure
doit refaire ce contrôle.

### 1.3 Le cache par défaut rejouerait le 04/11 — il faut un cache neuf

Le cache `data/deepseek/cache` contient **3 596 réponses** datées du **2026-10-26 au 2026-11-04**
(15 Mo). La clé de cache est un sha256 de `modèle + messages + température + max_tokens` ; les
fichiers ne stockent **pas** les messages. Un run aujourd'hui avec le cache par défaut aurait donc
**rejoué les réponses de l'ancien run** (même modèle demandé, mêmes prompts) sans le dire. Le run
utilise `DEEPSEEK_CACHE=/tmp/j43-cache`, **créé vide** : **1 212 fichiers uniques** pour
**1 218 appels** (six prompts identiques réutilisent la même clé).

## 2. La baseline a bougé : **0,8500 est daté**, la référence est **0,8625**

### 2.1 Le chiffre publié et le chiffre du HEAD

| corpus | baseline publiée (à `97256b8f`) | baseline au HEAD `ced21933` | écart |
|---|---:|---:|---:|
| **180** (20 hand + 160 synth) | 0,7749 | **0,7836** (630/804) | **+0,87 pt** |
| **432 réel** | 0,8754 | **0,8893** (2112/2375) | **+1,39 pt** |
| **612** (gold courant) | **0,8500** (2702/3179) | **0,8625** (2742/3179) | **+1,26 pt** |

Le **0,8500** n'est pas faux : il **reproduit exactement** dans un worktree détaché à
`97256b8f` (`evaluer_gold.py`, 2702/3179, `exactitude_ferme` 0,9295, `exactitude_ouvert` 0,7746).
Il est **daté**. Trois commits du 2026-11-06, postérieurs à la mesure de `rapport-etat-r.md`
(commit `f48d5d81`), ont modifié les règles POS :

| commit | effet publié | jetons gagnés sur 612 |
|---|---|---:|
| `7a45325f` — la ponctuation a une POS (`PONCT`) | 85,00 → 85,75 % | **+25** |
| `6b976cb1` — R4-FR filtré (adjectif connu ou suffixe) | 85,75 → 85,84 % | **+3** |
| `c43dd5cc` — la règle « que » (pronom après un nom) | 85,84 → 86,25 % | **+13** |
| (règle PRON, variation résiduelle) | — | **−1** |
| **total** | **85,00 → 86,25 %** | **+40** |

Les diagonales des matrices de confusion le confirment : `PONCT` passe de 0 à **25**, `CONJ` de
55 à **68**, `ADJ` de 62 à **65**, `PRON` de 430 à **429**. Le reste est inchangé. Les fichiers
`gold*.json` et `evaluer_gold.py` sont **identiques** entre `97256b8f` et le HEAD
(`git diff --stat` vide) : la différence vient bien des règles, pas du banc ni du gold.

**Conséquence pour la décision** : comparer le tagger à **0,8500** donnerait **+9,75 pts** ;
comparer à **0,8625** donne **+8,49 pts**. Le seuil de **+5** est franchi dans les deux cas,
mais le chiffre publié doit être le second.

### 2.2 Les contrôles négatifs sur le 612

| contrôle | ce qu'il fait | exactitude |
|---|---|---:|
| **majoritaire** | toujours `NOUN` (682/3179) | **0,2145** |
| **classe fréquente** | toujours `VERB` (792/3179) | **0,2491** |
| **permutation** | les POS prédits par l'heuristique sont permutés entre jetons (graine 0) | **0,1667** |
| **uniforme** | tirage uniforme sur les 12 classes | **0,0833** |

Les quatre contrôles restent **sous 0,25** ; le tagger (0,9475) et l'heuristique (0,8625) sont
loin au-dessus. La permutation teste le **métrique** (le score ne vient pas du déséquilibre des
classes) ; le majoritaire teste le **plancher** ; aucun ne teste la **généralisation**, qui est
traitée au § 4.3.

## 3. Le protocole et le coût

### 3.1 Le protocole

- **Gold** : `gold.json` **20 hand** + `gold_reel.json` **432 réel** + `gold_synthetique.json`
  **160 synthétiques** = **612 phrases**, **3 179 jetons**.
- **Taggers** : `NeuronalLLMPOS` (POS) + `NeuronalLLMChunks` (syntagmes), tous deux par l'API,
  température 0, sans serveur local. La **pragmatique** n'est pas appelée : la décision porte sur
  le POS.
- **Six modes** : heuristique, neuronal, parallèle, cascade (seuil 0,6), parallèle par niveau,
  cascade par niveau. Les modes de fusion relisent le **même** cache de tagger : les appels API
  sont **2 par phrase** (POS + syntagmes), pas 2 par mode.
- **609 phrases** portent des jetons (3 phrases n'en ont pas) : **609 appels POS + 609 appels
  syntagmes = 1 218 appels**.
- **Un refus composite** : `s015` (« ma fenêtre marche que les fenêtre ouvre »), **syntagmes**
  seulement (`ValueError: longueur BIO 6 / 7`). Le POS de `s015` est rendu (**7 étiquettes**) ;
  **0 refus POS** sur 609 phrases. Le seuil `aucun_refus` du JSON est faux **à cause des
  syntagmes**, pas du POS.

### 3.2 L'estimation de la consigne et le mesuré

| grandeur | estimation (432 → 612) | mesuré | écart |
|---|---:|---:|---:|
| appels | ~1 200 | **1 218** | +1,5 % |
| tokens | ~360 000 | **358 962** | −0,3 % |
| durée | ~20 min | **20 min 59 s** (1 259,2 s) | +5 % |
| latence moyenne / appel | 0,94 s (run 432) | **1,033 s** | +10 % |
| latence médiane | — | **1,011 s** | — |

Le run 432 de référence (`pensee-quatre-modes-432-run2.json`) : **858 appels**, **254 454
tokens**, **807,6 s**, soit **1,986 appel/phrase**, **296,6 tokens/appel**, **0,941 s/appel**.
Le passage à 612 donne **1 218 appels**, **358 962 tokens**, **1 259,2 s** : la consigne était
juste à quelques pour cent.

### 3.3 Le coût facturé

Tarif public `deepseek-flash` au 2026-11-13 (hors pointe / pointe) : entrée **cache hit**
0,003 / 0,006 $ par M, entrée **cache miss** 0,15 / 0,30 $ par M, sortie 0,60 / 1,20 $ par M
([tarifs](https://api-docs.deepseek.com/quick_start/pricing)). Le run a consommé, d'après les
`usage` du cache : **155 136 tokens d'entrée en cache hit**, **174 822 en cache miss**,
**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).

| tarif | entrée hit | entrée miss | sortie | **total** |
|---|---:|---:|---:|---:|
| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
| **pointe** | 0,0009 $ | 0,0524 $ | 0,0328 $ | **~0,086 $** |

Le run a eu lieu un **samedi 03:00 UTC** : **hors pointe**, donc **~0,04 $**. Pour **1 000
phrases** : **~1 990 appels**, **~587 k tokens**, **~34 min** séquentielles, **~0,07 $** hors
pointe (**~0,14 $** en pointe). Le POS seul coûterait **la moitié** (~609 appels, ~180 k tokens,
~10,5 min) ; les syntagmes ne sont appelés ici que parce que le composite les demande.

## 4. La mesure

### 4.1 Les six modes, ventilés par source

| mode | 612 | hand 20 | réel 432 | synth 160 |
|---|---:|---:|---:|---:|
| **heuristique** | **0,8625** | 0,8857 | 0,8893 | 0,7682 |
| **neuronal** (API) | **0,9475** | 0,9714 | 0,9360 | 0,9828 |
| parallèle | 0,9475 | 0,9714 | 0,9360 | 0,9828 |
| cascade (0,6) | 0,9475 | 0,9714 | 0,9360 | 0,9828 |
| parallèle par niveau | 0,9475 | 0,9714 | 0,9360 | 0,9828 |
| cascade par niveau | 0,9475 | 0,9714 | 0,9360 | 0,9828 |

Les **cinq** modes neuronaux rendent la **même exactitude** et les **mêmes ventilations** : sur ce
gold, la politique de fusion (confiance 0,6, priorité par niveau) **n'ajoute ni ne retire rien**.
Le tagger seul porte le gain ; la fusion est **neutre**, pas un levier.

### 4.2 L'écart, les comptes exacts et la significativité

| corpus | heuristique | neuronal | gain | IC95 bootstrap | McNemar (b/c) | p |
|---|---:|---:|---:|---:|---:|---:|
| **612** | 2742/3179 = **0,8625** | 3012/3179 = **0,9475** | **+8,49 pts** | **[+7,23 ; +9,74]** | **344 / 74** | **1,1 × 10⁻⁴²** |
| hand 20 | 93/105 = 0,8857 | 102/105 = 0,9714 | +8,57 pts | [+2,75 ; +15,38] | 9 / 0 | 3,9 × 10⁻³ |
| réel 432 | 2112/2375 = 0,8893 | 2223/2375 = 0,9360 | **+4,67 pts** | **[+3,45 ; +6,01]** | 181 / 70 | 1,7 × 10⁻¹² |
| synth 160 | 537/699 = 0,7682 | 687/699 = 0,9828 | **+21,46 pts** | [+18,80 ; +24,15] | 154 / 4 | 1,4 × 10⁻⁴⁰ |

Lecture : le tagger corrige **344** jetons que l'heuristique rate et n'en casse que **74**. Le
bootstrap **par phrase** (4 000 tirages, graine 0) donne **+8,47 pts** de moyenne et
**[+7,23 ; +9,74]** : l'intervalle est au-dessus de **+5**. Le test de McNemar exact sur les
discordants est **très significatif** ; il ne dit rien de la généralisation, seulement que l'écart
n'est pas du bruit d'échantillonnage sur ces 612 phrases.

### 4.3 Ce que la ventilation dit — et que le 612 cache

Le **612** agrège trois corpus de difficulté très inégale :

- **réel 432** : **+4,67 pts** [+3,45 ; +6,01] — l'estimation ponctuelle est **sous +5**, mais
  l'IC **contient 5** ; c'est le corpus de généralisation, et c'est le plus honnête ;
- **synth 160** : **+21,46 pts** — les phrases sont générées par la grammaire du bloc, donc
  **faciles pour l'API** et **difficiles pour l'heuristique** ; ce sous-corpus **tire le 612
  au-dessus de +5** ;
- **hand 20** : **+8,57 pts** — mais ces 20 phrases ont servi au **choix du modèle et du prompt**
  (jeu de développement) ; le chiffre est **in-sample**.

La décision de la consigne porte sur le **612** ; elle est donc **intégrer**. La réserve est
explicite : **le gain sur le réel seul est +4,67**, et le +8,49 du 612 **dépend des 160
synthétiques**. Un split réel tenu à l'écart (dev/test par `crc32(id) % 3`, comme B13) est la
prochaine mesure qui peut faire descendre le chiffre sous +5, voire sous +2.

### 4.4 L'hybride « fermé heuristique / ouvert modèle » — une piste, pas un résultat

Le contrat de L garde les **classes fermées** (`DET, PREP, PRON, CONJ, AUX, ADV, NUM`) à
l'heuristique et confie l'**ouvert** au neuronal. Mesuré **a posteriori** sur les mêmes
prédictions (aucun appel supplémentaire) :

| mode | 612 | hand | réel 432 | synth |
|---|---:|---:|---:|---:|
| neuronal | 0,9475 | 0,9714 | 0,9360 | 0,9828 |
| **hybride par classe** (fermé = heuristique, ouvert = modèle) | **0,9516** | 0,9333 | 0,9461 | 0,9728 |

L'hybride gagne **+0,41 pt** sur le 612 (3025 vs 3012), mais il **perd** sur le hand et le synth,
et McNemar contre le neuronal donne **31/44, p = 0,17** : **non significatif**. Ce n'est **pas**
le mode à intégrer sur cette preuve. La piste — remplacer le seuil de confiance 0,6 par une
**règle de classe** — mérite une mesure dédiée, pas une décision.

## 5. La décision

### 5.1 La règle

La consigne fixe **deux bornes** ; la fiche explicite la zone qu'elle laisse ouverte.

| mesure sur le 612 | décision |
|---|---|
| **< +2,0 pts** | **négatif nommé** : le tagger n'est pas additif au gold courant ; garder l'heuristique, fermer R0.7 tagger |
| **≥ +5,0 pts** | **intégrer via l'API DeepSeek** (jamais le 7B local, règle 11) |
| **2,0 à 5,0 pts** | **zone grise** (non tranchée par la consigne) : aucune décision automatique ; mesure tenue à l'écart avant de trancher |

Si le gain avait été **< +2**, le négatif nommé aurait été : « *le tagger POS API n'est pas
additif au gold 612 (gain X pts) ; l'heuristique reste la référence ; R0.7 tagger fermé, le
+9,4 contre 0,85 était un artefact de corpus et de date* ». Ce n'est **pas** le cas.

### 5.2 Appliquée : **intégrer**

**+8,49 pts ≥ +5** → **intégrer**. Le mode retenu est le **neuronal seul** (`NeuronalLLMPOS` par
API) : c'est le plus simple, il rend 0,9475, et les modes de fusion **ne font pas mieux**. Le
tagger **remplace l'heuristique sur le POS** ; l'heuristique reste aux autres niveaux
(pragmatique, syntagmes selon le contrat) et sert de **repli** en cas de refus ou de panne
réseau.

**Contrat d'intégration proposé à R** :

1. **Route** : `NeuronalLLMPOS("deepseek-chat", transport=…)` avec le client
   `tools/llm/deepseek.py` ; **aucun** serveur local (`llama-server`, `ollama`), règle 11.
2. **Cache** : garder le cache de production (`data/deepseek/cache`) pour ne pas re-payer les
   répétitions ; pour **toute mesure**, cache **neuf** (§ 1.3).
3. **Repli** : si le POS refuse ou dépasse le timeout, garder l'heuristique ; le taux de refus
   POS mesuré est **0/609**. Le refus `s015` est **syntagmes**, pas POS.
4. **Coût** : ~0,07 $ et ~34 min par 1 000 phrases en séquentiel ; parallélisable (limite API
   2 500 requêtes concurrentes), à arbitrer avec le débit du bloc.
5. **Décision de production** : intégrer le POS API **derrière un drapeau** (route API activée
   par configuration), avec l'heuristique par défaut hors ligne. Le bloc reste utilisable sans
   réseau.
6. **Prochaine mesure** : le **split réel tenu à l'écart** (§ 4.3) ; si le gain réel tombe
   **< +2**, rouvrir la décision et nommer le négatif. Si le gain réel reste **≥ +5**, la route
   API devient le défaut.

### 5.3 Ce que la décision ne dit pas

- Elle ne dit pas que le **7B local** est mauvais : il n'est plus sur le disque, et la règle 11
  l'interdit comme serveur local. Le 0,9440 du 180 n'est pas comparable au 612.
- Elle ne dit pas que la **fusion** est inutile : elle est **neutre** ici, et l'hybride par classe
  est une piste **non significative** (+0,41 pt, p = 0,17).
- Elle ne dit pas que le **réel** gagne +8,49 : le réel seul est **+4,67** [+3,45 ; +6,01].

## 6. La commande exacte avec la clé

### 6.1 Prérequis

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
test -r "$HOME/.config/drave/deepseek.key" && echo CLE-OK
```

Attendu : `CLE-OK`. Le fichier doit être **0600** ; il ne doit **jamais** être copié dans le
dépôt, dans un JSON de mesure ou dans un message.

### 6.2 Le run complet (612 phrases, ~21 min)

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
DEEPSEEK_KEY_FILE="$HOME/.config/drave/deepseek.key" \
DEEPSEEK_CACHE="$(mktemp -d /tmp/j43-cache.XXXXXX)" \
DEEPSEEK_MODEL=deepseek-chat \
PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
  --sortie /tmp/tagger-612.json
```

- `DEEPSEEK_KEY_FILE` : la clé, lue par `tools/llm/deepseek.py` ; jamais affichée.
- `DEEPSEEK_CACHE` : **neuf** ; sans lui, le cache par défaut rejoue les réponses du 04/11.
- `DEEPSEEK_MODEL=deepseek-chat` : l'alias historique, servi par `deepseek-flash` ; le modèle
  renvoyé est consigné dans le JSON (`modeles_renvoyes`).
- `--sortie` : le JSON de mesure (47 Ko), avec les six modes, les quatre ventilations, les
  matrices de confusion, les appels, les tokens, la latence et les refus.

**Attendu** (à la latence près) :

```text
phrases 612 tokens 3179
sources Counter({'reel': 432, 'synth': 160, 'hand': 20})
heuristique · 0.86 s POS all 0.8625
neuronal · ~1253 s POS all 0.9475
parallele · ~1.2 s POS all 0.9475
cascade · ~1.3 s POS all 0.9475
parallele_niveau · ~1.2 s POS all 0.9475
cascade_niveau · ~1.2 s POS all 0.9475
appels 1218 tokens 358962 refus 1 latence_moyenne 1.033
```

### 6.3 Le smoke test (3 phrases, ~6 appels)

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
DEEPSEEK_KEY_FILE="$HOME/.config/drave/deepseek.key" \
DEEPSEEK_CACHE="$(mktemp -d /tmp/j43-smoke.XXXXXX)" \
DEEPSEEK_MODEL=deepseek-chat \
PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
  --limite 3 --sortie /tmp/tagger-612-smoke.json
```

Attendu : `appels 6`, `tokens ~1805`, `refus 0`. C'est le contrôle qui dit que la clé, le
transport et le parsing JSON fonctionnent **avant** de lancer 21 minutes.

### 6.4 Si la clé est dans l'environnement

```bash
DEEPSEEK_API_KEY="$(cat "$HOME/.config/drave/deepseek.key")" \
DEEPSEEK_CACHE="$(mktemp -d /tmp/j43-cache.XXXXXX)" \
PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
  --sortie /tmp/tagger-612.json
```

La variable reste **locale au processus** ; ne pas l'exporter dans un shell durable, ne pas la
mettre dans l'historique partagé.

### 6.5 Le banc historique

`tools/tests/linguistique/qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432) :
`charger(a.gold_reel)` avec `--gold-reel` à `True` par défaut. Il **ne peut pas** produire le 612
sans étendre `charger` et `_sources` (`qualifier_cascade.py`). La fiche **ne modifie pas** ce
banc : le nouveau `qualifier_tagger_612.py` est **additif** et c'est la commande de § 6.2 qui fait
foi. Si R préfère le banc historique, il faut y porter le chargeur 612 et la ventilation `reel`
(le reste — modes, mesures — est identique).

## 7. Ce qui pourrait rendre ce résultat faux

- **Un seul run, un seul jour, un seul alias.** Température 0, mais l'API n'est pas déterministe
  au bit près ; il n'y a **pas** de seconde passe. Le modèle est `deepseek-flash`
  (V4.1-Flash-1017) : une version différente peut changer le chiffre.
- **Le 612 n'est pas le réel.** Le +8,49 dépend des **160 synthétiques** (+21,46) ; le réel 432
  seul est **+4,67** [+3,45 ; +6,01]. Le split réel tenu à l'écart n'est **pas** fait.
- **Les 20 hand sont in-sample** : ils ont servi au choix du modèle et du prompt en 2026-11-02 ;
  leur +8,57 n'est pas une mesure de généralisation.
- **La baseline bouge.** 0,8500 est daté ; 0,8625 est le HEAD. Si R modifie encore les règles POS,
  la référence change et le gain avec elle.
- **Le gold est vivant.** Toute nouvelle phrase avec cible change l'exactitude ; le JSON donne les
  comptes (2742/3179, 3012/3179) pour que la comparaison reste possible.
- **Le POS n'est pas le contrat entier.** La mesure ne dit rien des **spans**, de la
  **morphologie**, des **traits UD** ni de la **pragmatique** ; la tokenisation est celle de
  `Heuristique._mots`, pas celle du modèle.
- **Le cache peut mentir.** Un run avec le cache par défaut rejoue l'ancien modèle sans le dire ;
  le run utilise un cache neuf, mais un futur lecteur doit vérifier `modeles_renvoyes` et la date.
- **Le coût en dollars est une estimation**, pas une facture : les tokens sont mesurés, la
  répartition entrée/sortie est reconstruite depuis le cache (six prompts dupliqués, ±0,5 %).
- **Le refus `s015`** invalide le seuil `aucun_refus` du JSON composite ; il **n'invalide pas** le
  POS (7/7 étiquettes rendues). Un lecteur pressé qui regarde `seuils["aucun_refus"]` conclura à
  tort que la mesure POS a un refus.
- **Pas de comparaison au 7B local** : le GGUF n'est plus sur le disque et la règle 11 interdit le
  serveur local. Le 0,9440 du 180 reste un chiffre historique, pas un concurrent mesuré ici.

## 8. Fichiers

- **Cette fiche** : `reports/rapport-coordination-r.md` ; **version machine** :
  [`rapport-coordination-r.json`](rapport-coordination-r.json).
- **Mesure brute** : [`tagger-612.json`](tagger-612.json) — 47 Ko, six modes, quatre ventilations,
  matrices de confusion, appels, tokens, latence, refus, modèle renvoyé.
- **Analyse appariée** : embarquée dans `rapport-coordination-r.json` (`analyse_appariee`) :
  comptes exacts, McNemar, bootstrap par phrase, contrôles, hybride.
- **Banc** : `tools/tests/linguistique/qualifier_tagger_612.py` — **nouveau**, additif, 200 lignes ;
  aucun fichier existant modifié.
- **Lus, non modifiés** : `tools/bloc_linguistique.py`, `tools/llm/deepseek.py`,
  `tools/tests/linguistique/qualifier_quatre_modes.py`,
  `tools/tests/linguistique/qualifier_cascade.py`,
  `tools/tests/linguistique/evaluer_gold.py`, `tools/tests/linguistique/gold.json`,
  `gold_reel.json`, `gold_synthetique.json`.
- **Non écrits** : `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `journal/`. La session
  principale y porte le chiffre **+8,49** et la décision **intégrer** ; la fiche ne remplace ni
  l'état ni la roadmap.
- **Commit** : les fichiers ci-dessus, `git add` explicite, message portant **+8,49** et
  **intégrer**. Aucun autre chemin n'est indexé.
