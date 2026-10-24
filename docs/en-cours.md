2026-10-24

# En ce moment

**Mis à jour : 2026-10-24, 08 h 24 HAE (heure locale, EDT).**

> Cette page dit l'**état courant**, pas l'histoire. Les résultats mesurés sont dans
> [`reports/`](../reports/), le récit daté dans [`journal/`](../journal/), la mission et l'ordre des priorités dans
> [`AGENTS.md`](../AGENTS.md).

## La synthèse (lire si on ne lit qu'une page)

**La cible.** Un **étage entrée-sortie** qui lit et produit **toutes les langues, dialectes et styles**, dans tous
les registres, et qu'on juge en **qualité de traducteur** — restitution à l'identique et traduction du sens. Quand il
sera **fiable**, l'**étage 2** (pensée abstraite, indépendante de la langue) pourra commencer : on n'y passe pas
avant ([AGENTS.md](../AGENTS.md) § 1).

**La décision de périmètre (21/10, soir).** Les langues à couvrir s'arrêtent au **français inclus** (Ethnologue 2026) — un sous-ensemble des **20** déjà
mesurées ; les autres restent des **marges**, pas le critère. *L'étage 2 devient le chantier principal* — l'entrée-sortie est
**fiable sur le périmètre**, et les registres restants (parlé, technique) continuent en parallèle, sans bloquer.

**Les résultats du moment (21 octobre).**

- **Le juge a changé** : le banc UDHR était **contaminé** (le 7 B **récite** l'article 1 au lieu de traduire,
  mesure 61). Le juge est désormais un **texte neuf** : un règlement européen de 2025, 139 unités alignées par
  structure, traductions humaines.
- **La qualité réelle** y est de **55-76 de chrF** (0,5-14 B, mesures 62-63-66) — **+30 à +40** au-dessus du
  plancher, **loin de 100**. Elle **se réplique** sur un second règlement (+1,1 à +2,5, mesure 67).
- **La taille aide, mais de moins en moins** : 54,7 → 73,3 (eng→fra) du 0,5 au 14 B ; le gain par doublement tombe
  à **+0,9** (7 → 14 B, fra→eng) — mesures 63 et 66. *Le levier n'est pas la taille seule.*
- **Six registres mesurés** : juridique (+35,3 de marge), **presse** (+38,6), **littéraire** (+25,9),
  **parlé préparé** (TED2020 : +39,8 / +40,7, mesure 143), **technique** (**JRC juridico-technique : +36,4 /
  +34,9, mesure 159** ; **prose MultiUN : +33,2 / +32,9, mesure 165** ; WikiMatrix miné : +41 / +46, gonflé) et **dialogue** (OpenSubtitles : +32,3 / +33,6, mesure 148) ; le **dialogue spontané** (DiaBLa) donne **+35,0 / +39,3** au 1,5 B avec ses **références indépendantes** (+40,3/+44,2 en post-édition : le biais est de +5) — plus facile que les sous-titres, la carte gagne sa ligne — le littéraire est le plus dur, mais **pas par le
  contenu** : **96 %** des noms, **0,5 %** d'omissions ; l'écart est de **style** (mesures 64 et 68).
- **La couverture des langues est le facteur** : sur les **24 langues officielles de l'UE**, **+35,8** de marge sur
  le hasard pour les **13 langues annoncées** par le modèle, **+21,5** pour les **10 autres** ; les trous sont
  l'**irlandais (+8,0)** et le **maltais (+10,8)** (mesure 71). *L'écart brut entre langues est surtout la
  distance* (mesure 69), et le plancher **dépend de l'écriture** (28ᵉ piège). **La taille ne comble pas cet écart** :
  il passe de 15,6 (3 B) à 14,2 (7 B), soit −1,4 (mesure 72).
- **L'entrée sait signaler son bruit** (fautes et langues mêlées : **AUC 1,00**), **pas le corriger** : 8/9 des
  corrections empirent, et la plus fluide est la plus fausse (mesure 65).
