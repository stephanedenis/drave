# S — 9/9 paragraphes jugés (19/19), 150 verdicts de banque ; la page `/` sert encore l'ancien arbre plat et la rétro-traduction n'existe pas

> **Ligne de roadmap** : S · **Date** : 2026-11-06 · **Verdict** : le chantier S a deux couches
> désormais séparées. La passe de validation des candidats sur **`/paragraphes`** est **finie** :
> 9 paragraphes, 19 candidats,
> **19 verdicts**, **0 restant**, **11 acceptés** (10 `resolu` + 1 `compatible`) et **8 exclus**.
> La **banque de phrases** (`/`) ne l'est pas : **150 verdicts** sur **74 des 207 phrases**
> (35,7 %), **84 lectures acceptées**, mais la page sert les **369 candidats stockés le 02/11**,
> **sans `profondeur`** ; la mesure v7, elle, donne **359 candidats** et **99 à profondeur ≥ 3**.
> Les référents des 19 verdicts **ne sont pas un gold** : **12 des 28 mappings contredisent la
> source anglaise**, **2 formes manquent** ; le « 14/14 » de la fiche de traduction est un
> résultat **côté traduction**, pas une validation humaine. La **rétro-traduction n'existe pas** :
> 0 script, 0 mesure, 0/9 paragraphe, et `DEEPSEEK_API_KEY` est absente. Enfin, les **71 langues**
> sont le **lexique B7** (35 concepts, 1 433 couples), **pas l'UDHR** (456 langues) et **pas un
> corpus de référents** : **0/71** testée par S.

## Ce que dit l'état, en un tableau

| quoi | valeur mesurée | source |
|---|---:|---|
| page `/paragraphes` | **9/9** paragraphes, **19/19** candidats, **11** acceptés / **8** exclus / **1** `compatible` | `paragraphes.json`, `paragraphes-validations.jsonl` |
| verdicts `/paragraphes` dans git | **8 committés**, **11 non committés** (a004–a009) | sous-module `523d8c1` + `git status` |
| référents des 19 verdicts | **28** mappings, **16** justes, **12** faux, **2** manquants | audit source anglaise (§ 2) |
| banque de phrases | **150** verdicts, **147** paires, **74/207** phrases jugées, **84** acceptées / **63** exclues | `validations.jsonl` |
| banque affichée vs v7 | **369** stockés (0 `profondeur`) vs **359** dynamiques, **99 à ≥ 3** | `phrases_generees.json`, `mesure_arbre` |
| 71 langues | **71** déclarées, **66** avec item, **62** avec item fort, **32** fortes, **5** vides | `tools/jeux/lexique_multilingue.json` |
| UDHR | **456** langues, **13 996** articles | `data/udhr/` |
| rétro-traduction | **0/9**, 0 script, 0 mesure, clé absente | `grep`, environnement |
| analyseur | **61/61** types, **144/144** rôles, **50/50** compléments, **56 tests** | `mesure-analyseur.json`, tests |

Le dépôt est sur **`s/v7`**, HEAD **`de7c9113`** au moment de l'audit ; un commit concurrent
**`0a9381f0`** a depuis pris la version initiale de ce rapport — mes corrections de chronologie
sont dans le working tree, non committées. Le sous-module `tools/structures`
est sur **`master`**, HEAD **`523d8c1`** (2026-11-04), avec **un fichier modifié** :
`donnees/paragraphes-validations.jsonl` (+11 lignes).

## 1. Les 71 langues : le lexique B7, pas l'UDHR

**Où.** Les 71 langues sont déclarées dans `tools/jeux/lexique_multilingue.json` (`langues`,
version 1, source Wikidata CC0, 2026-10-26). Elles sont chargées par
`tools/jeux/lexique_multilingue.py`, mesurées par `tools/jeux/mesure_langues.py`, et mises en
corpus par `tools/jeux/corpus_multilingue.py` (449 surfaces). La mesure est dans
`reports/rapport-langues-maitres.md` et `reports/jeux-langues-mesures.json` ; le concept est dans
`docs/theorie/jeux-symboliques.md`.

**Lesquelles.** `ar` arabe · `bn` bengali · `ca` catalan · `cs` tchèque · `da` danois ·
`de` allemand · `el` grec · `en` anglais · `eo` espéranto · `es` espagnol · `et` estonien ·
`eu` basque · `fa` persan · `fi` finnois · `fr` français · `gl` galicien · `he` hébreu ·
`hi` hindi · `hr` croate · `hu` hongrois · `id` indonésien · `is` islandais · `it` italien ·
`ja` japonais · `ka` géorgien · `kk` kazakh · `ko` coréen · `lt` lituanien · `lv` letton ·
`mk` macédonien · `ms` malais · `mt` maltais · `nb` norvégien bokmål · `nl` néerlandais ·
`nn` norvégien nynorsk · `pl` polonais · `pt` portugais · `ro` roumain · `ru` russe ·
`sk` slovaque · `sl` slovène · `sq` albanais · `sr` serbe · `sv` suédois · `sw` swahili ·
`ta` tamoul · `th` thaï · `tr` turc · `uk` ukrainien · `ur` ourdou · `vi` vietnamien ·
`zh` chinois · `af` afrikaans · `am` amharique · `az` azéri · `be` biélorusse · `bs` bosnien ·
`cy` gallois · `ga` irlandais · `hy` arménien · `km` khmer · `ky` kirghize · `lo` lao ·
`mn` mongol · `ne` népalais · `pa` pendjabi · `si` cingalais · `so` somali · `uz` ouzbek ·
`yo` yoruba · `zu` zoulou.

