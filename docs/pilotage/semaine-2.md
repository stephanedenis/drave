# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle négatif** et ce qui pourrait la rendre fausse.
>
> **La règle.** Chaque vague : **2 à 4 sous-agents**, un **résultat mesuré**, un **contrôle
> négatif**, une **fiche + son JSON**, l'**état**, un **commit vérifié**. Une ligne bloquée est
> **nommée** et on prend la suivante : on ne reste jamais en attente.

## 1. Le point de départ (15/11)

| chantier | acquis | ce qui manque | fiche |
|---|---|---|---|
| **gold réel** | **452** phrases (402 + H50), 184 cibles ; l'ancien nom est **obsolète** | H50 n'est pas encore un **test** ; **10 GP/SUB** à annoter (dont 4 dans H50) ; le dénominateur passe à **194** | [C3](../../reports/rapport-gold-reel-50.md) |
| **page `/` de S** | **369** candidats stockés, **0** profondeur ; la v7 donne **359** dont **99 à ≥3** ; **56** tests | décider garder/régénérer ; **106 conservés**, **41 à re-juger** ; référents **9/16** faux | [C2](../../reports/rapport-coordination-s-v2.md) |
| **Panini** | protocole gelé : **60 paires** (20/20/20), **59 textes**, **27 paires signées** | **26 textes à signer** avec le même extracteur V14 ; puis rejeu et calibration | [B1](../../reports/rapport-protocole-date.md) |
| **restitution** | v2 : **16/46** cadres non vides exacts, F1 **0,5270**, lieu **0,4000** | v3 doit améliorer les **rôles** (`agent`, `prédicat`, `lieu`), pas le format | [D2](../../reports/rapport-restitution-v2.md) |
| **tagger** | **+8,49** pts sur 612, **+6,1** sur 452 ; 4 cas d'erreur caractérisés | la question du **défaut** : coût, latence, clé absente, hors-ligne | [D1](../../reports/rapport-exemples-tagger.md) · [E2](../../reports/rapport-tagger-erreurs.md) |

**Le gold n'est pas à recompter.** 452 est le **nombre** ; H50 est le **statut de test** ; les
10 GP/SUB sont le **levier**. Ajouter 50 phrases ne servirait à rien : c'est la **discrimination**
qui manque, pas le volume.

**Ce qui est déjà clos.** D1, D3, E1 et E2 ne rouvrent pas : ils fournissent les exemples, la
FAQ, les liens et les cas d'erreur. B2 est un **négatif** (les atomes ne prédisent pas les
niveaux) et B3 est **clos** (CIC 42/42) : la semaine 2 ne les rejoue pas, elle attend les
signatures de B1.

## 2. Les cinq jours × deux vagues

Cinq jours de travail (**16 → 20/11**), deux vagues par jour ; **21–22/11 = réserve** pour les
décalages et la clôture. Un jour sans sa deuxième vague est un jour à requalifier, pas à attendre.

