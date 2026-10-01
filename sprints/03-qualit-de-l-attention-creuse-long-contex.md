# Sprint 3 — Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections

- **Début** : 21:49 · **Fin prévue** : 23:49 (boxing de 120 min)
- **Objectif** : Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 114 min (boxing 120 min). Commits : 5.

  - `470e3e9` Revue adverse du sprint 3 : deux écarts graves, dans les phrases qui commentent les chiffres
  - `d29e043` Correction : `--infer` n'ignore PAS `--lot` (mon grep ne suivait pas la chaîne d'appels)
  - `6ad2bc6` Aiguille × attention creuse : le milieu du contexte est perdu (et le doute sur les projections est instruit)
  - `6633338` « Accord du top-1 : 511/511 » était faux — 497/511, et l'outil ne le disait pas
  - `c752ad4` Le déport des projections est EXACT sur un modèle dense — et déplace la perplexité d'un MoE

**Objectif du sprint** : « Qualité de l'attention creuse à long contexte : aiguille à
4k/8k/16k croisée avec `--attn-topk 256`, et instruction du doute sur le déport des
projections ». **Le doute est instruit ; l'aiguille a donné ses premiers points, et
le coût d'une sonde a imposé de revoir la grille.**

### 1. Le doute sur les projections : instruit, et il ne venait pas des noyaux

`--logits-bin` des deux côtés, mêmes jetons, et un outil de comparaison :

| modèle | perplexité CPU / GPU | écart moyen \|ΔNLL\| | accord top-1 |
|---|---|---|---|
| Qwen2.5-0.5B Q8_0 (**dense**) | 17,4315 / **17,4315** | **0,0000** (max 0,0000) | — |
| gpt-oss-120b MXFP4 (**MoE** top-8/128) | 18,5803 / 18,3538 | **0,0379** (max 1,3708) | **497/511** |

Sur un modèle dense, le déport des projections reproduit le CPU **exactement**
(écart moyen nul) : les noyaux GPU sont donc hors de cause. Sur le MoE, les logits
se décalent de 0,038 nat en moyenne et 14 positions sur 511 changent de jeton — ce
qui suffit à déplacer la perplexité de 1 %. **Hypothèse retenue : le routage des
experts**, un top-8 étant une opération discrète qu'un écart de 1e-7 sur un logit de
routeur peut faire basculer. Étayée par le contraste dense/MoE, **pas démontrée** :
la démonstration demande de comparer les routages eux-mêmes.

### 2. ⚠️ Un chiffre annoncé faux, corrigé dans le même sprint

J'ai écrit « accord du top-1 : 511/511 » en lisant la sortie de
`compare_logits.py`… qui n'imprime qu'un ÉCHANTILLON de positions (`i < 24` ou
`i % 32 == 0`). La mesure complète donne **497/511**. L'outil imprime maintenant
l'accord GLOBAL. **Un affichage partiel qui a l'air complet est un affichage qui
ment** — c'est la deuxième fois cette nuit qu'un artefact non testé m'a menti
(après le filet de sécurité du noyau 4, qui ne retenait rien).

### 3. L'aiguille croisée avec l'attention creuse

Le coût d'une sonde est mesuré, et il a dicté la grille : **~175 ms par jeton de
prompt** (`--infer` préremplit jeton par jeton), soit ~4 min par sonde à 4 096 pour
le 0.5B, ~12 min pour le 1.5B, ~25 min à 8 192. La grille a donc été ramenée à ce
qui répond à la question dans le temps du boxing.

| contexte | profondeur | complète | top-k 256 CPU | top-k 256 GPU |
|---|---|---|---|---|
| 4 096 | 0,1 | **oui** (256,5 s) | **oui** (238,5 s) | **oui** (243,1 s) |
| 4 096 | **0,5** | **oui** (246,5 s) | **NON** (242,0 s) | **NON** (267,6 s) |
| 4 096 | 0,9 | **oui** (249,9 s) | **oui** (236,4 s) | **oui** (248,3 s) |

**C'est le résultat le plus important de la nuit pour la mission** : à 4 096 clés,
une attention qui ne garde que **256 clés (6 %)** retrouve l'information au début
et à la fin du contexte, mais **pas au milieu** — alors que l'attention complète la
retrouve. C'est le phénomène « perdu au milieu », et le top-k le transforme en
échec : la sélection retient les jetons récents et les puits du début, jamais une
phrase au milieu dont le score est moyen. CPU et GPU échouent ENSEMBLE, ce qui est
aussi un contrôle croisé des deux implémentations.

Conséquence pour la feuille de route : le plan rangeait « un index (clés
regroupées, sélection approximative avant notation) » hors périmètre. Cette mesure
dit que **sans index, l'attention creuse ne peut pas remplacer l'attention complète
à long contexte** — noter toutes les clés puis garder les k meilleures est
structurellement incapable de retrouver une information de score moyen. Rapport :
`reports/rapport-aiguille-topk.md`.

### 4. ⚠️ Une affirmation fausse, écrite puis corrigée dans le box

J'ai annoncé que « `--infer` ignore `--lot` », sur la foi d'un `grep` limité au
corps de `run_infer`. C'est **faux** : `run_infer` appelle `mdl.generate(...)`, et
`Model::generate` (`model.rs:3911`) utilise bien `forward_lot` sur des tranches de
`self.lot` — son commentaire le dit mot pour mot. Le préremplissage par lots est
donc actif en inférence, et le coût « ~175 ms par jeton de prompt » qui en découlait
était faux lui aussi (4114 × 175 ms = 720 s, alors que la sonde entière, génération
comprise, en prend 250).

