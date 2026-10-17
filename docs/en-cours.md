# En ce moment

> Ce fichier est **écrit à la main à chaque round** : c'est ce que la page d'accueil du serveur de
> documentation affiche en premier. Il dit l'état **courant**, pas l'histoire (l'histoire est dans
> `journal/` et dans les fiches).

**Mis à jour : 2026-10-17, 0 h 14 HAE.**

## Le travail du moment : la tour de vision

La faculté **perception visuelle** est passée aujourd'hui de « **bloquée par un modèle absent** » à
« **vérifiée à l'entrée** » :

| étape | résultat |
|---|---|
| modèle téléchargé | **Qwen2-VL-2B** (986 Mo) + son **`mmproj`** (710 Mo, 520 tenseurs) |
| bugs d'architecture corrigés | **5** — MLP à deux matrices + quick-GELU · fenêtre locale **conditionnelle** · jetons d'image écrits · **biais des LayerNorm** (ignorés) · **convention de rotation 2-D** (lue dans la source) |
| cause de l'écart avec la référence | **le mmproj a perdu une tranche temporelle** du noyau de patchs (0,00 % sur l'une, absente sur l'autre) |
| embedding de patchs, noyau réparé | **EXACT** — 0,00 % sur les 256 patchs |
| couche 0 **à poids égaux** | **cosinus +1,00000059**, écart **5,9e-06** (l'arrondi f32) |
| les 32 couches à poids égaux | **justes sur les 8 premières** (1e-5 : les conventions sont bonnes) ; au-delà, l'écart croît (1e-3 → 0,75) — la tour **amplifie les arrondis**, et c'est mesuré **sur deux images** (une synthétique qui explose à 33 273, une naturelle qui reste à 249) |
| pourquoi les couches profondes ne se comparent pas | **trouvé** : l'attention **s'effondre** (entropie 3,36 → **0,16** entre les couches 1 et 15) et **bascule** d'un patch à l'autre — l'écart est **discret** (variation totale 0,94), aucune tolérance ne peut le résorber |
| **la tour est VÉRIFIÉE** | couche par couche, **en isolation** (même état d'entrée aux deux implémentations, comparaison de la couche seule) : **écart max 7,58e-06 sur les 31 couches** — les conventions du moteur sont justes dans toute la tour |
| le **PROJECTEUR** | ✅ **VÉRIFIÉ** : cosinus **+0,99997509**, écart **0,71 %** (= la quantification Q8_0). L'écart de 66,6 % d'avant venait de **MA comparaison** — je nourrissais la référence avec l'état en **ordre de lecture** alors que son `view` regroupe les quatre entrées **consécutives** (donc une ligne, pas un bloc) |
| le chemin image, complet | embedding **exact** · 31 couches **isolées à 7,58e-06** · `post_ln` conforme (**+1,00000012**) · projecteur **0,71 %** — la porte vérifie désormais les étapes 5 **et** 6 |
| et une leçon pour moi, deux fois | j'ai tiré **deux** conclusions fausses sur le *code* alors que le défaut était dans **ma mesure** : un « correctif » démenti par un panic (`post_ln` fait 1280 poids), puis un écart de 66,6 % qui venait de l'**ordre de mes entrées**. *L'instrument se vérifie avant la conclusion.* |
| ⚠️ **avertissement (levé)** | il y avait un écart entre le **source** et le **binaire** pendant l'investigation du projecteur ✓ ; **il est levé** — le binaire a été reconstruit depuis, et la passe de portes en cours tourne sur une construction propre ✓ |
| ce qui reste | l'**injection** (le chemin image → jetons du modèle de texte) et la **vision multimodale de bout en bout** (une question sur une image) |
| **deux serveurs, deux usages** | **mdserve** = le **navigateur** de documents (**arbre**, **rechargement** toutes les 3 s, **épingles**, **filtrage**, changement de racine ✓) sur **http://127.0.0.1:8771/** (local seulement ✗) · **`serveur-doc.py`** = la page « où en est le travail » sur **http://localhost:8787/** (accessible du réseau ✓). Les deux sont des services `systemd --user` qui redémarrent seuls ✓ |
| **comment s'en servir** | [`docs/utilisation.md`](utilisation.md) — écrit le 16/10 : le **chat** (`tools/chat.py` ✓), le serveur, la mesure, les portes, la vision, **et ce qui manque** (un plus gros modèle, le mRoPE, un serveur d'inférence, `--silence`) |
| lecture du dépôt | un **serveur de documentation** est en ligne : `http://localhost:8787/` (ou `http://192.168.1.101:8787/`) — **service `drave-doc`** (`systemd --user`, `Restart=always`, `linger` ✓), il **relit le disque à chaque requête** (aucun cache ✓) et **redémarre seul** (testé en le tuant ✓) |

## Nouveau : E9, l'homéostasie synaptique (défini et mesuré ce soir)

Le seul emplacement vide de `docs/biologie-pour-drave.md` est **défini et mesuré** : **l'amplitude
globale du changement plastique**. Résultat : **le coût hors domaine est monotone en l'amplitude**
(−0,58 % à ×0,6 → +1,64 % à ×1,25), et l'**optimum ×0,6-0,75 domine le delta entier** —
m32 **−8,75 %** contre −7,47 %, hors domaine **−0,58 %** contre **+0,33 %**. Le réglage publié
jusqu'ici (delta entier) était donc **hors de l'optimum** ✗. Et l'échelle n'a pas besoin d'un oracle : **minimiser la perplexité du modèle sur un texte NEUTRE** (sa propre activité récente, ni rejouée ni visée) désigne **×0,75** ✓ — une règle qu'un cerveau peut appliquer, lui qui a son activité d'hier et pas le domaine de demain. **Et le réglage se RÉPLIQUE** sur trois volumes de rejeu (3, 10, 20 morceaux) : à chaque fois ×0,6 fait mieux en domaine **et** coûte moins cher hors domaine, avec un bénéfice qui **grandit** avec le rejeu (0,7 point à 3 morceaux, 1,4 point à 20). Un essai **par couche** (§ 1ter) montre que **amortir les couches hautes** est le meilleur profil (−0,65 % hors domaine contre −0,04 % pour l'inverse) — mais l'écart est **petit** et le réglage **uniforme** reste le meilleur en domaine : **une seule échelle suffit**. Fiche : [`reports/rapport-e9-homeostasie.md`](../reports/rapport-e9-homeostasie.md). **Et une porte** (`porte-homeostasie.sh`, la 46ᵉ) vérifie désormais le réglage : ×0 rend le modèle, l'activité croît avec l'amplitude, et la domination de ×0,6 est **reproduite** à chaque passe.

