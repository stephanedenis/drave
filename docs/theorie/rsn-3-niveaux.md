# La RSN à trois niveaux — le noyau, les faits, les affirmations

> **Ce que ce document est.** La **structure de la RSN** que la base doit adopter, alignée sur
> l'architecture de **Nipada** (le projet parent : [`../Panini/research/philosophy-theory/`](../../../Panini/research/philosophy-theory/DOCUMENT_DE_CONTEXTE_v3.0.md))
> — un **noyau formel** qui ne décrit jamais, une **couche descriptive** qui porte le contingent, et
> des **instantiations candidates** qui gardent leur contexte source. Le code :
> [`tools/rsn.py`](../../tools/rsn.py) ; la mesure : [`rapport-rsn.md`](../../reports/rapport-rsn.md).

## Le principe de séparation (la phrase de référence de Nipada)

> *Le noyau ne décrit jamais — il infère. NIPADA décrit ce que le noyau ne peut inférer. Les deux ne
> se mélangent pas : ce qui est démontré entre dans le noyau avec sa preuve ; ce qui ne l'est pas
> reste une hypothèse de la couche descriptive, avec son degré et son statut.*

C'est exactement la distinction que la RSN doit porter : **un fait démontré** n'est pas **une
affirmation candidate**. Le premier est **vrai dans le système** ; la seconde est **plausible dans le
monde**, avec sa source.

## Les trois niveaux

### Niveau 1 — Le noyau : le calcul et les certitudes

