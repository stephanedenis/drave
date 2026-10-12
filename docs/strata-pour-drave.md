# Strata → Drave — ce qu'on adopte de l'extérieur

> **2026-10-12 08:51 HAE** (heure lue sur la machine). Note d'apport extérieur (convention :
> `docs/organisation-du-depot.md` § 1, préfixe `*-pour-drave.md`). Le pendant biologique est
> `docs/biologie-pour-drave.md` (E1-E9) ; ici les idées portent **S1-S6**.
>
> **Source** : <https://github.com/Niko1221/Strata>, lu le 2026-10-12 (API GitHub, `README.md`,
> `docs/HOW_IT_WORKS.md`, 8 issues ouvertes). **Règle de lecture** : tous les chiffres cités sont
> **les leurs**, relevés tels quels ; **aucun n'est reproduit ici**, et aucun ne remplace une porte
> du dépôt. Une idée de cette note ne s'engage qu'avec sa porte.

---

## 0. Pourquoi on regarde ce projet

Strata attaque **le même problème que Drave** — un MoE dont les experts ne tiennent pas dans la
mémoire rapide, lus à la demande — avec des paris différents : un seul GPU + la RAM + le CPU en
parallèle, une seule machine, un seul modèle. 22 278 étoiles, 2 150 forks et 803 issues ouvertes
en 18 jours (API du 12/10) : ce n'est pas la preuve que c'est bon, c'est la preuve que la classe
« gros MoE sur matériel ordinaire » est devenue une attente de masse.

Ce qu'on prend : **six idées**, dont trois tombent sur des manques déjà inscrits chez nous
(`docs/manques.md`). Ce qu'on ne prend pas : le produit (§ 3).

| # | leur fait | leur chiffre | ce que ça touche chez nous |
|---|---|---|---|
| — | le modèle est un MoE de 125 G, **24 576 experts**, ~10 par jeton | — | même classe que K3 / V4 |
| — | cache d'experts en VRAM qui **apprend en cours de conversation** | — | **déjà tranché chez nous** : plafond ×1,41, verdict ×1,09 (`docs/roadmap-drave.md` § 3) |
| — | profil de routage persisté (`data/expert-profile-*.bin`) | +7 tok/s (99 → 106) sur des prompts hors recensement, 0 sur petite carte | **S3** |
| — | brouillon = la **couche MTP du modèle lui-même** | 2,4-3,2 jetons acceptés par passe, ×1,6-1,8 | **S1** — c'est M5 |
| — | prompt-lookup **conditionné** à l'acceptation mesurée | 6-11 % sur les éditions de code, « inchangé » ailleurs | **S2** |
| — | préchargement des experts de la couche suivante **pendant** l'attention | préremplissage > 1 000 tok/s | **S4** — c'est notre manque de méthode |
| — | table n-gram de **28,8 Go** sur SSD, quelques rangées par jeton | — | à surveiller, pas à copier |

---

## 1. Les idées, traduites pour le moteur

### S1 — Le brouillon est **dans le modèle** (M5 change de cahier des charges)

**Leur idée.** Pas de second modèle : la couche de prédiction multi-jetons est dans le même GGUF
(`blk.40`), lue et exécutée comme le reste. Elle propose jusqu'à 3 jetons, une seule passe les
vérifie tous.

**Pourquoi ça compte chez nous.** `docs/manques.md` M5 porte déjà le cahier des charges mesuré :
brouillon générique **×0,70**, paire alignée **×1,09**, brouillon minuscule **×1,52**. Le gagnant
mesuré est donc *minuscule*, et Strata montre où le prendre : **dans la cible**, sans entraîner ni
servir un second modèle. Et la cible qui nous intéresse est exactement celle où le spéculatif paie :
« le décodage spéculatif ne paie pas sur une cible qui tient en RAM — c'est la cible qui est trop
rapide » (`docs/modele-pour-drave.md` § 0). K3/V4 **ne tiennent pas en RAM** : une passe vérifiée y
remplace plusieurs passes liées au disque.

**Ce qui change par rapport au plan.** `docs/roadmap-drave.md` axe 2 attend « un modèle brouillon ».
À réécrire : le premier essai n'est pas un modèle séparé, c'est **une couche de la cible** (dernière
couche, ou tête MTP si le GGUF en porte une). Le prérequis vérifiable devient : *le modèle porte-t-il
une couche MTP, et son taux d'acceptation dépasse-t-il le coût d'une passe ?*