**Combien testées.** La mesure B7 (rejouée le 06/11, `--complet`, 3,5 s) donne :

| mesure | valeur | ce qu'elle teste |
|---|---:|---|
| langues déclarées | **71** | le lexique |
| clés de labels | **75** | 71 langues + 4 variantes (`pt-br`, `sr-ec`, `zh-hans`, `zh-hant`) |
| concepts | **35** | pièces, rangs, enseignes, jeux, notions de maîtres |
| couples concept-langue | **1 433** | 1 429 canoniques + 4 variantes |
| moyenne concepts/langue | **20,13** | — |
| langues avec ≥ 1 label | **71/71** | — |
| langues avec ≥ 1 item du corpus | **66/71** | les 449 surfaces |
| langues avec ≥ 1 item fort | **62/71** | échecs ou cartes |
| langues « fortes » | **32/71** | pièce N/P + un rang + une enseigne |
| langues sans item | **5/71** | `mt`, `ky`, `lo`, `si`, `yo` |
| notation | **5 112/5 112** | 72 items × 71 langues |
| corpus multilingue | **449/449** au niveau 4 | 11 paires |
| invariance inter-langues | **11/11** | mêmes empreintes RSN |
| permutation des libellés | **186/449** ; **12/275** forts (4,4 %) | contrôle négatif |
| détection des noms de jeux | **315/315** | 5 jeux |
| langue détectée | **340–344/449** selon le run | non reproductible au cas près |

Les 32 langues fortes sont : `ar`, `bn`, `ca`, `cs`, `da`, `de`, `el`, `en`, `eo`, `es`, `et`,
`eu`, `fa`, `fi`, `fr`, `hu`, `it`, `ja`, `lv`, `nb`, `nl`, `pl`, `pt`, `ru`, `sl`, `sq`, `sr`,
`sv`, `uk`, `vi`, `zh`, `af`. Les 5 vides (`mt`, `ky`, `lo`, `si`, `yo`) ont 1 à 4 labels mais
aucun item de corpus ; ce ne sont pas des langues « non testées », ce sont des langues **sans
surface** dans le corpus de jeu.

**Le point important.** Ces 71 langues ne contiennent **aucune phrase**, aucun pronom, aucune
anaphore : ce sont des **libellés de concepts de jeu** (lemmes), pas de la grammaire. Elles
mesurent la couche lexicale (le même sens dans 71 langues), pas la référence. **S ne les a pas
testées : 0/71.** Les fiches S répètent « les 71 langues de l'UDHR (le travail L) » : c'est un
raccourci faux. L'UDHR a **456 langues** (`data/udhr/langues.jsonl`), **13 996** lignes d'articles
et **13 222** articles « propres » ; il n'existe **aucun sous-ensemble UDHR à 71 langues** dans le
dépôt. Les 71 sont B7 ; l'UDHR est un autre corpus, aligné par construction, mais sans annotation
de référents. Une lecture de l'UDHR à 71 langues serait possible, mais ce serait un **nouveau
protocole d'annotation**, pas le test de référents promis par la fiche.

**Contrôle négatif.** Si les 71 langues étaient un corpus de référents, elles porteraient des
phrases et des anaphores ; elles portent 35 concepts et 0 phrase. Le contrôle de permutation le
confirme : mélanger les libellés fait tomber les items forts de **275/275 à 12/275** (4,4 %), donc
le signal mesuré est bien le **sens lexical**, pas la structure de phrase.

**Ce qui pourrait le rendre faux.** Les 1 433 couples incluent 4 clés de variantes ; le compte
canonique est **1 429**. La détection de langue n'est pas stable au cas près : cinq runs donnent
**340, 342, 343, 343, 344** sur 449 — le taux (~76 %) est stable, le chiffre exact non ; la cause
probable est un départage non déterministe (hash), non élucidée. Le docstring de
`lexique_multilingue.py` dit encore « 53 langues » alors que la donnée en porte 71 : dérive de
documentation, sans effet sur la mesure. Enfin, 5 langues n'ont aucun item : le « 71/71 » de la
notation ne veut pas dire « 71/71 testées sur le corpus ».

## 2. La page `/paragraphes` : 9/9, 19/19, et le faux « 8 restants »

