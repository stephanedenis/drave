# En ce moment

> Ce fichier est **écrit à la main à chaque round** : c'est ce que la page d'accueil du serveur de
> documentation affiche en premier. Il dit l'état **courant**, pas l'histoire (l'histoire est dans
> `journal/` et dans les fiches).

**Mis à jour : 2026-10-17, 20 h 10 HAE.**

## Le travail du moment : la couche commune entrée-sortie (chapitre 7)

La question de la nuit : **une couche qui abstrait la langue** — l'état d'un modèle peut-il porter le **sens**
sans porter la **langue**, et la langue redevenir un **paramètre** à la sortie ? **35 mesures**, 14 pièges,
3 erratums. L'état, en un tableau :

| ce qui **tient** | le chiffre | les mesures |
|---|---|---|
| le noyau est **neutre** (la langue n'y est pas lisible) | **50,1-53,6 %** = le hasard, **5 réplications** (plan **2×2** : prose/littérature × 256/512) | 1, 15, 19, 29, 36 |
| le noyau **garde le sens** | contenu **87,7 / 86,5 %** | 4, 30 |
| la langue vit **aux extrémités** | **58-68 %** en surface, 50 % au milieu | 1, 15, 19, 24 |
| le **sens partagé** est au **milieu** | **+0,083** (couches 8-16), **+0,030** en surface | 18 |
| la langue est un **petit paramètre** | **1,33 %** des poids, **5 ms** de bascule | 2, 3, 7, 24 |
| on peut **penser sans langue** | **50,6-56,2 %** sur **huit** itérations | 11 |
| **un** îlot langue-spécifique existe ✗✓ | couche 3 à **69,0 %** au milieu du 512 littéraire — le seul des cinq modèles | 36, 37 |

**Ce qui a été RETIRÉ** (et qu'il ne faut pas citer comme acquis) : « le relevé est teinté par la langue » (9) ·
« la correction de rang 1 répare » (9) · « la langue comme paramètre **commande** la sortie » (25) · « le sens partagé
vit dans le **récit** » (31) · « la **part de dialogue** l'explique » (32-33) · « l'**alignement** explique la
variation » (22).

**Ce qui reste OUVERT** : pourquoi le signal varie de **17×** entre paires bien alignées (le genre, la taille, le
dialogue, la fidélité, la richesse et l'entropie ont tous échoué) · **peut-on penser deux pas** (trois objectifs, le
même mur) · le signal est-il **utilisable** à l'échelle (un livre sur deux, top-5 37 % au mieux).

**Le corpus français** : 21 textes classiques (**15,7 Mo**, **87 341 formes** — Proust, Stendhal, Hugo, Voltaire,
Baudelaire, Chateaubriand, Diderot, Montesquieu, Corneille, Verne, Zola), trouvés dans les projets `Panini/` et
`Panini-Research/` de Stéphane — et **cinq fichiers mal nommés** détectés au passage (dont trois des quatre
« allemands » du corpus « vérifié », qui sont anglais).

**En une phrase** ✓✓ : *la langue n'est **ni dans l'état** (le noyau est au hasard, cinq fois répliqué) **ni
dans le relevé** (0,7 point) — elle vit à l'**entrée** et à la **surface**, et c'est exactement la structure d'une
couche commune : un contenu partagé, une surface paramétrée par 1,33 % des poids.* Le même sens dans deux langues
se retrouve **mieux que le hasard** (trois livres sur cinq) mais **reste faible**, et **la pensée itérée est sans
langue** — elle ne tient simplement qu'**un pas**.

*La fiche complète : [docs/synthese/07-modeles-alternatifs-entree-sortie.md](synthese/07-modeles-alternatifs-entree-sortie.md)*
· *les notes : [journal/2026-10-17.md](../journal/2026-10-17.md)* · *les chiffres dans
[en-cours.md](en-cours.md)*.

## Plus tôt : la tour de vision

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
| **la synthèse théorique** | [`docs/synthese/`](synthese/index.md) — **six chapitres vulgarisés** et **six schémas SVG** : l'idée, l'anatomie interne, les modes et les portes, les douze facultés et la biologie, la pensée sans verbaliser, et la méthode avec ses cinq pièges |
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

## ⚠️ TROIS OBJECTIFS, LE MÊME MUR — la limite est dans la représentation (17/10, 22 h)

Le round précédent disait : « il faut un objectif différent » ✗ — récompenser le **déplacement informatif**.
C'est fait ✓ (`--marge` : le pas doit **améliorer** le contenu d'au moins marge × 100 %, ce qui **exclut
l'identité** ✓✗). Deux marges testées :

| marge | k=0 | **k=1** | k=2 | k=4 | k=8 |
|---|---:|---:|---:|---:|---:|
| **sans** | 82,2 % | **79,9** ✓ | 93,8 ✗ | 101,3 ✗ | 97,4 ✗ |
| **0,05** | 82,2 % | **80,3** ✓ | 93,7 ✗ | 103,1 ✗ | 99,9 ✗ |
| **0,10** | 82,2 % | **80,4** ✓ | 93,3 ✗ | 103,7 ✗ | 95,3 ✗ |

**La marge n'y change rien** ✗✓ : le contenu s'améliore toujours au **premier** pas et **se dégrade** ensuite,
de la même façon ✗. Les **trois** objectifs — conservation, conservation + contraction, et **progrès exigé** —
donnent **le même mur** ✗✗.
→ **La limite n'est donc PAS dans l'objectif** ✗✓ : c'est la **représentation** qui ne porte pas de second pas ✓✓.
*Il n'y a pas de second pas à trouver* ✓ — et c'est la **troisième** démonstration de la nuit (16/10 sur les
opérateurs, 17/10 sur deux modèles et deux langues, et maintenant contre **trois** objectifs) ✓.
→ **Et la langue reste au hasard** ✓✓ (50,4-61,3 %) : la neutralité **tient** sous toutes les variantes ✓✓ —
c'est le résultat **positif** du chapitre : *la langue n'est pas dans la pensée* ✓✓, même quand la pensée bute.
**Ouverture** ✓✓ : le pas suivant n'est plus à chercher dans les **objectifs** ✗ mais dans **l'entraînement du
modèle lui-même** ✓ — la récurrence **dans** la boucle (programme du 16/10 ✓), la seule porte ouverte ✓.

## ⚠️ LE « SECOND PAS » NE S'OBTIENT PAS — et la recette du 16/10 se reproduit (17/10, 21 h 30)

`--k-entrainement 4` ✓ (entraîner l'opérateur sur k pas tirés ✓), en gardant l'œil sur la langue :

| k | contenu | langue (hasard = 50 %) |
|---:|---:|---:|
| 0 | 82,2 % | 56,2 % |
| 1 | **82,2 %** | 68,2 % ✗ |
| 2 | **82,2 %** | 67,6 % ✗ |
| 4 | **82,2 %** | 51,4 % ✓ |
| 8 | **82,2 %** | **50,0 %** ✓✓ |

**Le contenu est exactement plat** (82,2 % à **tous** les k) → l'opérateur a appris **l'identité** ✗✓ : la seule
façon de rester bon à k=8 est de **ne pas bouger** ✓✓ — la **solution triviale** du 16/10 (son § 15 ✓).
**Le résultat se reproduit sur un autre modèle, une autre tâche, une autre langue** ✓✓ : c'est une
**réplication**, et c'est la meilleure chose qu'un résultat négatif puisse être ✓.
**Donc le second pas ne s'obtient pas par cette recette** ✗✓ : entraîner sur k **choisit** la solution triviale ✓
— une propriété de **l'objectif**, pas de l'opérateur ✓✓.
**Et la langue varie** ✗ (68,2 % à k=1, 50,0 % à k=8) alors que l'opérateur est quasi-immobile ✓✗ → la **petite
dérive** suffit à changer la **séparabilité linéaire** de la langue ✓✓. *La neutralité de langue n'est pas une
propriété robuste de l'état* ✗ : elle dépend de la position exacte dans l'espace ✓.
→ **Conclusion** ✓✓ : (1) la neutralité **tient** avec un opérateur entraîné sur un pas ✓ (mesure 11) ; (2) elle
**n'est pas** une propriété de l'état ✗ (la dérive la fait remonter à 68 %) ; (3) le **second pas** reste hors
d'atteinte ✗✓ — il faudra un **objectif différent** ✗ (contraindre le **déplacement** à être informatif, pas
seulement contractant ✓).

## ✅ LA PENSÉE ITÉRÉE EST SANS LANGUE — mais elle ne tient qu'un pas (17/10, 21 h)

La jonction des chapitres 5 et 7, jamais mesurée : **itérer** l'état préserve-t-il sa **neutralité** ?

| k | contenu (état → mot suivant) | **langue** (hasard = 50 %) |
|---:|---:|---:|
| 0 | 82,2 % | 56,2 % |
| **1** | **79,9 %** ✓ | 53,9 % |
| 2 | 93,8 % ✗ | 52,8 % |
| **3** | 99,5 % ✗✗ | **50,7 %** ✓✓ |
| **4** | 101,3 % ✗✗ | **50,6 %** ✓✓ |
| 8 | 97,4 % ✗ | 54,0 % |

**La langue ne revient pas** ✓✓✓ : sur **huit** itérations, le classifieur reste entre **50,6 et 56,2 %**, soit
**au hasard** ✓✓ (minimum **50,6 %** à k=4 ✓). *La pensée itérée est sans langue* ✓✓ — **penser ne dépend pas de
la langue où l'on parle** ✓✓✓.
**Et le contenu ne tient qu'un pas** ✗ : il **s'améliore** au premier (82,2 → **79,9** ✓) puis **s'effondre**
(93,8 → **101,3** ✗✗, pire que l'embedding moyen ✓) — **exactement** le résultat du 16/10 sur un autre modèle ✓✓.
→ **La réponse complète** ✓✓ : *on peut penser **sans langue**, mais on ne peut penser qu'**un pas*** ✓ — la
neutralité est **stable** ✓✓, le contenu ne l'est pas ✗. **Les deux propriétés sont indépendantes** ✓✓, et c'est
une information neuve ✓.
**Neuvième piège** ✗✓ : mon premier essai **accumulait** `Z = cel(Z)` — les lignes « 2 » et « 4 » montraient 2 et
3 pas ✗✓. *Le label mentait, pas la mesure* ✓ — famille **nouvelle** : après les réglages et les instruments,
**le code lui-même** ✓✗. Corrigé en une ligne ; la conclusion, elle, n'a pas changé ✓.

## ⚖️ NOYAU BILINGUE CONTRE MONOLINGUE + ADAPTATEUR (17/10, 20 h 30)

| dispositif | **français** | anglais |
|---|---:|---:|
| **noyau bilingue** (4,79 M, 10,2 Mo mixtes) | **1,0737** ✓✓ | **1,6493** ✓ |
| noyau monolingue (2,43 M, 96 Mo anglais) | **3,2928** ✗ | **2,2786** ✓ |
| monolingue + **adaptateur français** | **1,4546** ✓ | 3,1438 ✗ |

**Le noyau bilingue gagne** ✓✓ (1,0737 contre 1,4546 — **35 %** de perte en plus pour l'adaptateur ✗), **mais
l'adaptateur rattrape les DEUX TIERS de l'écart** ✓✓ (3,2928 → 1,4546) pour **131 k paramètres** et vingt minutes ✓
— quand le bilingue a demandé **les deux corpus** ✓.
⚠️ **Ce que la mesure ne peut pas dire** ✗ : les deux noyaux n'ont **ni la même taille ni les mêmes données** ✗✓
→ ce n'est **pas** une comparaison à budget égal, c'est une comparaison de **trois dispositifs réels** ✓. Et le
vrai arbitrage est ailleurs ✓✓ : sur un modèle de **7 milliards**, réentraîner sur deux langues est hors de prix ✗,
tandis qu'un adaptateur coûte **1,33 %** et **5 ms** ✓✓ — *c'est à l'échelle que l'adaptateur devient la bonne
réponse* ✓, et ce chapitre ne peut pas le mesurer, seulement le nommer ✓.

## ✅ CINQUIÈME RÉPLICATION — et le plan 2×2 est complet (17/10, 20 h)

Il manquait une case : **dim 512 sur littérature** (val **2,6097**, le meilleur des cinq) :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| **1** | **53,6 %** | 50,7 % | **le hasard** ✓ |
| **2** | **53,5 %** | 50,5 % | **le hasard** ✓ |
| **3** | **69,0 %** | 50,1 % | ✗✗ **couche langue-spécifique AU MILIEU** |
| **4** | **52,2 %** | 50,2 % | **le hasard** ✓✓ |
| **5** | **52,1 %** | 50,8 % | **le hasard** ✓✓ |
| **6** | **52,4 %** | 51,3 % | **le hasard** ✓✓ |
| 8 | 63,9 % | 51,6 % | ✗ (la surface) |

**Le plan 2×2, complet** :

| corpus ▼ / taille ▶ | dim 256 | dim 512 |
|---|---|---|
| **prose** | **50,2 %** | **51,4 %** |
| **littérature** | **50,1 %** puis **51,5 %** | **52,1-53,6 %** |

**La cinquième réplication tient** : cinq couches au hasard (1, 2, 4, 5, 6) — *cinq modèles, deux tailles, deux
corpus, même résultat* ✓✓✓. Et la zone neutre est la **plus large** (cinq couches), cohérent avec : plus de capacité
et de données, plus d'abstraction ✓✓.
**Mais la couche 3 est une exception** : **69,0 %** — une couche **langue-spécifique au MILIEU**, entre deux couches
neutres. *La structure n'est pas monotone* : le noyau est **neutre avec des îlots**, et c'est une nuance **neuve**
que les quatre premiers modèles ne montraient pas.
→ **Ce que cela dit du mécanisme** : le réseau peut **router la langue par une couche intermédiaire** quand il en a
la capacité, tout en gardant le reste abstrait. *La neutralité n'est pas une propriété de **toutes** les couches,
mais de **la plupart** — et la proportion augmente avec la capacité* ✓✓.

## ⚠️ LA VARIATION DE 17× RESTE INEXPLIQUÉE — et c'est la réponse (17/10, 22 h 30)

Trois candidats de plus, mesurables sans modèle :

| livre | ratio de longueur | TTR (fr) | entropie (fr) | **écart** |
|---|---:|---:|---:|---:|
| **Candide** | 0,98 | **0,220** | 4,72 | **+0,1161** |
| **Proust** | 0,92 | 0,125 | 4,61 | +0,0925 |
| **Verne** | 1,19 | 0,185 | 4,72 | +0,0779 |
| **Alice** | 1,22 | 0,199 | 4,70 | +0,0087 |
| **Don Quijote** | 0,92 | **0,083** | 4,48 | +0,0068 |

| corrélation avec l'écart | valeur |
|---|---:|
| ratio de longueur (fidélité ✓) | **−0,25** ✗ |
| richesse lexicale (TTR ✓) | **+0,42** ✗ |
| entropie des octets ✓ | **+0,51** ✗ |

**Aucun candidat n'explique la variation** : les trois corrélations restent faibles (|r| ≤ 0,51) sur **cinq** points
— et avec cinq points, **aucune** n'est significative.
→ **C'est la réponse** ✓✓ : après le **genre** (mesure 31), la **part de dialogue** (mesures 32-33), l'**alignement**
(mesure 22), la **taille** (mesure 31), la **fidélité**, la **richesse** et l'**entropie** — *la variation de 17× est
une propriété de la **paire** texte-traduction, et la nuit s'arrête là* ✓✓.
→ **Pour la suite** ✓✓ : pour **savoir** si un livre donnera un signal, il faut le **mesurer** — pas le prédire.
*Une conclusion modeste, mais c'est une conclusion* ✓✓ : elle ferme la question, et elle dit ce qu'il faudrait pour
aller plus loin (des **dizaines** de paires, un **vrai** alignement phrase à phrase, un modèle **plus grand**).

## ⚠️ LE MEILLEUR INDICATEUR RÉFUTE L'HYPOTHÈSE — la relation était SPURIEUSE (17/10, 21 h 15)

La vraie part de dialogue (fraction des **caractères** à l'intérieur des guillemets, `« … »` / `" … "`) :

| livre | dialogue (fr / en) | moyenne | **écart** |
|---|---:|---:|---:|
| **Candide** | 0,4 / 0,1 % | **0,3 %** | **+0,1161** ✓✓✓ |
| **Don Quijote** | 2,0 / 0,2 % | **1,1 %** ✗ | **+0,0068** ✗✗ |
| **Proust** | 11,8 / 0,0 % | 5,9 % | +0,0925 ✓✓ |
| **Verne** | 19,6 / 0,0 % | **9,8 %** | +0,0779 ✓ |
| **Alice** | 0,0 / 34,8 % | **17,4 %** | +0,0087 ✗ |

**L'ordre est cassé** ✗✗ : **Proust** (5,9 %) et **Verne** (9,8 %) gardent un signal fort ; **Don Quijote** (1,1 %
seulement) garde le plus faible. *La part de dialogue n'ordonne plus rien.*
**Et la raison est visible** : les éditions n'ont pas les **mêmes conventions** — le Proust anglais n'a **aucun**
`" … "`, l'Alice français **aucun** `« … »`. *L'indicateur mesure la **typographie de l'édition**, pas le dialogue
du texte.*
→ **La relation de la mesure 32 était SPURIEUSE** : le premier indicateur (4 livres sur 5) était un **hasard
heureux** — et le meilleur indicateur le montre. *C'est ce qu'un bon instrument doit faire : tuer une relation qui
n'en était pas une* ✓✓.
→ **Ce qui reste** : le signal varie de **17×** sans que ni le genre, ni la taille, ni la part de dialogue ne
l'expliquent — *une propriété de la **paire** texte-traduction*, et **rien de plus simple** n'est démontré.

## ✅ LA PART DE DIALOGUE PRÉDIT L'ÉCART — quatre livres sur cinq (17/10, 20 h 45)

Indicateur grossier (lignes commençant par un tiret de dialogue, ou majoritairement entre guillemets), **identique**
pour tous :

| livre | **part de dialogue** | **écart cross-lingue** |
|---|---:|---:|
| **Candide** | **0,3 %** | **+0,1161** ✓✓✓ |
| **Proust** (*Swann*) | 3,3 % | +0,0925 ✓✓ |
| **Verne** | 13,1 % | +0,0779 ✓ |
| **Don Quijote** | 9,4 % ✗ | +0,0068 ✗ |
| **Alice** | **21,4 %** | +0,0087 ✗ |

**La relation est forte et dans le bon sens** ✓✓ : **quatre** livres sur cinq s'ordonnent exactement par la part de
dialogue — *plus un texte est **narratif**, plus le sens partagé entre les deux langues est retrouvable* ✓✓
(Candide 0,3 % → +0,116 ; Alice 21,4 % → +0,009).
**Et l'exception est instructive** ✗✓ : **Don Quijote** (9,4 % de dialogue) fait **aussi mal qu'Alice** — **9 %**
suffisent à faire tomber le signal à +0,007 quand 13 % (Verne) le laissent à +0,078. *L'indicateur est grossier* ✗
(il ne compte que les lignes **entièrement** de dialogue, pas les répliques **dans** les paragraphes) — et Don
Quijote est **massivement** dialogué à l'intérieur.
→ **Une relation plausible et testable** ✓✓ — *le sens partagé vit dans la **narration**, pas dans le **dialogue***
✓✓ — appuyée sur **quatre livres sur cinq** ✗✓, avec une exception et un indicateur grossier. *Une piste, pas un
résultat* ✓✓ : elle demande **plus de livres** (les 1905 textes sont là) et un **vrai** indicateur de dialogue (les
répliques **dans** les paragraphes).

## ⚠️ L'HYPOTHÈSE RÉCIT/DIALOGUE EST RÉFUTÉE — le signal varie de dix-sept fois (17/10, 20 h 15)

En cherchant les **auteurs présents dans les deux langues** (les traductions gardent l'auteur, pas le titre) :
**sept** apparaissent, dont **trois** paires de la même œuvre (Don Quijote, Proust, Candide). Deux mesurées :

| livre | genre | **rang médian** (16,5) | **top-5** (15,6 %) | **écart** |
|---|---|---:|---:|---:|
| **Candide** | conte (récit) | **13** | **31,2 %** ✓✓ | **+0,1161** ✓✓✓ |
| **Le Tour du monde** | aventures | **9** ✓✓ | 28,1 % ✓ | +0,0779 ✓ |
| **Alice** | dialogue | 17 ✗ | 12,5 % ✗ | +0,0087 ✗ |
| **Don Quijote** | roman (récit) | 19 ✗ | 25,0 % ✓ | +0,0068 ✗ |

**L'hypothèse est réfutée** ✗✓ : **Don Quijote** est un **récit** et fait **aussi mal qu'Alice** (+0,007 contre
+0,009) ; **Candide**, un autre récit, fait **le meilleur score du chapitre** (+0,116, 7/32 en top-1, top-5 31 %).
*Le genre n'explique rien.* **Et la taille non plus** : Candide 228 Ko (meilleur) mais Alice 179 Ko (pire).
→ **Le signal varie de DIX-SEPT FOIS** (+0,007 à +0,116) entre **quatre livres bien alignés** (Sancho 2173/2207
pour Don Quijote, 0,1-1,7 % pour les autres) — **aucune variable simple ne l'explique** : ni le genre, ni la
taille, ni l'alignement. *C'est une propriété de la PAIRE texte-traduction, pas d'une catégorie* ✓✓.
→ **Résultat utile** ✓✓ : on **ne peut pas prédire** si un livre donnera un signal — il faut le **mesurer**. Un
chapitre qui finit sur « ça dépend du livre, mesurez-le » est un chapitre honnête ✓.

## ✅ LE CONTENU SE RÉPLIQUE AUSSI — le noyau neutre n'est pas appauvri (17/10, 19 h 40)

Mesure 4 rejouée sur le modèle v2 :

| couche | contenu **anglais** | contenu **français** | **mêlé** |
|---:|---:|---:|---:|
| **1** | **87,7 %** | **86,5 %** | 93,0 % |
| **2** | **86,3 %** | **84,3 %** | 92,3 % |
| **8** | **79,4 %** | **77,5 %** | 82,7 % |

**Le noyau neutre garde le sens** ✓✓ : aux couches 1-2, où la langue est **illisible**, le contenu reste à
**87,7 / 86,5 %** — à **9 points** du meilleur (79,4 %). *C'est la réplication de la mesure 4, sur un autre
corpus* ✓✓.
**Et la colonne « mêlé » reste la plus mauvaise** (93,0 contre 87,7) : un **seul** relevé **linéaire** pour deux
langues coûte toujours (mesure 8) ; c'est le **non-linéaire** qui referme l'écart (mesures 5 et 9) ✓✓.
→ **Toutes les mesures qui reposaient sur l'ancien corpus sont rejouées** ✓✓ : la neutralité (§ 29) et le contenu
(§ 29-30). *Le chapitre ne repose plus sur un corpus périmé* ✓✓.

## ✅ LE CORPUS ENRICHI ÉLARGIT LA ZONE NEUTRE — quatrième réplication (17/10, 19 h 15)

Corpus français passé de **66 322** à **87 341** formes ; modèle bilingue réentraîné (validation **2,6504** contre
**2,6846** ✓✓ — le corpus enrichi aide aussi la langue) ; mesure de neutralité rejouée :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| **1** | **52,7 %** | 53,4 % | **le hasard** ✓✓ |
| **2** | **51,8 %** | 51,4 % | **le hasard** ✓✓ |
| **3** | **51,5 %** | 50,5 % | **le hasard** ✓✓ |
| 4 | 58,5 % | 51,2 % | ✗ |
| **5** | **51,5 %** | 50,1 % | **le hasard** ✓✓ |
| 8 | 56,2 % | 50,8 % | ✗ (la surface) |

**La neutralité tient, et elle s'élargit** ✓✓ : **quatre** couches au hasard (1, 2, 3 et **5**) contre **trois**
avec l'ancien corpus → *plus le corpus est riche, plus le noyau devient abstrait* ✓✓, ce qui est cohérent avec la
tendance du § 20 (le sens partagé vient avec les données ✓).
**Et le modèle est meilleur** (2,6504 contre 2,6846) : un corpus plus varié **améliore** la langue **et**
l'abstraction — *les deux ne s'opposent pas* ✓.
**La surface reste langue-aware** (58 % aux couches 4 et 6, 56,2 % à la dernière) — comme dans **toutes** les
mesures du chapitre : *la langue vit aux extrémités, pas au milieu* ✓✓.
→ **Quatre réplications** ✓✓ : prose (50,2 %), dim 512 (51,4 %), littérature v1 (50,1 %), littérature v2
(51,5 %) — **quatre modèles, quatre corpus, même résultat** ✓✓✓.

## ⚠️ LE CRIBLE ÉLARGI : cinq fichiers mentent sur leur langue — dont TROIS des quatre « allemands » (17/10, 18 h 45)

Crible des 1905 textes (langue **annoncée par le nom** contre langue **détectée**) :

| fichier | annoncé | **détecté** | taille |
|---|---|---|---:|
| `pg2000_en.txt` | anglais | **français** | 2173 Ko |
| `pg21053_en.txt` | anglais | **allemand** | 838 Ko |
| `metamorphosis_de.txt` | allemand | **anglais** ✗✗ | 790 Ko |
| `pride_prejudice_de.txt` | allemand | **anglais** ✗✗ | 688 Ko |
| `frankenstein_de.txt` | allemand | **anglais** ✗✗ | 332 Ko |

**Cinq fichiers se trompent de langue** (0,26 % des 1905 ✓) — peu ✓, mais assez pour ruiner une mesure ✓ (c'est ce
qui est arrivé avec Dracula).
**Et le corpus « multilingue vérifié » est le pire** ✗✗ : **trois** de ses quatre fichiers « allemands » sont
**anglais**. *Un nom de fichier n'est pas une langue, et un dossier « vérifié » n'est pas vérifié* ✓✓.
**Mon corpus français n'est pas touché** ✓✓ : il a été construit sur une **détection**, pas sur les noms — c'est
pourquoi `pg2000_en.txt` (français) y est **inclus à bon droit** ✓✓.
→ **Conséquence pratique** ✓✓ : tout corpus de ce dépôt doit être **re-vérifié par la langue détectée** avant
usage ✓ — `tools/cribler_corpus.py` fait ce contrôle, et il devrait passer sur **tout** corpus importé.

## ✅ L'INVENTAIRE DE LA MACHINE : 1905 textes, 21 français, et un second fichier mal nommé (17/10, 23 h 30)

Mon premier scan était **limité** ✗ — un scan complet de `Panini/`, `Panini/research/data/`, `Panini-Research/data/`
donne **1905 textes** (> 100 Ko, uniques), dont **21 français** ✓✓ : **Proust** (*Du Côté de Chez Swann*),
**Stendhal** (*Le rouge et le noir*), **Hugo** (*Les misérables*), **Voltaire** (*Candide*), **Baudelaire**
(*Les Fleurs du Mal*), **Chateaubriand**, **George Sand**, **Diderot**, **Montesquieu**, **Corneille**, **Verne**,
**Zola**.

**Corpus reconstruit** ✗✓ (en-têtes Gutenberg retirés) :

| | ancien | **nouveau** |
|---|---:|---:|
| textes | 18 | **21** |
| taille | 13,2 Mo | **15,7 Mo** |
| **formes** | 66 322 | **87 341** ✓✓ (+31 %) |

**Et un second fichier mal nommé** ✗✓ : `pg2000_en.txt` est un **Don Quijote en français** ✓✗. Après
`dracula_fr.txt`, c'est le deuxième — *le nom d'un fichier n'est pas sa langue, et seule la lecture le dit* ✓✓.

**Ce que cela change** ✗✓ : les mesures 12, 19 et 20 (neutralité, littérature, tendance) reposent sur l'**ancien**
corpus → elles demandent à être **refaites** sur le nouveau, plus riche de 31 %. C'est la prochaine étape, et elle
est courte (le modèle littéraire à réentraîner, vingt minutes, et trois mesures à rejouer).

## ✅ LE SIGNAL CROSS-LINGUE EST UTILISABLE — sur un livre sur deux (17/10, 23 h)

| livre | **rang médian** (hasard 16,5) | **top-5** (hasard 15,6 %) | top-1 |
|---|---:|---:|---:|
| **Le Tour du monde** ✓ | **9 / 32** ✓✓ | **28,1 %** ✓✓ | 3/32 |
| **Alice** ✗ | 17 / 32 ✗ | 12,5 % ✗ | 2/32 |

**Pour Verne, le signal est utilisable** ✓✓ : le vrai homologue tombe à un **rang médian de 9 sur 32** (contre 16,5
au hasard) et dans le **top-5 dans 28 %** des cas (contre 15,6) — *une recherche cross-lingue réelle, faible mais
fonctionnelle* ✓✓. **Pour Alice, rien** ✗ (rang 17 = le hasard ; top-5 **sous** le hasard ✓).
→ **L'utilisabilité dépend du livre** ✗✓ — et je ne sais pas pourquoi ✗. L'hypothèse la plus simple : *le sens
partagé vit dans le **récit** (Verne ✓) plutôt que dans le **dialogue** (Alice ✓)* ✓✓ — mais elle **n'est pas
testée** ✗, et deux livres ne suffisent pas ✓.
→ **C'est le premier résultat **utilisable** du chapitre, et il est **borné*** ✓✓.

## ⚠️ SUR QWEN, LA SORTIE SUIT L'AMORCE — PAS L'ADAPTATEUR (17/10, 22 h 30)

La mesure 6 avait montré qu'un LoRA de langue **commande** la sortie d'un modèle-jouet (amorce anglaise +
adaptateur français → **français**). La même expérience sur **Qwen** :

| amorce | adaptateur | **sortie** | verdict |
|---|---|---|---|
| anglais | aucun | **en 20** · fr 0 | suit l'amorce ✓ |
| **anglais** | **français** | **en 27** ✗ · fr 0 | **suit l'amorce, PAS l'adaptateur** ✗✓ |
| français | aucun | **fr 16** ✓ | suit l'amorce ✓ |
| français | français | **fr 19** ✓ | suit l'amorce ✓ |

**Le résultat du jouet ne se transfère pas** ✗✓ : sur Qwen, l'adaptateur français **ne fait pas** écrire en
français à une amorce anglaise ✗. *La « langue comme paramètre » qui **commande** la sortie est une propriété du
noyau **monolingue**, pas du multilingue* ✗✓. Et la raison est claire : Qwen est un modèle **instruct
multilingue** — son **suivi de l'amorce** est fort, et un LoRA de **0,9 %** ne peut pas le renverser ✗. Sur le
jouet, l'adaptateur **était** le seul signal de langue ✓.
→ **La conclusion juste est plus étroite** ✓✓ : le paramètre de langue **ajuste la qualité** (7,6 %) mais **ne
choisit pas la langue** quand le modèle sait déjà les deux ✗✓. *Un modèle multilingue n'a pas besoin qu'on lui
**dise** en quelle langue écrire — il lit l'amorce* ✓✓. Cohérent avec la mesure 24 (−7,6 %, peu à gagner) et la
mesure 20 (le sens partagé vient avec le modèle) : *plus le noyau est riche, moins le paramètre de langue a de
rôle* ✓ — il **rattrape** ce qui manque, il ne **dirige** pas ce qui existe ✓.

## ✅ LA LANGUE COMME PARAMÈTRE SUR UN VRAI MODÈLE — effet huit fois plus petit (17/10, 21 h 45)

LoRA (rang 8, **4,4 M** paramètres = **0,9 %** des 494 M de Qwen) entraîné sur la littérature française, taux 1e-4 :

| | perte **français** | perte **anglais** |
|---|---:|---:|
| Qwen seul | 3,0900 ✗ | **2,7238** ✓ |
| **Qwen + LoRA français** | **2,8555** ✓ (−7,6 %) | 2,8466 (+4,5 %) ✓ |

**La langue est bien un paramètre sur un vrai modèle** ✓✓ : le LoRA améliore le français de **7,6 %** et n'abîme
l'anglais que de **4,5 %** (*un paramètre de 0,9 % des poids, et les deux langues marchent* ✓✓).
**Mais l'effet est huit fois plus petit** ✗✓ (−7,6 % contre **−53 %** sur le jouet monolingue ✓) : **parce que
Qwen est déjà multilingue** ✓✓ — il n'a **pas besoin** du patch ✗. *L'adaptateur est un rattrapage pour modèle
monolingue, pas une nécessité pour un modèle multilingue* ✓✓, exactement la conclusion du § 20.
→ **Le chiffre qui manquait** ✓✓ : sur un modèle **déjà** multilingue il y a **peu à gagner** (7,6 %) ; sur un
modèle **monolingue** il y a **beaucoup à gagner** (−53 %) ✓✓. *Le paramètre de langue sert d'autant plus que le
noyau en est dépourvu* ✓✓.

**Trois pièges d'outillage de plus** ✗✓ : le premier essai a tourné **8 h de CPU en 32 min** (le modèle n'avait
jamais été déplacé sur la carte ✓✗ — *un dispositif qui n'est pas là où l'on croit* ✗✓) ; le second a échoué sur
`Expected all tensors to be on the same device` (les paramètres du LoRA sur CPU, le noyau sur `cuda:0` ✓✗ —
*deux objets qui doivent être ensemble et ne le sont pas* ✓) ; et le taux **1e-3** a **divergé** ✗ (perte 7,89,
français +26 % et anglais **+221 %** ✗✗ — *sur un 0,5 B, le taux d'un jouet est toxique* ✓✓). Trois corrections,
une mesure ✓.

## ✅ LE CRIBLE DU CORPUS : une paire cassée sur trois, dans les DEUX corpus (17/10, 20 h)

`tools/cribler_corpus.py` ✓ — trois contrôles **sans modèle** (titre de l'en-tête Gutenberg ✓, rapport de
longueur ✓, nom propre commun ✓) :

| corpus | paires | verdict |
|---|---:|---|
| `gutenberg_multilingual_verified` | 3 | **2 OK ✓ · 1 CASSÉE ✗** |
| `gutenberg_multilingual_corpus` | 2 | **1 OK ✓ · 1 CASSÉE ✗** |

**La même paire est cassée dans les deux corpus** ✗✓ : `dracula` a **85 Ko** de français pour **850 Ko** d'anglais
(rapport **0,101**) et le fichier français est **« Vocations Explained… »** ✗. *L'erreur a été copiée d'un corpus
à l'autre* — elle ne se détecte pas en comparant les corpus, seulement en **vérifiant les fichiers** ✓.
**Les autres paires sont saines** ✓✓ (Alice 179/147 et 160/147, Le Tour du monde 451/374 — rapports 1,20-1,22,
plausibles pour une traduction ✓).
**Et le crible a une limite** ✗✓ : l'extraction du **titre** ne marche que sur les en-têtes au format français ✗ —
les fichiers anglais donnent « (titre absent) », donc ce contrôle est **partiel** (il n'a pas vu Dracula ✗ ;
c'est le **rapport de longueur** qui l'a attrapé ✓✓).
→ **Pour la suite** ✓✓ : les mesures cross-lingues du § 21 sont **deux fois valides** (Verne ✓, Alice ✓) et **une
fois du bruit** (Dracula ✗). *Un crible de dix minutes a supprimé une mesure et confirmé deux autres* ✓.

## ⚠️ LE CONTRÔLE D'ALIGNEMENT — et un fichier MAL ÉTIQUETÉ dans le corpus (17/10, 19 h 30)

Le contrôle (déviation de position relative des noms propres identiques dans les deux langues) :

| livre | nom | occurrences (fr / en) | **écart** | verdict |
|---|---|---:|---:|---|
| **Le Tour du monde** | Fogg | 655 / 608 | **0,3 %** | ALIGNÉ ✓✓ |
| | Passepartout | 423 / 398 | **0,1 %** | ALIGNÉ ✓✓ |
| **Alice** | Alice | 395 / 399 | **1,7 %** | ALIGNÉ ✓✓ |
| **Dracula** | Dracula | **0** / 33 | — | ✗✗ |
| | Mina | **0** / 233 | — | ✗✗ |

**Alice et Verne sont alignés** ✓✓ (0,1 à 1,7 % ✓) → la **variation de huit fois** entre leurs signaux (+0,009 et
+0,078) **n'est PAS un défaut d'alignement** ✓✓ : elle vient du **contenu** (Alice est un dialogue, Verne un
récit ✓) ou du modèle ✓. *C'est un résultat, pas un artefact* ✓✓.
**Mais « Dracula » français n'est pas Dracula** ✗✗ : le fichier contient **« Vocations Explained: Matrimony,
Virginity… »** ✓✗ — un **autre livre** ✓, et le rapport de longueur le criait (**0,101** : 10× moins de
caractères ✓✓). La mesure du § 21 comparait donc **Dracula à un traité religieux** ✗✓ : son « +0,0334 » est du
**bruit** ✓✓.
→ **La réplication porte sur DEUX livres, pas trois** ✗✓ : Verne **+0,078** ✓✓ et Alice **+0,009** ✓. Le signe
reste **positif deux fois sur deux** ✓✓ — la réplication **tient** — mais l'amplitude varie de **huit fois**
entre deux livres **bien alignés** ✓✓.
→ **Et le corpus de Panini contient au moins une erreur d'appariement** ✗✓ : *il faut le signaler* ✓✓ — un corpus
mal étiqueté est **invisible** tant qu'on ne vérifie pas les ancres ✓✓.
**Douzième piège** ✓✓ : *vérifier l'appariement avant de mesurer l'appariement* ✓. Le contrôle a coûté dix minutes
et il a **supprimé une mesure** ✗✓ — le meilleur rapport coût/résultat possible pour un instrument ✓✓.

## ✅ LE SIGNAL CROSS-LINGUE SE RÉPLIQUE EN SIGNE — pas en amplitude (17/10, 19 h)

Trois livres avec une paire fr/en (Le Tour du monde, Alice, Dracula), même dispositif (Qwen, couche 8, 32
segments, milieu, centrés) :

| livre | retrieval (hasard 3,1 %) | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| **Le Tour du monde** | **3/32** (9,4 %) | −0,2139 | −0,2919 | **+0,0779** ✓✓ |
| **Dracula** | 0/32 ✗ | −0,1432 | −0,1766 | **+0,0334** ✓ |
| **Alice** | 2/32 (6,2 %) | −0,2839 | −0,2925 | **+0,0087** ✓ |

**Le signe est positif dans les trois livres** ✓✓ (+0,078 · +0,033 · +0,009) — *le signal se **réplique*** ✓✓, ce
n'est pas un accident d'un livre ✓.
**Mais l'amplitude varie de huit fois** ✗✓ (0,009 à 0,078) → **réel et fragile** ✓✓ ; le retrieval ne suit qu'un
livre sur trois ✓✗ : *c'est un signal, pas un alignement* ✓.
**Et la variation peut venir de l'ALIGNEMENT** ✗✓ : je n'ai vérifié les ancres que pour **Le Tour du monde** ✓ —
Alice et Dracula peuvent avoir des structures **différentes** (abrégements, découpages ✓), et le confondant du
§ 16 revient ✗✓. *La prochaine étape n'est pas une mesure de modèle, c'est un contrôle d'alignement* ✓.
→ **Ce qui reste, honnêtement** ✓✓ : la couche commune **existe** ✓✓ ; elle **garde le sens** ✓✓ ; **le même sens
dans deux langues** se retrouve **mieux que le hasard, de façon reproductible en signe** ✓✓, mais avec une
amplitude **petite et variable** ✗✓. *Une piste, pas un acquis* ✓✓ — et c'est la réponse **nuancée** qu'il faut
écrire ✓.

## ✅ LA NEUTRALITÉ SE RÉPLIQUE SUR LA LITTÉRATURE — et le signal croît avec le modèle (17/10, 18 h 45)

**Le modèle littéraire** (4,79 M ✓, 11,7 Mo mixtes ✓ — Maupassant, Dumas, Flaubert, Verne ✓, validation
**2,6846** ✓) :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| **1** | **50,1 %** | 50,2 % | **le hasard** ✓✓ |
| **2** | **52,3 %** | 50,2 % | quasi ✓✓ |
| **3** | **50,4 %** | 50,8 % | **le hasard** ✓✓ |
| 4 | 59,9 % | 50,6 % | ✗ |
| **5** | **67,7 %** | 52,1 % | ✗✗ (le pic) |

**La neutralité se réplique** ✓✓ (couches 1-3 au hasard, comme sur la prose et en dim 512 ✓) — **trois modèles,
trois corpus, même résultat** ✓✓✓. **Mais la zone neutre est plus COURTE** ✗✓ : la langue revient dès la couche
4 et culmine à **67,7 %** en couche 5 ✓✗, contre 6-7 sur la prose ✓. *Plus le texte est riche, plus tôt la langue
réapparaît* ✓ — un texte littéraire porte **plus de signal de langue** (registre, style ✓) ✓✓.

**Et le signal cross-lingue croît avec le modèle** ✓✓ — trois points, une tendance :

| modèle | taille | **écart cross-lingue** | retrieval |
|---|---:|---:|---|
| octets, prose | 2,43 M | +0,022 | 0/24 |
| octets, **littérature** | 4,79 M | **+0,034** | **2/32** ✓ |
| **Qwen2.5-0.5B** | 494 M | **+0,083** ✓✓ | **3/32** ✓ |

**Tendance monotone** ✓✓ (+0,022 → +0,034 → +0,083) : *le sens partagé n'est pas un miracle — c'est une
propriété qui s'acquiert avec la capacité et les données* ✓✓. **Et le retrieval suit** ✓ (0/24 → 2/32 → 3/32 ✓)
mais **reste loin** d'un alignement ✗✓ : même le meilleur n'atteint que **3× le hasard** ✓. *C'est un signal, pas
une traduction* ✓.
→ **Pour le projet** ✓✓ : la couche commune **n'est pas à construire** ✗ — elle **vient avec le modèle** ✓✓, et
la seule chose à **ajouter** est le **paramètre de langue** (1,33 % ✓✓) pour la **sortie** ✓. *C'est la conclusion
la plus économique du chapitre* ✓.

## ✅ SUR QWEN, LE SENS SE RETROUVE — et la structure du chapitre est CONFIRMÉE (17/10, 18 h 15)

Même dispositif (Le Tour du monde, 32 segments, milieu, états centrés), avec le **tokeniseur** de Qwen ✓ :

| couche | retrieval | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| **8** | **3/32** (9,4 %) ✓ | −0,2139 | −0,2919 | **+0,0779** ✓✓ |
| **16** | **2/32** (6,2 %) ✓ | −0,1692 | −0,2522 | **+0,0830** ✓✓ |
| 23 | 1/32 (3,1 %) ✗ | −0,6716 | −0,7011 | +0,0295 |

*(hasard 3,1 % ; rappel : le modèle en octets de 2,4 M donnait **+0,022** et 0/24)*

**Le sens se retrouve, et quatre fois mieux** ✓✓ : l'écart atteint **+0,083** aux couches moyennes (contre +0,022
pour le petit modèle ✓) et le retrieval passe de **0/24** à **3/32** (trois fois le hasard ✓).
**Et la structure du chapitre est confirmée** ✓✓✓ : l'écart est **maximal aux couches moyennes** (8 et 16 ✓) et
**s'effondre à la dernière** (23 : +0,030 ✗) → *la couche profonde est **langue-spécifique*** ✗✓ et *le **sens
partagé** vit dans les couches **intermédiaires*** ✓✓ — exactement ce que les mesures 1 à 9 disaient d'un
modèle-jouet, et cette fois sur un **vrai modèle multilingue** ✓✓.
**Mais le retrieval reste loin de 100 %** ✗ : 9,4 % pour un hasard de 3,1 % ✓ — trois fois le hasard, ce n'est pas
un alignement ✗✓. **Un signal réel mais faible** ✓✓, à répliquer ✓ (32 segments, un seul livre, un état moyen,
un seul modèle ✗).
→ **Où en est la question** ✓✓ : la couche commune **existe** ✓✓ ; elle **garde le sens** ✓✓ ; la langue est un
**paramètre de 1,33 %** qui commande la sortie ✓✓ ; et **le même sens dans deux langues se retrouve trois fois
mieux que le hasard** ✓✗ — *c'est la question qui reste ouverte* ✓.

## ✏️ L'ALIGNEMENT ÉTAIT BON — c'était l'ÉCHANTILLON qui était mauvais (17/10, 17 h 45)

La mesure précédente accusait l'**alignement** ✗. **C'était faux** ✗✓ : les deux éditions sont **remarquablement
alignées** ✓✓ — écart de position relative des noms propres :

| nom | occurrences (fr / en) | **écart** |
|---|---:|---:|
| **Aouda** | 136 / **136** ✓ | — |
| **Fogg** | 655 / 608 | **0,3 %** ✓✓ |
| **Passepartout** | 423 / 398 | **0,1 %** ✓✓ |

Le confondant était mon **échantillonnage** ✗✓ : je prenais les **400 premiers octets** de chaque segment ✓✗ —
souvent un **titre de chapitre** ou des blancs ✓✓. *L'état moyen mesurait la mise en page, pas le récit* ✗✓.

Avec un échantillonnage au **milieu** (de la prose) :

| segments | retrieval | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| 24 | 0/24 ✗ | −0,6283 | −0,6502 | **+0,0219** ✓ |
| 40 | 1/40 ✗ | −0,6058 | −0,6109 | +0,0052 ✓ |

**Le signe s'inverse** ✓✓ : les homologues sont maintenant **un peu plus** similaires (+0,022 contre −0,053 ✗) →
**il existe un signal cross-lingue réel** ✓✓ — mais **très faible** ✗, et il ne suffit pas à retrouver (le hasard ✓).
**L'explication** : un modèle **en octets de 2,4 M**, sans objectif de traduction ✗, n'a aucune raison de porter le
sens d'une langue à l'autre ✓✓. **C'est un fait du modèle, pas un défaut de la mesure** ✓.
→ **La conséquence est nette** ✓✓ : ce test a besoin d'un modèle **multilingue entraîné** — le **Qwen2.5-0.5B** du
dépôt *est* multilingue ✓✓, et il est **là** ✓. *Prochaine mesure, et elle ne demande rien à construire* ✓✓.

**Onzième piège** ✓✓ : j'ai accusé l'**alignement** alors que le coupable était mon **échantillon** ✓✓ — et
l'accusation était **mesurable** (0,1 à 0,3 % d'écart ✓). Variante de la règle : *avant d'accuser un maillon,
mesure-le* ✓.

## ⚠️ LE RETRIEVAL CROISÉ ÉCHOUE — mais le test est INVALIDE, pas les états (17/10, 17 h)

Question **forte** : le même contenu dans deux langues donne-t-il des états comparables ? Dispositif : un livre
**parallèle** (Le Tour du monde en 80 jours ✓ — le français est l'original ✓), 24 segments, retrieval croisé
(hasard 4,2 % ✓) :

| essai | retrieval | homologues | autres |
|---|---:|---:|---:|
| dernière couche | **0/24** ✗ | +0,8695 | +0,8706 |
| **centré** ✗ | 0/24 ✗ | −0,6564 | −0,6032 |
| couche 6, centré | 0/24 ✗ | −0,6714 | −0,6311 |

**Le retrieval échoue partout**, et les homologues sont **moins** similaires que les autres ✗✗.
**MAIS LE TEST EST INVALIDE** ✗✓ — et le confondant est mesurable : les deux éditions n'ont pas la même longueur
(**451 Ko** contre **375 Ko**, **20 %** d'écart ✗✗) → un découpage **proportionnel** **dérive** ✓✗ : après
quelques chapitres, les segments ne couvrent plus le même passage ✗✓. *Le test ne mesure pas le sens : il mesure
la dérive* ✓✓.
**Et le premier essai le montrait** : toutes les similarités valaient **0,87** (une direction commune dominante
✓✗) — le centrage la retire ✓ mais ne répare pas un **mauvais appariement** ✗.
→ **Conclusion honnête** : *cette mesure ne tranche rien* ✗ — et elle apprend que le maillon faible est
l'**alignement**, pas le modèle ✓✓. **Dixième chiffre déguisé de la nuit** (ici en verdict sur les états ✗✓).
→ **Le dispositif qu'il faudrait** ✓✓ : un alignement **ancré sur le contenu** — les **noms propres**
(« Phileas Fogg », « Passepartout » apparaissent aux **mêmes endroits de l'histoire** ✓✓) et les **chapitres**
(37 dans chaque édition ✓, mais la version française numérote par **titres** ✗✓). *Aligner sur les noms, puis
vérifier par les chapitres* — prochaine mesure, et elle est courte ✓.

## ✅ UN VRAI CORPUS FRANÇAIS, ET LA NEUTRALITÉ À L'ÉCHELLE (17/10, 16 h)

**Le corpus** ✓✓ : mon « corpus français » était de la prose de dépôt ✗ (4,45 Mo, 15 201 formes). Les projets
`Panini/` et `Panini-Research/` (signalés par Stéphane ✓) contenaient des textes **Gutenberg** ✓ — 66 textes,
**18 français** ✓ → **13,2 Mo**, **66 322 formes** (4,4× plus ✓✓), avec **Maupassant, Dumas, Flaubert, Verne** ✓.
*En-têtes et pieds de page Gutenberg retirés* ✗✓ — sans quoi le corpus contenait 18 fois la même licence anglaise ✓✗.

**La neutralité à l'échelle** ✓✓ (modèle bilingue **dim 512**, 9,57 M ✓) :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| **2** | **51,4 %** | 50,5 % | **le hasard** ✓✓ |
| 4 | 59,2 % | 50,5 % | ✗ |
| **6** | **51,2 %** | 50,7 % | **le hasard** ✓✓ |
| **8** | **67,9 %** | 50,3 % | ✗✗ la surface |

**Le noyau est neutre à l'échelle** ✓✓ (51,4 et 51,2 % aux couches 2 et 6, comme 50,2 % en dim 256 ✓) — **la
propriété se réplique**. **Et la surface devient PLUS langue-aware** ✗✓ : **67,9 %** au dernier étage (contre
51,0 % en dim 256) — le modèle plus large a **plus de capacité** pour porter la langue **dans la sortie** ✓✓,
ce qui **renforce** la lecture : *la langue vit à la surface, et d'autant plus que le modèle est grand* ✓✓✓.
**Et l'entrée n'est plus langue-aware** (50,8 % à la couche 0, contre 62,4 % en dim 256) : avec des embeddings
plus larges, les statistiques d'octets se **diluent** ✓✓.
→ **Les deux résultats centraux — noyau neutre ✓ et langue à la surface ✓ — tiennent quand le modèle double** ✓✓.

## ✅ LE RELEVÉ PARTAGÉ SUFFIT — 0,7 point (17/10, 20 h)

La mesure 8 disait « le relevé est teinté de la langue » (pénalité +8,7 à +19,5 ✗) — mais elle comparait un
relevé appris sur **une** langue et appliqué à **l'autre**. La mesure 9 pose l'autre question celle qui compte
pour une couche commune : un relevé appris sur **les deux** vaut-il le relevé **de chaque** langue ?

| relevé | paramètres de langue | anglais | français |
|---|---:|---:|---:|
| **partagé** (les deux ✓) | **0** ✓ | **79,1 %** | **76,5 %** |
| partagé + **rang 1** | 512 | 79,1 % | 76,5 % |
| **complet** par langue ✗ | 65 536 | **78,4 %** | **75,9 %** |

**Le relevé partagé suffit** ✓✓ : **0,7 point** d'écart avec deux relevés séparés. **Et le rang 1 ne récupère
rien** ✗ — non parce que la langue n'est pas de rang 1, mais parce qu'**il n'y a rien à corriger** ✓.
→ **L'erratum de la mesure 8 était lui-même trop fort** ✗✓ : un relevé appris sur **une** langue ne se
transfère pas ✗ (pénalité +8,7 à +19,5 ✓), mais un relevé appris sur **les deux** ne perd que **0,7 point** ✓✓.
*Deux questions différentes, mesurées séparément.*
→ **La conclusion devient la plus simple** ✓✓ : la langue ne vit **ni dans l'état** (50,2 % = hasard ✓✓)
**ni dans le relevé** (0,7 point ✓✓) — elle vit dans **l'entrée** (les octets ✗, 62,4 %) et dans **la surface de
sortie** (couches 6-7 ✓, l'adaptateur ✓✓). *Un contenu commun, une surface paramétrée* ✓✓✓.

## ✏️ LE RELEVÉ EST TEINTÉ DE LA LANGUE — erratum de la mesure 5 (17/10, 19 h 30)

La mesure 5 disait : « un seul relevé non linéaire mêlé (71,5 %) bat deux relevés linéaires par langue
(79,3 / 76,5) ✓✓ ». Elle était vraie mais **incomplète** ✗ : il fallait comparer à des relevés **de même
langue et aussi puissants** ✓. Mesure croisée (`tools/lecture_croisee.py` ✓, dernier étage ✓) :

| relevé appris sur | état **anglais** | état **français** |
|---|---|---|
| **ANGLAIS** | **76,7 / 55,9** | 82,5 / 72,2 |
| **FRANÇAIS** | 84,8 / 75,7 | **73,1 / 53,0** |

| | diagonale | croisé | **pénalité** |
|---|---:|---:|---:|
| linéaire | 74,9 % | 83,7 % | **+8,7** ✗ |
| **non linéaire** | **54,5 %** ✓✓ | 73,9 % | **+19,5** ✗✗ |

**Le relevé EST teinté de la langue** ✗✓ (pénalité **+8,7** à **+19,5**) — et **le non-linéaire l'aggrave**
✗✓ (un lecteur plus puissant se spécialise davantage : *plus de puissance, plus de langue*). Le relevé partagé
fonctionne donc, mais **il coûte 17 points** ✗.
→ **La conclusion se précise** ✓✓ : l'**état** est neutre ✓, mais le **lien état → mots** est langue-dépendant ✓
— *c'est donc dans le relevé que la langue vit* ✓, et c'est **là** que l'adaptateur agit (1,33 % ✓). « Penser
dans une langue et conclure dans une autre » **ne marche pas** avec le même relevé ✗✓ — il faut **changer de
paramètre**, ce qui coûte **5 ms** ✓✓.
**Erratum assumé** ✓ : une comparaison n'est valide que si **tous** les lecteurs sont aussi puissants ✓ —
comparer un non-linéaire à des linéaires, c'est comparer deux **familles de lecteurs**, pas deux langues ✗✓.
*Huitième chiffre déguisé de la nuit — et cette fois c'est une mesure antérieure qui était en cause.*

## ✅ LA BASCULE COÛTE 5 ms ET 530 Ko — l'idée est utilisable (17/10, 19 h)

`tools/cout_bascule.py` ✓ — médiane sur cinq essais, comparaison avec un rechargement complet ✓ :

| ce qu'on échange | taille | temps |
|---|---:|---:|
| **adaptateur** (chargement) | **530 Ko** | **4,82 ms** |
| **adaptateur** (application) | — | **0,19 ms** |
| **modèle entier** (rechargement ✗) | 9,8 Mo | **134,64 ms** |

**La bascule de langue coûte 5,0 ms et 530 Ko** ✓✓ — contre **134,6 ms et 9,8 Mo** ✗ (rapport **×27** en temps,
**×18** en mémoire ✓✓). Et **le rapport ne peut que s'améliorer** ✓ (raisonnement, pas mesure ✗) : un modèle de
7 B pèse des milliers de fois plus qu'un adaptateur ✓, qui reste petit ✓. L'adaptateur de **surface**
(32 768 poids ✓) pèserait **≈ 130 Ko** ✓✓ pour **84 % du gain** ✓.
→ ***Un noyau, N adaptateurs de quelques centaines de Ko, une bascule en millisecondes*** ✓✓ — *la langue est un
fichier, pas un modèle* ✓. C'est la réponse la plus utile du chapitre ✓.

## ✅ LA SORTIE SUIT L'ADAPTATEUR, PAS L'AMORCE (17/10, 18 h 30)

`tools/generer_par_langue.py` ✓ : deux amorces (une par langue), trois adaptateurs, 120 octets générés, et la
langue de la sortie comptée par ses **mots-outils** ✓ :

| amorce | adaptateur | sortie (mots-outils) |
|---|---|---|
| anglais | aucun | fr 0 · **en 5** |
| **anglais** | **français** | **fr 6** · en 0 ✓✓ |
| **français** | **aucun** | fr 0 · **en 13** ✗ (le noyau ignore l'amorce) |
| français | français | **fr 12** · en 0 |
| **français** | **anglais** | fr 0 · **en 7** ✓✓ |

**La sortie suit l'adaptateur, pas l'amorce** ✓✓✓ : amorce **anglaise** + adaptateur **français** → **français** ;
amorce **française** + adaptateur **anglais** → **anglais**. C'est la définition **opérationnelle** de « la langue
comme paramètre » ✓✓. Et **sans adaptateur**, le noyau écrit sa langue d'entraînement ✓ quelle que soit l'amorce
(la française donne `en 13 · fr 0` ✗✓) — *la langue est un paramètre d'entrée mais pas de sortie* ✓.
⚠️ **Ce que ce test ne dit pas** ✗ : le texte est de la **bouillie** (2,4 M en octets ✓) — la mesure porte sur
**la langue**, pas la qualité ✓.

**La chaîne complète** ✓✓ : l'entrée porte la langue (62,4 % ✗) → le noyau l'abstrait (50,2 % = hasard ✓✓) →
il garde le sens (87,8 % ✓✓) → le relevé n'est pas propre à la langue (71,5 % non linéaire ✓✓) → la langue est
un paramètre de **32 768 poids (1,33 %)** ✓✓ → qui **fait marcher** la langue (3,19 → 1,50 ✓) → et **commande
la sortie** ✓✓✓. *La couche commune existe, elle garde le sens, et la langue y est un paramètre qui commande la
sortie* ✓✓.

## ✅ LE « RELEVÉ PROPRE À LA LANGUE » ÉTAIT UN ARTEFACT DE LINÉARITÉ (17/10, 18 h)

La mesure précédente concluait que le relevé *mêlé* était toujours pire ✗ — et se demandait si c'était le
relevé ou sa **linéarité** ✗. Réponse avec un MLP **régularisé** (arrêt anticipé ✓) :

| couche | linéaire mêlé | **MLP mêlé** | gain |
|---:|---:|---:|---:|
| 2 | 92,4 % | **86,3 %** | −6,1 |
| 5 | 88,9 % | **80,5 %** | −8,4 |
| 7 | 83,4 % | **73,9 %** | −9,5 |
| **8** | 81,6 % | **71,5 %** | **−10,1** ✓✓ |

**Le non-linéaire bat le linéaire partout** ✓✓ (dix points à la couche 8) → le « relevé propre à la langue »
n'était **pas** une propriété de l'état ✗✓, c'était une limite du **lecteur** ✓✓. *Septième fois de la nuit
qu'un chiffre se déguise — cette fois en propriété d'architecture.*
**Et le résultat décisif** ✓✓✓ : à la couche 8, **un seul** relevé non linéaire **mêlé** (71,5 %) fait **mieux**
que les **deux** relevés linéaires par langue (79,3 en anglais, 76,5 en français ✓✓). *Un relevé partagé
suffit — s'il est non linéaire* ✓.
→ La chaîne est complète ✓✓ : l'entrée porte la langue ✗ → le noyau ne la porte plus ✓✓ → le noyau garde le
sens ✓✓ → la surface la fait revenir ✓ → **le relevé n'est PAS propre à la langue** ✓✓ → l'adaptateur reste
utile **pour générer** ✓ (3,19 → 1,50 de perplexité ✓), pas pour **lire** ✓✓. *Lire le sens est une chose,
produire dans une langue en est une autre* ✓.

## ✅ LE NOYAU NEUTRE PORTE LE SENS — mais le relevé reste propre à la langue (17/10)

`tools/contenu_par_couche.py` ✓ : le **contenu** (état → embedding suivant, λ par validation croisée ✓), par
couche et par langue, sur le modèle bilingue ✓ :

| couche | **anglais** | **français** | **mêlé** | la langue ? |
|---:|---:|---:|---:|---|
| **1** | **87,8 %** | **87,3 %** | **93,0 %** | **NEUTRE (50 %)** ✓✓ |
| **2** | **86,5 %** | **85,3 %** | 92,4 % | **NEUTRE (50 %)** ✓✓ |
| 6 | 82,1 % | 80,6 % | 86,0 % | la langue revient ✗ |
| 7 | 80,4 % | 78,5 % | 83,4 % | la langue revient ✗ |
| 8 | **79,3 %** | **76,5 %** | **81,6 %** | — |

**Le noyau neutre porte le sens** ✓✓ : aux couches 1-2, où la langue est **illisible**, le contenu reste à
**87,8 / 87,3 %** — à **8 points** du meilleur (79,3 % à la couche 8). *La neutralité n'est pas une perte* ✓✓.
**Mais le relevé reste propre à chaque langue** ✗✓ : la colonne « mêlé » (un seul mapping pour les deux ✓) est
**toujours pire** (93,0 contre 87,8 ✓) — les états ne sont pas séparables par la langue ✓ (mesure 1 ✓) mais
**ne se lisent pas avec le même relevé** ✗✓.
→ ***La couche commune est commune pour l'ÉTAT, pas encore pour le RELEVÉ*** ✓ — et c'est exactement là que
l'adaptateur intervient : il **fournit** ce relevé propre à la langue ✓✓, pour **1,33 %** de paramètres ✓.

**La chaîne complète, chaque maillon mesuré** ✓✓ : l'entrée porte la langue (62,4 % à la couche 0 ✗) → le
noyau ne la porte plus (50,2 % ✓✓) → le noyau garde le sens (87,8 % ✓✓) → la surface la fait revenir
(59,4 % ✓) → le relevé en a besoin (le « mêlé » est pire ✗✓) → l'adaptateur la fournit (−44,6 % pour 1,33 % ✓✓).

## ✅ OÙ BRANCHER : le dernier étage suffit, et la langue coûte **1,33 %** (17/10)

| placement | paramètres | part | perte **français** | anglais |
|---|---:|---:|---:|---:|
| aucun | — | — | **3,1953** ✗ | **1,9001** ✓ |
| **partout** (rang 8) | 131 072 | 5,12 % | **1,5046** ✓✓ | 2,9139 |
| **dernier étage** (rang 8) | **32 768** | **1,33 %** | **1,7714** ✓✓ | 2,7439 |
| **dernier étage** (rang 32) | 131 072 | 5,12 % | **1,6820** ✓ | 2,7347 |

**Le dernier étage prend 84 % du gain avec 1,33 % des paramètres** ✓✓ (−44,6 % contre −52,9 % pour 5× plus ✓).
*La langue est essentiellement un réglage de surface* ✓✓. **Mais à budget égal, « partout » reste un peu
meilleur** ✓ (1,5046 contre 1,6820) : le noyau contribue de quelques points, au prix de **quatre fois** les
paramètres ✗✓. **Et le placement de surface abîme moins l'autre langue** ✓ (2,74 contre 2,91).

**Les trois mesures ensemble** ✓✓ : (1) la **couche commune existe** (noyau neutre, 50,2 % = le hasard ✓) ;
(2) la **langue est un paramètre** (131 k, deux adaptateurs interchangeables ✓✓) ; (3) et ce paramètre est
**plus petit qu'on ne croyait** — **32 k = 1,33 %**, au dernier étage ✓✓. *Un noyau, et un petit module par
langue* : l'idée est directement utilisable ✓.

## ✅ LA LANGUE EST UN PARAMÈTRE — deux adaptateurs de 131 k sur un noyau gelé (17/10)

`tools/adaptateur_langue.py` ✓ : LoRA rang 8 sur les 28 projections = **131 072 paramètres** (**5,1 %** d'un
modèle de 2,43 M ✓), **noyau entièrement gelé** ✓, entraîné sur **une** langue ✓, évalué sur **deux** ✓ :

| adaptateur | perte **français** | perte **anglais** |
|---|---:|---:|
| aucun | **3,19** ✗ | **1,90** ✓ |
| **français** (131 k) | **1,50** ✓✓ (−53 %) | 2,91 ✗ |
| **anglais** (131 k) | 3,02 | **1,40** ✓✓ (−26 %) |

**Chaque adaptateur fait marcher sa langue** ✓✓ (−53 % et −26 %) **sans toucher un seul poids du noyau** ✓, et
**ils sont interchangeables** ✓✓ : le même noyau, deux adaptateurs, deux langues qui marchent — *c'est la
définition de « la langue comme paramètre »*, et c'est **mesuré**.
**Le prix est asymétrique** ✗✓ : l'adaptateur français abîme l'anglais (1,90 → 2,91 ✗) alors que l'anglais
laisse le français à 3,02 ✓ — parce que le noyau a été entraîné **en anglais** : l'adaptateur anglais reste
près de lui, le français doit le déplacer ✓.
→ **Réponse à la question** ✓✓ : pour une couche commune, il n'est **pas nécessaire de réentraîner** un noyau ✗
— quelques dizaines de milliers de poids suffisent ✓✓. Reste à **choisir où brancher** l'adaptateur (couches
6-7, où la langue reparaît ✓).

## ✅ LA COUCHE COMMUNE EXISTE DÉJÀ — et la langue n'est qu'à la SURFACE (17/10)

Modèle **en octets** (8 couches, 4,79 M) entraîné sur un corpus **mixte** de **10,2 Mo** (6,0 anglais + 4,5
français ✓), puis un classifieur **linéaire** de langue sur l'état **par couche** ✓ (`tools/langue_dans_etat.py`),
avec un **témoin intra-langue** ✗ (deux moitiés de l'anglais : ce qu'on peut faire **sans** la langue ✓) :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| 0 | **62,4 %** | 53,1 | la langue est dans l'**entrée** ✗ |
| **1** | **50,2 %** | 50,7 | **le hasard** ✓✓ |
| **2** | **50,3 %** | 51,8 | **le hasard** ✓✓ |
| 4-5 | 53,8-53,9 % | ~50 | presque le hasard ✓ |
| **6** | **59,4 %** | 50,1 | la langue **revient** ✗ (surface) |
| **7** | **59,6 %** | 50,7 | la langue **revient** ✗ (surface) |
| 8 | **51,0 %** | 50,9 | le hasard ✓ (prêt pour la tête) |

**Le noyau est neutre** ✓✓ (couches 1-2 au **hasard** : l'état ne sait pas dans quelle langue le texte est
écrit ✓) **et la langue ne revient qu'à la surface** ✗✓ (couches 6-7, ~59 % ✓) — c'est **exactement** la
structure demandée : *un contenu neutre, une surface paramétrée par la langue* ✓✓✓.
**Et l'entrée porte la langue** (62,4 % à la couche 0 ✓) : les octets anglais et français n'ont pas les mêmes
statistiques ✓ — seul endroit où « la langue » est dans les données ✓.

*Deux pièges traversés, et écrits* : le **corpus français** n'existait pas ✗ (constitué depuis le français
réel du dépôt ✓, et **filtré** — sans quoi ses mots les plus fréquents étaient `stephane`, `home`, `bash` ✗✓) ;
et le **signe** d'un classifieur linéaire est **arbitraire** ✗✓ (43,4 % = **56,6 %** avec l'autre orientation ✓)
— **sixième** chiffre déguisé de la nuit, et la même règle l'a démasqué ✓.

## ✅ LE PRIX DE LA PLANÉITÉ, ET LA RÉPONSE AU § 19

Il manquait le **non-récursif** à la taille du récursif ✓ — entraîné (96 Mo, 15 000 pas ✓) et tout mesuré au
**lecteur régularisé** ✓ :

| modèle | validation | **contenu t=1** | **prix de la planéité** |
|---|---:|---:|---:|
| **s256** — sans récurrence | 2,8911 | **81,9** ✓ | — |
| **d256** — avec récurrence | **2,8183** ✓ | 85,1 | **+3,2** |
| **s512** — sans récurrence | 2,7632 | **83,4** ✓ | — |
| **d512** — avec récurrence | **2,7297** ✓ | 85,8 | **+2,4** |

**Le prix de la planéité diminue avec la capacité** ✓✓ : **+3,2** points à 2,43 M, **+2,4** à 9,57 M (−25 %
pour **4×** de paramètres ✗✓) → la réponse au § 19 est **oui, mais lentement** ✓ : un point fixe plus large est
un peu plus lisible, et le prix baisse — sans disparaître ✗ (à ce rythme il faudrait ~40× la capacité, ce qui
n'est pas la bonne voie ✗).
**Et la récurrence AMÉLIORE la langue** ✓✓ : 2,8183 contre 2,8911 · 2,7297 contre 2,7632 — le **bloc partagé
régularise** ✓ : *le modèle qui pense est aussi un meilleur lecteur* ✓✓. C'est le résultat le plus encourageant
de la nuit pour la suite ✓.

**La nuit répond en trois lignes** ✓✓ : (1) **l'état porte le sens** (80,3 % à 16 jetons, 38 points devant le
mot ✓ ; empreinte 49,3 contre 76,9, trois exécutions ✓) ; (2) **l'itération s'obtient et se paie** (plate ✓
contre +3,2 / +2,4 points de lisibilité ✗ — et le prix **baisse** avec la capacité ✓) ; (3) **la récurrence
n'est pas qu'un coût** — elle améliore le modèle de langue ✓✓. *C'est sur cette phrase que la nuit se
termine* ✓.

## ✅ LA PASSE DU 17/10 À 00 h 55 : 46 portes, **44 vertes, 2 rouges**, 97 min

**La première passe dont le verdict se lit au REGISTRE** ✓✓ (le correctif de la nuit : chaque porte écrit son
**code de sortie** ✓ et la synthèse y est ajoutée ✓). Le compte ne dépend donc plus des **marqueurs** des
journaux ✗✓ — la méthode que l'audit du 16/10 avait montrée **non fiable** ✗.

* **46 portes · 44 vertes · 2 rouges** ✓ — et les **deux rouges sont les structurels connus**
  (`porte-indice` ✓, `porte-melange` ✓), exactement ceux de la veille ✓ : **aucun rouge nouveau** après une
  nuit où **sept outils** et **trois documents** ont été édités ✓✓ ;
* **97 min** ✓ (contre 88 la veille ✓ — même ordre ✓) ;
* **et la méthode de lecture a changé** ✓✓ : `awk '$2 != 0'` sur le registre ✓ au lieu d'un `grep` de
  marqueurs ✗ — *une passe qui écrit ses codes de sortie est une passe qu'on peut vérifier ; une passe qui
  n'écrit que ses journaux est une passe qu'on doit croire* ✓.

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