- **L'étage 2 est ouvert** (périmètre tenu, mesures 73-76 et 107) : la représentation neutre **existe** (un pont
  linéaire retrouve la bonne traduction dans **28-69 %**, mesure 77), elle **ne dépend presque pas de la taille**
  (+3,7, mesure 78) ; la **composition** est démontrée sur des phrases alignées (**0,61 / 0,84**, mesure 80) et
  **profite de la taille** (**0,76 / 0,865** au 7 B, mesure 81) ; mais le **pas de pensée linéaire n'existe pas** :
  après l'**erratum 6**, l'opérateur prédit la **moyenne** (effondrement 0,89-0,99, retrieval au hasard, mesure 113)
  et un opérateur **contrastif** ne fait pas mieux (mesure 113) ; avec **630 séries** et **1 323 transitions**
  (mesure 115), ni le linéaire ni le MLP ne retrouvent la phrase suivante — *l'état d'une phrase ne porte pas la
  suivante* ; le **contexte** (8 phrases, moyenne + GRU) ne porte pas le **contenu** non plus (0,14 contre 0,125,
  mesure 116) ; un **code de plan** de 32 dimensions ne dépasse la moyenne que de **+0,02** (0,86-0,89 contre
  0,83-0,88, mesure 117) ; la **langue** est parfaitement décodable (1,00) alors que la **position** ne l'est pas
  (0,13 contre 0,125, mesure 118) — *l'état porte la langue, pas la structure* ; l'**état latent entraîné avec la
  tâche** collapse en point fixe (mesures 109-110) — *le plan est un mince résidu : il faut l'**entraîner** dans le
  modèle* ; c'est fait : un LoRA contrastif fait passer le retrieval de contenu de **0,239 à 0,443** (hasard 0,125 ;
  contrôle à cibles mélangées **0,227**) — **le plan s'entraîne** (mesure 119) et le **même** état porte **trois
  pas** (0,443 / 0,295 / 0,341, mesure 120) ; mais les contrôles **tempèrent** : le transfert aux cibles figées est
  de +0,05 à +0,08 (mesures 121, 123) et **nul à 16 phrases** (0,193 contre 0,189, mesure 122) — le gain est surtout
  l'adaptation de l'espace cible ; c'est fait : **contre des cibles figées**, le plan transfère (0,324 / 0,273 / 0,216 en moyenne de deux graines, mesure 124), mais seul h1 est solide.
- **Le raisonnement est dans l'état** (mesures 125-164 ; la carte complète est dans
  [05](synthese/05-la-pensee-sans-verbaliser.md)) : synthétique **1,00 → 0,51**, naturel **0,50-0,59** ; un **pont
  linéaire** l'aligne (**0,81-0,97** synthétique, **0,59-0,77** naturel), à 3/7/14 B, jusqu'à **12 entités** ;
  l'alignement **s'apprend** par l'entraînement bilingue (**0,656**) et **sature** (**0,753**) ; le **plan
  résiste** (ponts, bilinguisme, contraste : 0,25-0,39, effet côté cible).
- **Ce qui tient déjà** : la langue est **lisible partout** (80-100 %), le **sens traverse les langues** (96 % sur
  les paires couvertes), l'alignement **suit la généalogie** (37/28/11 %), et la **restitution exacte** existe pour
  un modèle spécialisé (85 %) mais **meurt à 10 langues** (4 %).
- **Le périmètre démographique est tenu** : les langues jusqu'au **français inclus** (Ethnologue 2026) sont
  couvertes, et les **20** le sont aussi (mesures 73-76 et 107) — les 19 sur texte neuf, le **pidgin nigérian** lu
  (+4,4 au 14 B) et écrit avec un adaptateur 14 B (**+5,8 [+4,1 ; +7,6]** sur 71 pages, mesure 112) ; *les 20 sont
  une **marge**, le critère s'arrête au français* ✓✓.

**Le plan de match, en relation avec la cible.**

