# Drave

**Ce dépôt est le carnet de mesures d'un projet de recherche : construire une intelligence qui traduit correctement
toutes les langues, puis raisonne sans passer par les mots.** On y trouve les résultats — les réussites, les échecs,
et les contrôles qui permettent de distinguer les deux.

Si vous arrivez ici sans connaître le projet, lisez les quatre premières sections (le problème, l'idée, ce qu'on a
trouvé, comment on le sait). Le reste est un guide du dépôt.

> **L'état courant, daté, est dans [`docs/en-cours.md`](docs/en-cours.md).** Ce README explique le projet et ce
> qu'il a mesuré ; il ne remplace pas l'état.

---

## Le problème

Les grands modèles de langue traduisent étonnamment bien. Mais ils le font comme de **grosses têtes** : ils
empilent des capacités, et leurs représentations internes ne sont **pas partagées** entre les langues. Prenez une
phrase et sa traduction : dans les états internes du modèle — les vecteurs qu'il calcule à chaque couche — le
français et l'anglais de la même phrase sont deux points **sans rapport géométrique**. Le modèle sait traduire,
mais il ne « pense » pas dans un espace commun.

Cela pose deux questions concrètes :

1. **Peut-on mesurer la qualité d'un traducteur** sur toutes les langues et tous les registres, sans se raconter
   d'histoires (sans benchmark contaminé, sans score qui ne mesure rien) ?
2. **Peut-on obtenir une pensée indépendante de la langue** — un état qui porte le sens et le raisonnement, que
   l'on sache lire en français comme en anglais — **sans** construire un modèle plus gros ?

Le projet répond par des expériences contrôlées, sur des modèles ouverts (Qwen2.5, 0,5 à 14 milliards de
paramètres). La thèse, en une phrase : **la structure bat la taille** — une petite carte d'alignement, calculée une
fois, rend un modèle ouvert utilisable dans toutes les langues.

---

## L'idée : deux étages, dans cet ordre

**Étage 1 — l'entrée-sortie linguistique.** Lire et produire toutes les langues, dans tous les registres
(juridique, presse, littéraire, parlé, technique, dialogue). On le juge comme un **traducteur** : la traduction
est-elle fidèle, et le sens passe-t-il ? On ne déclare rien « complet » sans chiffres qui couvrent langues,
registres et domaines.

