# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
> porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

## 1. À qui s'adresse le produit

| vous êtes… | ce que vous obtenez | ce qu'il faut savoir |
|---|---|---|
| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôles, attachement, acte de parole | c'est une **annotation**, pas une traduction ni une correction |
| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le schéma n'est pas encore versionné (§ 7) |
| **chercheur du dépôt** | le banc des fiches : gold 612, 239 cibles, rejeu | les règles sont dessinées sur ce gold : lire la **couverture**, pas seulement l'exactitude |

**Prérequis** : le dépôt, Python 3.10+ (testé en 3.13), **aucune dépendance externe**, aucun GPU,
aucun accès réseau. Les quatre gold sont versionnés dans `tools/tests/linguistique/` ; le corpus
UDHR, lui, ne l'est pas (voir § 4).

**Ce que ce n'est pas** : un produit grand public, un traducteur, un générateur, un correcteur,
un serveur. Le produit **lit** et **étiquette** ; il n'écrit pas de texte.

## 2. Ce que le produit fait

Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;
le produit en expose cinq, plus le coût et la trace.

| ce que vous demandez | ce que vous obtenez | mesure du 06/11 |
|---|---|---|
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,7581** (fermé **0,9004**, ouvert **0,6234**) |
| **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,6474** ; tête **0,7671** (vivant 612) |
| **attachement** | par syntagme : `role`, `cible`, `candidats` | **235/236** exacts sur les spans prédits ; couverture **0,9874** |
| **pragmatique** | acte (assertion, question, exclamation), négation, modalité, double sens | acte **0,9967**, négation **0,9771**, modalité **0,9886**, double sens **0,9444** |
| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
| **coût et trace** | octets, caractères, étiquettes, étapes | local, sans réseau |

**Ce que « attachement » veut dire.** Pour un syntagme, le bloc publie la **cible** à laquelle il
le rattache — le verbe pour un GN sujet ou un GP, l'antécédent pour une REL — et une liste de
**candidats**. C'est une lecture, avec sa confiance ; ce n'est pas un arbre syntaxique complet.

**Comment on le sait.** Le banc est le **gold 612** : 20 phrases `hand`, 432 réelles, 160
synthétiques ; **239 cibles** d'attachement ; **3 179 tokens**. Les règles ont été dessinées sur
ce gold : la mesure est **in-sample**, limitée par un split dev/test (153/153 et 69/69).

**Les contre-épreuves.** Le CLI imprime son propre plancher : **cible exacte tirée au hasard
1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat
aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**
**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un
résultat.

**Les deux bases.** Les chiffres publiés par la fiche v12 sont ceux du **gold gelé 602** ; le
banc vivant a **612** phrases (10 ajoutées après le gel, sans cible). Les deux bases donnent le
même attachement (235/236, couverture 0,9874 ; le gelé : 231/232, 0,9707) mais pas le même F1 :
**0,6503** sur le gelé, **0,6474** sur le vivant. Toujours lire la base avec le chiffre.

## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/drave.py analyser "Le chat dort."
```
```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.92 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». Le gold `g001`
attend exactement ces deux spans et `assertion`. `POS` est la suite des mots ; `COUVERTURE` est
la **confiance maximale déclarée** par niveau, pas une précision.

### 3.2 Analyser en JSON et lire l'attachement

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --json \
  | jq -r '[.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) → \(.meta.attachement.cible // "—")"] | join(" · ")'
```
```
GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
```

**Lecture.** Un appel = **une annotation** ; les phrases sont des étiquettes de niveau `phrase`,
pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas `g011` du
gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus
large) : dans la sortie lisible, elle apparaît comme un **doublon REL** ; le JSON la marque
`union: true`, à filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) § 2).

### 3.3 Mesurer sur le gold

```bash
python3 tools/drave.py evaluer
```
```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 83.83 %  (fermé 91.33 %, ouvert 76.73 %)
SYNTAGMES   F1 64.74 %  (P 67.05 % / R 62.59 %)
  tête      F1 76.71 %  (P 82.03 % / R 72.03 %)
ATTACHEMENT exact 98.33 % · couverture 98.74 % · exact sur span 99.58 % · top-k 97.91 %
  tête      couverture 100.00 % · top-k 99.15 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 55.37 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
