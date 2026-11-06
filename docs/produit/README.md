# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le CLI unifié **`tools/drave.py`** est
> **livré** : `analyser`, `evaluer`, `rejouer`, `--version` ; la **porte produit**
> (`bash tools/porte-produit.sh`) le vérifie en **6 contrôles** et **1 min 56** ; le smoke test
> `tools/tests/test_produit.py` passe **6 tests en 1,2 s**. Les exemples du § 3 sont réels : ils
> ont été lancés pour ce document.
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
| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (UDHR, article 15 tenu à part) |
| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,7581** (fermé **0,9004**, ouvert **0,6234**) |
| **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,5849** ; tête **0,7336** (vivant 612) |
| **attachement** | par syntagme : `role`, `cible`, `candidats` | **222/222** exacts sur les spans prédits ; couverture **0,9289** |
| **pragmatique** | acte (assertion, question, exclamation), négation, modalité, double sens | acte **0,9967**, négation **0,9771**, modalité **0,9886**, double sens **0,9444** |
| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |
| **coût et trace** | octets, caractères, étiquettes, durée (`--duree`), étapes | local, sans réseau |

**Ce que « attachement » veut dire.** Pour un syntagme, le bloc publie la **cible** à laquelle il
le rattache — le verbe pour un GN sujet ou un GP, l'antécédent pour une REL — et une liste de
**candidats**. C'est une lecture, avec sa confiance ; ce n'est pas un arbre syntaxique complet.

**Comment on le sait.** Le banc est le **gold 612** : 20 phrases `hand`, 432 réelles, 160
synthétiques ; **239 cibles** d'attachement ; **3 179 tokens**. Les règles ont été dessinées sur
ce gold : la mesure est **in-sample**, limitée par un split dev/test (153/153 et 69/69). Les
contre-épreuves sont publiées : permutation des cibles **1,997/220 = 0,908 %** (p = 0), candidat
aléatoire **42,14 %** de top-1 (contrôle de l'audit v10, 220 labels ; la fiche v12 donne une
marge du même ordre). Un chiffre sans sa contre-épreuve n'est pas un résultat.

**Les deux bases.** Les chiffres publiés par la fiche v12 sont ceux du **gold gelé 602** ; le
banc vivant a **612** phrases (10 ajoutées après le gel, sans cible). Les deux bases donnent le
même attachement (222/222, couverture 0,9289) mais pas le même F1 : **0,5893** sur le gelé,
**0,5849** sur le vivant. Toujours lire la base avec le chiffre — c'est la leçon de l'audit v10.

## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/bloc_linguistique.py --texte "Le chat dort." --json \
  | jq -r '"\(.langue) \(.script) · " + ([.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) [\(.debut):\(.fin)] → \(.meta.attachement.cible // "—")"]
           | join(" · "))'
```
```
fr Latn · GN Le chat [0:7] → dort · GV dort [8:12] → chat
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». `jq` ne sert qu'à
l'affichage ; le produit n'en dépend pas. Le JSON complet contient aussi les niveaux `graphème`,
`mot`, `morphème`, `discours` et `document`, la `phrase` et la `pragmatique`.

### 3.2 Analyser un fichier et garder le JSON

```bash
printf "Le livre que j'ai lu est intéressant.\n" > /tmp/page.txt
python3 tools/bloc_linguistique.py --fichier /tmp/page.txt --json > /tmp/page.json
jq -r '"\(.langue) · \(.etiquettes|length) étiquettes · " + ([.etiquettes[]
       | select(.niveau=="syntagme")
       | "\(.type) \(.valeur) → \(.meta.attachement.cible // "—")"] | join(" · "))' /tmp/page.json
```
```
fr · 42 étiquettes · GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
```

**Lecture.** Un fichier = **une annotation** ; les phrases sont des étiquettes de niveau
`phrase`, pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas
`g011` du gold). Le bloc publie aussi une **seconde lecture d'union** (`union: true`, span plus
large) : c'est une lecture concurrente, pas un doublon à consommer naïvement.

### 3.3 Mesurer sur le gold

```bash
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/gold.json >/dev/null; echo "exit=$?"
jq -r '.heuristique.all | "POS \(.pos.exactitude) · F1 \(.syntagme.f1) · tête \(.syntagme.tete.f1) · attachement \(.attachement.exact)/\(.attachement.labels) (couverture \(.attachement.couverture))"' /tmp/gold.json
```
```
exit=1
POS 0.7581 · F1 0.5849 · tête 0.7336 · attachement 222/222 (couverture 0.9289)
```