## L'ÉTALEMENT, et sa CONTRE-ÉPREUVE (à lire ensemble)

Un critère de **lot** — choisir les morceaux qui **étalent** le plus les pertes — donnait **−10,80 %**
contre −7,21 % pour le hasard, sur **une** graine. La contre-épreuve :
**trois graines** à 3 morceaux → l'étalement gagne **les trois** (moyennes **−10,53 % contre −8,76 %**)
mais de **1,8 point seulement**, du même ordre que le bruit de graine ✗ ; et à **10 morceaux**, il
**perd** contre le hasard (6,5938 contre **6,5073**) ✗.
→ **Le critère n'est pas établi** ✗ ; en revanche **E9 a passé la même épreuve** : sur trois graines, ×0,6 gagne m32 **et** le hors domaine **à chaque fois**, avec un écart de **1,06 point** pour une dispersion de graine de 0,2 — l'effet est **cinq fois le bruit** ✓. (Deux résultats testés le même soir de la même façon : l'un tient, l'autre non — c'est à cela que sert une contre-épreuve.) ce qui reste solide, c'est la **loi** (rejouer compte plus que
choisir, et les critères de **lot** tiennent mieux que ceux de **morceau**). Et la leçon : **une graine
ne mesure pas un critère**. Fiche : [`reports/rapport-sommeil-selection.md`](../reports/rapport-sommeil-selection.md) § 6 et 6bis.
**Ce qui se compose quand même** : étalement ×0,6 (E9) — le coût hors domaine passe de +1,94 % à **−0,05 %** ✓.
**Et la règle d'E9 tient sur trois graines** : minimiser la perplexité sur un texte **neutre** désigne **×0,75** à chaque fois (courbe en U), sans rien savoir du domaine visé ✓ — c'est ce qui la distingue d'un oracle. (Le critère de **diversité**, lui, était déjà validé sur trois graines : la loi « les critères de lot tiennent mieux » a passé l'épreuve ✓.)

## Une reproduction qui n'a pas abouti, et c'est écrit