| jour | vague | tâche | porteur | livrable mesuré | dépend de |
|---|---|---|---|---|---|
| **J1 · 16/11** | matin | **Le gold réel 452, nommé et tenu à l'écart** : retirer l'ancien nom ; figer le split **402 / H50** ; annoter les **10 GP/SUB** (4 dans H50) ; sha256 du gold avant/après. | S + pilote | [fiche gold 452](../../reports/rapport-gold-452.md) + JSON ; 402 vs H50 ; **184 → 194** cibles ; double codage **4/10**. | C3 ; le gold est à S |
| | après-midi | **La page `/` de S, décidée** : garder l'ancien banc ou régénérer ; si régénération, signature + **106 conservés** + **41 en quarantaine** ; mesurer `/` (369/0) contre la v7 (359/99). | S (écrit) + pilote (mesure) | fiche de décision + JSON ; la liste des 41 ; **0** écriture du pilote dans `tools/structures/`. | C2 ; S doit trancher |
| **J2 · 17/11** | matin | **Le tagger sur H50** : cache chaud puis API ; POS/F1/attachement sur **402** et **H50** ; coût et latence par phrase. | R/B13 | fiche tagger H50 + JSON ; **402 ne baisse pas** ; une règle qui ne gagne que H50 est **rejetée**. | J1 (split) |
| | après-midi | **Le tagger par défaut ?** : matrice défaut / sans clé / clé invalide / réseau coupé ; coût pour 1 000 phrases ; garantir le **hors-ligne par défaut**. | R/B13 + pilote | fiche de décision + JSON ; **sans clé = code 0** en défaut, **`--tagger` = code 4** ; **0 socket** en défaut. | E2 ; J2 matin |
| **J3 · 18/11** | matin | **Panini, le corpus à date contrôlée** : envoyer le manifeste et la commande ; recevoir les **26 signatures** (même V14) ; calibrer sur **44** ; rejouer les **60 paires**. | Panini + humain ; pilote rejoue | fiche protocole v2 + JSON ; si incomplet : **statut incomplet, aucune p-value** ; dates permutées + calibration. | B1 ; signatures externes |
| | après-midi | **Restitution v3 — la qualité des rôles** : `_role_gp` distingue **lieu / temps / destinataire / possession / complément** ; mesurer agent, prédicat, lieu. | R/B13 | fiche v3 + JSON ; gold v2 **46** + gold S **61/144** ; le codec 46/46 ne compte pas comme fidélité ; rôle constant rejeté. | D2 ; gold S |
| **J4 · 19/11** | matin | **Restitution v3 — l'or de rôles** : annoter les **seconds cadres** et les rôles hors cadre ; précision/rappel **par rôle**, plusieurs phrases par texte. | S + R/B13 | fiche or v3 + JSON ; **double codage** ; un or permuté doit s'effondrer. | J3 après-midi |
| | après-midi | **La page `/` de S, recette** : S intègre la migration et les référents (**14 occurrences / 12 formes**) ; le pilote rejoue **56 tests** et mesure `/`. | S (écrit) + pilote (recette) | fiche de recette + JSON ; **106/41** vérifiés ; `/` sert **359/99**, pas **369/0** ; 8765 intact. | J1 ; S |
| **J5 · 20/11** | matin | **La décision du tagger** : appliquer la décision (défaut, opt-in ou `auto` avec clé) ; tests E2 ; docs ; non-régression 452. | R/B13 | fiche + JSON ; **défaut hors ligne** conservé si le coût ou le repli ne tiennent pas ; 4 cas E2 rejoués. | J2 après-midi |
| | après-midi | **La clôture** : passe complète, revue, rapport de semaine 2, état, roadmap, journal, tag. **21–22 = réserve** pour les décalages. | pilote | rapport semaine 2 + JSON ; portes lues par `awk '$2 != 0'` ; rouges tolérées nommées ; tag `semaine-2026-11-22` posé à la clôture (20, ou 22 si la réserve sert). | toutes |

**La question du tagger par défaut n'est pas tranchée d'avance.** La recommandation soumise à la
mesure est : **défaut hors ligne**, `--tagger` **opt-in**, un mode `auto` seulement si la clé
existe et sans changer le code de sortie. J2 fournit le coût et les cas d'erreur ; J5 applique ou
rejette.

## 3. Les dépendances

| dépendance | ce qu'elle bloque | parade (règle 8) |
|---|---|---|
| **S** : session en pause, territoire `tools/structures/` + gold | J1 gold, J1/J4 page | le pilote ne touche **ni** le gold **ni** `tools/structures/` ; il livre la spec et la liste des 41 ; la ligne est **nommée bloquée** et J2 prend la main. |
| **Panini** : 26 signatures, même extracteur V14 | J3 matin, le test à date contrôlée | si absent à J3 : **statut incomplet**, aucune p-value, manifeste et demande publiés ; on prend la restitution. Le test ne se fait **jamais** sur les 27 paires choisies par disponibilité. |
| **H50** : sélectionné sur les erreurs de l'heuristique | le score du tagger | H50 est un **stress test**, pas une généralisation ; contrôle **402** + un échantillon neuf ; une règle qui ne gagne que H50 est du sur-apprentissage. |
| **or de rôles** : 46 textes écrits à la main | la restitution v3 | gold S **61/144** + double codage ; le codec 46/46 est un invariant, pas une compréhension ; rôle constant et or vide comme contrôles. |
| **tagger par défaut** : garantie hors-ligne | la décision de J5 | aucun défaut sans le test **sans clé** (code 0) et **clé invalide** (code 4) ; `auto` ne s'active que si la clé existe. |
| **N2 / A6.2** : hors périmètre | rien cette semaine | on ne les touche pas ; aucun GPU réservé ; les runs N2 restent à N2. |