**Lecture.** Le banc mesure **20 combinaisons** (4 lectures × 5 sources) et écrit un JSON de
recherche ; ici on lit la ligne `heuristique.all`. Le **code de sortie est 1** parce qu'une seule
rouge est ouverte : `cascade_pos` (voir § 4). Ce n'est pas un échec de l'analyse : c'est une
comparaison défavorable entre l'heuristique et la cascade de contrat.

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/bloc_linguistique.py --fichier /tmp/page.txt --json > /tmp/a.json
python3 tools/bloc_linguistique.py --fichier /tmp/page.txt --json > /tmp/b.json
cmp /tmp/a.json /tmp/b.json && echo "identique · $(sha256sum /tmp/a.json | cut -c1-16)…"
```
```
identique · c1f3c76a5a40fcbd…
```

**Lecture.** Deux exécutions indépendantes rendent le **même octet** : l'analyse est
déterministe. C'est la garantie de base du rejeu. Attention : `--duree` ajoute un champ
`cout.duree_s` volatil ; pour comparer, ne pas l'utiliser (ou l'ignorer).

### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/bloc_linguistique.py --texte "" --json \
  | jq '{langue, script, refus, etiquettes: (.etiquettes|length)}'
```
```json
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "etiquettes": 0
}
```

**Lecture.** Un texte vide (ou de la ponctuation seule) est **refusé** : `refus: "vide"`, zéro
étiquette. Le produit **n'invente pas**. Aujourd'hui la commande sort **0** ; le CLI cible doit
sortir **3** (§ 6). Tant que ce n'est pas fait, un script doit tester `.refus`, pas le code de
sortie. Pour la langue, `und` est une réponse honnête : « Élodie sourit. » rend `und` (confiance
0,04 < seuil 0,12), même avec `--langue fr` — l'indice n'est pas une contrainte (§ 4).

## 4. Ce que le produit ne fait pas encore

**1. Il n'écrit pas de texte.** Pas de restitution, pas de traduction, pas de génération : le
produit rend des **étiquettes**, jamais une phrase. Les résultats de traduction de la vitrine
([`README.md`](../../README.md)) sont une recherche sur un modèle externe ; ils ne sont pas dans
ce produit.

**2. Dix-sept spans restent inatteignables.** Sur **239 cibles**, **222** sont attachées
(couverture **0,9289**) ; **17** ne le sont pas : **8 REL, 5 SUB, 4 GP**. Elles sont
**inatteignables sans corriger le gold ou le lexique** — quatre sont des cas réels nommés dans
l'audit v10 (`r035`, `r255`, `r264`, `g017`), les autres viennent du gold synthétique, dont le
lexique est disjoint. Conséquence : **222/222 (1,0000)** est l'exactitude **conditionnelle aux
spans prédits**, pas la couverture du langage. Lire les deux ensemble.

**3. La rouge `cascade_pos`.** La cascade (heuristique + `MockNeuronal`) donne **0,7465** en POS,
sous l'heuristique **0,7581** : la fusion par confiance laisse gagner le stub. C'est une **rouge
tolérée**, listée dans les références de non-régression. Elle améliore pourtant les syntagmes
(F1 **0,6141** contre **0,5849**, tête **0,7432** contre **0,7336**) : c'est un **échange**, pas
un gain. Le produit par défaut reste l'heuristique. La cascade avec le vrai tagger 7B a été
mesurée à **0,9415** en POS sur 180 phrases, mais elle exige un serveur local 7B, que la règle 11
interdit aujourd'hui : ce n'est pas un chemin livré.

**4. Pas de neuronal.** `MockNeuronal` est un **contrat** déterministe, pas un tagger de qualité.
Le vrai adaptateur (`NeuronalLLM`, `NeuronalLLMPOS`) parle à un serveur local ; il n'est ni requis
ni utilisé par défaut.

**5. Les classes ouvertes sont fragiles.** POS fermé **0,9004**, ouvert **0,6234** : les mots
inconnus tombent souvent en NOUN. Exemple réel : dans « Le livre que j'ai lu… », `lu` est tagué
NOUN ; dans « The day when we left… », `left` est NOUN. Un lexique plus large améliorerait ces
cas, pas une règle.

