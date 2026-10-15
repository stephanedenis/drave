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
* **une seule paire brouillon/cible** (8 couches contre 24, même modèle) : d'autres profondeurs, un
  brouillon d'une autre famille, ou un Eagle3 (qui s'attache aux états cachés de sa cible) ne sont
  pas mesurés ;
* **rien sur l'échantillonnage** (`--temp > 0`) : le décodage spéculatif échantillonné (avec
  correction) est un autre algorithme, et il n'est pas ici.