**Le compte.** `donnees/paragraphes.json` porte **9 paragraphes** (a001–a009), tous issus d'Alice.
Le serveur régénère leurs candidats à la volée (`generateur.analyser`) : **2, 3, 3, 2, 2, 1, 2, 1,
3** candidats, soit **19**. `paragraphes-validations.jsonl` porte **19 verdicts** : **10
`resolu`**, **8 `exclu`**, **1 `compatible`**, **0 `double_sens`**. Au sens de la page (résolu +
compatible + double sens), **11 lectures sont acceptées** et **8 exclues** ; **9/9 paragraphes**
ont au moins une lecture acceptée ; **0 candidat n'est sans verdict**.

| id | candidats | verdicts | acceptés | exclus | référents justes |
|---|---:|---:|---:|---:|---:|
| a001 | 2 | 2 | 2 | 0 | 4/5 |
| a002 | 3 | 3 | 1 | 2 | 1/3 |
| a003 | 3 | 3 | 1 | 2 | 4/4 |
| a004 | 2 | 2 | 1 | 1 | 1/1 |
| a005 | 2 | 2 | 1 | 1 | 2/3 |
| a006 | 1 | 1 | 1 | 0 | 3/4 |
| a007 | 2 | 2 | 1 | 1 | 0/0 |
| a008 | 1 | 1 | 1 (`compatible`) | 0 | 0/5 |
| a009 | 3 | 3 | 2 | 1 | 1/3 |
| **total** | **19** | **19** | **11** | **8** | **16/28** |

**Le « 8 restants » est faux, et il mélange verdicts et paragraphes.** La page a 9 paragraphes,
pas 17. Après a001–a003, il restait **6** paragraphes (a004–a009), pas 8. Le chiffre **8** est
celui des **verdicts committés** sur a001–a003 (commit `7ccc60f` : 8 verdicts), pas celui des
paragraphes restants. Les **11 verdicts** a004–a009 ont été ajoutés le **2026-11-04** et sont
**toujours non committés** : un clone à `523d8c1` voit 8 verdicts et 6 paragraphes sans verdict ;
le working tree local voit 19/19. C'est pourquoi `docs/pilotage/en-cours.md:59` et
`docs/pilotage/roadmap.md:34` disent encore « a001–a003 faits » alors que
`docs/pilotage/roadmap.md:356` dit déjà « a001–a009 faits ». **Les données arbitrent : 9/9 et
19/19 dans le working tree ; 8 verdicts dans git.**

**Les référents ne sont pas validés.** Chaque verdict enregistre un dictionnaire `referents`
(formes uniques par paragraphe) ; les 19 verdicts en portent **28 mappings** (les mêmes valeurs
sont répétées d'un candidat à l'autre). Comparés à la source anglaise et à la table de la fiche
`rapport-s-traductions.md` :

