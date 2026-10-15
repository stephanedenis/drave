# Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %)

> Campagne : **cerveau** · expérience : **M5** (décodage spéculatif) — mesuré **avec le réflexe
> entraîné du dépôt**, pas avec un modèle HuggingFace (`tools/speculatif.py`, 8 oct, faisait cela
> avant qu'un réflexe existe).
> Question : à quoi sert un réflexe qui **se trompe** ? Réponse : à **proposer**. Le réflexe propose
> K jetons, le cerveau en **vérifie** K **en une passe**, garde le préfixe ratifié et corrige le
> premier jeton faux. La seule quantité qui décide est le **taux d'acceptation** — et c'est aussi la
> mesure la plus honnête de l'accord réflexe/cerveau : **aucune sonde, aucune cible**, juste deux
> générations gourmandes comparées jeton à jeton.
> Verdict : **le mécanisme marche, le taux ne paie pas encore.** Avec le réflexe **distillé** (E5),
> l'acceptation va de **2,4 % à 30 %** selon l'invite à K = 4 (**75 %** à K = 1 sur une invite), et
> les jetons par vérification de **1,00 à 2,00**. Avec le **lecteur non entraîné** (tête empruntée,
> 8 couches), l'acceptation est de **0 % partout** (0 sur 22 propositions, trois invites) — et
> c'est exactement ce que E5 annonçait (0,0 % d'accord). **Le gain net reste sous 1** : à 0,33× le
> coût de la cible par pas, il faut ~3 jetons ratifiés par passe pour rentrer dans ses frais, et le
> meilleur cas mesuré en donne **2,00**.
> Date réelle : **2026-10-15 04 h 05-04 h 30 HAE** (heure lue sur la machine)
> Protocole : `tools/speculatif_drave.py` (nouveau) · le brouillon et le vérificateur sont **le même
> moteur** `drave` (le brouillon : `--couches 0:8 --tete-partielle`, avec ou sans
> `--adaptateur-sortie`) · invite tokenisée **une fois** par le moteur, puis **tout en
> identifiants** (`--ids-file`) — un aller-retour texte → jetons → texte ne redonne pas la même
> suite · `--temp 0` (gourmand) des deux côtés · K = 1 et K = 4 · 12 à 16 jetons par bras.

## 1. Les taux

| brouillon (réflexe 8/24 couches) | invite | K | propositions | ratifiées | **taux** | jetons / vérification |
|---|---|---:|---:|---:|---:|---:|
| **tête empruntée** (non entraînée) | « Le ciel est bleu parce que » | 1 | 6 | **0** | **0,0 %** | 1,00 |
| **tête empruntée** | « The history of the city » | 1 | 6 | **0** | **0,0 %** | 1,00 |
| **tête empruntée** | « La mémoire est » | 1 | 6 | **0** | **0,0 %** | 1,00 |
| **distillée** (E5, KL) | « Le ciel est bleu parce que » | 1 | 6 | 0 | 0,0 % | 1,00 |
| **distillée** | **« The history of the city »** | 1 | 4 | **3** | **75,0 %** | 1,50 |
| **distillée** | « La mémoire est » | 1 | 6 | 0 | 0,0 % | 1,00 |
| **distillée** | « The history of the city begins » | 4 | 20 | 6 | **30,0 %** | **2,00** |
| **distillée** | « The first world war was » | 4 | 24 | 5 | **20,8 %** | 1,71 |
| **distillée** | « In the year 1892 the » | 4 | 42 | 1 | **2,4 %** | 1,00 |

Ce que ça dit :

* **le mécanisme fonctionne de bout en bout** : le moteur génère, le pilote compare, le préfixe
  ratifié est gardé, la correction est le jeton du cerveau — et la suite produite est **exactement**
  celle du cerveau seul (c'est la garantie du décodage spéculatif, et elle est vérifiée de fait :
  la trajectoire du vérificateur dans le pilote est celle de la génération normale) ;