Vouloir tester **E5 sur d'autres graines** (la leçon « une graine ne mesure pas un critère ») a buté
sur trois obstacles : un **mauvais drapeau** (`--couches-lora` appartient à l'exporteur ✗ — et je
l'avais **masqué avec `>/dev/null`**, ce qui a coûté deux tours ✗), un **mauvais bras** (`--bras lora`
au lieu de `lora+adaptateur` : l'accord tombait à 100 %, c'est-à-dire mesurait le chemin **complet** ✗),
et la **mémoire** (15,3 Go demandés pour 15,55 Go : le protocole de la fiche **ne rejoue pas** dans
16 Go ✗). **E5 n'est donc PAS testé sur plusieurs graines** — et un **deuxième mur** est apparu : à volume réduit
(10 morceaux), la **distillation n'est jamais retenue** ✗ — l'époque est choisie sur la **perplexité**,
or la distillation la **dégrade par construction** → la meilleure époque est **0** (le modèle **non
entraîné**, exporté sans un mot ✗). Sa table se lit donc comme les autres tables à graine unique : un
**ordre de grandeur** ✗ ; le chiffre publié n'est ni confirmé ni infirmé. La correction du défaut est
**faite** : un **garde-fou** avertit maintenant, dans le tableau de résultats, quand un bras distillé a
une époque retenue de 0 (le modèle **non entraîné**) — écrit en **une** édition, vérifié par un essai à
blanc. `--epoque-forcee` est **fait** ✓ et il a permis de voir le fond du mur : à 10 morceaux, la
distillation **DIVERGE** ✗✗ — trois époques suffisent à porter la perplexité à **2,7e12**. L'époque 0
retenue par l'outil n'était donc pas un artefact mais **le moindre mal** ✓✓ (le défaut d'outil est
réel : il ne dit pas *pourquoi* ✗). Conséquence : **E5 n'est pas scalable vers le bas** ✗ — son
résultat (574,70, dégradé mais stable) n'existe **qu'à son volume** (29 morceaux). Et le balayage du
taux le confirme : à 10 morceaux **la fenêtre est VIDE** ✗ — 1e-3/3e-4/1e-4 **détruisent** le modèle
(2,7e12 / 2,7e11 / 6,96e4) et **1e-5 n'apprend rien** (17,72 contre 17,58 de base). Il n'y a pas de
réglage à trouver : il y a un **manque de données** — le KL sur 151 936 logits pousse tout le vecteur
à la fois. Remède **essayé** : **tronquer le KL** (`--kl-tronque K`) — il **élargit la fenêtre d'un facteur 10** ✓
(KL tronqué K=64 ou 512 **stable à 1e-4**, où le KL plein **détruisait** le modèle) et il **apprend**
(+8,6 % de perplexité au lieu de +216 %). Mais mon hypothèse « c'est la forme, pas l'amplitude » est à
moitié fausse ✗ : à taux égal, K=64 fait **pire** que le KL plein (la distribution renormalisée sur 64
classes a un gradient **plus grand** par dimension) — il faut **les deux** (tronquer *et* baisser).
**Recette qui tient à 10 morceaux** : `--distiller --kl-tronque 64 --pas-lora 1e-4`.
⚠️ Et l'**accord n'a pas pu être mesuré** ✗ — **cause trouvée** : l'**adaptateur exporté est
l'IDENTITÉ** (diagonale 1,0, norme 29,93326 = √896 ✓), donc le réflexe est réduit aux 8 premières
couches avec une **tête empruntée**, qui rend des jetons **incohérents** (le cerveau : `[51667, 11042,
320…]` ; le réflexe : `[43850, 71112, 145375…]`, **identique avec et sans adaptateur** ✗). Le 0,0 %
mesure donc **le modèle**, pas la mesure ✓. **Sa raison n'est pas trouvée** ✗ (l'adaptateur est pourtant
dans l'optimiseur à 1e-3 et appliqué dans la passe avant ✗) : pistes nommées — le **snapshot** de la
meilleure validation, ou le **chemin de gradient**. **Le diagnostic est fermé** : à l'époque **forcée 10** (LoRA entraîné, norme 6,57), l'adaptateur est
**exactement** l'identité (écart **0,0**) → **il ne reçoit aucun gradient** ✗, et `Adam` **ignore
silencieusement** un paramètre sans gradient — la même famille de défaut que les trois autres de la
nuit (*un calcul qui n'a pas lieu et qui ne le dit pas*). **Et le siège du défaut est localisé** : l'adaptateur **s'entraîne quand il est SEUL** (norme **34,49**
contre 29,93 à l'initialisation, écart 0,199 ✓) et **pas quand il est JOINT** avec le LoRA (écart
**exactement 0,0** ✗) — or c'est le bras **joint** qu'utilise E5 ✗. La recherche passe donc de
« quelque part dans l'outil » à **une fonction** : la boucle jointe. **La cause était écrite dans le code** ✗✓ : avec `--objectif plein`,
`logits_chemin` rend les logits du **modèle complet** et le commentaire dit « l'adaptateur **ne joue
pas** : il n'existe que sur un chemin tronqué » ✓ — mes runs utilisaient `--objectif plein` ✗ : c'était
**mon** erreur. Avec **`--objectif tronque`**, l'adaptateur s'entraîne ✓ (écart 0,057468) — mais
l'accord reste **0 %** ✗, cette fois **cohéremment** : mon réflexe a une perplexité de **18 231**
contre **181,54** chez E5, soit **100× pire** → le **volume** (10 morceaux contre 29 ✗), et le volume
est ce qui **ne tient pas** dans 16 Go. **Quatre murs, deux franchis** (stabilité ✓, objectif ✓), deux
non (mémoire ✗, volume ✗).