- **16/28 justes** ; **12/28 faux** ; **2 formes manquantes**.
- Sur le périmètre de la fiche (a001–a003, **12 formes uniques / 14 occurrences**) : **9/12
  justes**, **3 faux**, **2 manquants**. Les 2 manquants sont exactement ceux que la fiche dit
  avoir retrouvés par l'anglais : `les` → *it* → **les conseils** (a001), `l'` → *it* → **la
  boîte** (a002). L'outil les classe `DET` et ne les propose pas ; le journal humain ne peut donc
  pas les contenir.
- Les **12 faux** : a001 `en` → Alice (partitif « les larmes », non référent) ; a002 `en` →
  Alice (préposition « en verre ») ; a002 `y` → Alice (attendu : la boîte) ; a005 `en` → coup
  (attendu : la salle) ; a006 `cela` → « Comme » (attendu : attendre à la petite porte) ; a008
  `Je`, `me`, `je` → « le contenu » / « Je me sens toute drôle » (attendu : Alice), `on` →
  « Je me sens toute drôle » (indéfini), `en` → « Je me sens toute drôle » (préposition) ; a009
  `se` → « Un moment » (attendu : Alice), `en` → « Un moment » (préposition).
- **6/9 paragraphes** ont au moins un faux (a001, a002, a005, a006, a008, a009) ; a003, a004 et
  a007 sont propres.
- **0 note** sur 19 verdicts ; le seul `compatible` est **a008**, précisément le paragraphe à
  **0/5** : le statut dit « pas tranché », ce qui est cohérent, mais le journal enregistre quand
  même 5 référents faux.

Les valeurs enregistrées ressemblent fortement aux **défauts de la page** : antécédent pour les
pronoms personnels et possessifs (`elle`, `sa`, `se`, `lui`…), premier candidat pour les clitiques
(`en`, `y`, `cela`, `on`). La page dit « tranchez d'abord les référents, puis la structure », mais
**ne force pas** la résolution : le clic enregistre les `<select>` tels quels, même par défaut.
Le journal ne permet donc pas de distinguer un défaut d'un choix humain. **Conséquence : les 19
verdicts valident la structure, pas la référence.** Le « 14/14 » de la fiche de traduction reste
un résultat **côté traduction** (l'anglais confirme 14 occurrences) ; il n'est **pas** dans le
journal humain.

**Ce que la page a de solide.** Les 9 arbres sont dynamiques (le `generateur` v7), les 9 SVG
passent le test du cadre, les 19 candidats sont tous jugés, et les 56 tests passent (4,3 s). La
page est le seul endroit où l'arbre v7 est réellement visible.

## 3. La banque de phrases : 150 verdicts, 74 phrases, une page restée au 02/11

**La couverture.** `phrases.json` (7 phrases du banc) + `phrases_generees.json` (200 phrases de
littérature) = **207 phrases**, **369 candidats stockés**. `validations.jsonl` porte **150
verdicts** (tous datés du **2026-11-03**, cinq rafales de 10 h à 16 h), sur **147 paires
(phrase, candidat) uniques** : 3 lignes sont des révisions. **74 phrases** ont tous leurs
candidats jugés (**35,7 %**), **0 phrase partielle**, **133 phrases sans aucun verdict**
(64,3 %) ; **147/369 candidats** sont jugés (**39,8 %**). Les 7 phrases du banc sont **7/7**
jugées ; les 200 phrases de littérature sont **67/200** (33,5 %).

| mesure | valeur |
|---|---:|
| verdicts (lignes) | **150** |
| paires uniques | **147** |
| phrases jugées en entier | **74/207** (35,7 %) |
| phrases sans verdict | **133** (64,3 %) |
| candidats jugés | **147/369** (39,8 %) |
| dernier verdict : `resolu` / `exclu` / `compatible` | **73 / 63 / 11** |
| toutes lignes : `resolu` / `exclu` / `compatible` / `double_sens` | **74 / 64 / 11 / 1** |
| lectures acceptées (dernier verdict) | **84** (73 + 11), **57,1 %** de 147 |
| lectures exclues | **63**, **42,9 %** |
| niveau 0 / 2 / 3 (dernier verdict) | **141 / 4 / 2** |
| verdicts avec contexte | **6/147** (4,1 %) |
| notes | **1/150** (0,7 %) |

**Les révisions.** Deux paires ont été revues : `p002-c2` (`double_sens` → `compatible`, 31 s
plus tard) et `p003-c2` (`exclu` → `resolu` → `exclu`, les deux derniers à 36 s d'intervalle ; la première
exclusion était à 10 h 32). Cinq lignes pour deux
paires, **3 lignes supersédées** (2 % des lignes). Le seul `double_sens` n'a pas survécu : la
banque finale n'en porte **aucun**. La note unique est `p002-c2` : « il est préférable de dire
l'homme au téléscope » — une préférence sémantique, pas une erreur.

**Le contexte est presque absent.** **141/147** verdicts finaux sont au niveau 0 (phrase seule) ;
seuls **6** portent un contexte (p001, p002, p007). p003–p006 ont été jugés sans contexte. La
mesure « niveau minimal de contexte » repose donc sur **6 verdicts**, pas sur 147 : elle ne dit
rien de la pragmatique de la banque.

**L'export est à jour, la fiche ne l'est pas.** `data/structures/banque-validee.jsonl` porte
**84 lignes / 67 phrases**, SHA-256 `3ca1ac20…`, daté du **2026-11-04 08:42** ; le manifeste
`reports/s-banque-validee.json` le confirme. La fiche `reports/rapport-s-banque-partielle.md`
parle encore de **81 lignes / 65 phrases**, SHA `2d27b712…` : elle est en retard de **3 lectures
acceptées et 2 phrases**. Les 8 verdicts ajoutés après elle (16 h 39–16 h 46) expliquent l'écart :
`c010-c1` et `c066-c2`/`c066-c3` ajoutent 3 acceptées, `p003-c2`, `c066-c1`, `c067-c1`,
`c067-c2` ajoutent 4 exclusions (dont une révision transitoire).

**Le point dur : la page `/` ne montre pas la v7.** La page `/` charge les candidats **stockés**
dans `phrases_generees.json` (mtime **2026-11-02 20:35**), pas la sortie courante du générateur.
Or **369/369** de ces candidats n'ont **pas** de champ `profondeur` (ils ont l'ancien `niveau`
plat) ; leur profondeur maximale est **10 à 0, 277 à 1, 82 à 2** — exactement le négatif
« 277/369 plats » de la fiche `rapport-s-banque-partielle.md`. La mesure dynamique v7 sur les
mêmes 207 phrases donne **359 candidats** : **2 à 0, 37 à 1, 221 à 2, 84 à 3, 13 à 4, 2 à 5**,
soit **99 à ≥ 3** (27,6 %), et **294/371** formes avec un antécédent proposé, **77 sans** (20,8 %).
Entre les deux vues : **304 candidats identiques**, **55 changés**, **10 orphelins** (9 phrases
ont moins de candidats) et **5 verdicts humains à risque** si l'on régénère par index :
`p006-c2` (`compatible`), `c023-c3` (`exclu`), `c056-c2` (`exclu`), `c056-c3` (`resolu`),
`c064-c2` (`exclu`). Une migration par **signature** (texte + type + rôle des segments) peut les
sauver ; une régénération naïve les perd.

**Conséquence.** Le motif d'arrêt humain — « il manque trop souvent de profondeur » et « les
référents ne semblent pas résolus avant que je tranche » — est **toujours vrai sur `/`** : la page
sert l'ancien arbre plat. Le correctif v5/v7 n'est visible que sur `/paragraphes`, où les
candidats sont régénérés à la volée. **La banque ne peut pas reprendre tant que `/` n'est pas
migrée.** C'est le blocage n° 1 du chantier, et il n'est pas un manque de verdicts : c'est un
décalage entre la donnée affichée et la mesure.

**Le grand modèle.** `donnees/llm.jsonl` porte **2 lignes**, toutes deux `fournisseur:
baseline`, `mode: local`, sans DeepSeek. Aucune comparaison au grand modèle n'a été faite sur la
banque ; la clé est absente.

## 4. La rétro-traduction : elle n'existe pas

**État.** Aucun fichier, aucun script, aucune mesure. La recherche dans le dépôt (hors archives
et journaux de session) ne trouve que **cinq mentions** dans les fiches S et le README :
`rapport-s-traductions.md`, `rapport-s-limites-v6.md`, `rapport-s-paragraphes.md`,
`rapport-s-fait-divers.md`, `tools/structures/README.md`. Toutes disent « quand la clé sera là ».
Il n'y a **ni `retro_traduction.py`, ni JSONL, ni chrF, ni 9/9** : **0 paragraphe testé, 0 appel**.

**Les briques existantes, et ce qui manque.** Le dépôt a le client API
(`tools/llm/deepseek.py`), le corpus de prompts (`tools/llm/prompts_publics.jsonl` : 5 articles
UDHR × 10 langues, avec référence humaine), le lanceur (`tools/llm/enseignant.py`) et la mesure
chrF (`tools/llm/mesure.py`). Mais ce dispositif mesure une **traduction aller** contre une
référence humaine ; il ne fait **pas** FR → EN → FR, et il ne connaît **pas** les 9 paragraphes
d'Alice. Le harnais de rétro-traduction reste à écrire, dans `work/` (pas dans
`tools/structures/` ni `data/`).

**Le protocole mesurable** (9 paragraphes, 2 passes, 18 appels) :

1. écrire `work/retro-traduction/prompts-fr-en.jsonl` (9 prompts FR → EN, avec `meta.reference`
   = la cible française d'origine) ;
2. `enseignant.py` sur ces prompts → `work/retro-traduction/fr-en.jsonl` ;
3. construire `prompts-en-fr.jsonl` à partir des réponses EN (même `meta`) ;
4. `enseignant.py` → `work/retro-traduction/fr-en-fr.jsonl` ;
5. `mesure.py` sur ce fichier → chrF aller-retour contre la cible d'origine ; 2 relectures
   humaines des 9 paires.

**Les commandes exactes qui existent** (clé requise ; cache redirigé hors de `data/`) :

```bash
# un appel, brique existante
DEEPSEEK_CACHE="$PWD/work/deepseek-cache" DEEPSEEK_API_KEY=... \
  python3 tools/llm/deepseek.py --prompt "Traduis en anglais : <paragraphe>" --json