**6. La langue n'est pas forcée.** `--langue` est un **indice** : sous le seuil de confiance, la
sortie reste `und`. Il n'y a pas de `--langue-forcee`. Les profils UDHR (398 langues, 0,9687)
ne sont pas versionnés : `data/` est hors dépôt, et le corpus XML source est externe. Sans eux,
la détection se rabat sur les indices internes.

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
| **une phrase** | ~0,6 ms en régime | après le démarrage Python |
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
| **déterminisme** | même entrée → même JSON, octet pour octet | deux exécutions + `cmp` (§ 3.4) ; `--duree` ajoute un champ volatil |
| **hors réseau** | le chemin par défaut n'ouvre aucune socket | analyse `heuristique` seulement ; les adaptateurs neuronaux sont locaux et non utilisés |
| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | `bloc_linguistique.py --texte ""` |
| **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
| **spans lisibles** | indices en **points de code Unicode**, 0-based, `[debut:fin)` | « Élodie » → `[0:6]` ; emoji = 1 point |
| **UTF-8** | le JSON est en UTF-8, non échappé | `--json` |
| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |

**Codes de sortie — contrat cible.** Ils ne sont pas tous implémentés aujourd'hui (voir § 7) :

| code | sens | aujourd'hui |
|---:|---|---|
| **0** | succès : annotation rendue, évaluation conforme, rejeu identique | `bloc_linguistique.py` sort 0, **même sur refus** |
| **1** | résultat non conforme : seuil manqué, divergence de rejeu | `evaluer_gold.py` sort **1** à cause de `cascade_pos` |
| **2** | usage invalide : argument, fichier, JSON | `argparse` sort 2 |
| **3** | refus d'analyse (`refus` non vide) | **non implémenté** |
| **4** | dépendance absente : modèle, profils | **non implémenté** |

**Ce qui n'est pas garanti** : le chemin neuronal, un texte hors domaine, la calibration des
confiances, la stabilité du schéma (pas de champ `version`), et le comportement sur un lot de
textes (une invocation = un texte).

## 7. Le CLI en préparation — contrat et manques

Le prototype *tools/drave.py* est **en cours d'écriture** par une autre session. Ce qui suit est
le **contrat attendu** ; rien n'est supposé livré. Chaque commande a son **équivalent
exécutable** dans le tableau plus bas.

```bash
python3 tools/drave.py --version
python3 tools/drave.py analyser "Le chat dort."
python3 tools/drave.py analyser --fichier page.txt --json --sortie page.json
python3 tools/drave.py evaluer
python3 tools/drave.py rejouer page.json
```

**Sorties attendues** (forme cible ; les valeurs sont celles du 06/11) :

```
$ python3 tools/drave.py --version
drave 0.1.0 · schéma annotation/1 · commit bdeca168 · s/v7 · Python 3.13.16

$ python3 tools/drave.py analyser "Le chat dort."
fr · Latn · refus=- · 3 mots · 2 syntagmes · acte=assertion
  POS        Le/DET   chat/NOUN   dort/VERB
  syntagmes  GN « Le chat » [0:7] agent → dort
             GV « dort »     [8:12] predicat → chat
  unités     2 (61,5 %)

$ python3 tools/drave.py evaluer
gold vivant 612 · 239 cibles · 3 179 tokens
attachement  222/222 exact (1,0000) · couverture 0,9289 · top-k 221/239
syntagmes    F1 0,5849 · tête 0,7336
POS          0,7581 (fermé 0,9004 · ouvert 0,6234)
pragmatique  acte 0,9967 · négation 0,9771 · modalité 0,9886 · double sens 0,9444
spans        17 non attachés (8 REL, 5 SUB, 4 GP)
verdict      conforme · 1 rouge tolérée : cascade_pos (0,7465 < 0,7581)

$ python3 tools/drave.py rejouer page.json
rejeu : 1 annotation · 42 étiquettes · identique · sha256 c1f3c76a5a40fcbd…
```

`0.1.0` est la **seule version du dépôt** (`drave-core/Cargo.toml`) : il n'existe encore ni
version Python ni champ `schema` dans le JSON. Le `commit` et la branche viennent de Git ; le
reste est à figer.

**Options minimales du contrat** :