**Étage 2 — la pensée abstraite.** Une fois l'entrée-sortie fiable, on regarde **l'intérieur** du modèle : son
**état** (le vecteur qu'il calcule après avoir lu un texte). Cet état porte-t-il le sens, la composition, le
raisonnement ? Et le même état le porte-t-il dans toutes les langues ? On le juge sur des **opérations** —
représenter, composer, inférer, planifier — pas sur la fluidité du texte produit. C'est le sens de « penser sans
verbaliser » : la réponse est dans l'état, avant et sans la génération.

*Ce que cela veut dire concrètement : on ne demande pas au modèle d'écrire sa réponse ; on lit directement dans son
état, avec une sonde — un classifieur linéaire aussi simple que possible.* Si une sonde linéaire retrouve la
réponse, l'information y est, et elle est accessible.

---

## Ce qu'on a trouvé

### 1. Traduire : correct, jamais parfait

Sur un texte **neuf** (un règlement européen de 2025, jamais vu à l'entraînement), la qualité se situe entre
**55 et 76 sur 100** (chrF, une mesure de similarité de caractères), selon la taille du modèle. Le chiffre qui
compte n'est pas le score brut, mais la **marge** : la traduction fait **+30 à +40 points** de mieux que « recopier
la source » (le plancher). Autrement dit : le modèle traduit vraiment, mais il reste loin de 100.

Les registres ne se valent pas : le **littéraire** est le plus dur (+25,9 de marge), suivi du **dialogue** (+32,3)
et de la **prose technique** (+33) ; la **presse** (+38,6) et le **parlé préparé** (+39,8) sont les plus faciles.
La taille aide, mais de moins en moins : +0,9 seulement entre 7 et 14 milliards.

Les langues : sur les 24 langues officielles de l'UE, les langues que le modèle annonce font **+35,8** de marge,
les autres **+21,5** — les trous sont l'irlandais et le maltais. Le critère démographique est tenu jusqu'au
**français inclus** (les 20 langues les plus parlées), y compris le **pidgin nigérian** (+5,8 écrit avec un
adaptateur).

### 2. Le raisonnement est déjà dans l'état

On donne au modèle une petite énigme : « Alice est devant Bob. Bob est devant Carl. Qui est devant tout le
monde ? » Les phrases sont mélangées, il faut donc composer. Une sonde linéaire lit la réponse dans l'état :
**100 %** pour deux personnes, **51 %** pour six, contre 5 % de hasard. **Le modèle compose sans écrire.**

### 3. Mais le français et l'anglais ne sont pas dans le même espace

La même sonde, entraînée en français, ne lit **pas** l'état anglais : 5,8 %, le hasard. La capacité est là, la
**géométrie** ne l'est pas. D'où l'idée centrale du projet : un **pont** — une simple carte linéaire, apprise sur
des phrases appariées, qui traduit un état anglais vers l'espace français. Résultat : **100 / 91 / 68 / 52 / 46 %**
pour 2 à 6 personnes, contre 4-8 % sans pont. Ce pont :

- marche pour d'**autres relations** (la taille : 0,85 à 0,44), d'**autres langues** (espagnol, allemand, et
  **arabe** — une autre famille, une autre écriture) ;
- doit rester **linéaire** (un réseau plus puissant échoue) ;
- fonctionne à **plusieurs couches** (12, 18, 24), et avec **un seul pont** pour toutes les longueurs ;
- tient à **toutes les échelles** (3, 7 et 14 milliards : 0,81 à **0,975**), et jusqu'à **12 personnes** (0,70 au
  14 B) — *pas de mur, une pente que la taille aplatit.*

### 4. L'alignement peut s'apprendre

Le pont est une pièce externe. On a donc entraîné le modèle lui-même (un petit adaptateur, LoRA) sur les deux
langues : la sonde française lit alors l'état anglais à **65,6 %** ; avec un objectif contrastif qui rapproche
explicitement les deux langues, **74,2 %**. L'alignement **émerge entre 400 et 800 pas** d'entraînement, puis
**sature** (75,3 %). Le prix : l'in-langue baisse (de 98,7 % à 77,6 %). *La tête bien faite a un coût, et il est
mesurable.*

### 5. Ce qui résiste : le plan

Un état de **plan** résume un contexte plus long (les quatre premières phrases d'une série) pour prédire la
cinquième. Lui ne s'aligne pas : ni les ponts, ni le bilinguisme, ni le contraste, ni une récurrence entraînée ne
le font transférer au-delà de ~0,36 (le hasard est à 0,125). Son apparence de transfert venait d'un **effet côté
cible** : la tâche rend les cibles françaises plus faciles à retrouver, sans aligner les langues. *C'est le
contre-exemple qui donne sa valeur au pont : toutes les tâches ne s'alignent pas de la même façon.*

### 6. Le naturel confirme le synthétique

Sur **XNLI** (2 490 paires prémisse/hypothèse traduites en français et en anglais), l'inférence est dans l'état
(50 % en français, 58 % en anglais, contre 33 % de hasard) ; le pont la transfère à **59 %**, et un fine-tuning à
**75-77 %**. *Le pont ne marchait pas que sur des énigmes fabriquées.*

---

## Comment on le sait (et pourquoi on peut nous croire)

Un dépôt de recherche produit beaucoup de chiffres. Le danger n'est pas de se tromper : c'est de croire un chiffre
qui ne mesure rien. Trois règles, payées par des erreurs trouvées à temps :

1. **Le juge doit être neuf.** Le banc initial (la Déclaration des droits de l'homme) était **dans les données
   d'entraînement** : le modèle **récitait** l'article 1 au lieu de le traduire. Toutes les mesures ont été
   refaites sur un texte postérieur à l'entraînement.
2. **Toujours un plancher et un contrôle.** La qualité se mesure en **marge** au-dessus de « recopier la source » ;
   chaque expérience a son **contrôle négatif** (paires mélangées, étiquettes mélangées) et son intervalle de
   confiance. Une référence de traduction **minée** (et non humaine) gonfle la marge : on l'a vu et corrigé.
3. **Ce qui pourrait le rendre faux est écrit à côté.** Six erratums ont retiré des mesures après coup — dont un bug
   de carte des lignes qui avait fait croire à une « falaise » du raisonnement. Les mesures retirées restent dans la
   fiche.

La méthode complète et ses sept leçons : [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md).

---

## Ce que contient le dépôt

| vous cherchez… | allez à |
|---|---|
| **l'état courant** (ce qui est vrai aujourd'hui) | [`docs/en-cours.md`](docs/en-cours.md) |
| **les résultats**, mesure par mesure, avec les contrôles | [`reports/07-mesures-couche-commune.md`](reports/07-mesures-couche-commune.md) · [`reports/`](reports/) |
| **la théorie** (7 chapitres) et la carte du raisonnement | [`docs/synthese/index.md`](docs/synthese/index.md) · [chap. 5](docs/synthese/05-la-pensee-sans-verbaliser.md) |
| **la méthode** et ses pièges | [`docs/synthese/06-comment-savoir.md`](docs/synthese/06-comment-savoir.md) |
| le **récit daté** de la recherche | [`journal/`](journal/) |
| les **instruments** (les expériences sont rejouables) | [`tools/`](tools/) |
| les **corpus** | [`data/`](data/) (non versionné) |
| le **moteur d'inférence** (Rust) | [`drave-core/`](drave-core/) |
| les **règles de travail** du dépôt | [`AGENTS.md`](AGENTS.md) |

**Le vocabulaire, en trois lignes** : une **couche** est une couche de neurones ; un **étage** est un niveau
d'architecture (étage 1 entrée-sortie, étage 2 pensée) ; une **unité de sens** est un élément de la représentation
neutre (la « RSN »), jamais un « jeton » de tokeniseur. Le glossaire : [`docs/glossaire.md`](docs/glossaire.md).

## Par où commencer

1. [`AGENTS.md`](AGENTS.md) — la mission et les règles non négociables (5 min) ;
2. [`docs/en-cours.md`](docs/en-cours.md) — l'état courant, daté ;
3. [`docs/synthese/05-la-pensee-sans-verbaliser.md`](docs/synthese/05-la-pensee-sans-verbaliser.md) — la carte du
   raisonnement, si c'est l'étage 2 qui vous intéresse ;
4. [`reports/07-mesures-couche-commune.md`](reports/07-mesures-couche-commune.md) — les mesures, si vous voulez
   vérifier.

Pour rejouer : les outils sont dans [`tools/`](tools/) et chaque résultat a son JSON dans `reports/`. Les portes de
qualité du dépôt :

```bash
python3 tools/revue_documentation.py   # classement, structure, fraîcheur, cohérence, vocabulaire
bash tools/porte-tableaux.sh           # liens, tableaux, date de la page vivante
bash tools/toutes-les-portes.sh        # toutes les portes (~1 h)
```

## Le moteur

Le dépôt contient aussi un **moteur d'inférence** (`drave-core/`), en Rust, sans dépendance : il exécute les grands
modèles comme des **événements**, pas comme des matrices — les fichiers GGUF sont lus en place (mmap), les
projections se font en listes creuses ou en produit dense, le calcul se découpe en régions réparties sur plusieurs
processus ou machines. Il fait tourner du 0,5 B au 120 B sur le CPU de cette machine, MoE compris. Ce que ça vaut,
tâche par tâche : [`reports/campagne-benefices.md`](reports/campagne-benefices.md).

*La recherche (étages 1 et 2) utilise des modèles Qwen via PyTorch sur GPU ; le moteur est le runtime léger qui
vise à long terme à exécuter ces mêmes modèles sans GPU. Les deux vivent dans le même dépôt.*

## Ce qui reste ouvert

- **Le plan multi-tâches** : la seule variante non testée (entraîner le plan et le raisonnement ensemble).
- **La prose scientifique** (articles) : le corpus parallèle humain manque ; le MultiUN reste la référence technique.
- **Le 32 B** et la profondeur au-delà de 12 personnes.
- **Le dialogue réel** : les sous-titres sont du parlé écrit et contraint.
- **Les langues peu dotées** hors périmètre.

---

*Un résultat qui n'a pas de contrôle négatif n'est pas un résultat.*