# un lot, brique existante (prompts au format prompts_publics.jsonl)
DEEPSEEK_CACHE="$PWD/work/deepseek-cache" DEEPSEEK_API_KEY=... \
  python3 tools/llm/enseignant.py \
    --prompts work/retro-traduction/prompts-fr-en.jsonl \
    --sortie work/retro-traduction/fr-en.jsonl

# la mesure chrF, brique existante
python3 tools/llm/mesure.py \
  --entree work/retro-traduction/fr-en-fr.jsonl \
  --json work/retro-traduction/mesure.json
```

**Ce qui bloque.** `DEEPSEEK_API_KEY` est **absente** de l'environnement au 2026-11-06 21:49 ; le
harnais FR → EN → FR n'existe pas ; les 9 prompts n'existent pas. La règle 11 interdit un serveur
local : la rétro-traduction passera par l'API, jamais par `llama-server`/`ollama`. **Sans clé, on
ne simule pas** : le mode `--dry-run` rend des réponses factices, non mesurables.

**Ce qu'elle mesurerait.** 9/9 paragraphes, 18/18 appels, un chrF aller-retour par paragraphe et
une moyenne, et 2 relectures humaines pour les pertes de sens (référents, négation, concession,
temps). Aucun seuil n'est fixé aujourd'hui : le premier passage est **descriptif**, il ne prouve
pas la fidélité. Le chrF élevé peut venir de la recopie de surface ; le contrôle est la lecture
humaine des 9 paires, pas le score seul.

## 5. Ce que les verdicts humains disent de la qualité

**La structure est jugée, et de façon décisive.** Les 19 verdicts de `/paragraphes` couvrent tous
les candidats ; 11 sont acceptés, 8 exclus ; 9/9 paragraphes ont une lecture préférée. Le seul
`compatible` (a008) est le paragraphe où l'humain n'a pas tranché les référents (0/5) : le statut
est cohérent avec l'état de la référence. Sur la banque, **84/147** lectures sont acceptées
(57,1 %, dont 73 `resolu` = 49,7 % et 11 `compatible` = 7,5 %) et **63/147** exclues (42,9 %).
Autrement dit, l'heuristique propose souvent une lecture plausible, mais **quatre fois sur dix**
elle propose une lecture que l'humain écarte : c'est un signal utile, pas une accuracy.

**La référence n'est pas validée.** 12/28 mappings faux, 2 formes absentes, 0 note : le journal
des 19 verdicts ne peut pas servir de gold de référents. La fiche de traduction a raison sur
l'anglais (14 occurrences confirmées, 2 retrouvées), mais le journal humain n'en contient que 12
formes, dont 9 justes. **Le « 14/14 » est un résultat de traduction, pas de validation humaine.**

**La couverture est partielle et datée.** 74/207 phrases (35,7 %), 147/369 candidats (39,8 %),
**133 phrases jamais vues** ; un seul annotateur (`auteur: humain`, sans identité), une seule
journée (2026-11-03) pour les 150 verdicts, deux journées (03–04/11) pour les 19 paragraphes ;
**1 note** sur 169 verdicts (150 + 19), **0 note** sur les paragraphes. Il n'y a **aucun
double-codage**, aucune mesure d'accord inter-annotateurs, aucun test-retest — seulement deux
paires révisées, dont un flip-flop `exclu → resolu → exclu` en 36 s. La stabilité des
statuts n'est donc pas mesurée.

**Le contexte est un décor.** 141/147 verdicts finaux au niveau 0, 6 avec contexte (4,1 %). Le
banc de phrases a bien un contexte pour p001–p003 et p007, mais p003–p006 ont été jugés sans ;
la mesure « niveau minimal » ne repose que sur 6 verdicts. La couche pragmatique est nommée, pas
mesurée à l'échelle de la banque.

**L'analyseur est bon sur son gold, pas général.** **61/61** types, **144/144** rôles, **50/50**
compléments, couverture **1,00**, **56 tests** ; les contrôles tiennent (baseline **104/144**,
règles coupées **106/144**, rôles mélangés **0,10**). Mais le gold est de la **même main** que les
règles, les vagues 5 et 6 ont été écrites **après** les règles, et le corpus réel donne **65,5 %**
de GN+GV sur la littérature propre contre **9,1 %** pour le mélange — et **8,5 %** sur le CEGEP
OCR, au plancher du mélange. Le 61/61 est un instrument de cohérence, pas une preuve de
généralité ; la prochaine limite nommée (nom après adjectif hors lexique) est fermée, mais il
reste la voix, les causatives, les verbes à double complément.

## 6. Les blocages restants

| blocage | preuve | ce qu'il faudrait |
|---|---|---|
| **la page `/` sert l'ancien arbre** | 369 candidats stockés, **369/369 sans `profondeur`** ; 10/277/82 vs 359/2/37/221/84/13/2 ; **5 verdicts à risque** | migrer par signature (action A1), puis régénérer `phrases_generees.json` |
| **les référents ne sont pas validés** | **12/28** faux, **2** manquants, **0 note** ; valeurs = défauts de la page | auditer/corriger les 14 formes (action A2) ; forcer la résolution avant le verdict |
| **la rétro-traduction n'existe pas** | 0 script, 0 mesure, **0/9** ; clé absente | harnais `work/` + clé API (action A3) |
| **11 verdicts non committés** | sous-module `M donnees/paragraphes-validations.jsonl` (+11) ; parent à `523d8c1` | commit (hors mission) ; sinon un clone ne voit que 8 verdicts |
| **la banque est partielle** | **133/207** phrases sans verdict ; 1 annotateur ; 1 jour | reprendre après A1, avec un second lecteur |
| **les 71 langues ne testent pas les référents** | 35 concepts, 0 phrase, **0/71** par S ; UDHR = 456 langues | retirer la ligne « 71 langues de l'UDHR » du plan S ; si besoin, annoter l'UDHR |
| **la comparaison au grand modèle est absente** | `llm.jsonl` : **2 baselines**, 0 DeepSeek | clé API ; sinon le banc reste un témoin local |
| **la fiche de banque est périmée** | fiche 81/65 SHA `2d27b712…` vs export **84/67** SHA `3ca1ac20…` | mettre la fiche à jour (84/67) |
| **les docs S sont en retard** | en-cours:59 et roadmap:34 disent a001–a003 ; roadmap:356 dit a001–a009 | corriger après commit des 11 verdicts |
| **le gold est de la même main** | 61/61, contrôles 104/106/0,10 ; corpus 65,5 % vs 9,1 % | nouvelle vague holdout, autre main, après les règles |

## 7. Les 3 prochaines actions de S

Les trois actions ci-dessous **n'écrivent ni dans `tools/structures/` ni dans `data/`** : elles
produisent des copies et des mesures dans `work/` et des fiches dans `reports/`. Les écritures
dans les répertoires sacrés sont laissées à une session suivante, avec le diff correspondant.

### A1 — Débloquer la banque `/` : préparer la migration v7 (P0)

**Pourquoi.** C'est le plus gros gisement : **133 phrases** jamais vues, et la page `/` montre
l'ancien arbre. Tant que la page sert les 369 candidats de 02/11, reprendre la validation
reviendrait à juger le même arbre plat qui a fait arrêter l'humain.

**Livrable.** `work/banque-v7/phrases_generees-v7.json` (copie, pas l'original) et
`work/banque-v7/migration.json` : correspondance par **signature** (texte + type + rôle des
segments), liste des 5 verdicts à risque, des 10 orphelins et des 55 candidats changés.

**Mesure.** 369 → 359 candidats ; **0 verdict perdu** (les 5 à risque sont remappés) ;
304 identiques / 55 changés / 10 orphelins ; 99 candidats à ≥ 3 au lieu de 0 dans la vue
affichée.

**Commande existante (lecture seule) pour la mesure courante :**

```bash
cd tools/structures && PYTHONDONTWRITEBYTECODE=1 \
  python3 -c 'import json, mesure_arbre; print(json.dumps(mesure_arbre.mesurer(), ensure_ascii=False, indent=1))'