## 4. Les risques

| risque | effet | parade |
|---|---|---|
| **S ne reprend pas** | la page `/` et le gold attendent | spec + 41 prêts, J2 avance, la ligne reste bloquée et nommée ; aucun contournement du territoire. |
| **Panini ne signe pas** | pas de test à date contrôlée | `statut incomplet` publié, pas de p-value ; la demande et le manifeste sont le livrable ; on enchaîne. |
| **H50 est circulaire** | le gain paraît plus grand qu'il n'est | 402 + échantillon neuf ; le contrôle négatif est la **non-régression du reste**, pas le gain sur H50. |
| **le défaut casse le hors-ligne** | code 4 sur une machine sans clé | défaut heuristique ou `auto` avec clé ; E2 rejoué ; le défaut n'ouvre **aucune socket**. |
| **v3 sur-apprend l'or 46** | gain faux, F1 gonflé | or plus large, double codage, or permuté ; le gold S et le codec restent des contrôles séparés. |
| **une seule annotation** | or bruité, chiffres instables | double codage sur un sous-ensemble, sha256, second lecteur ; les désaccords sont publiés. |
| **dix vagues en cinq jours** | timeouts, vagues bâclées | 2 à 4 sous-agents, mandats courts, livrables partiels acceptés ; **21–22** absorbe le décalage. |
| **concurrence des sessions** | `index.lock`, états qui bougent, mesures qui dérivent | `git add` explicite, re-mesure avant chaque fiche, un seul écrivain de l'état. |
| **dates Panini estimées / traductions** | le test mesure la version ou la traduction | calibration sur les 44, dates permutées, ROPE, pré-enregistrement ; les limites sont écrites. |

## 5. Les livrables et la clôture

| livrable | contenu | preuve |
|---|---|---|
| **le plan** | ce document ; lien depuis `en-cours.md` ; la semaine 1 reste l'archive | revue de documentation, 120 lignes max |
| **les fiches** | gold 452/H50 ; tagger H50 ; tagger défaut ; page `/` (décision + recette) ; protocole date v2 ; restitution v3 + or de rôles ; rapport semaine 2 | une fiche + un JSON par vague, contrôle négatif et limites nommés |
| **le code** | règles de rôles v3 ; décision tagger (si retenue) ; migration `/` et référents (S, sous-module) ; tests | tests verts, non-régression 452 et 56 tests S |
| **l'état** | `en-cours.md`, `roadmap.md`, journal du jour, compteurs | `verifie_en_cours.py`, `revue_documentation.py` |
| **la clôture** | passe complète, tag `semaine-2026-11-22`, semaine 21–22 en réserve | `bash tools/toutes-les-portes.sh` ; `awk '$2 != 0'` ; tag annoté |

**Un chiffre sans contrôle n'est pas un résultat.** Chaque fiche nomme sa base (452, H50, 402,
612), son commit, son dispositif, son contrôle et ce qui pourrait la rendre fausse. Les 41
verdicts de S ne sont **pas** migrés par index ; les 26 signatures de Panini ne sont **pas**
remplacées par un sous-ensemble commode.

## 6. Ce que la semaine ne fait pas

- **Pas de N2, pas d'A6.2, pas de B10.3** : ce sont des lignes d'autres sessions ou des bloqués
  nommés ; aucun GPU n'est réservé par ce plan.
- **Pas de nouveau format de restitution** avant la qualité des rôles : la v3 est une mesure de
  fidélité, pas une couche de plus.
- **Pas de tagger par défaut** sans le test hors-ligne et sans le repli ; l'option `--tagger`
  reste le chemin sûr tant que la décision n'est pas mesurée.
- **L'ancien libellé est retiré** : il disparaît au profit de **gold réel 452**, **lot dur H50**
  et **cibles 184 → 194**.
