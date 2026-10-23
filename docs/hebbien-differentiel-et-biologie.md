# Notre hebbien différentiel face à la biologie

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> 9 octobre 2026. Le dépôt applique, mesure, sauve, recharge **et réfute** une règle
> hebbienne différentielle (`--hebb-diff`, `rapports/rapport-capteur-hebbien.md`,
> commits `f29b4f5`, `5a7e76b`, `7fd59f6`). Ce document met cette règle en face de ce
> que la biologie a établi — non pas pour l'habiller, mais pour comprendre **pourquoi
> elle échoue**, et ce que la biologie propose à la place.

---

## 1. Ce que notre règle fait, exactement

    Δx = x(t) − x(t−1)            (le changement de l'entrée)
    Δy = y(t) − y(t−1)            (le changement de la sortie)
    D ← D·décroissance + η · Δy ⊗ Δx     (seuil d'événement sur Δx ; forme signée possible)
    y' = y + D·x                  (W reste intact : exportable, réversible)

Quatre réglages, tous nés de mesures : un **seuil d'événement** (sous lui, Δx n'est
que du bruit de dernier bit), une **forme signée** (`signe(Δx)·signe(Δy)`, bornée par
construction), une **décroissance** (sans elle, la bande stable se réduit d'un facteur
dix), et un **écrêtement** de sécurité.

**Les mesures, et elles sont dures.**

| test | résultat |
|---|---|
| en échantillon, η = 1e-4 | perplexité 40,176 contre **40,279** (−0,26 %) |
| en échantillon, seuil + décroissance | **39,985** (−0,73 %) — le meilleur |
| η = 1e-3 sans décroissance | 53 783 (**+33 %**) : divergence |
| autre texte, hors échantillon | 29,151 contre 29,151 — **identique** |
| autre article (40 langues) | 1116,532 contre 1116,532 — **identique** |
| **langues NON VUES** (jpn, hin, ell, heb, tha, kor) | pic **0,6027 → 0,5461** — **dégrade de 5 à 10 %** |

**Cause, écrite dans le commit de verdict** : `D += η·Δy⊗Δx` accumule les statistiques
de transition de ce qu'elle voit ; **rien ne distingue le partagé du spécifique**. Sur
une langue nouvelle, la matrice ajoute une composante fausse qui éloigne la
représentation de la direction commune.

Et une seconde limite, mesurée ailleurs (`rapport-capteur-hebbien.md`) : **créer des
nœuds à partir d'une trace hebbienne linéaire n'ajoute rien sur 69,2 % des poids** —
argument de rang : les lignes de `W` engendrent déjà l'espace entier (896/896 pour
`ffn_gate`), donc « toute nouvelle ligne est une combinaison linéaire des
existantes ». Ce qui échappe vraiment au span linéaire, ce sont les **monômes
quadratiques** (401 856 dans un espace de 896 dimensions).

---

## 2. Les cinq points où notre règle EST biologique

1. **Elle porte sur des CHANGEMENTS, pas sur des niveaux.** `Δx`, `Δy` sont des
   dérivées temporelles discrètes. C'est la forme de la **STDP** : ce qui compte
   n'est pas l'activité absolue mais la *coïncidence temporelle*, et les synapses
   corticales sont adaptatives (facilitation, dépression) — elles répondent au
   changement.
2. **Le seuil d'événement est un seuil de spike.** Notre justification était
   numérique (« la plupart des Δx ne sont que des derniers bits ») ; la biologie a la
   même : sous le seuil, un potentiel postsynaptique ne déclenche rien, et le bruit
   ne doit pas être appris.
3. **La décroissance est le renouvellement synaptique.** Sans oubli, il n'y a pas
   d'apprentissage stable — notre bande stable s'élargit d'un facteur dix avec elle.
4. **La forme signée est le principe de Dale.** Un neurone est excitateur *ou*
   inhibiteur ; `signe(Δx)·signe(Δy)` est borné par construction, comme une synapse
   dont l'effet est contraint.
