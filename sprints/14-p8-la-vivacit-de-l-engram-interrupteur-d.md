# Sprint 14 — P8 — la vivacité de l'engram : interrupteur DRAVE_SANS_ENGRAM, A/B perplexité et vides, et le masque des jetons d'image

- **Début** : 21:20 · **Fin prévue** : 23:20 (boxing de 120 min)
- **Objectif** : P8 — la vivacité de l'engram : interrupteur DRAVE_SANS_ENGRAM, A/B perplexité et vides, et le masque des jetons d'image
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La question de P8 est fermée : l'engram est VIVANT

Le plan P8 laissait une question qui ne se déduit pas : une injection branchée,
vérifiée contre la référence numpy et **non nulle** peut encore n'entrer dans
aucun calcul sans que rien ne le dise. Le seul moyen de l'établir est de couper et
de regarder bouger. `DRAVE_SANS_ENGRAM=1` (déclaré dans `VARS_LUES`, **annoncé**
quand il est actif : « le moteur calcule un autre modèle que V4.1 ») le permet.

Passe complète V4.1, mêmes jetons (`270,15301,6605,223`), ctx 8, 8 bits
d'activation des deux côtés :

| mesure | avec engram | sans engram |
|---|---|---|
| perplexité (3 jetons notés) | **1 743 713,6243** | **1 427 298,2128** |
| écart | — | 22,2 % (soit +0,200 nat de perte moyenne) |
| vides `engram_kv` / `engram_sortie` | 16 fichiers, non nuls (rms 0,058 à 0,73) | **aucun fichier** (le bloc n'a pas tourné) |
| couche 0 (tous les vides internes) | — | **identique au bit près** (contrôle : l'engram est aux couches 1 et 14) |
| couches 1 à 39 | — | **toutes différentes** (8,24 à la couche 1, 12,54 à la couche 14, 42,28 à la couche 39) |

2 528 tenseurs comparés, 2 431 différents ; hors le vide du **flux final**
(`hidden_final`, étiqueté `-0-` par le dumping, écart 1,63 = la conséquence sur la
sortie du modèle), la couche 0 est identique au bit près.

**Et l'ablation grandit avec le contexte** (mêmes réglages, mêmes jetons, deux
fenêtres) :

| contexte | avec engram | sans engram | écart |
|---|---|---|---|
| ctx 8 (3 jetons notés) | 1 743 713,6243 | 1 427 298,2128 | **+22,2 %** |
| ctx 32 (31 jetons notés) | 115 521,8693 | 74 328,5818 | **+55,4 %** |

L'écart DOUBLE quand la fenêtre passe de 4 à 32 jetons : c'est le comportement
d'une mémoire d'n-grammes (plus de contexte = plus de n-grammes touchés, donc plus
d'injection), et cela renforce la preuve de vivacité. Cela laisse aussi une
question ouverte, écrite plus bas : **retirer l'engram AMÉLIORE la perplexité sur
ces fenêtres**, ce qu'une mémoire entraînée avec le modèle ne devrait pas faire.

**Ce que ça prouve, et ce que ça ne prouve pas.** L'injection entre bien dans le
calcul (elle change l'état dès la couche 1 et la sortie du modèle) et elle a un
effet matériel. Cela ne prouve pas qu'elle est *correcte* — cette preuve-là reste
la comparaison à la référence numpy (`tools/verifier_v41_engram.py`, projection à
~1e-5, injection à ~1e-6). Que l'engram **dégrade** la perplexité sur quatre jetons
à froid (+22 %) n'est pas un contre-argument : c'est une mémoire d'n-grammes
interrogée sans contexte, et la mesure n'a pas été faite à contexte long.

### 2. Le masque des jetons d'image : décision écrite

`dead_mask` (`image_sentinel_mask`) est ce qui, côté référence, remplace les jetons
d'image par `K_ENGRAM_DEAD_ID` pour que le hachage d'n-grammes ne mémorise pas les
placeholders. Le moteur ne l'a pas : il passe un masque vide (« garder partout »),
et c'est exact pour du texte **seul**, qui n'a aucun jeton sentinelle.

Décision de ce bloc : **ne pas l'implémenter**, et écrire sa condition de
réouverture — un chemin multimodal V4.1 qui produit des jetons sentinelles
(`docs/plan-mla-vision.md`, §« ce qu'il faut injecter à la place des jetons
d'image »). L'implémenter aujourd'hui serait deviner la forme d'une entrée qu'aucun
chemin du moteur ne produit.

### 3. Les correctifs de la revue adverse (commit `81dbd2d`)

La relecture adverse du bloc 13 a rendu son rapport dans cette boîte. Le détail des
trouvailles est dans [`sprints/13`](13-les-deux-enigmes-du-decoupage-v41.md) ; ce
qui a été corrigé **ici** :

| correction | preuve |
|---|---|
| compteur des octets REÇUS : le préfixe de corps (`1 + 4·np`) n'était pas compté — 17 octets sur un flux V4.1 | mesuré sur Qwen : 3 664 / 3 664 (au lieu de 3 664 / 3 663) ; sur V4.1 : **82 016 / 82 016** |
| `norme_finale` : `take()` en **tête** (il n'était que dans la branche `hc_retarde`) | les deux branches laissaient la `pre` en place ; le `forward` suivant l'aurait consommée |
| trame `debut = 0` portant une `pre` : **refusée** en le disant (elle était ignorée en silence) | nouveau refus dans le nœud moteur |
| LOT recevant une `pre` : **refusé** (ce chemin ne saurait pas l'appliquer) | nouveau refus côté pilote |
| `portes.sh` ignorait le code retour de la porte du découpage (« modèle absent » → « toutes les portes sont vertes ») | démontré avant/après : `MODELE=/inexistant.gguf` → code 1 → ❌ |
| `timeout 180` sur le pilote dans la porte (un interblocage la laissait tourner) | — |
| plafonds de la porte resserrés (6e-2 / 1e-2) + contrôle « mode 4 ≤ mode 2 » | 3,65e-2 et 4,45e-3 mesurés |
| `mktemp -d` dans la porte : deux exécutions ne se tronquent plus le journal | — |
| chiffres publiés corrigés : 953 tenseurs (et non 2 544), 82 016 au retour (et non 81 999), « interblocage » (et non « faux et muet ») | digeste régénéré, cinq documents alignés |
| la **réduction finale** n'était couverte par aucun tenseur (« réduction finale comprise » était plus fort que la mesure) | `norme_finale` vide son résultat (`reduit`) ; mesuré : `reduit-0-{0,1,2}` du pilote **identique au bit près** à `hidden_final-0-{0,1,2}` de la référence — 0,000e+00 sur 5 120 valeurs |
| `np = 1` n'était exercé par aucun test | test `une_trame_a_premix_porte_est_lue_et_comptee` (trame forgée à 4 copies, pré-mix relu tel quel, compte d'octets vérifié) — 63 tests |

### 4. La vérification de bout en bout, refaite avec le binaire corrigé

V4.1 découpé à la couche 20, après TOUS les correctifs :

```
  référence locale  : perplexité 1743713.6243  (68.1 s)
  deux nœuds        : perplexité 1743713.6243  (50.7 s)
  écart             : 0.00e0
  transport         : dense f32 · 82016 octets par flux (aller) · 82016 au retour · 3 flux
```

## Rétrospective — garder / changer / doute

**Garder.**

- La **porte qui coupe** : `DRAVE_SANS_ENGRAM` a coûté vingt lignes et a répondu en
  une mesure à une question que trois vérifications partielles laissaient ouverte.
  Le motif « interrupteur + A/B » vaut pour tout composant dont on ne sait pas
  s'il est vivant — le compresseur, l'indexeur et le cache partagé sont tous
  vérifiés par tenseur, aucun par coupure.
- **La relecture adverse a payé** : trois chiffres publiés étaient faux, et l'un
  d'eux (la porte qui dit « vert » sur un échec) était un instrument de mesure
  défaillant — exactement ce que le dépôt interdit.

**Changer.**

- **Un chiffre agrégé doit nommer son ensemble.** « 0 sur 2 544 » était un
  sous-ensemble mal étiqueté : la passe de référence du pilote écrit dans le même
  répertoire et écrase les mêmes noms. Écrire « 0 sur 953 (passe répartie) » est
  aussi court et ne peut pas être faux. Action : quand un chiffre compte des
  fichiers, compter AUSSI ceux qui ne peuvent pas échouer, et les nommer à part.
- **Un compteur fait partie de la mesure.** Les octets reçus étaient sous-comptés
  de 17 octets et personne ne l'aurait vu sans la relecture : un compteur non
  symétrique (émission ≠ réception) doit être tenu par un test — c'est fait (33 et
  non 32).

**Doute.**

- L'A/B de l'engram est fait sur **quatre jetons** et un seul texte. À contexte
  long, la mémoire d'n-grammes pourrait aider au lieu de nuire ; rien ici ne le
  dit. C'est une mesure de *vivacité*, pas de *qualité*, et elle est présentée
  comme telle.
- La porte du découpage tourne sur un modèle **sans hyper-connexions** : `np = 1`
  n'est exercé par aucun test automatique (le pré-mix n'est couvert que par le run
  V4.1 manuel de 4 minutes).

## Planning du bloc 15 — P9 : le poste qui fait 14 secondes par jeton

Le profil de la passe V4.1 est sans ambiguïté (mesuré, `--ppl` ctx 8) :

```
  postes (ms/token) : projets-attn 0.00 | rope 0.00 | attention 12369.91 | proj+mlp 9383.19 | total 21753
  dont attention : scores 0.00 | softmax 0.00 | somme pondérée + écriture KV 12369.91
```

**12,4 s par jeton dans la somme pondérée de l'attention** — le chemin V4 utilise
un `matvec_f32` naïf là où le reste du moteur passe par des noyaux i8/i16
vectorisés. C'est ce poste qui rend toute vérification à contexte long inabordable
(32 jetons = 5,4 min ; 1 024 jetons = 3 h).

Chantiers du bloc 15 :

1. **Mesurer avant de toucher** : profil par couche et par tête sur quelques
   jetons, pour savoir si le poste est la boucle `Σ_h poids_h · v` elle-même ou
   l'écriture du cache KV (`--banc-kv` existe déjà).
2. **Accélérer SANS changer un chiffre** : noyau vectorisé (AVX2, comme
   `dot8_avx`) ou parallélisation par tête, avec la **preuve d'égalité au bit
   près** sur les vides (`DRAVE_DUMP_COUCHES`) avant/après — la règle du dépôt est
   qu'aucune optimisation ne change une sortie sans le dire, et ici elle ne doit
   rien changer.
3. **Publier le gain** en secondes par jeton, la porte V4-Flash (8430,4966)
   servant de garde-fou.

## Portes

- `tools/portes.sh rapide` : **toutes vertes** (62 tests au moment du passage,
  63 depuis l'ajout du test `np = 1` en fin de bloc), Qwen 19,3885,
  clusters 799,8557, V4-Flash 8430,4966, engram, et les cinq modes du découpage).
- `tools/porte-flux.sh` : durcie dans ce bloc (code retour, délai, plafonds,
  `mktemp -d`) — 5/5 verts, et son échec précoce est maintenant vu par `portes.sh`.
- V4.1 découpé : écart **0,00e0** avec le binaire final.

## Ce qui reste, nommé

- **`np = 1` n'est exercé que par un test de DÉCODAGE** (trame forgée, pré-mix relu
  et compté) : l'ÉMISSION d'un `np = 1` réel — le pilote qui porte la `pre` de son
  dernier raccord — n'est couverte que par un run V4.1 manuel de 365 Go. Une porte
  qui l'exerce demanderait un petit modèle V4.1 synthétique : à écrire, ou à
  assumer.
- **Le masque des jetons d'image** : décision écrite ci-dessus (sans objet en
  texte, réouverture avec un chemin multimodal V4.1).
- **L'engram nuit-il, ou est-ce notre lecture ?** Mesuré : le retirer AMÉLIORE la
  perplexité (+22,2 % à ctx 8, +55,4 % à ctx 32). Une mémoire entraînée avec le
  modèle ne devrait pas dégrader ses prédictions. Ce qui est établi : la formule
  est fidèle — l'adressage (règle collante comprise), la lecture des rangées, la
  projection et la porte ont été vérifiés contre la transcription numpy (0 écart
  sur 480 000 adresses, rangées au bit près, projection ~1e-5, injection ~1e-6), et
  la relecture du portage publié
  ([`mudler/vllm.cpp`](https://github.com/mudler/vllm.cpp/blob/main/src/vllm/model_executor/models/deepseek_v4_1_engram.cpp),
  relu ce bloc) confirme les quatre règles : `rolling ^= valeur × multiplicateur`,
  `rangée = rolling % premier + décalage`, la règle **collante** du blocage
  (un n-gramme à cheval sur un trou vaut le pad) et la porte
  `sigmoid(±√max(|dot|, 1e-6))` avec `hidden + porte × valeur`. Ce qui n'est PAS
  établi : que la table, le `token_map` et les poids d'injection du fichier Q2
  soient ceux avec lesquels ce modèle a été entraîné — et c'est la seule
  explication qui reste si la formule est juste. À creuser au bloc suivant si le
  temps le permet : comparer les mêmes jetons à la référence d'exécution (vLLM)
  quand elle saura charger ce fichier, ou vérifier la cohérence
  `engram_vocab_size`/`compressed_vocab_size`/`token_map` contre les métadonnées
  (fait : table dense de 99 092 entrées ✓).
- **L'engram à contexte long** reste à mesurer : 1 024 jetons coûtent 3 h avec le
  poste d'attention actuel (12,4 s par jeton) — c'est le chantier du bloc 15.
