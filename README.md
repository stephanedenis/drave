# Drave

**Une intelligence en deux étages** : une **entrée-sortie linguistique** qui lit et écrit toutes les langues, dans
tous les registres, et une **pensée abstraite** qui raisonne sans verbaliser. Le projet ne cherche pas la plus grosse
tête, mais la **tête bien faite** — la structure qui rend un modèle ouvert utile partout, et une méthode qui ne croit
pas ses propres chiffres.

> **L'état courant, daté, est dans [`docs/en-cours.md`](docs/en-cours.md).** Ce README dit la **vision** et les
> **axes** ; il ne remplace pas l'état.

---

## La vision

### 1. Deux étages, dans cet ordre

1. **L'entrée-sortie linguistique** — lire et produire **toutes** les langues, dialectes et styles, dans les
   registres techniques, littéraires, juridiques, quotidiens. On la juge en **qualité de traducteur** : restitution
   à l'identique, et traduction du sens. On ne « déclare complet » que sur des **chiffres** qui couvrent langues,
   registres et domaines.
2. **La pensée abstraite, indépendante de la langue** — seulement après. Elle ne peut pas être bâtie sur une
   entrée-sortie qui n'est pas fiable. On la juge sur des **opérations** : représenter, composer, inférer, planifier.

*Le temps est un plancher, pas un plafond : on s'arrête quand l'étage est fait, mesuré et écrit.*

### 2. La tête bien faite, pas la grosse tête

Les mesures de ce dépôt montrent que **la taille ne suffit pas** : le gain par doublement tombe (+0,9 de 7 à 14 B,
mesure 66), elle ne comble pas les écarts de couverture (mesure 72), et pour le raisonnement naturel elle ne change
presque rien (mesure 161). Ce qui marche est **structurel** : un **pont linéaire** entre les langues (mesures
126-141), un **entraînement bilingue** qui aligne les états (147-152), une **carte** de ce qui est vrai et de ce qui
ne l'est pas. *La petite structure, calculée une fois, bat la capacité ajoutée.*

### 3. Une méthode falsifiable

Le danger n'est pas de se tromper : c'est de **croire** un chiffre qui ne mesure rien. Chaque résultat porte son
**contrôle négatif**, son **plancher**, son **intervalle**, et **ce qui pourrait le rendre faux** — écrit à côté du
chiffre, avant de conclure. Les erreurs trouvées restent écrites (six erratums) ; les mesures retirées aussi.
La méthode et ses pièges : [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md).

---

## Les axes de recherche

### Axe 1 — L'entrée-sortie linguistique (étage 1)