5. **Garder `D` séparé de `W` est une architecture biologique.** Le cerveau distingue
   la plasticité *rapide* des poids de la plasticité *lente* structurelle ; et
   l'original n'est pas détruit (nos modèles restent exportables et réversibles).

**Et une correspondance plus profonde, sur le fond** : si l'entrée d'une couche est
*déjà* le résidu d'une prédiction, alors `Δx` **est** l'imprévu — et l'imprévu est
sparse. C'est exactement le principe du **codage prédictif** (Rao & Ballard :
la rétroaction porte la prédiction, la voie montante porte l'erreur —
[PubMed 10195184](https://pubmed.ncbi.nlm.nih.gov/10195184/)), et c'est aussi la
proposition déjà consignée au dépôt pour le transport : « prédire une couche pour ne
transporter que l'imprévu » (commit `c4ffbc8`). **Un modèle prédictif produit
naturellement le flux d'événements que Drave exécute à bas coût.**

---

## 3. Les trois écarts, et ce que la biologie propose

### Écart 1 — pas de crédit : notre règle apprend TOUT, également

Notre `D` n'a aucune notion d'utilité : elle corrèle, elle ne juge pas. C'est
précisément pourquoi elle dégrade une langue non vue — elle y apprend les
statistiques de cette langue comme si elles étaient générales.

**Ce que la biologie fait** : la plasticité corticale est **à trois facteurs** —
pré × post × **neuromodulateur** (dopamine, acétylcholine) : la corrélation hebbienne
ne devient un changement durable que si un signal diffus la valide
([règle à trois facteurs](https://scipedia.bohrium.com/en/sciencepedia/feynman/keyword/three_factor_learning_rule)).
Le cervelet fait la même chose avec une architecture dédiée : la fibre grimpante
porte l'**erreur**, et la dépression synaptique est une règle delta (Marr, Albus —
[revue](https://utoronto.scholaris.ca/server/api/core/bitstreams/6fbf5f92-e36e-4031-9dcc-670e5a0e2156/content)).

**Traduction pour nous** : moduler `η` par un signal **global** — la perte du jeton,
sa nouveauté, ou l'erreur de la couche suivante — transforme notre règle en règle à
trois facteurs, sans rétropropagation par poids. C'est un changement **local** dans
le moteur (`η` devient `η · m(t)`), et c'est mesurable en une soirée avec les outils
existants (adapter sur A, noter sur B).

### Écart 2 — pas de décorrélation : elle apprend le commun ET le spécifique

Notre verdict dit lui-même ce qu'il faudrait : « une règle **contrastive** —
`D -= η·(différentiel INTER-langue)`, l'anti-Hebbien sur la direction de la langue ».

**Ce que la biologie fait** : l'anti-Hebbien est partout — décorrélation dans la
rétine, dans le système électrosensoriel, et l'inhibition latérale qui **retire la
composante commune** avant qu'elle ne soit apprise. La théorie BCM ajoute un seuil
*dynamique* qui suit l'activité moyenne : un même Δ qui prédit bien ne renforce plus.

**Traduction pour nous** : soustraire la moyenne (ou la direction dominante) du
différentiel avant de l'accumuler. C'est une ligne de code dans `HebbDiff::pas`, et
c'est **exactement l'expérience que le verdict réclame**.

### Écart 3 — nos structures sont saturées, donc la croissance ne veut rien dire

Créer un nœud linéaire dans une matrice de rang plein n'ajoute rien (mesuré : 100 %
dans le span). **En biologie, la croissance structurelle existe** — de nouvelles
épines dendritiques apparaissent avec l'apprentissage et sont préférentiellement
impliquées dans la tâche apprise
([Cell Reports 2022](https://www.sciencedirect.com/science/article/pii/S2211124722010464)),
et les axones se réorganisent même dans le SNC mature
([Physiol Rev 2015](https://journals.physiology.org/doi/pdf/10.1152/physrev.00010.2015)).
Deux différences expliquent que cela marche chez elle et pas chez nous :

1. **Ses matrices sont creuses** (~10 % de probabilité de connexion) : y ajouter une
   connexion ajoute une **dimension réelle**, là où une matrice dense de rang plein
   n'a plus de place. C'est le lien direct avec `docs/biologie-pour-drave.md` § 4 :
   **c'est dans un connectome inné creux que la croissance hebbienne a un sens.**
2. **Ses unités sont non linéaires** : une dendrite fait des opérations que la somme
   ne fait pas (spikes NMDA, branches comme petits réseaux à deux couches). Nos
   monômes quadratiques (401 856 directions vraiment neuves) sont le **cartoon** de
   cette non-linéarité — et le dépôt a déjà identifié que c'est là, et pas dans la
   trace linéaire, que se trouve le contenu neuf.

---

## 4. Ce que cela change pour le modèle ad hoc

Trois conséquences, et elles convergent avec les deux autres documents :

1. **La règle locale n'est pas condamnée : elle est incomplète.** Notre verdict est
   négatif pour une règle **purement** hebbienne-différentielle. La biologie n'en
   utilise pas — elle utilise la même, **multipliée par un modulateur** (écart 1) et
   **soustraite de sa propre moyenne** (écart 2). Les deux corrections tiennent en
   quelques lignes et se mesurent avec le harnais existant.
2. **Un modèle prédictif rend le flux sparse par construction.** Si la couche `l`
   prédit la couche `l+1` et que seul l'imprévu voyage, alors les activations sont
   des **résidus** — sparse par nature, donc exactement ce que le chemin par listes
   exécute à bas coût. C'est la version « apprentissage » de ce que
   `docs/modele-pour-drave.md` propose côté « inférence » (poids creux, groupes
   d'événements).
3. **La croissance doit être non linéaire, ou ne pas être.** Le seul chemin de
   création de nœuds qui ajoute de la capacité est celui des **caractéristiques
   quadratiques** (ou d'une non-linéarité par dendrite). Une trace linéaire, même
   parfaite, ne peut pas dépasser le rang de la matrice.

---

## 5. Les expériences, avec les outils du dépôt

| # | expérience | ce qu'elle teste | coût |
|---|---|---|---|
| **E7** | **règle à trois facteurs** : `η ← η · m(t)` où `m` est un signal global (perte du jeton, ou nouveauté mesurée par `‖Δx‖`) ; adapter sur A, noter sur B et sur des langues exclues | la modulation suffit-elle à empêcher l'apprentissage du spécifique ? (le verdict actuel : sans elle, −5 à −10 % hors langue) | quelques lignes dans `HebbDiff::pas`, une soirée de mesures |
| **E8** | **anti-Hebbien** : soustraire la moyenne courante du différentiel avant accumulation | la décorrélation rend-elle `D` transférable ? C'est la correction que le verdict réclame explicitement | idem |
| **E9** | **caractéristiques quadratiques** : trace `H[o][(i,j)] += y[o]·x_i·x_j` sur une projection ouverte (`attn_k`, `attn_v`, `ffn_down` — les 30,8 % non saturées), puis moindres carrés sur le résidu | la croissance structurelle ajoute-t-elle de la capacité **là où il y a de la place** ? | quelques jours, c'est le seul des trois qui demande du code neuf |

**Le premier à faire est E7** : c'est le moins coûteux, il teste l'écart le plus
grave (l'absence de crédit), et il se mesure exactement avec le protocole qui a
produit le verdict négatif — donc la comparaison est directe.

---

## 6. Ce que ce document ne dit pas

- Notre règle **reste réfutée en l'état** : les parallèles ci-dessus expliquent
  *pourquoi*, ils ne la réhabilitent pas. Aucune des trois corrections (E7, E8, E9)
  n'a été implémentée ni mesurée.
- Les correspondances biologiques sont **structurelles**, pas quantitatives : la
  STDP a des fenêtres de quelques dizaines de millisecondes, nos pas sont des jetons ;
  un « neuromodulateur » n'a pas d'équivalent propre dans un moteur déterministe.
- Et une réserve de fond : la biologie **n'optimise pas une perplexité**. Elle
  stabilise un organisme. Nos tests hors échantillon sont plus sévères que ce qu'un
  cerveau aurait à passer — mais c'est le seul critère dont nous disposons, et il a
  dit non.