| option | commande | sens |
|---|---|---|
| `--fichier F` | `analyser` | lire un fichier au lieu du texte |
| `--langue L` | `analyser` | **indice** de langue, pas une contrainte |
| `--mode M` | `analyser` | `heuristique` (défaut), `parallele`, `cascade` |
| `--profils F` | `analyser` | profils UDHR (`data/udhr/articles.jsonl`, non versionné) |
| `--json` | `analyser`, `evaluer`, `rejouer` | sortie machine UTF-8 |
| `--sortie F` | `analyser`, `evaluer` | écrire dans F (aujourd'hui : redirection shell) |
| `--duree` | `analyser` | ajouter `cout.duree_s` (volatil) |
| `--gold vivant\|gele` | `evaluer` | base 612 ou 602 (défaut : vivant) |
| `--bloc heuristique\|cascade` | `evaluer` | lecture mesurée (défaut : heuristique) |
| `--strict` | `evaluer` | une rouge tolérée devient fatale (sortie 1) |

**Équivalents exécutables aujourd'hui** :

| commande cible | équivalent réel | état |
|---|---|---|
| `--version` | `git log -1 --format='%h %s'` + `python3 --version` | pas de version produit |
| `analyser TEXTE` | `python3 tools/bloc_linguistique.py --texte TEXTE --json` | livré |
| `analyser --fichier F` | `python3 tools/bloc_linguistique.py --fichier F --json` | livré |
| `evaluer` | `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/gold.json` | livré, sortie de recherche |
| `rejouer F` | deux exécutions + `cmp` (§ 3.4) | manuel |

**Ce qui manque pour livrer le CLI** :

| manque | conséquence |
|---|---|
| **le fichier *tools/drave.py*** | pas de point d'entrée unique ; il faut connaître deux scripts |
| **`--version` et un champ `schema`** | impossible d'épingler un rejeu à une version de format ; aucun consommateur ne peut vérifier ce qu'il lit |
| **`rejouer`** | le déterminisme se vérifie à la main (deux fichiers + `cmp`) |
| **les codes 3 et 4** | un refus ressemble à un succès ; une dépendance absente n'est pas distinguée |
| **une sortie produit stable** | le JSON expose les 9 niveaux internes ; `meta.attachement` et `candidats` n'ont pas de schéma publié |
| **`candidats` structurés** | ce sont des **chaînes d'affichage** (« « qui dort » → voisine »), pas des objets `{span, cible}` ; un programme doit les reparser |
| **`role` normalisé** | les valeurs mélangent `predicat`/`prédicat` et `qualite`/`qualité` ; fragile pour un filtre |
| **un `evaluer` qui ne confond pas rouge tolérée et échec** | aujourd'hui `evaluer_gold.py` sort 1 à cause de `cascade_pos` ; la cible sort 0, et 1 seulement avec `--strict` |
| **un schéma de gold publié** | un utilisateur ne peut pas mesurer son propre corpus sans lire le code |
| **un test de fumée et une porte** | le commit du 06/11 annonce le smoke test et la porte ; ils ne sont pas encore là |
| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
| **le chemin neuronal** | la cascade 7B (0,9415) exige un serveur local interdit par la règle 11 ; pas de chemin neuronal livré |

## 8. Où aller ensuite

| si vous voulez… | allez à |
|---|---|
| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
| **le contrat du bloc** (9 niveaux, substitution, activation) | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
| **les chiffres de l'attachement** (v12, 222/222) | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) · [`reports/pensee-v12.json`](../../reports/pensee-v12.json) |
| **l'audit des mesures** (contrôles, spans, bases) | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |
| **la cascade réelle** (0,9415, 7B, non livrée) | [`reports/rapport-pensee-gold-cascade.md`](../../reports/rapport-pensee-gold-cascade.md) |
| **la rouge tolérée** et les repères des passes | [`docs/pilotage/references-non-regression.md`](../pilotage/references-non-regression.md) |
| **l'ancien constat « pas de produit »** (27/10) | [`docs/pilotage/utilisation.md`](../pilotage/utilisation.md) |
| **la théorie de la couche heuristique** | [`docs/theorie/pre-traitement-linguistique.md`](../theorie/pre-traitement-linguistique.md) |

**Un mot sur la méthode.** Le produit ne remplace pas la fiche : les chiffres vivent dans
`reports/`, avec leur dispositif, leur contrôle négatif et ce qui pourrait les rendre faux. Cette
notice dit seulement ce qu'un utilisateur peut en faire **aujourd'hui**, et ce qu'il ne peut pas
encore faire.