**1.1 Le juge.** Un banc de traduction ne vaut que s'il n'est pas dans les données d'entraînement. L'UDHR était
**contaminée** (le 7 B **récite** l'article 1, mesure 61) ; le juge est désormais un **texte neuf** — un règlement
européen de 2025, 139 unités alignées, traductions humaines — complété par des corpus post-cutoff (ONU, presse) et
par un **contrôle de mémoire**.

**1.2 Les registres.** Six registres mesurés, chacun avec sa **référence** et son **plancher** (la marge = traduction
− source) :

| registre | référence | marge |
|---|---|---:|
| juridique | EUR-Lex (humain) | +35,3 |
| presse | presse (humain) | +38,6 |
| littéraire | Verne (traductions) | +25,9 |
| parlé préparé | TED2020 (humain) | +39,8 / +40,7 |
| technique — juridico | JRC-Acquis (humain) | +36,4 / +34,9 |
| technique — prose | MultiUN (humain) | +33,2 / +32,9 |
| dialogue | OpenSubtitles (humain) | +32,3 / +33,6 |

*Leçon payée : une référence **minée** (WikiMatrix, +41/+46) **gonfle** la marge ; elle doit être une traduction, pas
un parallèle miné (mesures 145 et 159).*

**1.3 Les langues et la couverture.** Sur les 24 langues officielles de l'UE, la marge est de **+35,8** pour les
langues annoncées par le modèle et **+21,5** pour les autres ; les trous sont l'**irlandais (+8,0)** et le
**maltais (+10,8)** (mesure 71). Le critère démographique est **tenu** : les langues jusqu'au **français inclus**
sont couvertes, et les **20** le sont aussi (mesures 73-76 et 107) — les 19 sur texte neuf, le **pidgin nigérian**
lu (+4,4 au 14 B) et écrit avec un adaptateur (**+5,8 [+4,1 ; +7,6]** sur 71 pages, mesure 112). L'alignement des
langues **suit la généalogie** (37/28/11 %). *Le chrF n'est pas comparable entre écritures (29ᵉ piège).*

**1.4 La fidélité et le style.** Le littéraire est le plus dur, mais **pas par le contenu** : **96 %** des noms,
**0,5 %** d'omissions ; l'écart est de **style** (mesure 68). L'entrée sait **signaler** son bruit (AUC 1,00) mais
**pas le corriger** : 8/9 des corrections empirent (mesure 65). Le miroir entrée/sortie est une règle : toute mesure
d'entrée se double d'une mesure de sortie.

### Axe 2 — La représentation neutre (la RSN)

**2.1 Une représentation partagée, mais non alignée.** Un pont linéaire retrouve la bonne traduction dans
**28-69 %** (mesure 77) ; la similarité entre les langues va de 0,78 à 0,92 ; et **la taille n'y change presque
rien** (+3,7, mesure 78). *La RSN existe ; elle n'est pas donnée.*

**2.2 La composition.** Le sens d'une phrase est partagé et positionné : composition **0,61 / 0,84** (mesure 80),
qui **profite de la taille** — **0,76 / 0,865** au 7 B (mesure 81), plafond à 14 B (mesure 87).

**2.3 Le code partagé.** Une ACP commune (non supervisée) ne suffit pas : 0,14-0,98 à 64 dims, 0,34-1,00 à 256
(mesure 138). La **CCA** aligne réellement mais un code de 64 dims perd l'information (139) ; à **256 dims**, elle
récupère 0,57-1,00 (140) — sans battre le pont poolé (0,81 à 6 entités).

### Axe 3 — Le raisonnement

**3.1 Le raisonnement synthétique est dans l'état.** Sur des chaînes d'ordre contrôlées (prémisses mélangées), une
sonde linéaire retrouve la conclusion à **1,00 → 0,51** (FR) et **1,00 → 0,53** (EN), contre 5 % de hasard
(mesure 125).

**3.2 Un pont linéaire l'aligne.** EN→FR : **1,00 / 0,91 / 0,68 / 0,52 / 0,46** (2-6 entités), contre 0,04-0,08 sans
pont (mesure 126). Il est **structurel** (relation « taille », 127), **langue-général** (FR/ES, FR/DE et **arabe** ;
128, 131, 133), **linéaire** (un MLP échoue, 129), **multi-couches** (12/18/24, 130), **poolé** (0,94 / 0,91 /
0,81 ; 135), et il tient au **7 B** (0,95 / 0,87 / 0,81 ; 137) et au **14 B** (0,975-1,00 ; 141).

**3.3 La profondeur et l'échelle.** Le raisonnement tient jusqu'à **12 entités** : 0,95 → 0,47 au 3 B, 0,97 → **0,70**
au 14 B (157-158). *Pas de mur : une pente, que la taille aplatit.*

**3.4 Le raisonnement naturel.** Sur **XNLI** (2 490 paires FR/EN traduites), l'inférence est dans l'état (FR 0,502,
EN 0,576 contre 33,3 % ; 160) ; le pont la transfère à **0,592** (160), et le **fine-tuning** pousse le pont à
**0,75-0,77** (163-164). *Le domaine compte plus que le volume : 13 394 paires hors domaine ne changent pas la sonde
(164).*

**3.5 L'alignement s'apprend — et sature.** L'entraînement **bilingue** fait passer la sonde FR→EN de 0,058 à
**0,656** (150) ; le **contraste correct** ajoute +9 (**0,742** ; 147), le **mélangé** coûte −15 (149). La courbe
montre un seuil entre **400 et 800 pas** (151), et une **saturation** à 0,753 / 0,826 in-langue (152). *Le prix de
l'alignement est l'in-langue : 0,987 → 0,776.*

### Axe 4 — Le plan et la dynamique

**4.1 L'état de plan.** Un état qui résume la série lue : la **suite** est dans l'état de plan, mais **la dynamique
n'est pas un pas isolé**. Le meilleur état est le **contexte joint** des 4 phrases (la dernière phrase), pas une
moyenne, ni un code de 32 dims, ni une récurrence (mesures 113-117, 167).

**4.2 Le plan ne s'aligne pas.** Les ponts (132, 134), l'adaptateur du raisonnement (153), le **bilinguisme** (155),
le **contraste** (156, 166) et la **récurrence de bout en bout** (167) échouent : son transfert apparent (0,364) est
un **effet côté cible** (155), et sa géométrie est **ancrée dans la langue**. *La ligne plan est close : contexte
joint + tâche.*

### Axe 5 — La méthode et l'instrument

**5.1 Les sept leçons** (payées par une erreur trouvée à temps) : le juge **post-cutoff**, le **plancher**
obligatoire, la **référence minée** qui gonfle, le **domaine avant le volume**, les **contrôles négatifs**, les
**petits tests** qui mentent (≥ 200-300 items), la **carte des lignes** assertie à la source. Détail :
[`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md).

**5.2 L'instrument.** 223 outils, 167 mesures et leurs JSON de résultats, une **validation croisée par conte**
(k-fold), une **reproductibilité** par graine, et des **portes** qui vérifient l'invariant (liens, tableaux, dates,
cohérence, vocabulaire) : `tools/revue_documentation.py`, `tools/porte-tableaux.sh`,
`tools/toutes-les-portes.sh`.

### Axe 6 — Le moteur et l'ingénierie

**Le moteur d'inférence** (`drave-core/`) exécute les grands modèles comme des **événements**, pas comme des
matrices : les GGUF sont lus en place (mmap), les projections se font en listes creuses ou en produit dense, et le
calcul se découpe en régions réparties sur plusieurs processus ou machines. **Rust, `std` seul, zéro dépendance.**
Ce qui tourne : du 0,5 B au 120 B sur le CPU de cette machine, MoE compris ; ce que ça vaut, tâche par tâche :
[`reports/campagne-benefices.md`](reports/campagne-benefices.md). Les documents du moteur :
[`REPRISE.md`](REPRISE.md) (la check-list), [`docs/etat.md`](docs/etat.md) (l'index des modules),
[`docs/etat-cerveau.md`](docs/etat-cerveau.md) (les douze capacités).

---

## L'état en chiffres (22-23 octobre 2026)

| question | réponse | mesures |
|---|---|---|
| la qualité de traducteur | 55-76 de chrF, **+30 à +40** au-dessus du plancher, répliquée | 62-67 |
| les registres | six mesurés, du littéraire (+25,9) au parlé (+40,7) | 64-70, 143-165 |
| la couverture | les 20 langues couvertes, critère arrêté au **français inclus** | 73-76, 107-112 |
| la représentation | partagée mais non alignée (pont 28-69 %), insensible à la taille | 77-78 |
| la composition | **0,61 / 0,84 → 0,76 / 0,865** (7 B) | 80-81, 87 |
| le raisonnement synthétique | dans l'état (1,00 → 0,51), pont linéaire 0,46-1,00 | 125-141, 157-158 |
| le raisonnement naturel | XNLI 0,50-0,59, pont 0,59 → **0,77** (fine-tuning) | 160-164 |
| l'alignement | appris par le bilingue (0,656 → 0,753), sature | 142-152 |
| le plan | contexte joint, **résiste** à l'alignement | 113-124, 132-167 |

*La carte complète du raisonnement est dans
[`docs/synthese/05-la-pensee-sans-verbaliser.md`](docs/synthese/05-la-pensee-sans-verbaliser.md) ; la fiche de
résultats, mesure par mesure, dans [`reports/07-mesures-couche-commune.md`](reports/07-mesures-couche-commune.md).*

---

## Ce qui reste ouvert

- **Le plan multi-tâches** : la seule variante non testée (entraîner le plan et le raisonnement ensemble).
- **La prose scientifique** (articles) : le corpus parallèle humain manque ; le MultiUN reste la référence technique.
- **Le 32 B** et la profondeur au-delà de 12 entités.
- **Le dialogue spontané** : les sous-titres sont du parlé écrit et contraint, pas de la conversation réelle.
- **Les langues peu dotées** hors périmètre, et les 19 (marges).

---

## Où est quoi

| besoin | document |
|---|---|
| **l'état courant**, daté | [`docs/en-cours.md`](docs/en-cours.md) |
| la **théorie** (7 chapitres) | [`docs/synthese/index.md`](docs/synthese/index.md) |
| la **carte du raisonnement** | [`docs/synthese/05-la-pensee-sans-verbaliser.md`](docs/synthese/05-la-pensee-sans-verbaliser.md) |
| la **méthode** et ses pièges | [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md) |
| les **résultats**, une fiche par mesure | [`reports/`](reports/) · [`reports/07-mesures-couche-commune.md`](reports/07-mesures-couche-commune.md) |
| le **récit** daté | [`journal/`](journal/) |
| les **corpus** | [`data/`](data/) (non versionné) |
| les **instruments** | [`tools/`](tools/) |
| le **moteur** | [`drave-core/`](drave-core/) |
| les **règles de travail** | [`AGENTS.md`](AGENTS.md) · [`docs/agent/`](docs/agent/) |

## Démarrer une session de travail

**Lire, dans cet ordre** (10 minutes) :

1. [`AGENTS.md`](AGENTS.md) — la mission, les règles non négociables, le routage vers le document de chaque tâche ;
2. [`docs/en-cours.md`](docs/en-cours.md) — l'**état courant** : la synthèse, les chantiers, les questions ;
3. [`journal/`](journal/README.md) — les **faits datés** (celui du jour d'abord) ;
4. [`docs/synthese/index.md`](docs/synthese/index.md) — la **théorie** en sept chapitres.

**Vocabulaire** : *couche* = couche de neurones ; *étage* = niveau d'architecture (étage 1 entrée-sortie, étage 2
pensée) ; *unité de sens* = élément de la RSN (jamais « jeton »). Le glossaire :
[`docs/glossaire.md`](docs/glossaire.md).

**Vérifier l'arbre** :

```bash
python3 tools/revue_documentation.py   # classement, structure, fraîcheur, cohérence, vocabulaire
bash tools/porte-tableaux.sh           # liens, tableaux, date de la page vivante
bash tools/toutes-les-portes.sh        # toutes les portes (~1 h, registre dans $JOURNAUX/registre.txt)
cd drave-core && cargo test --release  # le moteur (122 tests)
```

---

## La règle du dépôt

**Le défaut le plus coûteux n'est pas un calcul faux : c'est un réglage qui ne fait rien, une mesure qui ne mesure
rien, une porte qui ne peut pas échouer.** Chaque capacité est livrée avec sa **porte**, ses **tests**, sa **mesure**
et sa **documentation** — et une erreur corrigée reste écrite à côté de la valeur d'origine.

*Un résultat qui n'a pas de contrôle négatif n'est pas un résultat.*