* **le réflexe distillé est RATIFIÉ, la tête empruntée jamais** : 0 sur 22 propositions pour la tête
  non entraînée (trois invites), contre 2,4 à 30 % pour le distillé — c'est la **confirmation en
  boucle** de ce que E5 mesurait par sonde (0,0 % contre 51,0 % d'accord par position), **sans
  aucune sonde** ;
* **le taux dépend énormément de l'invite** : 75 % à K = 1 sur une invite anglaise, **0 %** sur les
  trois invites **françaises** — le réflexe distillé a été entraîné sur **wikitext2** (anglais), et
  une invite hors de son domaine ne lui laisse aucune chance. C'est une propriété du **réflexe**,
  pas du mécanisme ;
* **et le gain net reste sous 1** : la formule du pilote du 8 octobre
  (`(acceptés + 1) / (1 + K·c)`, `c` = coût du brouillon rapporté à la cible ≈ 0,33 pour 8 couches
  sur 24) donne **0,95** au meilleur cas mesuré (K = 4, 30 %), **0,89** à 20,8 %, **0,43** à 2,4 %.
  Autrement dit : **à ce degré d'accord, le décodage spéculatif coûte plus qu'il ne rapporte** — et
  c'est un chiffre, pas une opinion.

## 2. Ce que ça change pour le cerveau

* **le réflexe a une place, et elle est nommée** : il n'écrit pas le texte (il se trompe), il ne
  remplace pas le cerveau (il ne l'imite pas assez) — mais il **propose**, et le cerveau **corrige
  pour le prix d'une passe**. C'est l'architecture des deux systèmes, et elle est maintenant
  **exécutable dans ce dépôt** (`tools/speculatif_drave.py`), avec ses chiffres ;
* **la condition pour que ça paie est chiffrée** : il faut **≥ 3 jetons ratifiés par passe** à
  K = 4 pour c ≈ 0,33. Le meilleur cas mesuré en donne 2,00 — **il manque un facteur 1,5**, et il
  est atteignable par deux chemins mesurés ailleurs : un **réflexe entraîné sur plus de données**
  (le forward-only gagne ÷1,47) ou une **distillation plus fidèle** (T = 2 à 4, ou KL + λ·CE avec
  le pas d'apprentissage réajusté — la piste ouverte de E5) ;
* **et le contraste français/anglais est un avertissement** : un réflexe est **spécialisé par son
  sommeil**. Un cerveau qui veut un réflexe utile doit **dormir sur ce qu'il va rencontrer** — ce
  que la fiche du sommeil disait déjà par un autre bout (« ce qui se consolide est la structure
  partagée ») ;
* **ce qui reste ouvert pour M5** : la version **moteur** (un vrai décodage spéculatif par lots,
  qui amortit le coût du brouillon au lieu de relancer le processus) n'est **pas** écrite — c'est la
  porte de M5, et elle a maintenant sa spécification mesurée : **taux d'acceptation ≥ 3/4 à K = 4**,
  sans quoi la porte doit rester rouge.

## 2bis. La PORTE (44ᵉ) : l'invariant est vérifié, pas espéré

`tools/porte-speculatif.sh` exécute le mécanisme et vérifie ce qui doit être vrai **à chaque fois** :

| vérification | ce qui est exigé | ce qui a été rendu |
|---|---|---|
| **1. l'invariant** | la suite du pilote est **identique, jeton pour jeton**, à celle du cerveau seul | ✅ **8 jetons identiques** (`[512, 13309, 321, 1788, 12422, 84, 13, 356]` des deux côtés) |
| **2. le taux est rendu** | un taux dans [0, 1] et ≥ 1 jeton par vérification | ✅ 0,0 % et 1,00 (brouillon non entraîné) |
| **3. le témoin** | la tête **non entraînée** n'est **jamais** ratifiée | ✅ 0 sur 20 propositions |
| **4. le réflexe entraîné** *(conditionnel)* | s'il est présent, il doit être ratifié **au moins une fois** | ✅ **30,0 %** (6/20), 2,00 jetons par vérification |
| **5. un brouillon invalide** | échoue **en le disant**, sans rendre de suite | ✅ (chemin inexistant ⇒ échec avec message) |

* **l'invariant est la propriété qui rend le mécanisme acceptable** : un brouillon qui se trompe
  **ne peut pas** faire dériver la sortie — le vérificateur corrige, et la porte le **vérifie** au
  lieu de l'espérer. C'est ce qui distingue ce mécanisme de tout ce que la nuit a mesuré de
  négatif (le cycle, la récurrence, l'échange d'activations : eux **changent** la sortie, et ils
  n'apportent rien) ;
* **la vérification 4 est conditionnelle, et c'est dit** : le réflexe distillé vient d'un
  entraînement **hors porte** (10 min de GPU) ; si le fichier n'est pas là, la porte **le dit** au
  lieu de juger (le précédent du dépôt : `--banc-vision` annonce « pas de `v.patch_embd.weight` ») ;
* **et la porte est rapide** (~1 min) : elle ne mesure ni la qualité ni le temps, seulement ce qui
  doit être **exact**.

## 2ter. Deux tentatives pour combler le facteur 1,5 — deux échecs, et c'est écrit

Le § 2 nommait les deux chemins possibles (« une distillation plus fidèle »). Les deux ont été
essayés le soir même, à la même mesure (**l'accord par position avec le maître**, sur m32 et m20) :

| distillation (8 couches + lecteur + LoRA) | accord m32 | accord m20 | verdict |
|---|---:|---:|---|
| **E5** : T = 1, rang 8, 30 morceaux, 20 époques | **51,0 %** | **68,1 %** | la référence |
| **T = 2** (rang 8 puis rang 4, pas 1e-3 puis 3e-4) | 22,1 % | 30,6 % | **pire**, et l'entraînement **diverge** (validation 13 995 → 2 032) |
| **T = 4** | — | — | **diverge** (validation 72 017) |
| **rang 4**, 26 morceaux (le levier qui gagne en perplexité) | 47,3 % | 60,7 % | **légèrement pire** |

* **la température, qui est la recette classique de la distillation, NUIT ici** : à T = 2 l'accord
  tombe de 51,0 % à 22,1 % (et à T = 4 l'entraînement explose). Deux hypothèses, aucune instruite :
  (a) l'échelle du gradient de la KL change avec T alors que le pas reste celui du balayage en
  perplexité ; (b) l'étudiant **tronqué** (8 couches sur 24) ne peut pas atteindre la distribution
  aplatie d'un maître de 24 couches, et l'aplatissement ne fait qu'éloigner la cible ;
* **le rang 4, qui gagne 2,35 points en perplexité, perd ici 3,7 points d'accord** : les deux
  objectifs n'ont pas le même optimum de capacité — **ce qui rend « bon petit modèle » ne rend pas
  « bon imitateur »**, et c'est la seconde fois que la nuit le mesure (la première : l'objectif
  lui-même, § 1 de `rapport-e5-distillation.md`) ;
* **le facteur 1,5 manquant n'est donc PAS comblé** : le meilleur réflexe reste celui de E5
  (51 % d'accord, 30 % d'acceptation à K = 4). La porte de M5 garde sa spécification
  (**≥ 3/4 à K = 4**) et **reste rouge** pour la rentabilité — ce qui est un résultat, pas un oubli ;
* *(et un détail d'instrument est noté : la colonne « train (perplexité équivalente) » affiche `inf`
  dès que la KL dépasse ~709 en exponentielle — c'est un débordement d'affichage, pas une mesure ;
  la validation, elle, reste finie et c'est elle qui choisit l'époque.)*

## 2quater. La condition de rentabilité est EXACTEMENT `p > c` — et les deux brouillons sont juste dessous

Le § 2 concluait « il manque un facteur 1,5 » à partir du gain `(acceptés + 1) / (1 + K·c)`. Cette
formule se simplifie, et la simplification est le vrai résultat : avec `acceptés = p·K` (p = taux
d'acceptation),

  **gain = (p·K + 1) / (1 + K·c) > 1 ⟺ p·K > K·c ⟺ p > c**

c'est-à-dire : **le gain dépasse 1 si et seulement si le taux d'acceptation dépasse le coût du
brouillon rapporté au cerveau** — et **K disparaît**. Le décodage spéculatif ne se juge donc pas sur
la profondeur du brouillon ni sur K, mais sur **une seule inégalité**.

Deux brouillons mesurés, deux distillations, deux coûts :

| brouillon | coût relatif `c` | seuil `p > c` | taux mesuré `p` (K = 4) | gain `(pK+1)/(1+Kc)` | verdict |
|---|---:|---:|---:|---:|---|
| **8 couches** distillé (E5) | 8/24 = **0,333** | p > **33,3 %** | **30,0 %** (2,00 jetons/vérif.) | **0,94** | ✗ **juste dessous** |
| **4 couches** distillé (ce round) | 4/24 = **0,167** | p > **16,7 %** | **14,3 %** (1,50) | **0,94** | ✗ **juste dessous** |

* **les deux sont à 0,94 — le même gain, pour des coûts et des accords différents** : réduire le
  brouillon de moitié divise son coût **et** son accord, et les deux effets s'annulent exactement
  dans l'inégalité. **Ce n'est donc pas la taille du brouillon qu'il faut optimiser, c'est l'accord
  par unité de coût** ;
* **et l'écart à combler est petit et chiffré** : il faut **33,3 %** d'acceptation au lieu de 30,0 %
  (8 couches), ou **16,7 %** au lieu de 14,3 % (4 couches) — soit **+10 % en relatif** dans les deux
  cas. Deux tentatives ont échoué (§ 2ter : la température et le rang) ; la piste qui reste est
  nommée : **plus de données de distillation**, ou un brouillon **de la même famille mais plus
  proche** de la cible (un 12 couches sur 24 coûterait 0,5 et demanderait p > 50 % — mesuré nulle
  part, et c'est la prochaine mesure à faire) ;
* **la fiche du 8 octobre** (`tools/speculatif.py`, deux modèles HuggingFace) donnait la même
  formule avec `c` supposé ; ici **les deux `c` sont mesurés** (4 et 8 couches sur 24) et l'inégalité
  est **testée** — la question de M5 n'est plus « est-ce que ça paie ? » mais « de combien manque
  l'accord ? », et la réponse est **10 %**.

## 3. Ce que cette fiche ne dit pas

* **trois invites (dont deux à K = 1) et 12 à 16 jetons** : les taux sont des points, pas des
  moyennes ; le taux « vraie » demanderait des dizaines d'invites et des centaines de jetons — la
  tendance (0 % non entraîné, 2-30 % distillé, dépendance forte à l'invite) est solide, les valeurs
  ne le sont pas ;
* **le temps est brut et non comparable** : le pilote **relance le moteur à chaque tour** (chargement
  du modèle inclus, ~1 s) ; les 36 à 104 s mesurés ne disent **rien** d'un décodage spéculatif
  implémenté dans le moteur — et c'est écrit dans l'en-tête du script ;
* **la vérification n'est pas par lots** : le cerveau régénère K jetons **séquentiellement**
  (`--n K`) au lieu d'une passe en parallèle sur les K positions ; le taux d'acceptation est le
  même, le **gain de temps** non (et il n'est donc pas mesuré) ;
* **deux profondeurs** (4 et 8 couches sur 24, même modèle) : la **12 couches** manque, et c'est
  précisément celle qui départagerait « p > c » d'une autre loi (elle demanderait p > 50 %) ; un
  brouillon d'une autre famille, ou un Eagle3 (qui s'attache aux états cachés de sa cible), ne sont
  pas mesurés non plus ;
* **rien sur l'échantillonnage** (`--temp > 0`) : le décodage spéculatif échantillonné (avec
  correction) est un autre algorithme, et il n'est pas ici.