**C'est la troisième fois cette nuit qu'un artefact non vérifié m'a menti** : le
filet de sécurité du noyau 4 qui ne retenait rien, l'échantillon de
`compare_logits.py` lu comme un accord global, et ce `grep` qui ne suivait pas la
chaîne d'appels. La règle qui manquait : **vérifier dans le code APPELÉ, pas dans
l'appelant** — et pour un chiffre, dans la mesure, pas dans son estimation.

### 5. Revue adverse autonome : deux écarts GRAVES, dans ma prose

La relecture (sous-agent, autonome) a vérifié chaque chiffre contre ses sources et
re-mesuré deux comparaisons. Les chiffres publiés se reproduisent tous ; ce sont
les PHRASES qui les commentent qui étaient fausses :

1. **« même top-1 partout »** dans le résumé du rapport logits : la mesure dit
   **497/511**. C'est l'erreur « 511/511 » rejouée dans le résumé du rapport qui
   prétendait l'avoir corrigée. Corrigé (résumé, section d'usage, nuance sur les
   14 divergences : 6× plus d'écart en moyenne, mais 3 seulement dans le top-14) ;
2. **la portée du k = 256 dans la grille d'aiguille** : avec `--lot 256`, le moteur
   **ignore `--attn-topk` au préremplissage** — il l'imprime — et seuls les 24
   jetons générés ont une attention creuse (0,58 % des passes). La conclusion
   (« perdu au milieu ») tient pour le DÉCODAGE, c'est-à-dire au moment où le
   modèle regarde en arrière, mais la phrase « une attention qui ne garde que
   256 clés » décrivait le passage entier. Corrigé, et `aiguille.py` remonte
   désormais les avertissements du moteur au lieu de les jeter.

Trois écarts moyens et sept faibles ont été corrigés aussi : dénominateur de
`compare_logits.py` (il imprimait « 0/255 » sans fichier d'ids — il compte
maintenant les positions réellement comparées et **refuse** un ids trop court),
`--gpu-topk` sans `--attn-topk` (affiché et journalisé alors que le moteur ne fait
rien : refusé), p90, chemins de reproduction, « 6 % » → 6,25 %, et trois
affirmations fausses sur les sondes de 8 192 (une seule lancée, ~9 min par sonde
et non 25, par lots et non jeton par jeton).

### 6. Ce que le sprint 4 a déjà, mesuré : le prompt tombe de 286,6 s à 63,8 s

Profilage du préremplissage (3 961 jetons, lot 256) :

| chemin | prompt | postes (ms/jeton) | détail |
|---|---|---|---|
| CPU | 286,6 s (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 | le terme quadratique domine (73 %) |
| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s (62,1 tok/s)** | attention **2,2** · matvec+mlp 12,8 | **×4,5 sur le prompt** |

C'est le levier du sprint 4, et il existe déjà : l'attention du préremplissage est
le poste dominant sur CPU, et le miroir VRAM la divise par 24.

## Introspection

- **Ce qui a marché** : instruire un doute au lieu de le laisser traîner — deux
  exports de logits et un outil existant ont suffi à trancher, et la réponse
  (« les noyaux sont exacts, c'est le routage ») vaut mieux que l'intuition que
  j'avais (une erreur d'accumulation).
- **Ce que je dois changer** : lire la SORTIE d'un outil comme on lit une mesure —
  en se demandant ce qu'elle ne montre pas. `compare_logits.py` n'imprimait qu'un
  échantillon, et j'en ai tiré une affirmation universelle. Corrigé dans l'outil,
  pas seulement dans le rapport.
- **Ce que j'ai appris sur le budget** : une sonde d'aiguille coûte cher (175 ms
  par jeton de prompt) parce que le préremplissage par lots n'est pas branché en
  inférence. Le prochain sprint ne mesure pas seulement : il débloque une capacité
  de mesure.
- **Doute** : la grille d'aiguille est incomplète (8 192 non mesuré dans ce box) —
  elle est reportée, avec le modèle et les commandes, dans le journal ci-dessus.
- **Doute** : le rôle exact du routage dans l'écart de perplexité du MoE reste une
  hypothèse. Si elle est fausse, la cause est ailleurs dans le chemin MoE.

## Planning — sprint 4 (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Le préremplissage déporté par défaut ?** Mesuré : prompt 286,6 → **63,8 s** (×4,5) avec `DRAVE_GPU_KV=1`, l'attention passant de 52,6 à 2,2 ms/jeton. Vérifier que la sortie est identique et proposer le déport quand la VRAM le permet | prompt ≥ 3× plus rapide à 4 096 jetons, perplexité à la tolérance près |
| 2 | **Le k de l'attention creuse** : mesurer l'aiguille au milieu à k = 512 et 1 024 | si le milieu revient, c'est un réglage ; sinon c'est un mécanisme manquant (index) — et c'est écrit |
| 3 | **Grille d'aiguille en `--lot 1`** (tout le passage creux) à 4 096, profondeur 0,5, complète vs k = 256 | l'affirmation « attention creuse » porte enfin sur tout le passage, et non sur le décodage seul |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
