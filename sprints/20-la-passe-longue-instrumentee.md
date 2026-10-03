# Sprint 20 — La passe longue, INSTRUMENTÉE : le profil par profondeur et les logits

- **Début** : 01:17 · **Fin prévue** : 03:17 (boxing de 120 min)
- **Objectif** : le bloc 19 a montré que la passe de 1 024 jetons **tourne** ; il
  n'a pas montré qu'elle est **juste**. Relancer la même passe (~60 min) avec
  `--ppl-profil` (perplexité par tranche de 256 positions) et `--logits-bin` : la
  courbe par profondeur distingue « médiocre partout » de « catastrophique au-delà
  de 1 024 », et les logits permettent de comparer sans relancer.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Le profil par profondeur, et ce qu'il révèle

Passe de 1 023 jetons, instrumentée (`--ppl-profil`, `--logits-bin`) :

| tranche | perplexité | jetons notés |
|---|---|---|
| 0-255 | 452 790,059 | 255 |
| 256-511 | 933 648,453 | 256 |
| 512-767 | 1 074 744,877 | 256 |
| **768-1 023** | **6 026 999,115** | 256 |

La perplexité **explose dans la dernière tranche (×5,6)** : un total unique ne
l'aurait jamais dit, et c'est précisément pour cela que le profil existait. Mais
avant d'accuser le contexte long, il fallait savoir si le TEXTE durcit : témoin
Qwen2.5-0.5B sur le même fichier, mêmes tranches de 256 positions →
17,4 · 21,6 · 26,0 · **32,3** (×1,85). Le texte durcit, mais pas de quoi expliquer
×5,6.

### 2. Et là, la mesure qui change tout : la perplexité ABSOLUE n'est pas plausible

Les valeurs ci-dessus (452 790 dans la MEILLEURE tranche) sont du niveau du
**hasard** : pour 129 280 jetons, une prédiction uniforme donne une NLL de
11,77 nats, soit une perplexité de 129 280. Vérifié sur les logits enregistrés
(31 positions, `--logits-bin`) :

| mesure | valeur |
|---|---|
| top-1 exact | **0 / 31** |
| NLL moyenne | **11,657 nats** (uniforme : 11,770) |
| rang du jeton correct | 149 à 111 907 sur 129 280 |

Le moteur prédit donc à peine mieux que le hasard. Test fonctionnel le plus simple
qui soit : **huit répétitions de « The sky is blue. »** (39 jetons) — un modèle qui
fonctionne y donne une perplexité de l'ordre de 1 à 2.

| moteur | modèle | PPL sur le texte répété |
|---|---|---|
| **llama.cpp** (référence externe) | V4-Flash IQ1_M | **1,844** |
| **Drave** | V4-Flash IQ1_M, mêmes 39 identifiants | **1,875** |
| Drave | V4.1-Flash Q2, 16 bits | **3 677,15** |
| Drave | V4.1-Flash Q2, 8 bits | 7 505,87 |
| Drave | V4.1-Flash Q2, 16 bits, **sans engram** | 3 677,15 |

Le tokenizer est hors de cause, et c'est établi par une référence externe :
`tools/tokenize_llama` (nouvel outil, compilé contre llama.cpp) rend
`671,12709,344,8295,16,455,…` pour le même texte, **identiques** aux identifiants
de Drave ; le moteur recolle d'ailleurs le texte à partir de ses propres
identifiants.

**Conclusion, et elle est dure : le chemin V4-Flash est JUSTE (1,875 contre 1,844
pour llama.cpp, soit 1,7 % d'écart attribuable à la quantification d'activation),
et V4.1 est CASSÉ.** Le défaut est donc dans un mécanisme que V4.1 a et que
V4-Flash n'a pas — chaîne mHC **retardée**, compresseur des ratios **1 et 2**,
engram — et il ne peut pas être dans le chemin partagé (`attn_v4`, compresseur CSA,
indexeur, hyper-connexions), puisque V4-Flash le partage et qu'il prédit.

L'engram est innocenté comme cause principale (3677 sans, 4799 avec : il nuit, mais
le modèle est déjà cassé sans lui).

### 3. Ce que ça corrige dans ce que le dépôt affirme

Le plan (P7, P8) et `REPRISE.md` disent « V4.1 tourne, la passe complète est
possible, l'engram est vivant ». Tout cela reste vrai **au sens du calcul** — la
passe tourne, les composants sont vérifiés contre leurs transcriptions — mais
**faux au sens du modèle** : V4.1 ne prédit pas. Un composant vérifié pièce par
pièce peut composer un modèle qui ne fonctionne pas, et c'est exactement ce qui
s'est passé : chaque vérification comparait le moteur à SA transcription numpy du
même document, jamais le modèle à une référence externe.