```

**Commande du harnais** (à écrire dans `work/banque-v7/preparer.py` ; n'existe pas encore) :

```bash
cd tools/structures && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  python3 ../../work/banque-v7/preparer.py
```

**Garde-fou.** Ne pas régénérer par index : `p006-c2`, `c023-c3`, `c056-c2`, `c056-c3`,
`c064-c2` seraient perdus. La signature est la clé.

### A2 — Auditer les 28 référents des 19 verdicts (P1, immédiat)

**Pourquoi.** Le journal enregistre 12 mappings faux et 2 formes manquantes ; si on l'utilise
comme gold, on apprend le défaut de la page, pas la référence. C'est le préalable à tout usage
des 19 verdicts comme banque de référents.

**Livrable.** `work/referents/verdicts-corriges.jsonl` (14 occurrences, 12 formes uniques) +
`reports/rapport-s-referents-verdicts.md` : table des 28 mappings, 12 corrections, 2 ajouts,
0 contradiction avec l'anglais.

**Mesure.** 28 mappings audités ; **14/14** occurrences avec un verdict ; **0** mapping faux ;
**0** forme manquante ; 6/9 paragraphes fautifs → **0/9**.

**Commande existante (extraction, lecture seule) :**

```bash
cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
src = {p["id"]: p for p in json.load(open("donnees/paragraphes.json"))["paragraphes"]}
vals = [json.loads(l) for l in open("donnees/paragraphes-validations.jsonl") if l.strip()]
for p in src.values():
    refs = {}
    for v in vals:
        if v["phrase_id"] == p["id"]:
            refs.update(v.get("referents") or {})
    print(p["id"], refs, "|", p["source_en"][:80])