1. **Compléter les registres** : juridique ✅, presse ✅, littéraire ✅ ; les six registres sont mesurés ; restent un **technique à référence humaine** et de la conversation **réelle**.
2. **Les langues sont closes au périmètre** : les langues jusqu'au **français inclus** sont couvertes ; les 20 le sont
   aussi (marges). La **direction inverse** (X→eng) et le **dialogue spontané** restent des **marges**, pas des portes.
3. **Choisir le levier** : la taille donne des rendements décroissants et **ne comble pas la couverture**
   (mesure 72) ; le prochain levier est la **couverture** — et un **découpage de surface** par langue/famille
   (MoE d'adaptateurs, C5.6), pas un noyau séparé —
   (données par langue et par domaine) et la **représentation** — la **RSN multi-niveaux**, en **unités de sens**,
   jamais en jetons.
4. **L'étage 2 est le chantier principal** : la représentation (77), la taille (78), la composition (79-81, 87) sont
   mesurées ; la **dynamique** est le verrou — l'opérateur linéaire **n'existe pas** (mesure 113), le latent
   **collapse** (109-110) — *la question suivante est celle du **plan** : un état qui porte la série, pas seulement
   la phrase*.

**Ce qui reste** : sur le périmètre, la **qualité** (le chrF est un **plancher**, pas une note absolue ; il n'est
même **pas comparable entre écritures**, 29ᵉ piège), le **technique miné**, les **langues peu
dotées** ; à l'étage 2, le **plan** — un état qui porte la série (113-115) ; son EN→FR monte à 0,364 **par l'entraînement de la tâche** (FR seul : 0,364 — le bilinguisme n'ajoute rien, mesure 155), pas par alignement ; un **contraste explicite** n'ajoute que +2 (0,386, mesure 156) le contraste **seul** la dégrade (0,318, mesure 166) et la **récurrence** (0,273, mesure 167) ni le **multi-tâches** (0,364, mesure 168) ne le sauvent — *la ligne plan est définitivement close : six variantes ont échoué*.

**Le bilan de la session (22-23 octobre)** : **quarante mesures** nouvelles (125-165) — les six registres mesurés
(juridique, presse, littéraire, parlé, technique, dialogue), la **carte du raisonnement**
([05](synthese/05-la-pensee-sans-verbaliser.md)) et les **sept leçons de méthode**
([06](synthese/06-comment-savoir.md)) ; l'étage 2 a sa structure : un état qui compose, un pont linéaire qui l'aligne,
et un plan qui résiste.

## Le tableau de bord des chantiers

**La roadmap** (les deux programmes, l'ordre du jour, la file « jamais en attente ») est dans
[`docs/roadmap.md`](roadmap.md). L'ordre actuel : **B2.6** (le plan multi-tâches), **A2.5** (le top-k GPU),
**A4.3** (le diff par couche), **A1.5/A5.3** (la décision par couche).

### Dépendances

```
C1 corpus/généalogie ──► C2 traduction ──► C5 qualité par domaine ──► C7 pensée abstraite
        │                     ▲                    ▲
        └──► C3 restitution ──┘                    │
        └──► C4 dialectes/styles ──────────────────┘
C6 documentation (transverse, ne bloque rien)
```

| chantier | dépend de | bloque | état |
|---|---|---|---|
| **C1** corpus et généalogie | — | C2, C3, C4 | **fait** |
| **C2** traduction (retrieval) | C1 | C5 | **mesuré** |
| **C3** restitution | C1 | — | **mesuré** |
| **C4** dialectes et styles | C1 | C5 (styles) | **mesuré**, époque à contrôler |
| **C5** qualité par domaine | C2, C4 | C7 | **ouvert** (juridique **propre** mesuré) |
| **C6** documentation et rangement | — | — | **fait** |
| **C7** pensée abstraite | C5 | — | **chantier principal** (périmètre entrée-sortie tenu) ; la dynamique est le verrou |

### Sous-chantiers : ce qui peut tourner en parallèle

| id | sous-chantier | indépendant ? | état | outil / fichier |
|---|---|---|---|---|
| **C5.1** | banc juridique **UDHR** | ✅ | **contaminé** (mesure 61 : le modèle récite l'UDHR) — banc de **mémoire**, plus juge | `tools/test_contamination.py`, `reports/contamination-*.json` |
| **C5.1b** | banc juridique **post-cutoff** (EUR-Lex 2025) | ✅ **parallèle** | **fait** (mesure 62), **répliqué** (67), **8 langues** (69) et **carte 24 langues** (71) | `tools/corpus_eurlex.py`, `tools/carte_langues.py`, `data/eurlex/`, `reports/traduction-*.json` |
| **C2.2** | **seuil de bruit** et correction de l'entrée | ✅ **parallèle** | **fait** (mesure 65 : détection AUC 1,00 ; correction 8/9 empirent) | `tools/seuil_bruit.py`, `reports/seuil-bruit-3b.json` |
| **C5.2** | banc **littéraire** (Verne) | ✅ **parallèle** | **fait** (mesure 64 : 47,7-49,8) ; **noms 96 %** (mesure 68 : le chrF bas est stylistique) | `tools/aligneur_litteraire.py`, `tools/analyse_litteraire.py` |
| **C5.3** | banc **modèle plus grand** (Qwen2.5 0,5 · 1,5 · 3 · 7 · 14 B) | ✅ **parallèle** | **fait** de 0,5 à 14 B (mesures 63 et 66) : le coude apparaît à 7 B en fra→eng (+0,9) | `tools/traduire_bench.py` |
| **C5.4** | corpus **technique** parallèle | ✅ **parallèle** | à construire | Gutenberg/`Panini` |
| **C5.5** | corpus **presse / actualité** parallèle | ✅ **parallèle** | **fait** (mesure 70 : marge +36 à +39) ; le **parlé préparé** est mesuré (TED2020, mesure 143) ; le **dialogue spontané** reste à construire | `tools/corpus_presse.py`, `data/presse/` |
| **C5.6** | **modules par langue / famille** (MoE de surface : adaptateurs, tête, routeur) | ✅ **parallèle** | **à mesurer** — il faut d'abord un **corpus d'entraînement par langue** (les 139 unités du banc sont pour l'évaluation) | `tools/adaptateur_langue.py`, banc 24 langues |
| **C2.1** | répliquer la généalogie **par domaine** | dépend de C5.2-C5.5 | à faire | `retrieval_udhr.py --genealogie` |
| **C4.1** | styles **à époque contrôlée** (couples contemporains) | ✅ **parallèle** | à faire | `style_traducteur.py` + dates |
| **C3.1** | restitution **par famille** (modules spécialisés) | ✅ **parallèle** | à faire | `restitution_udhr.py` |
| **C1.1** | familles **manquantes** (11 langues sans Glottolog) | ✅ **parallèle** | à faire | `genealogie_udhr.py` |

**Règle de parallélisation** : on lance **en même temps** tous les sous-chantiers marqués ✅ dont les entrées
existent déjà ; un sous-chantier qui dépend d'un autre attend son **chiffre**, pas sa documentation.

## Questions en attente (consolidées ici, jamais bloquantes)

| question | qui peut y répondre | état |
|---|---|---|
| la qualité de traduction vient-elle avec la taille ? | **moi** (mesure 62) | **oui, mais de moins en moins** : +1,7 à +6,3 du 3 au 7 B, et +0,9 à +3,8 du 7 au 14 B |
| le plancher « ne rien traduire » est-il battu sur **chaque** direction ? | **moi** (mesure 62) | **oui** : +30 à +40 points sur les 4 paires |
| l'UDHR est-elle utilisable comme juge ? | **moi** (mesure 61) | **non** : le modèle la récite — banc de mémoire |
| peut-on **corriger** automatiquement l'entrée abîmée ? | **moi** (mesure 65) | **non** : 8/9 des corrections empirent ; seule la restauration des accents gagne |
| quelle **unité de mesure** à l'entrée et à la sortie ? | **moi** (RSN en unités de sens ; jeton = technique) | en cours : la RSN est en unités de sens ; les métriques par jeton sont des diagnostics |
| quel domaine après le juridique ? | **moi** (mesures 64 et 70) | **presse mesurée** (au niveau du juridique) ; le **littéraire** reste 10 points en dessous ; le **parlé préparé** est mesuré (TED2020, mesure 143) ; le **dialogue spontané** reste à construire |
| la qualité dépend-elle de la **langue** ? | **moi** (mesures 69, 71) | la **couverture** du modèle : +35,8 (annoncées) contre +21,5 (non annoncées) ; trous irlandais/maltais |
| le **7 B** peut-il faire mieux que le 3 B pour le pidgin ? | **moi** (mesure 105) | **oui, un peu** : réparé par **autocast + GradScaler** (l'overflow fp16 était la cause) ; **+1,2** [−0,6 ; +3,1] contre +0,9 au 3 B, IC qui se recouvrent — la taille n'est pas le levier, le corpus reste la limite |
| peut-on **découper par langue** (MoE) pour alléger ? | **moi** (C5.6 ; synthèse 07) | **oui en surface**, non en noyau : adaptateurs/têtes par langue, routage par segment, 1,33 % de poids et 5 ms de bascule |
| le **critère démographique** de passage à l'étage 2 est-il atteint ? | **moi** (mesures 73-76, 107) | **oui, et le périmètre est arrêté au français inclus** : les langues jusqu'au **français** sont couvertes ; les **20** aussi (marge) — le pidgin est **lu** (+4,4 au 14 B) et **écrit** avec un adaptateur 14 B (**+5,8 [+4,1 ; +7,6]**, mesure 112) |
| le littéraire perd-il le **contenu** (noms, omissions) ? | **moi** (mesure 68) | **non** : 96,2 % des noms, 0,5 % d'omissions — l'écart est **stylistique** |
| le banc propre tient-il sur un **autre document** ? | **moi** (mesure 67) | **oui** : +1,1 à +2,5 points sur le règlement 2025/2509 (jouets) |
| faut-il des modules par **famille** pour la restitution ? | **moi** (C3.1) | à lancer |
| les styles à **époque contrôlée** : quels couples contemporains ? | **moi** (chercher dans Gutenberg) | à lancer |
| la vision de l'étage (ce qu'il **doit** être) | **Stéphane** | en attente, ne bloque rien |

## La priorité : l'intelligence, et son étage entrée-sortie

La vision de Drave a **deux programmes** (voir [`roadmap.md`](roadmap.md)) : le **moteur** (les flux) et
l'**intelligence** (les deux étages). **Dans l'intelligence, l'ordre est strict** : le premier étage est
l'**entrée-sortie** — lire et produire **toutes les langues, dialectes et styles**, dans tous les registres, et être
**jugé** sur sa **qualité de traducteur** (restitution à l'identique, et traduction du sens d'une langue à
l'autre). Entre le module pré-linguistique et le module post-linguistique circule une **représentation sémantique
neutre (RSN)** : une structure multi-niveaux, faite d'**unités de sens** — **jamais de jetons** (le jeton est
l'unité technique du tokeniseur, pas l'unité du sens). Le **module de pensée abstraite** (l'étage 2) attend que cet
étage soit fiable — et depuis le 21/10 au soir, **c'est lui le chantier principal** de l'intelligence, les registres
restants de l'étage 1 tournant en parallèle ; le **moteur**, lui, avance de son côté, par ses propres mesures.

**Le moteur, en ce moment** : le top-k GPU est **mesuré** (le noyau fusionné gagne jusqu'à ~64 k clés, la chaîne
séparée au-delà ; le seuil 131 072 est mesuré) ; la **porte du diff par couche** (A4.3) est en place (deux exécutions
identiques → flux identique ; le KV 8 bits → divergence nommée) ; la **quantification du KV par couche** (A5.3) :
l'int8 sur les couches 0-11 coûte **+2,28 %**, sur les 12-23 **+0,03 %** ; le **placement** (A2.6) a sa règle
générale (`choisir`, 4 tests) et le KV y passe ; **A6.1 et A6.3** ont rendu leurs négatifs (les produits n'ajoutent
que +0,0045 de R² ; aucun neurone ne reste à zéro).
Le **NLI français plus dur** (B2.8) est mesuré au 1,5 B : **DACCORD +26,9**, **GQNLI +56,7**, XNLI +35,9 de marge ;
à **profondeur relative fixe**, le **32 B est le meilleur** (0,600/0,772) et le 3 B le moins lisible (0,502) — la
lisibilité n'est pas la taille.

La **décision par couche** (A1.5) est mesurée : à 20-56 % de densité, le **dense** gagne de 2 % (9,2 contre 9,4 s)
et la perplexité est **identique** (28,4015) — la table prédit le dense pour 23 couches sur 24, la mesure suit.
Le **placement du KV** (A2.6) est mesuré à 8 k : en VRAM, le préremplissage passe de **297 à 154 s** (×1,93) et
l'attention de **32,3 à 5,6 ms/jeton** (×5,8) — le modèle de coût (les octets par jeton / la bande passante) est
écrit ; l'ordonnanceur qui l'applique reste à coder.

## Où en est cet étage (état au 21/10)

| ce qui est établi | le chiffre | la fiche |
|---|---|---|
| **la qualité de traducteur, sur texte non mémorisable** (règlements UE 2025) | **54,7 → 73,3** (eng→fra) et **63,1 → 76,6** (fra→eng) du 0,5 au 14 B · **répliqué** sur un 2ᵉ règlement (+1,1 à +2,5) | [07](../reports/07-mesures-couche-commune.md) |
| **le littéraire** (Verne, alignement validé) | **47,7-49,8** (3 B/7 B) · **noms 96 %**, 0,5 % d'omissions : le chrF bas est un écart de **style** (mesure 68) | [07](../reports/07-mesures-couche-commune.md) · [alignement](../reports/alignement-verne.md) |
| **la qualité par langue** (8 langues, mêmes 80 sources) | **45-71** de chrF brut mais **marge 33-40** sur le plancher ; le 7 B **comble le polonais** (+10,1) — l'écart brut est surtout la **distance** (mesure 69) | [07](../reports/07-mesures-couche-commune.md) |
| **la carte des registres** (marge sur le plancher, 7 B) | **juridique +35,3** · **presse +38,6** · **littéraire +25,9** · **parlé préparé +39,8 / +40,7** · **technique JRC +36,4 / +34,9** · **prose MultiUN +33,2 / +32,9** (miné +41 / +46, gonflé) · **dialogue +32,3 / +33,6** : le parlé préparé passe au-dessus de la presse ; le technique humain, le dialogue et le littéraire restent en dessous (mesures 62, 68, 70, 143, 148, 159) | [07](../reports/07-mesures-couche-commune.md) |
| **la carte des 24 langues** (marge sur le hasard) | **13 annoncées +35,8** · **10 non annoncées +21,5** (écart +14,2) · trous : **irlandais +8,0**, **maltais +10,8** · **la taille ne comble pas l'écart** : 15,6 (3 B) → 14,2 (7 B), −1,4 (mesures 71-72) | [07](../reports/07-mesures-couche-commune.md) |
| **le périmètre démographique** (Ethnologue 2026) | **arrêté au français inclus** : les langues jusqu'au **français** sont couvertes ✓ ; les **20** aussi, comme **marge** ✓ : les 19 sur des textes neufs (mesures 73-76) ; le **pidgin nigérian** est **lu** (+3,2 au 7 B, +4,4 au 14 B) et **écrit** avec un **adaptateur 14 B** : **+5,8 [+4,1 ; +7,6]** sur 71 pages de contes tenus à part, **7 plis positifs** (1000 pas, mesure 112) | [07](../reports/07-mesures-couche-commune.md) |
| **étage 2 — la représentation neutre** (3 B/7 B, JW 2026) | **partagée mais non alignée** : un pont linéaire retrouve la bonne traduction dans **28-69 %** (hasard 0,7 %), cosinus 0,78-0,92 ; **la taille ne change presque rien** (+3,7 en lecture, +1,4 en écriture) ; **lire ≈ écrire** ; le sens partagé vit dans les **premières couches** (4-6) — mesures 77-78 | [07](../reports/07-mesures-couche-commune.md) |
| **étage 2 — la composition** (3 B/7 B/14 B, Verne) | **démontrée sur phrases alignées** : retrieval **0,61** (3 B) → **0,76** (7 B) → **0,68** (14 B, réparti, OOM) ; ordre **0,84 → 0,865 → 0,855** ; **la courbe plafonne entre 7 et 14 B**, et le sens vit à **mi-profondeur** (50 %, 33 % au 14 B) — mesures 80-81, 87 | [07](../reports/07-mesures-couche-commune.md) |
| **étage 2 — le pas de pensée** (3 B/7 B/14 B, Verne) | **ni la phrase ni le contexte figé ne portent la suite** (erratum 6 + mesures 113-116) : l'opérateur linéaire prédit la **moyenne** (effondrement 0,89-0,99, retrieval 0-8,9 % contre 2,2 %) ; le **contrastif** reste au hasard ; sur **630 séries / 1 323 transitions**, linéaire et MLP restent au hasard (0-1,15 %) ; le **contexte** (8 phrases, GRU) reste à **0,14** de contenu contre 0,125 ; un **code de plan** de 32 dimensions ne dépasse la moyenne que de **+0,02** (mesure 117) ; la **langue** est décodable à 1,00, la **position** à 0,13 (mesure 118) ; l'**état latent** entraîné avec la tâche **collapse** (pas 1 à 0,00) ; le plan **s'entraîne** — 0,239 → **0,443**, contrôle 0,227 (mesure 119) — et porte **trois pas** (0,443 / 0,295 / 0,341, mesure 120) ; le transfert **réel** (cibles figées) est faible (+0,05 à +0,08, mesures 121 et 123) et **nul à 16 phrases** (mesure 122) ; entraîné **contre des cibles figées**, le plan transfère (0,324 / 0,273 / 0,216, mesure 124 ; h1 solide) | [07](../reports/07-mesures-couche-commune.md) |
| **étage 2 — le raisonnement transitif** (3 B, corpus contrôlé FR/EN) | **dans l'état** : 1,00 / 0,92 / 0,84 / 0,78 / 0,51 (FR) et 1,00 / 0,98 / 0,85 / 0,52 / 0,53 (EN) de 2 à 6 entités contre 5 % ; contrôles au hasard ; un **pont linéaire** rend le raisonnement indépendant de la langue (1,00 / 0,91 / 0,68 / 0,52 / 0,46, mesure 126), **structurel** (mesure 127), **langue-général** (FR/ES, FR/DE, arabe ; mesures 128, 131, 133), **linéaire** (mesure 129) et **multi-couches** (mesure 130) ; mais il **n'aligne pas l'état de plan** (mesures 132, 134) — les géométries sont **locales aux tâches** ; un **seul pont poolé** couvre les longueurs (0,94 / 0,91 / 0,81, mesure 135) ; il marche au **7 B** (0,95 / 0,87 / 0,81, mesure 137) le **multi-tâches** ne récupère pas le plan (0,136, mesure 136) ; un **code partagé** non supervisé ne suffit pas (0,34-1,00 à 256 dims, mesure 138) ; la **CCA** aligne mais 64 dims perdent l'information (mesure 139) ; à **256 dims** elle récupère (0,57-1,00, mesure 140) ; au **14 B**, pont quasi parfait (0,975-1,00, mesure 141) ; **entraîner en FR** ne l'aligne pas (mesure 142), ni le **multilingue** (mesure 144) ni le **contrastif faible** (mesure 146) ; un **contraste fort** l'apprend (sonde EN 0,742, mesure 147) | [07](../reports/07-mesures-couche-commune.md) |
| **le bruit d'entrée est signalable** (seuil 3,23 bits/token) | fautes et langues mêlées : **100 %** détectées, AUC **1,00** · accents : **25 %**, AUC 0,69 | [07](../reports/07-mesures-couche-commune.md) |
| **le banc UDHR est contaminé** — le modèle récite, il ne traduit pas | article 1 reproduit **mot pour mot** (7 B) | [07](../reports/07-mesures-couche-commune.md) |
| **la langue est lisible partout** dans l'état d'un modèle (pas de noyau neutre spontané) | 80-100 % dès la couche 1 (5 modèles d'octets, Qwen) | [07](../reports/07-mesures-couche-commune.md) |
| **le sens traverse les langues** — sur les paires bien couvertes | **96,4 %** (12 paires, dont fra↔cmn) · hasard 3,3 % | [07](../reports/07-mesures-couche-commune.md) |
| — mais sur un échantillon stratifié de 100 langues | **16,3 %** · 3,5× le hasard dans un vivier ouvert | [07](../reports/07-mesures-couche-commune.md) |
| **restitution exacte** : parfaite pour un modèle spécialisé, détruite par le partage | **85,1 %** (1 langue) → **0,6 %** (448 langues) | [07](../reports/07-mesures-couche-commune.md) |
| **généalogie** : l'alignement suit les familles (Glottolog, 55 familles) | **30,7 %** même branche · **22,0 %** même famille · **15,2 %** entre familles (hasard 3,3 %) | [07](../reports/07-mesures-couche-commune.md) |
| **dialectes** : lisibles, contenu retrouvé selon la couverture | 100 % lus · 30-100 % retrouvés | [07](../reports/07-mesures-couche-commune.md) |
| **styles** (traducteurs) : lisibles, contenu moins résistant | 87-100 % lus · 6-24 % retrouvés | [07](../reports/07-mesures-couche-commune.md) |
| **la langue est un petit paramètre de sortie** | 1,33 % des poids · 5 ms de bascule | [07](../reports/07-mesures-couche-commune.md) |

**Le corpus** : la Déclaration universelle des droits de l'homme, **448 langues**, 13 222 articles alignés, 43
écritures, 37 langues à variantes (`data/udhr/`, importeurs `tools/importer_udhr.py` et `tools/preparer_udhr.py`).

## Ce qui reste à faire, dans l'ordre

1. **qualité de traduction par domaine** : le **juridique** a un banc **propre** (mesure 62) et le **littéraire**
   est **mesuré** (mesure 64 : 47,7-49,8, le plus dur) ; il reste le **technique** et le **quotidien parlé** (la presse est faite), et les **langues peu dotées** — chaque
domaine avec un corpus **post-cutoff**, sinon on mesure la mémoire (mesure 61) ;
2. **l'unité de mesure de l'entrée et de la sortie** : passer des métriques par **jeton** (techniques, dépendantes
   du tokeniseur) aux **unités grammaticales multi-niveaux** (morphème, mot, syntagme, proposition, énoncé), à
   mesure que les modules s'approchent de **grammaires formelles** représentant les entrées et sorties en
   **compréhension totale** ; les métriques par jeton restent des **diagnostics d'instrument** ;
3. **restitution exacte à l'échelle** : au-delà de 10 langues partagées, elle meurt ; modules par famille, ou modèle
   beaucoup plus grand ?
4. **le style** : lisible, mais le sens ne le traverse qu'à 24 % ;
5. **seulement ensuite** : le module de pensée abstraite, indépendant de la langue.

## La carte de la documentation

- [AGENTS.md](../AGENTS.md) — la mission et les règles (à lire avant d'agir) ;
- [docs/README.md](README.md) — la porte d'entrée, la carte de la documentation ;
- [docs/synthese/index.md](synthese/index.md) — la synthèse théorique (7 chapitres, 7 schémas) ;
- [docs/utilisation.md](utilisation.md) — utiliser le dépôt ;
- [`reports/`](../reports/) — les résultats mesurés ; [`journal/`](../journal/) — le récit daté.