**Ce que le dépôt sait déjà des deux cibles** (vérifié dans nos propres documents, pas supposé) :
**K3** n'a **aucune couche MTP vérifiée** (`docs/roadmap-drave.md` axe 2) ; **V4.1** **déclare** des
clés `dspark_*` — « décodage spéculatif, cibles **37-39** » — dans la config lue par le moteur
(`docs/plan-deepseek41-complet.md` § 3.2), et une note de session décrit « MTP | `dspark` : 128 experts
top-3 sur les couches 37-39 » (`docs/glossaire.md` § 18). La question n'est donc pas *y a-t-il une
couche ?* mais *les **poids** du brouillon sont-ils dans le fichier, et que disent les clés ?*

**La porte.** Sur un modèle qu'on a déjà : jeton gourmand **identique au chemin sans brouillon** sur
N positions (la sortie ne change pas, seule la vitesse change), puis le taux d'acceptation. Une porte
qui ne sait pas échouer ne vérifie rien : elle doit être vue **rouge** avec un brouillon volontairement
désaligné.

### S2 — Le prompt-lookup, mais **payé seulement où il paie**

**Leur idée.** Quand la réponse recopie le contexte (édition de code, citation), un brouillon par
recherche dans le prompt propose jusqu'à 5 jetons — **activé seulement là où l'acceptation et le coût
mesurés le justifient**. Le mécanisme est un paramètre mesuré, pas une croyance.

**Pourquoi ça compte chez nous.** C'est le seul brouillon qui ne coûte **aucun poids** : rien à lire
sur le disque, donc rien à ajouter au volume — précisément notre facteur limitant. Il est orthogonal
à S1 et se mesure avec la même porte.

**La porte.** Même invariant que S1 (jetons identiques), plus le **taux d'acceptation par type de
tâche** ; si le taux tombe sous le coût de vérification, le mécanisme se désactive et l'écrit.

### S3 — Le recensement de routage devient un **artefact persisté**

**Leur idée.** Un profil d'experts est *rangé dans le dépôt* (`data/expert-profile-qwen36.bin`) :
comptage de routage sur quelques dizaines de prompts, classement, puis usage par le planificateur.
Mesuré contre un profil non classé : **99 → 106 tok/s** sur des prompts qui n'étaient pas dans le
recensement.

**Pourquoi ça compte chez nous.** On a déjà la matière : `--clusters` et le partitionnement par
co-activation (`docs/plan-modeles-lourds.md`, accord 1,000), et le convertisseur trace le routage
(`--trace /tmp/routage.txt`, `docs/format-clusters.md`). Ce qui manque n'est pas la mesure, c'est
**l'artefact** : un fichier de classement versionné, attaché au modèle, que le placement consomme —
au lieu d'un calcul refait à chaque fois.

**La porte.** Deux placements comparés sur la **même** trace, même modèle, mêmes jetons : profil
classé contre placement naïf. Le chiffre qui tranche est un **temps de lecture**, pas un tok/s de
vitre. Si le gain est nul, la fiche le dit — c'est un résultat, pas un échec.

### S4 — Le recouvrement : lire la couche suivante **pendant** que l'attention tourne (notre manque de méthode)

**Leur idée.** Le préremplissage avance par gros morceaux et **streame les experts de la couche
suivante pendant que la couche courante calcule**. C'est ce qui leur donne > 1 000 tok/s sur un
document de 32 K.

**Pourquoi ça compte chez nous.** C'est **exactement** le manque de méthode inscrit en bas de
`docs/manques.md` § 1 : « la lecture mmap atteint **8,6 Mo/s sur disque dur contre 243 Mo/s en
séquentiel** (÷28) — un préchargement ordonné (`madvise`, lecture des experts par grappe) n'existe
pas ». Strata ne nous apprend pas le chiffre (on l'a) : il nous apprend que **le préchargement est
une condition de conception, pas une optimisation** — chez eux il est branché sur la boucle de
couches, pas ajouté après.

**La porte.** Le même fichier, la même trace d'experts, deux exécutions : lecture à la demande contre
lecture préchargée par grappe (`madvise` + ordre de couche). Le critère est un **débit de lecture
(octets/s) et un temps de préremplissage**, mesurés séparément du décodage — voir § 4, c'est là que
leur bug le plus instructif se trouve.

### S5 — Le cache **adaptatif** — chez nous, sur les nœuds, pas en VRAM

**Leur idée.** Le cache d'experts du GPU se remplit d'un profil, puis **s'adapte à la conversation**.

**Pourquoi ça compte chez nous, et sous quelle forme.** En VRAM, c'est déjà tranché (×1,09). Mais la
question « **quel expert vit sur quel nœud** » est notre terrain : `docs/etat.md` note que la variante
`--echange experts` (C9) a un gain **nul entre vues valides**. La différence entre les deux situations
est instructive : Strata ne déplace pas un expert contre un autre, il **promeut ce qui est demandé**.
La variante à instruire n'est donc pas l'échange, c'est la **promotion** guidée par la trace de routage
de la conversation en cours.

**La porte.** Le gain doit être nul ou positif sur des vues valides, et la porte doit d'abord
**reproduire le zéro connu** de C9 — sans quoi elle mesure autre chose.

### S6 — Leur méthode de comparaison (à copier telle quelle)

Leur PR #1402 publie : **jetons gourmands identiques à llama.cpp b11438** (donc le calcul est le
même), un tableau tok/s côte à côte sur la même machine et le même fichier, et une section
**« ce qui n'a pas été testé »** nommée (AMD, SYCL, Windows, une seule carte). C'est notre axe 4
(« la porte de correction comme produit », `docs/roadmap-drave.md` § 2) appliqué à une fiche de
mesure. À reprendre dans `reports/` : la comparaison **et** la liste des limites.