### 4. Le nouvel instrument : le test des répétitions

Le test « huit répétitions d'une phrase » (39 jetons, ~3 min sur V4.1) est
**fonctionnel** : perplexité ≈ 2 = le modèle prédit ; milliers = il ne prédit pas.
C'est le seul contrôle du dépôt qui dit « ce modèle marche », et il manquait.
Il devient la première porte de tout chantier V4.1.

## Rétrospective — garder / changer / doute

**Garder.**

- **Le profil par profondeur** : c'est lui qui a mis le doigt sur la tranche
  768-1 023 (×5,6), et sans lui le total de 1 287 700 se lisait comme « un chiffre
  de plus ».
- **Le réflexe du témoin** : comparer à Qwen sur le même texte a séparé « le texte
  durcit » (×1,85) de « notre modèle s'effondre » (×5,6).
- **La référence externe** : `tools/tokenize_llama` (20 lignes) a éliminé le
  tokenizer en une minute ; `tools/ref_logits` a donné la PPL de llama.cpp sur le
  MÊME fichier de modèle, ce qui a transformé « c'est peut-être le modèle » en
  « c'est notre V4.1 » — la comparaison la plus utile de la nuit.

**Changer.**

- **Une vérification qui compare le moteur à sa propre transcription ne vérifie
  pas le modèle.** Toutes les vérifications de composants (mHC, compresseur,
  engram, indexeur) ont cette forme : le moteur contre une transcription Python du
  même document de référence. Elles sont nécessaires et insuffisantes — et le
  dépôt a publié « V4.1 tourne » sur cette base. La règle à ajouter : **tout
  modèle déclaré exécutable doit passer un test FONCTIONNEL** (le test des
  répétitions), pas seulement des tests de composants.
- **Une perplexité sans ordre de grandeur est un chiffre qu'on ne lit pas.**
  115 521, 1 743 713, 1 287 700 : ces valeurs étaient publiées depuis des blocs
  comme des références de non-régression, et aucune ne dit « c'est le hasard »
  sans être comparée à `ln(vocab)`. La comparaison au hasard devrait accompagner
  chaque PPL publiée.

**Doute.**

- Le défaut V4.1 n'est pas localisé : la chaîne retardée, le compresseur des
  ratios 1/2 et l'engram restent trois suspects, et l'engram n'est innocenté
  qu'en partie (il nuit *en plus*).
- Le test des répétitions est un test de *fonctionnement*, pas de justesse : un
  modèle qui l'aurait à 3,0 au lieu de 1,8 serait « vivant » mais peut-être faux.
  Il faut les deux — le test fonctionnel et la référence externe.

## Planning du bloc 21 — localiser le défaut V4.1

Le nouvel instrument (39 jetons, ~3 min) rend la bisection possible :

1. **Séparer les trois suspects** : la chaîne mHC **retardée**, le compresseur des
   ratios **1 et 2**, et l'**engram** (déjà isolable : 3 677 sans lui).
   - l'engram : `DRAVE_SANS_ENGRAM=1` ✓ fait ;
   - le compresseur : forcer `compress_ratio` par une variante de configuration,
     ou tester une couche de ratio 1 isolée ;
   - la chaîne retardée : comparer, sur les couches 0 et 1 (ratio 0, donc sans
     compresseur), l'état obtenu avec la chaîne retardée et la même couche
     exécutée avec la convention V4 (coefficients propres au raccord).
2. **Vérifier la tête** : la réduction finale de V4.1 (repliement par la `pre` de
   la dernière FFN) est vérifiée contre notre transcription — donc pas contre une
   référence. Un test fonctionnel sur un modèle V4.1 **synthétique** (comme
   `tools/mhc_v41_synthetique.py`) dirait si la composition est juste.
3. **Écrire la porte fonctionnelle** dans `tools/portes.sh` pour V4-Flash (déjà
   juste, 1,875) : elle servirait de garde-fou immédiat, et son absence est ce qui
   a laissé passer le défaut.

## Ce qui reste, nommé

- **V4.1 ne prédit pas** : c'est le constat du bloc, et il prime sur tout le
  reste — y compris sur les chiffres de performance de la nuit (qui restent
  valides : la passe est ×3,54 plus rapide, elle calcule juste un modèle cassé).
- **Aucune référence externe pour V4.1** : llama.cpp ne le charge pas.
- Le **tokenizer** est hors de cause (référence externe, identifiants identiques).