**Ce qu'il est.** Un **système formel** : un langage de termes (les arbres), l'**unification** et la
**résolution** (l'inférence), une **logique tri-état** — **prouvé**, **réfuté**, **inconnu** — et une
**bibliothèque de certitudes** (les énoncés clos, démontrés, avec leur trace de preuve).

**Ce qu'il porte dans la RSN** : les **relations démontrées** entre candidats — une égalité, un
ordre, une composition, une arithmétique. **Jamais un degré** : le noyau ne stocke pas de [0,1].

**Ce qu'il permet** : les **inférences fortes** — celles qui sont **vraies ou fausses**, pas
« probables ». Si la RSN dit `agent(chat, dort)` et `patient(toit, dort)`, le noyau peut **dériver**
que le chat et le toit ne sont pas le même objet (l'égalité est réflexive, symétrique, transitive) —
**sans** consulter la surface.

**L'incomplétude, assumée** : un système cohérent capable d'arithmétique ne contient pas toutes ses
vérités (Gödel). D'où le niveau 2 : ce que le noyau ne peut pas inférer doit être **décrit**.

### Niveau 2 — Les faits : la couche descriptive et le flou

**Ce qu'elle est.** La **description de la réalité observable** : les hypothèses avec un **degré**
([0,1], Zadeh), un **statut** (`open`, promu, réfuté), et la **contingence du monde** — ce que le
noyau ne peut pas inférer.

**Ce qu'elle porte dans la RSN** : les **faits falsifiables** — chaque candidat est un **énoncé
descriptif** avec son degré de confiance, sa provenance, et **ce qui le réfuterait**. Un fait n'est
pas vrai : il est **soutenu**, avec un degré, et **révisable**.

**La règle du flou (un seul système).** Les trois usages du flou de Nipada forment **un seul système
de qualification** : le degré [0,1] (le jugement), l'échelle Ł3 (le statut du moteur), le poids
relationnel (le graphe). **Aucun ne génère ni ne prouve** — c'est le noyau qui prouve.

**Ce qu'elle permet** : les **inférences floues** — les règles de composition (« si l'agent est
animé et le prédicat est un déplacement, alors l'agent se déplace ») qui produisent des **degrés**
nouveaux, sans jamais prétendre à la certitude.

### Niveau 3 — Les affirmations : les candidats et leur contexte source

**Ce qu'elles sont.** Les **instantiations candidates** — les artefacts d'implémentation révisables :
un syntagme étiqueté, une prédication extraite, une lecture possible. Leur point commun : **elles
gardent précieusement leur contexte source** (le texte, le span, la position, la langue, la version
de l'analyseur).

**Ce qu'elles portent dans la RSN** : les **affirmations candidates** — chaque candidat avec son
`contexte` (le texte source, le span, la provenance, la version), son **statut** (`hypothese`,
`retenu`, `refute`, `ouvert`) et son **score**.

**Pourquoi le contexte est précieux** :
- **la falsifiabilité** : sans le span, on ne peut pas revenir au texte pour vérifier ;
- **la traçabilité** : une affirmation sans source est une croyance, pas une donnée ;
- **l'extensibilité** : le contexte permet de **rejouer** l'analyse avec une autre version de
  l'analyseur et de **comparer** les affirmations.

## Pourquoi c'est la « meilleure » RSN

| propriété | ce que le niveau garantit |
|---|---|
| **un noyau mathématique robuste** | les inférences fortes sont **démontrées**, pas corrélées ; le noyau est une **spécification**, pas un programme (portable, auditable) |
| **des faits falsifiables** | chaque fait porte **ce qui le réfuterait** et son **degré** ; rien n'est « vrai par défaut » |
| **des affirmations candidates** | chaque affirmation garde **son contexte source** ; le statut est explicite ; le rejeu est possible |
| **l'extensibilité des concepts** | un concept nouveau est une **affirmation candidate** (niveau 3) — il n'entre dans le noyau que **démontré**, et dans les faits que **degré**. On peut ajouter un concept sans casser la base : c'est une **couche**, pas un schéma figé |

## La règle de promotion (le pont de Nipada)

- **Question au noyau** : la réponse est **tri-état**. *Inconnu* → l'énoncé est une **hypothèse** du niveau 2.
- **Promotion** (le seul chemin d'entrée dans le noyau) : une affirmation **dérivée** devient une **certitude**, avec sa trace de preuve. **Sans dérivation, elle reste une hypothèse.**
- **Réfutation** : seulement si la négation est **exprimée** ou **décidable** — jamais « faux par défaut ».
- **Versionnement couplé** : la RSN n'est testable qu'avec **sa** couche descriptive (le texte, les spans, la version de l'analyseur).

## L'état dans le code

| niveau | dans `tools/rsn.py` | état |
|---|---|---|
| **1 — le noyau** | `Noyau` : l'égalité, l'ordre, la composition, le tri-état | **à construire** (le module a le candidat et l'état, pas encore le noyau) |
| **2 — les faits** | `Candidate` : le `score`, la `provenance`, le `statut` | **partiel** (le degré existe, la falsifiabilité est à expliciter) |
| **3 — les affirmations** | `Candidate.corps` : la forme, le span, la langue | **partiel** (le contexte source est à structurer) |

**Ce qui manque, dans l'ordre** : le `Noyau` (les axiomes et les règles), le `contexte` structuré
(le texte, le span, la version), et les **règles de composition floues** (le niveau 2 → le niveau 1).

## L'interface (la substitution)

Les cinq verbes qui rendent un paradigme **substituable** — `assert`, `query`, `promote`, `explain`,
`context` — et les six adaptateurs (formel, flou, probabiliste, provenance, TMS, Dung) :
[`rsn-interface.md`](rsn-interface.md).

## Les limites

- **Nipada n'est pas Drave** : sa vision est un **système formel complet** ; la RSN en reprend la
  **structure**, pas l'ambition. Le noyau de Drave sera **minimal** (l'égalité, l'ordre, les spans).
- **Le flou n'est pas une preuve** : les degrés [0,1] sont des **jugements**, pas des vérités ; la
  confusion entre les deux est l'erreur que Nipada signale explicitement.
- **La promotion est un chantier** : elle exige un **vérificateur** de dérivations — c'est le
  « kernel » de Nipada, et il n'existe pas encore côté Drave.