PY
```

**Garde-fou.** Ne pas compter `en`/`y`/`on`/`cela` comme des anaphores par défaut : `en` et `y`
sont souvent des prépositions ou des partitifs ; `on` est indéfini ; `cela` reprend une
proposition. La correction doit **retirer** un référent, pas seulement le changer.

### A3 — Rétro-traduction des 9 paragraphes (P2, conditionnelle à la clé)

**Pourquoi.** C'est la seule mesure de **sortie** nommée par toutes les fiches S ; elle manque
entièrement. Elle mesurerait les pertes de sens que la traduction aller ne voit pas.

**Livrable.** `work/retro-traduction/` : 9 prompts FR → EN, 9 réponses EN, 9 prompts EN → FR,
9 réponses FR, `mesure.json` (chrF par paragraphe), et 2 relectures humaines.

**Mesure.** 9/9 paragraphes, 18/18 appels, chrF aller-retour (moyenne + min/max), 2 relectures ;
**aucun seuil** n'est fixé : le premier passage est descriptif.

**Commandes existantes** (voir § 4) : `deepseek.py`, `enseignant.py`, `mesure.py`. **Le harnais
FR → EN → FR et les 9 prompts n'existent pas** ; la clé est absente. Si la clé revient, l'action
peut démarrer sans toucher aux répertoires sacrés (`DEEPSEEK_CACHE=work/deepseek-cache`).

**Garde-fou.** Ne pas utiliser `--dry-run` comme mesure : les réponses factices ne sont pas des
traductions. Ne pas appeler un serveur local (règle 11).

## 8. Contrôles, et ce qui pourrait rendre ce rapport faux

**Contrôles négatifs.**

- **Le « 8 restants »** : s'il était vrai, il y aurait 8 paragraphes sans verdict ; il y en a
  **0**. Le compte 19/19 le réfute.
- **Le « 14/14 »** : s'il était dans le journal humain, les 19 verdicts porteraient 14 formes
  justes ; ils en portent **9/12** sur a001–a003 et **16/28** sur les 9. La source anglaise est
  le contrôle, pas la fiche.
- **La page `/` en v7** : si elle servait la v7, les 369 candidats stockés auraient
  `profondeur` ; **0/369** l'ont. La mesure dynamique est le contrôle.
- **Les 71 langues comme corpus de référents** : si c'en était un, elles auraient des phrases et
  des anaphores ; elles ont **35 concepts, 0 phrase**. La permutation (275 → 12) montre que le
  signal est lexical.
- **La couverture de la banque** : 150 verdicts ne sont pas 150 phrases ; ce sont **147 paires**
  sur **74 phrases**. Le compte des phrases est le contrôle du chiffre de tête.

**Ce qui pourrait rendre ce rapport faux.**

- **Le jugement « faux » sur les référents est le nôtre**, fondé sur la source anglaise et la
  table de la fiche. Une convention différente (possesseur vs possédé pour `sa` ; partitif vs
  référent pour `en`) déplacerait quelques cas. Les 12 signalés sont les plus robustes : ce sont
  des valeurs par défaut manifestement incompatibles (`en` → « coup », `se` → « Un moment »,
  `Je` → « le contenu »).
- **Les 19 verdicts sont un instantané** : les 11 derniers sont non committés ; un clone à
  `523d8c1` en voit 8. Le rapport décrit le working tree au 06/11 21:49, pas un commit.
- **Le taux d'acceptation n'est pas une accuracy** : un seul annotateur, une seule journée, pas
  de double-codage, pas de test-retest. Les 57,1 % de la banque et les 57,9 % des paragraphes
  sont des taux d'accord avec **un** lecteur, pas une vérité.
- **La détection de langue des 71 langues n'est pas stable** : 340–344/449 selon le run. Le
  chiffre exact ne doit pas être cité comme un point ; le taux ~76 % est la seule lecture
  robuste.
- **Les 1 433 couples incluent 4 variantes** ; le compte canonique est 1 429. Les 5 langues vides
  peuvent changer si Wikidata ajoute des labels.
- **Le snapshot peut bouger** : `generateur.py` a été modifié le 04/11 11:41 ; les mesures
  dynamiques sont celles du 06/11. Un commit des 11 verdicts ou une régénération de la banque
  changerait les comptes.
- **Pas de passe complète des portes** : les 56 tests du sous-module passent (4,3 s), mais
  `bash tools/toutes-les-portes.sh` n'a pas été lancé (lecture seule, pas de logs). Le rapport ne
  dit rien des 84 portes.
- **Le corpus de référence est partiel** : les 71 langues sont des lemmes, pas des phrases ; les
  449 surfaces sont des mots-clés, pas de la grammaire. Le « 100 % » du corpus multilingue ne
  dit rien de la syntaxe.

## 9. Fichiers

- Fiche : `reports/rapport-etat-s.md` (ce fichier) ; JSON : `reports/pensee-etat-s.json`.
- Données lues : `tools/structures/donnees/validations.jsonl` (150),
  `paragraphes-validations.jsonl` (19), `paragraphes.json` (9), `phrases.json` (7),
  `phrases_generees.json` (200), `llm.jsonl` (2), `mesure-arbre.json` ;
  `data/structures/banque-validee.jsonl` (84), `reports/s-banque-validee.json`.
- Langues : `tools/jeux/lexique_multilingue.json` (71), `tools/jeux/mesure_langues.py`,
  `reports/rapport-langues-maitres.md`, `reports/jeux-langues-mesures.json`,
  `data/udhr/` (456).
- Fiches S : `reports/rapport-s-analyseur.md`, `rapport-s-analyseur-roles.md`,
  `rapport-s-arbre-referents.md`, `rapport-s-banque-partielle.md`, `rapport-s-corpus-reel.md`,
  `rapport-s-fait-divers.md`, `rapport-s-limites-v6.md`, `rapport-s-paragraphes.md`,
  `rapport-s-traductions.md`.
- Commandes rejouées : `python3 -m unittest discover -s tests` (56 OK, 4,3 s) ;
  `python3 -m tools.jeux.mesure_langues --complet` (3,5 s) ;
  `python3 -c 'import mesure_arbre; …'` (359 candidats, 99 à ≥ 3, 294/371).
- **Aucun existant modifié ; aucun commit de ma part ; seuls les deux fichiers de ce rapport sont
  neufs.** Un commit concurrent `0a9381f0` a pris la version initiale ; les corrections de
  chronologie (36 s) sont dans le working tree, non committées.