```

**Lecture.** `exact 98.33 %` est le **rendement** (235/239 cibles) ; `exact sur span 99.58 %` est
l'**exactitude** sur les 236 segments dont le span est prédit. Les 3 cibles restantes n'ont pas
de segment au bon span : c'est un plafond de **couverture**, pas d'attachement. `--gold` mesure
le gold gelé 602 (F1 65,03 %, POS 84,15 %). La commande sort **0** : elle ne teste pas la cascade
(voir § 4).

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
```
```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 59
  JSON       : 11700 octets · sha256 b0a1709a97abe8d4…
```

**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
l'analyse est déterministe. C'est la garantie de base du rejeu.

### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```
```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=1
```

**Lecture.** Le CLI traite le refus comme une **erreur** : message sur `stderr`, **rien sur
`stdout`**, code **1**. Le bloc, lui, rend un JSON avec `refus: "vide"` (voir `exemples.md` § 4) :
c'est l'API qui porte l'état, le CLI qui le traduit en code. Un texte vide n'est jamais une
annotation « comme les autres ». Pour la langue, `und` est une réponse honnête : « Élodie
sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec `--langue fr` — l'indice
n'est pas une contrainte. Et `--langue de` sort **2** : le CLI n'accepte que `fr` et `en`.

## 4. Ce que le produit ne fait pas encore

**1. Il n'écrit pas de texte.** Pas de restitution, pas de traduction, pas de génération : le
produit rend des **étiquettes**, jamais une phrase. Les résultats de traduction de la vitrine
([`README.md`](../../README.md)) sont une recherche sur un modèle externe ; ils ne sont pas dans
ce produit.

**2. Trois spans restent inatteignables.** Sur **239 cibles**, **235** sont attachées
(couverture **0,9874**) ; **3** ne le sont pas : **1 REL, 2 SUB, 0 GP**. Elles sont
**inatteignables sans corriger le gold ou le lexique** — quatre sont des cas réels nommés dans
l'audit v10 (`r035`, `r255`, `r264`, `g017`), les autres viennent du gold synthétique, dont le
lexique est disjoint. Conséquence : **235/236 (0,9958)** est l'exactitude **conditionnelle aux
spans prédits**, pas la couverture du langage. Lire les deux ensemble.

**Le doublon REL de l'union.** Deux REL peuvent se chevaucher : la plus longue porte
`meta.union: true`. C'est une **lecture concurrente** publiée par l'union, pas un second
attachement ; la sortie lisible la montre comme un **doublon REL**, et il faut la filtrer pour
une lecture unique (garder `union: null`, ou le segment qui en contient un autre).

**3. `cascade_pos` : le plancher, pas le gain.** La « rouge » historique est devenue un
**plancher** : le banc exige **0,70** et la cascade rend **0,7465**, donc la porte
`porte-bloc-linguistique.sh` est **verte**. Mais la cascade (heuristique + `MockNeuronal`) reste
**sous l'heuristique (0,7581)** en POS : la fusion par confiance laisse gagner le stub. Ce n'est
pas un gain de POS ; c'est un **échange** — les syntagmes sont meilleurs (F1 **0,6141** contre
**0,6474**, tête **0,7707** contre **0,7671**). Le produit par défaut reste l'heuristique, et
`drave evaluer` ne mesure qu'elle. La cascade avec le vrai tagger 7B a été mesurée à **0,9415**
en POS sur 180 phrases, mais elle exige un serveur local 7B, que la règle 11 interdit
aujourd'hui : ce n'est pas un chemin livré.

**4. Pas de neuronal.** `MockNeuronal` est un **contrat** déterministe, pas un tagger de qualité.
Le vrai adaptateur (`NeuronalLLM`, `NeuronalLLMPOS`) parle à un serveur local ; il n'est ni requis
ni utilisé par défaut, et le CLI ne l'expose pas.

**5. Les classes ouvertes sont fragiles.** POS fermé **0,9004**, ouvert **0,6234** : les mots
inconnus tombent souvent en NOUN. Exemple réel : dans « Le livre que j'ai lu… », `lu` est tagué
NOUN ; dans « The day when we left… », `left` est NOUN. Un lexique plus large améliorerait ces
cas, pas une règle.

**6. La langue n'est pas forcée.** `--langue` est un **indice**, limité à `fr` et `en` dans le
CLI ; sous le seuil de confiance, la sortie reste `und`. Il n'y a pas de `--langue-forcee`. Les
profils UDHR (398 langues, 0,9687) ne sont pas exposés par le CLI et ne sont pas versionnés :
`data/` est hors dépôt, et le corpus XML source est externe. Sans eux, la détection se rabat sur
les indices internes.

