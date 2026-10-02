# Sprint 10 — V4.1 : la chaîne retardée, et le compresseur des ratios 1 et 2

- **Début** : 17:30 · **Fin prévue** : 19:30 (bloc de 120 min)
- **Objectif** : P7 du plan — « adapter le moteur à V4.1 », dont l'état était
  « constat fait : deux manques, aucun n'est du code à écrire ».
- **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.

## Le résultat

L'objectif de départ était **faux**, et c'est le résultat du sprint : les deux
manques annoncés pour V4.1 (« réduction finale non spécifiée », « ratio 2 sans
référence d'exécution ») sont **démentis par la source**. vLLM porte V4.1 en
entier, et elle dit que V4.1 n'a **pas de tête apprise** (le flux final se replie
avec la `pre` de la dernière FFN) et que ses coefficients **se retardent d'un
raccord** (`mhc_shifted_post_pre`).

Trois livraisons, toutes mesurées sur le fichier de **365,7 Go** :

| livraison | vérification | chiffre |
|---|---|---|
| chaîne mHC retardée + tête sans poids | recalcul numpy depuis les tenseurs du GGUF, 4 positions, **quatre** égalités | copie 0 **exacte** (0,000e+00) · mélanges 8e-08 · repli de la FFN 5e-08 · tête 6e-07 |
| compresseur ratio 2 (couche 2) | `tools/v41_compresseur_reference.py` | pool 5,08e-07 · norme+RoPE de bloc 3,04e-06 |
| compresseur ratio 1 (couche 20) | idem, sans porte ni `ape` | pool 3,47e-07 · 5,59e-06, un bloc par jeton |
| cache compressé partagé (34 couches consommatrices) | contrôle positif/négatif sur la couche 3 | sortie 1,30–2,16 d'écart selon que sa source a tourné ; source identique au bit |
| 4ᵉ égalité : le repli de l'entrée de la FFN | ajoutée après la relecture adverse | 1,0e-08 à 4,9e-08 |

Et trois bugs de configuration trouvés **par** l'exécution, chacun muet :
`n_expert` relu en GGUF-seul (le modèle partait **sans un seul expert**),
`rms_norm_eps` (1e-20 dans le JSON) ignoré au profit d'un repli sur 1e-6, et YaRN
déclaré dans le JSON et non lu (rotation fausse dès la position 1, et le message
accusait le modèle).

## Ce qui a coûté

| étape | coût |
|---|---|
| trouver la référence d'exécution (API GitHub + lecture de 5 fichiers vLLM) | ~35 min |
| lire la sémantique exacte du mHC retardé (3 fichiers, jusqu'au noyau TileLang) | ~25 min |
| implémenter la chaîne + les refus + `--tete-partielle` | ~35 min |
| trois bugs de configuration révélés par les passes avant | ~35 min |
| vérificateur numpy + référence du compresseur | ~30 min |
| portes, rapport, plan, glossaire, commits | ~25 min |

Le chemin a été **long et étroit** : quatre passes avant ont échoué avant la
première qui produise un chiffre (compresseur absent → `ffn_gate` absent →
réduction finale jamais atteinte → garde-fou du découpage).

## Introspection

**1. « Je n'ai pas trouvé » n'est pas « ça n'existe pas ».** Le refus précédent
disait « aucun moteur ne spécifie ce cas » alors que le fichier de référence
d'exécution était à deux requêtes de là. La leçon avait déjà été écrite au tour
précédent (elle est dans `REPRISE.md`), et elle a resservi : ce qui a débloqué le
sprint n'est pas une idée, c'est une **recherche**. Un refus doit donc dire *où
j'ai cherché*, pas seulement *ce que je n'ai pas trouvé* — c'est la différence
entre un constat et une croyance.

**2. La porte a attrapé ce que mes sondes ne pouvaient pas voir.** En calculant
la largeur du compresseur par `dims[0] / hidden` au lieu de `dims[0]`, j'ai donné
`0` aux couches CSA de V4-Flash (`1024 / 4096` en arithmétique entière) — et la
porte V4-Flash est tombée de **8430,2968** à **5026,4538**. Mes deux sondes d'une
seule couche (2 puis 3, sur 4 jetons) donnaient *exactement* la même valeur avant
et après : le bloc compressé n'y est construit qu'à la **dernière** position
évaluée, qui n'est jamais notée. Une sonde qui ne mesure pas le chemin modifié
est un instrument qui ment par construction ; la porte, elle, voit tout le
modèle. Corrigé, remesuré : **8430,2968**.

**3. Un chiffre publié sans vérifier ce qu'il mesure est un chiffre faux.** La
première passe avant de V4.1 a affiché `perplexité 82369,8653` : c'était le
produit d'une tête appliquée à un flux **non réduit** de 4 copies (la plage
partielle rend le flux brut, la tête ne voyait jamais le jour). Rien ne
plantait, le format était bon. C'est en allant lire les vides
(`hidden_final` absent) que l'absence de tête est devenue visible — pas en
regardant le chiffre. Deuxième chiffre faux du même genre : `ffn 2816` dans
`[config]`, qui est `intermediate_size` du `vision_config` (le texte vaut 2304) ;
champ inerte ici, mais affiché.