## Le mur de mémoire est tombé (deux GPU), et E5 ne reproduit pas sa configuration publiée

**Stéphane a mis deux GPU à disposition** (deux Quadro RTX 5000, 16 Go ✓) → le protocole d'E5 qui
échouait à **15,3 Go pour 15,55** ✗ est passé ✓ :

| bras (29 morceaux, graine 1) | accord m32 | m20 |
|---|---:|---:|
| témoin (perplexité) | **25,7 %** | 38,1 % |
| **distillé, KL PLEIN, taux 1e-3** *(le réglage publié)* | **24,9 %** ✗ | 38,9 % |
| **distillé, KL TRONQUÉ 512, taux 1e-4** *(la variante stable)* | **30,3 %** ✓ | **51,4 %** ✓✓ |
| *rappel : E5 publié (graine 0)* | *51,0 %* | *68,1 %* |

**La configuration publiée ne reproduit pas** ✗✓ (24,9 % contre 25,7 % pour le témoin : rien ✗) — **mais
la distillation fonctionne** ✓✓ dans la **variante stable** (KL tronqué à 512, taux 1e-4 ✓) : **+4,6
points** sur m32 et **+13,3** sur m20 ✓. Autrement dit : *la conclusion d'E5 dépend d'un réglage que sa
fiche ne mentionne pas* ✗✓ — et ce réglage, on l'a trouvé ici ✓. **Et le mur de mémoire n'existe plus** :
les protocoles « pleins » sont exécutables, et **deux bras peuvent tourner en parallèle** (un par carte ✓).

## Nouveau : l'étude « un modèle natif Drave » (16/10)

Demande : *développer un modèle optimisé pour Drave*. L'étude est écrite —
[`reports/rapport-modele-drave.md`](../reports/rapport-modele-drave.md) — et elle **découle des mesures
du dépôt**, pas d'intuitions : **8 coupes sans perte** (113,0068 ✓) mais un pont **30× plus cher** tôt
que tard ✓ ; le **réflexe** tombe d'accord **0 %** jusqu'à 16 couches ✗ (une tête empruntée plafonne à
267,98 ✓, distillé il atteint 30 % ✓) ; le **pas de pensée** amplifie (λ ≥ 3,7e4 ✗) et **aucun modèle
n'a d'opérateur de pensée** ✗ ; la contrainte **sans multiplieur** est déjà satisfaite (signes figés ✓) ;
**k-WTA 25 %** divise les paires par **3,97** sans toucher la perplexité ✓.