**7. Pas de RSN, pas de DRVM, pas de serveur.** Le bloc a le contrat, la trace et le coût ; il
ne produit pas le corps de la RSN, n'est pas un port DRVM et n'expose pas d'API HTTP. La couche
sémantique est un **compteur d'unités**, pas une représentation.

**8. Pas de classement appris ni de gold 200+.** L'attachement est une **heuristique de
proximité** avec candidats ; il n'y a pas de modèle de classement. Le gold fait 612 phrases, dont
160 synthétiques ; le gold 200+ réel reste à faire.

**9. Pas de calibration des confiances.** `confiance` est **déclarée** (0,3 pour un NOUN ouvert,
0,92 pour un DET), pas mesurée comme une probabilité. Elle sert à trier, pas à seuiller une
décision automatique sans contrôle.

**10. Pas de texte arbitraire garanti.** Les mesures sont sur le gold ; les règles y ont été
dessinées. Sur un texte hors domaine, la couverture et la précision peuvent baisser sans que le
JSON change de forme — d'où le rejeu et le contrôle par un gold à soi (§ 7, manque de schéma).

## 5. Performance

| ce qui est mesuré | valeur | conditions |
|---|---|---|
| **612 phrases du gold** | **0,36 s** (mesure du 06/11) ; **0,45–0,55 s** (audit) ; **~0,6 s** (chiffre rond publié) | heuristique, un cœur, 3 179 tokens |
| **`drave evaluer`** | **0,55 s** au total | une lecture (heuristique), démarrage Python compris |
| **`drave analyser`** | **0,15 s** au total | une phrase, démarrage compris |
| **cache du chunker** | **×138,7** à 160 répétitions (9 817,7 → 70,8 ms) | banc de texte **répété**, chemin chunker |
| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |
| **cache, corpus réel** | **×1,2** | phrases réelles, 6,1 tokens/phrase |
| **sortie** | **identique** : 0 différence sur 612 phrases, tous champs | le cache ne change pas une mesure |

**Ce que le ×139 veut dire — et ne veut pas dire.** C'est la suppression du **O(n²)** du chunker
sur un texte **répété** : 1 + 2S appels ramenés à 1, verbes de GV mémoïsés par span. Sur du texte
réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer
« ×139 plus rapide » sans la condition serait faux. Ce que le cache garantit, c'est que les
textes longs et répétés ne s'effondrent plus.

**Ce que le produit ne consomme pas** : pas de GPU, pas de modèle, pas de réseau, pas d'écriture
disque (hors le fichier de sortie). Le cache est **local à une analyse** et libéré à chaque
phrase. Les temps sont CPU, sur machine partagée ; ils varient avec la charge.

## 6. Garanties

| garantie | ce que ça veut dire | contrôle |
|---|---|---|
| **déterminisme** | même entrée → même JSON, octet pour octet | `drave rejouer` (§ 3.4) ; `tools/tests/test_produit.py` compare deux sorties |
| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; les adaptateurs neuronaux sont locaux et non utilisés |
| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : `stderr` + code 1 |
| **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
| **spans lisibles** | indices en **points de code Unicode**, 0-based, `[debut:fin)` | « Élodie » → `[0:6]` ; emoji = 1 point |
| **UTF-8** | le JSON est en UTF-8, non échappé, sans durée | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` |
| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |
| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |

**La porte produit, mesurée le 06/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
étiqueté en `fr` et `en`, `sha256 6b6def477a493444` deux fois, **6 tests** de fumée,
**183/183** portes d'autotest. Le smoke test est `tools/tests/test_produit.py`.

**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2** ; le contrat cible **3 / 4**
n'est pas encore là :

| code | sens | aujourd'hui |
|---:|---|---|
| **0** | succès : annotation rendue, évaluation rendue, rejeu identique | `analyser`, `evaluer`, `rejouer` |
| **1** | erreur ou **refus d'analyse** | `analyser ""` ; `rejouer ""` ; divergence de rejeu |
| **2** | usage invalide : argument, sous-commande, langue hors `fr`/`en` | `argparse` |
| **3** | refus **distinct** de l'erreur, avec l'annotation de refus sur `stdout` | **non implémenté** |
| **4** | dépendance absente : modèle, profils | **non implémenté** |

**Ce qui n'est pas garanti** : le chemin neuronal, un texte hors domaine, la calibration des
confiances, la stabilité du schéma (pas de champ `version`), et le comportement sur un lot de
textes (une invocation = un texte).

## 7. Le CLI livré — contrat et manques

Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.

```bash
python3 tools/drave.py --version
python3 tools/drave.py --aide
python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json]
python3 tools/drave.py evaluer [--gold] [--json]
python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
```

**Sorties réelles des commandes** (06/11) :

```
$ python3 tools/drave.py --version
drave 0.1.0