**4. Deux gros travaux en parallèle se sont écrasés.** Le premier essai de la
couche 2 et le second écrivaient le même journal et le même préfixe de vides ;
le premier a terminé après le second et a ajouté son `EXIT=134` au journal du
succès. Les chiffres du sprint ont été revérifiés après coup (identiques), mais
la règle « sérialiser les gros travaux » avait été écrite pour une raison, et
elle a été enfreinte **par moi**, dans le sprint même où je la citais.

**5. Ce qui a le mieux marché : le vérificateur écrit avant la confiance.** Les
trois égalités et les deux compresseurs ont été vérifiés par des scripts numpy
qui relisent les vides du moteur et les tenseurs du GGUF, écrits depuis la
**source externe** (noyaux vLLM), pas depuis le code Rust. C'est le même
instrument qu'en P4/P5, et c'est lui qui a trouvé quatre bugs d'attention en P3.

## Ce qui reste, nommé

- **Partage du cache compressé** (`kv_source_layer_ids`) : **fait** — les
  consommatrices indexent les tampons de leur source, prouvé par un contrôle
  positif/négatif (et non par relecture). Reste non vérifié : la valeur ABSOLUE
  d'une sortie de couche consommatrice contre une référence externe.
- **Indexeur de V4.1** : ses clés viennent du latent du compresseur principal
  (`indexer.attn_k` + `indexer.k_norm`) et il partage le cache de sa source. En
  attendant, le moteur garde tous les blocs (exact sous `indexer.top_k`, refusé
  au-delà) — et le dit.
- **Softmax par canal du compresseur** : le tableau du rapport ne le prouvait pas
  (l'état injecté était identique à toutes les positions, donc le pool y est
  insensible aux poids) — c'est maintenant un test unitaire à témoin lisible
  (`pool_du_compresseur_est_par_canal`, deux jetons différents, poids 0,5/0,5 et
  0,25/0,75). L'injection par position (fichier REFD) reste à faire pour un
  contrôle de bout en bout sur le vrai modèle.
- **Engram** : adressage et lecture validés, injection toujours pas branchée sur
  une passe avant.
- **Pré-mix sur le fil DRVF** (16 octets par jeton) : sans lui, un découpage de
  V4.1 entre nœuds est refusé — le moteur le dit, mais une grappe V4.1 répartie
  demandera ce champ.
- **DSpark / MTP**, et la **sélection à deux niveaux** (`candidate_*`).

## Revue — ce qui est livré, mesuré

Portes rapides vertes après les changements (`tools/portes.sh rapide`) :
`cargo test --release` **59 verts** · Qwen2.5-0.5B ctx 256 **19,3885** ·
Qwen3-30B clusters **799,8557** · threads **20** · les quatre routages · V4-Flash
43 couches ctx 32 **8430,2968** · engram (adressage) · `--config` de V4-Flash
« calculable : oui ». V4-Flash et Qwen sont donc **inchangés** : la chaîne V4
(`deepseek4`) n'est pas touchée par `hc_retarde`.

Commits : `93cb1b7` (chaîne mHC + trois correctifs de configuration + rapport),
`e4331d4` (compresseur des ratios 1 et 2 + référence numpy), puis le partage du
cache compressé, la 4ᵉ égalité, les correctifs de la revue et la régression
`comp_largeur` (portes vertes remesurées : V4-Flash **8430,2968**).

## Revue adverse (sous-agent, lecture seule, sur les deux commits)

Quatre affirmations **fausses** dans le rapport, toutes corrigées depuis :

| trouvaille | ce qui était écrit | ce qui est vrai |
|---|---|---|
| « les couches 0 et 1 tournent » | `--couches 0:1` = `[0,1)` : **une** couche, et les 56 vides le prouvent (`-0-` partout) | la couche 0 seule ; ① ne peut de toute façon porter que sur elle |
| « les 4 couches sources tournent » | la couche 14 est source **et** engram : `--couches 14:15` panique sur le manque engram | 3 sources chargeables (2, 8, 20), 2 vérifiées |
| « la rotation était fausse dès la position 1 » | à `--ctx 8`, le seuil est 4 × 65536 = 262144 : `cfg.yarn` vaut `None` avant comme après | seuls le message, `DRAVE_YARN=1` (inerte avant) et l'au-delà du seuil changent |
| « au-delà de 65536 jetons » (message du moteur) | le code bascule à **4 ×** la longueur d'origine | message corrigé (262144 pour V4.1) |

Et un **trou de couverture** réel : les trois égalités vivaient toutes en aval de
`l_last`, donc échanger `sa.pre` contre `sf.pre` au repliement de la FFN serait
passé inaperçu. Deux vides de plus (`hc_pre_attn`, `hc_mel_ffn`) et une quatrième
égalité ferment le trou — elle tient à **1,0e-08…4,9e-08**.

Le reste de la revue confirme les chiffres (égalités reproduites au bit près,
compresseur identique, témoins synthétiques identiques à 0,000e+00, chaîne V4
intacte branche par branche, correctifs de configuration inertes pour gpt-oss /
GLM-5.3 / Kimi / Qwen) et relève trois défauts mineurs, corrigés : provenance de
`rms_norm_eps` (le GGUF le déclare aussi), groupes de sources oubliés (9..13,
15..19), `--tete-partielle` invisible dans `--options-actives` et silencieusement
sans effet dans deux modes (il le dit maintenant). Un champ déclaré par le fichier
et lu par personne a aussi été trouvé — `index_source_layer_ids` — et il est
désormais lu, imprimé et vérifié contre la présence des indexeurs.