---

## 2. Ce qu'on n'adopte pas — et pourquoi c'est déjà écrit

| ce qu'ils font | pourquoi non, chez nous |
|---|---|
| cache d'experts en VRAM | mesuré : plafond ×1,41, verdict ×1,09 (`docs/roadmap-drave.md` § 3) |
| noyaux GPU pour le MoE | les poids ne peuvent pas être en VRAM : 2,7-3,9 Go/jeton pour 32 Go |
| courir après les tok/s sur les modèles qui **tiennent** en RAM | llama.cpp y est mûr ; leur propre PR #1402 pousse un 35B-A3B 4 bits pour cartes 8-12 Go, où llama.cpp `--fit on` fait déjà 51 tok/s. **Ça confirme notre § 3** : cette classe est saturée |
| installateur grand public, API OpenAI/Anthropic, serveur MCP | hors de notre axe ; mais la leçon « la porte de correction comme produit » reste (S6) |
| table n-gram de 28,8 Go sur SSD | à comprendre avant de copier : quelques rangées par jeton, lues par le cache du système — notre disque est déjà le goulot |

---

## 3. La veille — ce qu'on regarde chez eux

| quoi | pourquoi |
|---|---|
| **#1549** — avec le miroir hôte, le préremplissage s'effondre (1,03 tok/s contre 74,7 tout résident, ~72×) alors que le décodage tient | **leçon directe** : chez nous aussi le préremplissage et le décodage empruntent des chemins différents. Toute mesure de S4 les sépare, et une porte qui ne mesure que le décodage peut être verte sur un chemin inutilisable |
| **#1468** — accès mémoire illégal dans le préremplissage quand le morceau est large (intermittent) | notre `docs/plan-prefill-reparti.md` joue sur la même variable ; un morceau large est un levier **et** un risque |
| **#1440** — la comptabilité VRAM par carte est fausse (les allocations d'une carte sont imputées à l'autre) | c'est le genre de faute qui rend un budget faux **en silence** — nous avons C10 (budgets vérifiés au démarrage) pour ça |
| **#1402** — méthode de comparaison | le modèle de fiche de S6 |
| force-push et PR communautaires fermées par réécriture d'historique | **risque de gouvernance** : on lit leurs idées, on ne bâtit rien dessus |

---

## 4. La prochaine action (une seule)

Le dépôt choisit ce qui est mesurable maintenant, lui donne une porte, et l'écrit. Les deux
candidats, par ordre de coût croissant :

1. **S4 d'abord** — le préchargement ordonné (`madvise` + lecture par grappe) instruit un manque
   **déjà chiffré** (8,6 contre 243 Mo/s) et ne demande aucune notion nouvelle dans le moteur ;
   sa porte compare deux exécutions du même fichier, préremplissage et décodage mesurés séparément.
2. **S1 ensuite** — rouvrir M5 avec le cahier des charges corrigé (le brouillon est une couche de la
   cible, pas un second modèle). La question qui ne coûte rien est déjà cadrée par le § 1 : lire les
   clés `dspark_*` du shard qui porte la config, puis chercher les tenseurs des couches **37-39**
   (`tools/lire_meta_gguf.py`, puis `--tensors`) — K3, lui, n'a aucune couche MTP vérifiée. La porte
   ne s'écrit qu'après : jetons gourmands **identiques** au chemin sans brouillon, puis taux
   d'acceptation par type de tâche.

**Ce que cette note ne dit pas** : qu'un chiffre de Strata soit reproductible ici. Aucun ne l'est
tant qu'une porte ne l'a pas refait.