**Le modèle proposé (v0)** : octets (vocab 256 ✓), `dim 512 · 8-12 couches · MoE` ✓, **3 têtes précoces**
(le réflexe ✓), un **bloc de pensée contractant** ✓, un **pont de région appris** ✓, signes figés + k-WTA
✓. Tout est **déjà constructible** avec `tools/entrainer_moteur.py` ✓ (Qwen3 de zéro ✓ — son aide,
cassée par un `%` non échappé, a été réparée aujourd'hui ✓).
**Et la directive d'IDENTITÉ (16/10) a été mesurée tout de suite** ✓✓ : rendre les espaces d'entrée et
de sortie **identiques** (pour coupler **directement** pendant les itérations ✓) suppose de savoir de
combien ils diffèrent ✗ — or ils diffèrent **d'un facteur 648** (état 285,5 · embedding 0,440 ✓) **et**
par la direction (**cosinus +0,1387** ✗, *sous* le témoin de l'embedding moyen, 0,24 ✗✓). L'identité,
même avec une échelle et un décalage, fait **pire que le témoin bête** (99 % et 127 % contre 97 % ✗).
→ **Aucun raccord a posteriori ne peut marcher** ✗ : la seule voie est **d'entraîner** le modèle pour que
les deux espaces **coïncident** ✓✓ — l'entraîneur a déjà `tie_word_embeddings` ✓ ; il manque une **norme
finale calibrée** et une **perte d'alignement** (`‖état − e_{p+1}‖` ✓). C'est **la** modification à faire
au modèle natif, et elle est petite ✓.

**⚠️ Et l'essai immédiat a trouvé l'étape 0** ✗✓ : l'entraîneur **tourne** (4 M paramètres, val 4,8948
bits/octet, k-WTA 25 % sur 17 projections ✓) mais il écrit du **format HuggingFace** ✗ — alors que le
**moteur ne lit que du GGUF** ✗. **L'aller-retour entraîneur → moteur n'est pas câblé** pour un modèle
routé en octets ✓ (l'exporteur du dépôt est écrit pour du dense ✗) : c'est **le chaînon manquant**, il
est **petit** (le format est déjà lu par le moteur ✓, il manque l'écriture ✗), et il doit précéder tout
le reste — sinon rien n'est mesurable **dans le moteur** ✓.

**Quatre étapes, chacune mesurable avec un outil existant** : têtes précoces (`--accord` ✓) → bloc de
pensée (`cycle_sensibilite.py` ✓, `pas_latent.py` ✓) → pont de région (`porte-coupe.sh` ✓) → échelle ✓.
Et ses **risques sont écrits d'avance** ✗ : un 2 M en octets ne parle pas ✓ (c'est un banc ✓), la
qualité peut ne pas suivre la taille ✗, et l'objectif de **décomposition** (pertes par région ✓) n'a
été tenté par personne — c'est la partie originale, et la plus risquée ✓.

## Nouveau (16/10, après-midi) : « penser sans verbaliser » — première mesure

L'idée de Stéphane : un LLM verbalise chaque pas de pensée, un cerveau d'expert **pense sans dialogue
intérieur**. Drave sait écrire et relire un **état**, donc la question est exécutable ✓. Mesuré
(`reports/rapport-pensee-silencieuse.md`, `tools/pensee_silencieuse.py`) :

| réglage | perplexité de la suite | écart |
|---|---:|---:|
| A. lecture seule | **9,6503** | — |
| B. 1 pas **silencieux** (état réinjecté) | **294 181** | **+3 048 315 %** ✗✗ |
| B′. idem, état **normé** (échelle des entrées) | 292 935 | +3 035 398 % ✗✗ |
| **C. 16 jetons VERBALISÉS** | **9,5003** | **−1,55 %** ✓✓ |

**Deux résultats, dont un contre l'intuition** : (1) la **boucle d'état naïve détruit la prédiction** ✗✗
(cinq ordres de grandeur) — **et ce n'est pas un problème d'échelle** ✗✓ (normer ne change rien : 292 935
contre 294 181) → c'est une question de **sémantique** : le résidu **prélinguistique** n'est pas une
**entrée** ✓, la correspondance n'est **pas l'identité** ✓ ; (2) **verbaliser n'est PAS du gaspillage** ✓✓
— écrire 4 jetons améliore la suite de **0,40 %**, en écrire 16 de **1,55 %** (monotone ✓) : le jeton est
le **pont** qui remet l'état dans un espace que le modèle sait relire ✓.

**Et le LANGAGE ABSTRAIT a été construit et mesuré** ✓✓ (`tools/pont_abstrait.py` ✓) : un mapping
**appris** (ridge linéaire 896 × 896 ✓) de la sortie **prélinguistique** vers l'**entrée** post-linguistique
prédit l'embedding du jeton suivant avec **68,6 à 73 %** d'écart, quand **le mot que le modèle aurait
choisi** en est à **122,9 %** ✗✓ (pire que l'embedding moyen ✓) — *l'état bat le jeton, et à **16 jetons
d'avance** encore (84,6-84,9 % ✓)* ; et **toutes les couches se valent** (couche 2 : 72,9 % · couche 23 :
68,6 % ✓✓), ce qui **confirme** la phrase de Stéphane sur les couches intermédiaires ✓. **Mais la boucle
échoue encore avec ce pont** ✗ (453 609 contre 9,65 ✗) : le mapping est un **lecteur** (69 % d'erreur ✓),
pas un **inverse** ✗ — et le cycle, mesuré la même nuit, dit pourquoi (λ ≥ 3,7e4, le pas **amplifie** ✗).
*Lire la pensée est facile ; la faire tourner sur elle-même exige une dynamique contractante.* C'est la
cible, et elle est chiffrée ✓.

**Et le PAS LATENT a été appris et balayé** ✓ (`tools/pas_latent.py` ✓) : `h_p → h_{p+1}` est
**expansif** (λ de 30 à 120 selon l'amortissement ✗) et **aucun** amortissement ne donne à la fois
contraction et contenu ✗ — celui qui conserve le contenu (α = 0,1 ✓) le conserve **parce qu'il ne fait
rien** ✗✓. **La raison est le vrai résultat** ✓✓ : `h_p → h_{p+1}` est « **lire un jeton de plus** » ✗,
pas « penser » ✗ — il apporte de l'information neuve, donc il amplifie ✓. **Un pas de pensée devrait
retenir, et le modèle n'en contient aucun** ✗. La dynamique latente ne se **trouve** donc pas, elle
s'**apprend** ✓ : un module récurrent sur l'état, entraîné à **conserver le contenu** *et* à
**contracter** (λ < 1 ✓) — **exactement la pénalité que la fiche du cycle réclamait de son côté** ✓✓ :
les deux fils demandent **le même objet**.

Ouvre quatre mesures, dans l'ordre de ce qu'elles coûtent : le **pont entraîné** (un adaptateur
état → entrée ✓), le **contrôle apparié** de C (verbaliser **sans** garder les jetons ✓), le même
protocole sur le **cycle entraîné** ✓, et le **mode communication contre mode réflexion** (sonde
linéaire sur les états ✓).

## La passe du 16/10 à 02 h 49 : 44 vertes sur 46 — et elle est SIGNIFICATIVE

**46 portes, 44 vertes, 2 rouges** (les deux **structurels** connus : `porte-indice`, `porte-melange`),
~88 min, aucune sautée. **Et c'est la première passe où les portes peuvent ÉCHOUER** ✓✓ : deux d'entre
elles ne le pouvaient pas (`porte-tableaux`, dont le `sys.exit` n'était pas propagé, et
`porte-prechargement`, où un `rm -f` avalait le code) — elles ont été **corrigées pendant cette passe**,
par l'audit des 46 portes ✓. Les huit passes précédentes auraient donc pu passer **avec un document
cassé sans le dire** ✗.

Ce qui est vérifié **neuf** dans cette passe :
* `porte-tableaux` : **473 fichiers** (tableaux) **et 308 liens relatifs** (nouveau) ;
* `porte-homeostasie` (E9) : ×0 rend le modèle, activité **monotone**, **dominance de ×0,6 reproduite** ;
* `porte-cycle-c2` : la divergence est **bornée et de forme publiée** (14,65 → 275,52 → 940,22 →
  2 988,46 ✓) et **λ = 488,82 > 1 est MESURÉ** (nouveau) ;
* `porte-reflexe` : l'**assemblage** (refus ✓, **invariant d'identité** ✓, accord mesuré avant/après ✓) ;
* `porte-vision` : les couches **1, 15 et 31 en isolation** et le **projecteur** ✓.

## Où en est le dépôt

* **45 portes**, dernière passe **43 vertes** (les deux rouges sont structurels et connus :
  `porte-indice` et `porte-melange`).
* **La carte des facultés** ([`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md)) : neuf
  facultés faites et chiffrées, six partielles, trois négatives, plus **§ 5 « l'architecture qui
  suit »**.
* **La chaîne complète** tourne en une commande : `tools/boucle-cerveau.sh` (percevoir → retenir →
  se souvenir → consolider → agir).

## Les questions ouvertes (réécrites le 15/10 au soir)

1. **La vision multimodale** : le **chemin image est vérifié** (embedding exact, 31 couches à 7,58e-06, projecteur à 0,71 %) — il reste le **mRoPE** du modèle de langue, et le projet est maintenant **cadré en quatre pas mesurables** (valeurs d'or → positions en Rust → `rope` à trois sections → vérification de bout en bout ✓). Le seul pas incertain est le premier ✗ — **et sa cause est maintenant écrite** : dans la version installée, `get_rope_index` et son helper **ne s'accordent pas** ✗ (l'un attend une grille **fusionnée**, l'autre décompte en **patchs** : 16 positions rendues pour 4 jetons ✓). **Changement de plan** : les valeurs d'or ne s'extraient pas en *appelant* la référence ✗ mais en la **faisant parler** ✓ — chercher les `position_ids` explicites qui reproduisent **sa propre sortie par défaut** ✓✓ (une vérification **comportementale**, indépendante de la version ✓) — et elle est **outillée** : `tools/mrope_valeurs_or.py` compare la sortie **par défaut** du modèle à celles obtenues avec des positions **explicites**, pour **trois** conventions candidates (par blocs 2×2, raster, dégénérée ✓) ; il exige une grille ≥ 8×8 (sur 2×2 les deux premiers candidats sont identiques ✗) et **~4,4 Go de carte** — donc pas pendant une passe ✓. **Et le pas 3 est maintenant entièrement spécifié** ✓ : la règle est lue dans la source (`cos.split([32,48,48])`, chaque paquet prenant la ligne `i % 3`) — soit, en unités de fréquence, **16 pour `t`, 24 pour `h`, 24 pour `w`** ✓ ; pour le texte les trois lignes sont **égales** ✓, donc **le mRoPE est un sur-ensemble strict** de la RoPE déjà vérifiée ✓ et le pas 3 devient **mécanique** ✓.
2. **Le décodage spéculatif — verdict sur la famille** : cinq configurations, **cinq fois `p ≤ c`** ✗ (tronqué 4/8, distillé 8, réflexe n-grammes 4/8 : 1 à 4 % d'acceptation). Sur ce modèle et ces textes, **il ne paie pas** — un résultat, pas un échec. Rouvriraient la porte : un **élève distillé**, une vérification en **un** préremplissage, ou un texte à répétition **de contenu**.
3. **Le cycle** : **la cause est trouvée** — le pas de temps **amplifie**, et l'amplification **dépend de ε** : la réponse **sature** vers 0,2, donc **λ local ≥ 3,7e4** (mon premier chiffre, 206, était le régime **saturé** ✗ — corrigé dans la fiche). Une application expansive n'a pas de point fixe stable : d'où l'échec des **quatre** objectifs. **« Amener λ sous 1 » est inatteignable par l'entraînement seul** : il faudrait changer la **forme** du pas, pas son réglage. La cible réaliste de C2 devient la **BORNITUDE** — une boucle qui ne converge pas mais qui ne s'emballe pas.
4. **Le critère de rejeu** : la **diversité** tient (un seuil, validé sur trois graines) ; l'**étalement** ne tient **pas** (effet ≈ bruit, et il perd à 10 morceaux) ; le reste = des ordres de grandeur.
5. **L'homéostasie en ligne (E9)** : l'amplitude est un réglage mesuré (×0,6-0,75, trois volumes, trois graines) et une règle auto-contenue la désigne ; reste une règle qui **mesure en continu**.
6. **La modulation par jeton** : la politique par texte marche, mais exige **deux passes**.


## Comment lire le reste

| document | ce qu'on y trouve |
|---|---|
| [`docs/cerveau-facultes.md`](../docs/cerveau-facultes.md) | **la carte** : chaque faculté, son mécanisme le plus efficient, son coût, son verdict |
| [`docs/etat-cerveau.md`](../docs/etat-cerveau.md) | les douze capacités C1-C12 et l'état de chacune |
| [`reports/`](../reports/) | **une fiche par expérience** (protocole, chiffres, ce qu'elle ne dit pas) |
| [`journal/`](../journal/) | le récit jour par jour, écrit à la main |
| [`docs/references-non-regression.md`](../docs/references-non-regression.md) | les portes, leurs valeurs, et les pièges de lecture |
