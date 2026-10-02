# Sprint 11 — V4.1 : la passe complète, et la rotation des couches compressées

- **Début** : 17:30 · **Fin** : 19:30 (bloc de 120 min)
- **Objectif** : P7 du plan — rendre V4.1 exécutable de bout en bout, et vérifier
  chaque pièce contre une référence externe.
- **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.

## Le résultat

**Une passe avant V4.1 COMPLÈTE** : les 40 couches du fichier de 365,7 Go
s'exécutent — hyper-connexions retardées, cache compressé partagé (ratios 1 et 2),
engram (203 Go de tables lues sans être chargées), indexeur, MoE 384 experts, tête
sans poids appris. La liste des manques de `--config` est vide.

Quatre pièces ont été écrites **et vérifiées** dans ce bloc, chacune contre une
seconde implémentation écrite depuis la source externe (noyaux vLLM, code
llama.cpp) :

| pièce | vérification | chiffre |
|---|---|---|
| chaîne mHC **retardée** + tête sans poids | 4 égalités, numpy depuis le GGUF | copie 0 exacte (0,000e+00) · mélanges 8e-08 · repli FFN 5e-08 · tête 7e-07 |
| compresseur ratios 1 et 2 | `tools/v41_compresseur_reference.py` | couche 2 : pool 5,08e-07 · norme+RoPE 3,04e-06 · couche 20 : 3,47e-07 / 5,59e-06 |
| cache compressé partagé | contrôle positif/négatif | sortie de la couche 3 : 1,30–2,16 d'écart selon que sa source a tourné ; source identique AU BIT |
| engram (hachage → injection) | adresses par la référence + rangées relues | projection ~1e-5 (f32 sur 6 144 termes) · injection ~1e-6 · 6 336 octets/jeton/table |
| indexeur de V4.1 | clés + scores | clés 1,7e-06 · scores 2,9e-07 |

Et une **correction qui touche le déjà-livré** : sur les 41 couches compressées de
V4-Flash, le moteur appliquait son régime de rotation *retardé* (RoPE simple) là où
llama.cpp **et** vLLM appliquent YaRN ×16 à toutes les positions. Porte V4-Flash :
**8430,2968 → 8405,9477**. Rapport dédié :
[`reports/rapport-v4-yarn-compresse.md`](../reports/rapport-v4-yarn-compresse.md).

## Ce qui a coûté

| étape | coût |
|---|---|
| trouver la référence d'exécution de V4.1 (vLLM) et lire 6 fichiers | ~35 min |
| chaîne mHC retardée + tête + refus + `--tete-partielle` | ~35 min |
| trois bugs de configuration révélés par les passes avant | ~35 min |
| compresseur + cache partagé + indexeur | ~60 min |
| engram (hachage, rangées, projection, injection) + vérificateur | ~50 min |
| relecture adverse + régression `comp_largeur` + documentation | ~45 min |
| YaRN des couches compressées (source → correctif → porte) | ~40 min |

## Introspection

**1. La porte a attrapé ce que mes sondes ne pouvaient pas voir.** En calculant la
largeur du compresseur par `dims[0] / hidden` au lieu de `dims[0]`, j'ai donné 0
aux couches CSA de V4-Flash (`1024 / 4096` en arithmétique entière) : la porte est
tombée de 8430,2968 à 5026,4538. Mes deux sondes d'une seule couche donnaient
*exactement* la même valeur avant et après — parce que le bloc compressé n'y est
construit qu'à la **dernière** position évaluée, jamais notée. Une sonde qui ne
mesure pas le chemin modifié est un instrument qui ment par construction.

**2. Une comparaison mal apprêtée ne prouve rien, et il faut l'écrire.** J'ai
lancé une comparaison « décisive » YaRN contre RoPE simple sur 128 positions : le
moteur reprenait à la couche 2 **sans l'état de la couche 1**, donc les deux
régimes étaient indiscernables (corrélations 0,05 à 0,40 pour les deux, à 1e-3
l'un de l'autre). Le bon réflexe n'est pas de recommencer jusqu'à obtenir un
chiffre qui plaise, c'est de publier le protocole et de marquer la mesure comme
NON FAITE.

**3. « C'est petit, donc ça ne compte pas » est un raisonnement, pas une mesure.**
YaRN n'interpole que les basses fréquences : à la position 4, la paire la plus
lente tourne de 4e-4 rad au lieu de 2,5e-5. Les comparaisons à 0,9999 des sprints
précédents étaient donc *aveugles* à ce choix, et personne ne l'avait quantifié.
L'écart entre les deux régimes est de 0 à la position 0, 3,6e-04 à la position 1,
1,2e-02 à la position 9 — maintenant mesuré, et croissant avec la position.

**4. `pkill -f` se tue lui-même.** Le motif `ref_logits.*V4-Flash` figurait dans la
ligne de commande du shell qui le lançait : le job s'est tué avant de démarrer, et
j'ai perdu dix minutes de chargement d'un modèle de 284 Go. Vérifier `pgrep`
d'abord, ou tuer par PID.

**5. Une relecture adverse a trouvé quatre affirmations fausses et un vrai trou de
couverture.** Le trou : les quatre égalités vivaient toutes en aval de `l_last`,
donc échanger `sa.pre` contre `sf.pre` au repliement de la FFN serait passé
inaperçu. Corrigé par deux vides de plus et une quatrième égalité. Les quatre
affirmations fausses (« les couches 0 et 1 tournent », « les 4 sources tournent »,
« la rotation était fausse dès la position 1 », « au-delà de 65536 ») sont
corrigées dans le rapport et le plan, avec ce qui est vrai à la place.

**6. Ce qui a le mieux marché, encore : le vérificateur avant la confiance.** Six
scripts de vérification écrits depuis la source externe (jamais depuis le Rust) ont
trouvé, dans ce bloc : le bug d'ordre d'assemblage de l'engram (une clé par bloc,
pas par tête), le sens du softmax du compresseur, et l'aveuglement des mesures
YaRN. C'est le même instrument qu'en P3/P4/P5.

## Revue — ce qui est livré, mesuré

Portes rapides vertes à chaque étape (60 tests, Qwen 19,3885, clusters 799,8557,
V4-Flash **8405,9477** après le correctif YaRN, engram). Commits : `93cb1b7`,
`e4331d4`, `6208ccf`, `43c677d`, `4594d52`.

## Ce qui reste, nommé

- **Confirmation par tenseur** du YaRN des couches compressées (protocole au §5 du
  rapport dédié) — la justification du correctif est le code des deux références,
  pas encore une mesure d'état.
- **Sélection de l'indexeur exercée sur V4.1** : elle ne choisit qu'au-delà de
  `indexer.top_k` (512) blocs, soit une couche de ratio 1 à 513 positions — une
  passe d'UNE couche, à faire.
- **Sélection à deux niveaux** (`candidate_*`).
- **Pré-mix sur le fil DRVF** (16 octets/jeton) : sans lui, un découpage de V4.1
  entre nœuds est refusé.
- **Débit** : 14 s/jeton sur V4.1 (projections `f32` naïves du chemin V4) — un
  poste de P9, pas une mesure du modèle.