$ python3 tools/drave.py evaluer --gold
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement
...
SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)
  tête      F1 73.92 %  (P 81.36 % / R 67.72 %)
...
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)

$ python3 tools/drave.py rejouer "Le chat dort."
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 19
  JSON       : 4013 octets · sha256 6b6def477a493444…
```

**Options du CLI** :

| option | commande | sens |
|---|---|---|
| `--langue fr\|en` | `analyser`, `rejouer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
| `--json` | `analyser`, `evaluer` | sortie machine UTF-8 |
| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
| `-V`, `--version` | global | `drave 0.1.0` |
| `-h`, `--aide` | global | l'aide, largeur fixe |

**Ce qui manque encore** (le contrat cible, non livré) :

| manque | conséquence |
|---|---|
| **`--fichier` / l'entrée standard** | on ne peut analyser qu'un texte passé en argument ; pas de pipe, pas de fichier |
| **`--sortie`** | pas d'écriture directe d'un JSON ; il faut rediriger le shell |
| **`rejouer` sur un JSON sauvegardé** | `rejouer` prend un **texte**, pas une annotation ; on ne peut pas rejouer un fichier produit hier |
| **les codes 3 et 4** | le refus est confondu avec une erreur (code 1) et n'a pas de JSON sur `stdout` ; une dépendance absente n'est pas distinguée |
| **un champ `schema` / une version de format** | impossible d'épingler un rejeu à une version ; `--version` ne donne que `0.1.0`, sans commit ni schéma |
| **`--mode` / la cascade** | le CLI n'expose que l'heuristique ; `parallele` et `cascade` demandent le code Python |
| **`--profils`** | les 398 langues de l'autotest UDHR ne sont pas accessibles par le CLI |
| **`--duree`** | pas de durée dans le JSON du CLI (le bloc l'a avec `--duree`) |
| **un lot de textes** | une invocation = un texte ; pas de JSONL, pas de répertoire |
| **`candidats` structurés** | ce sont des **chaînes d'affichage** (« « qui dort » → voisine »), pas des objets `{span, cible}` ; un programme doit les reparser |
| **`role` normalisé** | les valeurs mélangent `predicat`/`prédicat` et `qualite`/`qualité` ; fragile pour un filtre |
| **`--strict`** | `evaluer` ne mesure pas la cascade et n'applique pas son plancher (0,70) ; c'est le banc de recherche (`evaluer_gold.py`) qui le fait |
| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
| **le chemin neuronal** | la cascade 7B (0,9415) exige un serveur local interdit par la règle 11 ; pas de chemin neuronal livré |

**Ce qui est déjà tenu** : `--version`, `--aide`, les trois sous-commandes, le JSON déterministe,
le rejeu par empreinte, la porte produit et le smoke test. Le reste est nommé ci-dessus, sans
être présenté comme acquis.

## 8. Où aller ensuite

| si vous voulez… | allez à |
|---|---|
| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
| **le contrat du bloc** (9 niveaux, substitution, activation) | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
| **les chiffres de l'attachement** (v12, instantané) | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) · [`reports/pensee-v12.json`](../../reports/pensee-v12.json) |
| **l'audit des mesures** (contrôles, spans, bases) | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |
| **la cascade réelle** (0,9415, 7B, non livrée) | [`reports/rapport-pensee-gold-cascade.md`](../../reports/rapport-pensee-gold-cascade.md) |
| **le plancher `cascade_pos`** et les repères des passes | [`docs/pilotage/references-non-regression.md`](../pilotage/references-non-regression.md) |
| **l'ancien constat « pas de produit »** (27/10) | [`docs/pilotage/utilisation.md`](../pilotage/utilisation.md) |
| **la théorie de la couche heuristique** | [`docs/theorie/pre-traitement-linguistique.md`](../theorie/pre-traitement-linguistique.md) |

**Un mot sur la méthode.** Le produit ne remplace pas la fiche : les chiffres vivent dans
`reports/`, avec leur dispositif, leur contrôle négatif et ce qui pourrait les rendre faux. Cette
notice dit seulement ce qu'un utilisateur peut en faire **aujourd'hui**, et ce qu'il ne peut pas
encore faire.
