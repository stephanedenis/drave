# Le cerveau Drave, faculté par faculté — et le modèle le plus efficient pour chacune

> **2026-10-14, 22 h 00 HAE** (heure lue sur la machine). Ce document est une **carte**, pas un
> plan : pour chaque faculté d'un cerveau, **le mécanisme que Drave emploie aujourd'hui**, **le
> chiffre qui le prouve**, et **son coût** — parce que « le plus efficient » veut dire : *à
> qualité donnée, le moins de paires, d'octets et de temps*. Ce qui n'est pas mesuré est écrit
> comme non mesuré, et ce qui manque est écrit comme un manque.
>
> Ce document ne remplace pas les autres : `docs/plan-cerveau-complet.md` porte les **douze
> capacités** (C1-C12), `docs/etat-cerveau.md` leur **état**, `docs/biologie-pour-drave.md` les
> expériences **E1-E9**, `docs/manques.md` ce qui **manque** (M1-M9, N1-N5). Ici, l'entrée est la
> **faculté**, pas la capacité : c'est la question « un cerveau, avec quoi ? ».

## 0. La carte en une table

| faculté | le mécanisme le plus efficient | le chiffre | coût | état |
|---|---|---|---|---|
| **perception** (entrées) | région frontière `--entree signal:F`, canal, gain, jeton | entrée constante ⇒ sortie constante, **au bit près** | **0 paire** | ✅ (texte et signal) |
| **réflexes** | chemin court **entraîné** (LoRA couches basses + lecteur de sortie) | **÷1,47** (m32) et **÷1,24** (m20) à 8 couches, lus par le moteur | 0,07 % des poids (rang 8) · **0,035 %** au point efficient (rang 4) | ✅ |
| **attention sélective** | **fenêtre + puits** (moitié des clés), et une **politique par texte** quand la sensibilité est mesurable | le coût de la moitié va de **+0,04 % à +7,39 %** selon le texte (**×180**) ⇒ un budget uniforme **casse** la tolérance de +1 % sur **5 textes sur 8** ; la politique par texte la tient partout pour **−14,1 % de clés** | clés ÷2, paires ÷2 | ✅ |
| **mémoire de travail** | **tampon exact** `--memoire K` — et le réseau **ne l'apprend pas** (R² −1,09 → **−2,77** entraîné) | R² **1,000**, erreur nulle, poursuite de `v[t−8]` ; avec le tampon en entrée, le modèle gelé lit **+0,879** et l'entraîné **+0,964** | **0 paire de plus** | ✅ |
| **mémoire épisodique** | magasin adressable par contenu (hachage/LSH) | élagué **83 %**, rappel **96,3 %** à 50 % de dégradation, round-trip **exact** | **11 jetons sur 2 048** | ✅ |
| **consolidation** (sommeil) | rejeu → LoRA rang 8 sur 8 couches — **ce qui se consolide est la structure PARTAGÉE** (au niveau du CORPUS : un lot homogène dans un corpus hétérogène ne transfère pas mieux) | **−16,4 %** en domaine ; **+1,3 %** hors domaine ; courbe −5,6 % (3) → **−10,0 %** (20) ; et sur un corpus **hétérogène**, mémorisation **−22,5 %** mais transfert **+1,2 %** | **0,035 %** des poids (rang 4, optimum mesuré), 10 époques | ✅ |
| **adaptation / habituation** | **RIEN** — le réseau calcule la différence lui-même | à retard 1, le changement `v[t]−v[t−1]` est lisible à **+0,921** avec le tampon **brut** ; le gain **négatif** (soustraire le passé) le **dégrade** à +0,817 (et la valeur avec) | 0 | ✅ (résultat négatif : la fenêtre suffit) |
| **modulation / arousal** | bus multi-canaux, **et une décision par texte** (métacognition : « ce texte supporte-t-il la moitié des clés ? ») | canal neutre ⇒ empreintes **identiques** ; aucun signal **scalaire** n'améliore ; mais la politique **par texte** tient la qualité pour **−14,1 % de clés** | ~0 | 🟡 mécanique faite, signal scalaire non trouvé — **la décision par contenu, si** |
| **inhibition / E-I** | gain par couche (côté amplification) | gain 0,75 ⇒ **−11,5 %** ; l'**inhibition dégrade** ; le ratio cortical de signes coûte **+4,9 à +10,8 %** à l'entraînement | 0 | ✅ |
| **latéralité / corps calleux** | deux jumeaux (échange **exact**, gain **nul**) — **et la FUSION de deux expériences** (`W + ΔA + ΔB`) | la somme **conserve le gain du spécialiste fort** (−7,3 % contre −7,4 %) et **accumule les coûts** (+1,2 % sur l'autre corpus) : pas d'interférence destructrice | ÷2 de calcul | ✅ (échange : négatif ; fusion : positive) |
| **timing / conduction** | délai par lien (`delai_ms`) | 50 ms × 64 pas = **+3,1 s**, perplexité **inchangée** | loi **3,4 ms/token par ms** | ✅ |
| **horloges / asynchronie** | pas par région, `--pas-max` borné | un pas de retard coûte **×633** ⇒ on **ne réutilise jamais** un état ; gigue 40 % (local), 49 % (5 ms) | — | 🟡 premier pas |
| **cycles (boucles cortico-thalamiques)** | graphe récurrent déroulé, `recurrent` + délai — **entraîné**, il dompte la divergence | pas 1 **exact** (14,6496), puis **divergence** 275,52 → **2 988,46** ; entraîné : 18,40 → 22,61 → 32,56 → **52,24** (**×228** au pas 4) mais **jamais mieux qu'une passe** | **N pas × régions** exécutions (4 pas = 4 passes) | ✅ (capacité) / ❌ (utilité : la boucle coûte 4× et perd) |
| **budget / câblage minimisé** | budgets **octets, latence, paires** par lien | trois refus distincts : codes **6**, **8**, **9** | — | ✅ |
| **plasticité structurelle** | croissance locale des connexions | 8,1550 (croissance) contre 8,1827 (masque statique à densité égale) : **+0,3 %**, dans le bruit | — | 🟡 |
| **apprentissage local (Hebb)** | 5 variantes mesurées | la meilleure est **ne rien faire** (négatif) | — | ❌ |
| **langage / décodage** | le modèle + **le réflexe qui PROPOSE, le cerveau qui VÉRIFIE** (`tools/speculatif_drave.py`) | réflexe : **×2,0** de débit, TTFT **÷3,1** ; **taux d'acceptation 2,4 à 30 %** (K = 4) et **75 %** (K = 1) pour le distillé, **0 %** pour la tête non entraînée ; gain net **0,95** au mieux — **sous 1** | — | 🟡 (mécanisme exécutable, rentabilité non atteinte : il manque ~×1,5) |
| **motricité / effecteurs** | `--sortie F` + réflexes ; le moteur **écrit** ce que le réflexe produit | le signal **courant** est dans la sortie (R² 0,992) ; le réflexe distillé génère **×2,0** plus vite mais **différemment** du cerveau | 357,8 M paires/décision (complet) | 🟡 |
| **observabilité** | trace globale (`--trace-globale`) | **126 croisements**, aucune divergence ; 1 bit changé ⇒ **DIVERGENT** (code 3) | — | ✅ |
| **robustesse aux pannes** | registre de régions, refus nommés | panne de lien : **code 7**, jamais de résultat partiel | — | ✅ |

**Lecture** : neuf facultés sont **faites et chiffrées**, six sont **partielles** (le mécanisme
existe, la valeur n'est pas trouvée), une est un **résultat négatif** (la règle locale), et une
seule — la **consolidation dans le moteur** — dépend encore d'un outil hors moteur (torch).

## 1. Les trois mémoires, et laquelle choisir

Un cerveau a au moins trois mémoires, et Drave les a **toutes les trois**, avec des coûts très
différents — c'est le choix de conception le plus net de la carte :

| mémoire | ce qu'elle retient | mécanisme | coût | ce qu'elle ne fait pas |
|---|---|---|---|---|
| **de travail** (quelques pas) | les K derniers pas d'un signal | **tampon exact** (`--memoire K`), lu directement | **0 paire** | ne généralise pas : elle rend ce qui est entré |
| **épisodique** (la journée) | des épisodes entiers, adressables par contenu | magasin clé/valeur, hachage/LSH, écriture en **une passe** | 11 jetons sur 2 048 lus | **n'écrit rien dans les poids** — donc n'apprend pas |
| **sémantique** (les poids) | ce qui se répète | **consolidation** : rejeu → LoRA → poids | **0,035 %** des poids au point efficient (rang 4, pas 1e-3 : −7,92 % ; rang 2 : 0,018 % pour −7,06 % ; rang 32, huit fois plus gros : −5,01 %) | **spécialise** : +1,3 % hors domaine |

**Le classement d'efficience est net** : à court terme, un **tampon** bat tout (R² 1,000 pour
zéro paire) ; à moyen terme, un **magasin épisodique** bat la consolidation (aucun oubli, coût
local) ; à long terme, seule la **consolidation** met l'expérience dans les poids — et elle se
paie en généralité. La récurrence, elle, **ne retient pas** : mesurée deux fois (locale :
R² 0,906 → 0,112 ; et le cycle : divergence), elle **amplifie**.

## 1bis. La perception VISUELLE : une tranche sur six, et elle est BLOQUÉE par un modèle absent

La vision n'est pas un oubli : c'est une tranche **vérifiée** et cinq qui manquent — et depuis le
15/10, un **empêchement mesuré**. État exact, tel que le plan (`docs/plan-mla-vision.md` § « détail
de la première tranche ») et la machine le donnent :

| tranche | état |
|---|---|
| **embedding de patchs** (`--banc-vision`, convolution 14 × 14 sur une image 28 × 28) | ✅ **vérifiée** contre la référence numpy (`tools/vision_ref.py`) : écart max **5,4e-7** — le bruit de virgule flottante |
| rotation 2-D des patchs (mRoPE) · 32 couches à attention locale une sur huit · norme finale · projecteur `mm.0`/`mm.2` · **injection des embeddings d'image dans le flux de jetons** | ❌ (l'injection est **le point d'architecture** qui manque au moteur) |
| **le modèle de vision** | ✅ **PRÉSENT depuis le 15/10 09 h** : `models/vision/Qwen2-VL-2B-Instruct-Q4_K_M.gguf` (986 Mo) **et** son `mmproj` (710 Mo, 520 tenseurs — c'est lui qui porte `v.patch_embd.weight` et **toute la tour**) |
| **la tour entière, vérifiée EN ISOLATION** | ✅ **écart max 7,58e-06 sur les 31 couches** (`tools/vision_isole.py` : même état d'entrée aux deux implémentations, comparaison de la couche seule — la seule méthode qui survive à l'effondrement de l'attention). Référence numpy écrite d'après les mêmes hypothèses ✗, référence `transformers` indépendante ✓ |
| **la tour entière** (MLP, rotation 2-D, `v.post_ln`, projecteur, injection) | ✅ **ELLE TOURNE, ET ELLE EST VÉRIFIÉE** : `--banc-vision` déroule les 32 couches et le projecteur ; la comparaison à `transformers` donne **862,9 contre 116 651,3** — mais **la référence explose elle-même à sa dernière couche** (×71,7, deux normalisations d'entrée essayées), donc l'écart n'est **pas attribuable**. **Cinq** corrections d'architecture ont été faites — MLP à deux matrices + quick-GELU, fenêtre locale **conditionnelle** (Qwen2-VL n'en a pas), écriture des jetons d'image, **les biais des LayerNorm, ignorés** (couche 0 : cosinus **−0,50 → +0,69**), et **la convention de rotation 2-D**, lue dans la source (`rotate_half` apparie `i` et `i + hd/2`, pas `(2i, 2i+1)`) — cosinus **+0,84** à la couche 2. **Avec le noyau réparé** (le mmproj a perdu une tranche temporelle : **0,00 %** sur l'une, absente sur l'autre — le noyau sommé se reconstruit depuis les `safetensors` et se donne au moteur par `DRAVE_VISION_NOYAU`), l'embedding de patchs devient **EXACT** (0,00 % sur 256 patchs, contre numpy ET contre la référence) et la **couche 0 atteint cosinus +0,9972** ; l'écart croît ensuite avec la profondeur (7 % → 60 % en six couches) — **signature de la quantification**, pas d'un bug de convention. Détail : le noyau de patchs du **mmproj** est **exactement la première tranche temporelle** du noyau 3-D de la référence (0,00 % d'écart), la seconde (même norme) étant **absente** — or Qwen2-VL traite une image fixe par **duplication de trame**, donc le modèle somme les deux. **Deux poids différents, pas deux codes** : la suite est un choix (reconstruire le noyau depuis les `safetensors`, ou se comparer à llama.cpp qui partage la conversion). Fiche : [`rapport-vision-qwen2vl.md`](../reports/rapport-vision-qwen2vl.md) |

**Conséquence, et elle a changé le 15/10 à 09 h** : le modèle est arrivé, la tour **tourne**, et
elle **ne concorde pas** avec la référence (facteur 135 sur la norme de sortie). La perception
visuelle est donc passée de « **bloquée par un manque de poids** » à « **mesurée, et fausse** » —
ce qui est un progrès de méthode : il y a un modèle, un banc, une référence indépendante et un écart
chiffré. Tant que l'écart tient, une éventuelle `porte-vision.sh` doit être **rouge**.
*(Ce qui suit est l'état d'avant le téléchargement, gardé pour la trace :*) La prochaine action est donc un **téléchargement** (un GGUF de vision,
p. ex. un Qwen2-VL), pas une ligne de code — et c'est exactement le genre de dépendance que le
dépôt refuse de supposer : `--banc-vision` **dit** « pas de `v.patch_embd.weight` dans ce fichier »
et rend la main au lieu d'inventer.

## 2. Ce qui manque, faculté par faculté

| faculté manquante ou partielle | ce qui l'établit | ce que ça bloque |
|---|---|---|
| **apprentissage DANS le moteur** | la boucle est rejeu (moteur) → mise à jour (**torch**) → mesure (moteur) : manque **M6** | l'adaptation en ligne, et un cerveau qui se consolide sans nous |
| **mémoire de travail du MODÈLE** | le tampon est dans le **moteur** ; le modèle ne retient pas **et ne l'apprend pas** (−2,77 après 8 époques, `rapport-memoire-travail-n5.md`) | toute tâche qui demande de retenir *dans* le réseau — sauf à lui donner la structure, qu'il sait alors **lire** (+0,964) |
| **un signal de modulation qui améliore** | cinq règles locales et cinq modulateurs mesurés ; le meilleur est **ne rien faire** | la valeur, la récompense, l'attention apprise |
| **un cycle qui serve** | le cycle est exact au pas 1 ; **entraîné**, il dompte la divergence (**×228** au pas 4, `rapport-cycle-entraine.md`) mais **dégrade encore** (~×1,4 par pas) et ne bat pas une passe | les boucles cortico-thalamiques *utiles* — la piste nommée est un objectif de **point fixe**, pas de prédiction |
| **perception visuelle (Qwen2-VL)** | le modèle et sa tour sont là ; `porte-vision.sh` entre dans la passe (refus, formes, tour mesurée) ; **la tour n'est pas vérifiée** (écart 55 à 79 % contre la référence, trois suspects nommés) | toute capacité multimodale — il reste à trancher la rotation par tête, la disposition q/k/v et l'ordre du MLP |
| **perception riche (vision, audio)** | les encodeurs (`bge-m3`) sont lisibles et **inexécutables** — manque **M4** ; **la vision a une tranche vérifiée (5,4e-7) mais AUCUN modèle de vision sur la machine** (cf. § 1bis) | toute la famille multimodal — et le prochain pas est un **téléchargement**, pas du code |
| **un sommeil structuré** | la consolidation marche, mais **hors** du moteur et sans protocole de sommeil (quoi rejouer, quand s'arrêter) | un cycle veille/sommeil automatique |
| **la latéralité qui apporte** | l'échange est exact et le gain **nul** (mesuré deux fois : couches et experts) | une raison de dupliquer un hémisphère, à part la robustesse |

## 3. La règle d'efficience, en une phrase

> **Ce qui doit être retenu exactement demande une STRUCTURE (un tampon : 0 paire). Ce qui doit
> être retrouvé demande un MAGASIN (épisodique : 11 jetons sur 2 048). Ce qui doit être su
> demande des POIDS (consolidation : 0,035 % des poids au point efficient, et une perte de généralité). Et ce qui
> doit être amplifié par le temps demande un CYCLE — qui, non entraîné, diverge.**

C'est la leçon que les mesures de ce dépôt donnent, et elle est contre-intuitive là où elle
compte : on cherche naturellement la mémoire **dans** le réseau (récurrence, état récurrent), et
les trois mesures de ce dépôt disent qu'elle est **à côté** — dans un tampon, dans un magasin, ou
dans une consolidation séparée.

## 3bis. Les facultés COMPOSENT-ELLES ? (mesuré le 14/10)

Une carte ne vaut que si les facultés tiennent **ensemble**. `tools/porte-cerveau.sh` exécute
**quatre facultés dans une seule commande** (`--entree` + `--entree-memoire 3` + `--delai 2` +
`--recurrence 0,5`) et vérifie que **chacune agit encore** quand les autres sont allumées :
déterminisme au bit près, la mémoire muette ? non, le délai muet ? non, la récurrence muette ?
non — et **les quatre configurations donnent quatre sorties distinctes** (aucun drapeau inerte).
C'est la seule chose que cette porte vérifie : la **coexistence**, pas les facultés (chacune a la
sienne).

## 3ter. La BOUCLE complète, en une commande (mesurée le 15/10 à 00 h 30)

`tools/boucle-cerveau.sh` exécute **la chaîne entière** sur un texte et la mesure au moteur à chaque
maillon — c'est la démonstration que les facultés **s'enchaînent** (les cartes montrent qu'elles
existent, la porte-cerveau qu'elles **coexistent**, celle-ci qu'elles **s'enchaînent**) :

| maillon | ce qu'il fait | ce qu'il a rendu (wikitext2, Qwen2.5-0.5B) |
|---|---|---|
| **percevoir** | `--tokenize` | **85 626** jetons, texte reconstruit **identique** |
| **retenir** | `--entree-memoire 8 --recurent` | déterministe au bit près, sortie **différente** sans la mémoire |
| **se souvenir** | `--episodique-essai` | round-trip **300/300 au bit près** |
| **consolider** | 3 morceaux rejoués, 8 époques, LoRA rang 8 sur 8 couches, export, **mesure moteur** | **17,0197 → 16,3429 (−3,98 %)** sur un morceau **jamais rejoué** (jeton 20 000) |
| **agir** | `--infer` (complet contre chemin court) | le réflexe produit **16 jetons différents** — un autre agent, comme mesuré |

*(La première version mesurait la perplexité sur les **1 024 premiers jetons** — c'est-à-dire le
**premier morceau rejoué** : elle annonçait −26 % de « consolidation » qui était de la récitation.
Attrapé en relisant le script, pas par un chiffre — et corrigé par `--depuis 20000`.)*

## 3quater. Ce qu'une DÉCISION coûte : deux monnaies, et la métrique du plan n'en voit qu'une

| configuration | paires par décision | écart |
|---|---:|---:|
| complet (24 couches, toutes les clés) | **357,8 M** | — |
| chemin court **8 couches** (réflexe) | **119,3 M** | **−66,7 %** |
| 8 couches **+ fenêtre 128 + 64 puits** | 119,3 M | −66,7 % |
| **4 couches** | **59,6 M** | **−83,3 %** |

**La profondeur est le seul levier de cette table, et il est exactement linéaire en couches.** La
**fenêtre d'attention ne déplace pas les paires** (119,3 M avec toutes les clés comme avec le
quart) : la métrique compte les **projections**, pas les **scores d'attention**. Un budget de
cerveau s'exprime donc en **deux monnaies** — les paires (profondeur, largeur, experts) et les
**clés/octets** (fenêtre, puits) — et le plan n'en comptait qu'une. Détail :
[`rapport-budget-decision.md`](../reports/rapport-budget-decision.md).

## 4. Où chaque chiffre se vérifie

| faculté | fiche |
|---|---|
| réflexes, chemin court | [`rapport-n4-dessin-b.md`](../reports/rapport-n4-dessin-b.md) · [`rapport-n4-porte-execution.md`](../reports/rapport-n4-porte-execution.md) |
| consolidation, budget, sélection, structure partagée, quatre jours, **homéostasie (E9)** | [`rapport-consolidation-c7.md`](../reports/rapport-consolidation-c7.md) · [`rapport-sommeil-budget.md`](../reports/rapport-sommeil-budget.md) · [`rapport-sommeil-selection.md`](../reports/rapport-sommeil-selection.md) · [`rapport-consolidation-structure-partagee.md`](../reports/rapport-consolidation-structure-partagee.md) · [`rapport-vie-quatre-jours.md`](../reports/rapport-vie-quatre-jours.md) · [`rapport-consolidation-balayage.md`](../reports/rapport-consolidation-balayage.md) · [`rapport-e9-homeostasie.md`](../reports/rapport-e9-homeostasie.md) · `porte-homeostasie.sh` |
| cycle C2 (capacité, puis entraîné) | [`rapport-cycle-c2.md`](../reports/rapport-cycle-c2.md) · [`rapport-cycle-entraine.md`](../reports/rapport-cycle-entraine.md) |
| récurrence locale | [`rapport-c2-recurrence.md`](../reports/rapport-c2-recurrence.md) |
| mémoire de travail, périphérie | [`rapport-memoire-travail-n5.md`](../reports/rapport-memoire-travail-n5.md) · [`rapport-c8-peripherie.md`](../reports/rapport-c8-peripherie.md) · [`note-peripherie-c8.md`](note-peripherie-c8.md) |
| mémoire épisodique | fiches 24, 29, 30, 31 · `porte-episodique.sh`, `porte-indice.sh` |
| fenêtre, puits et **politique** de budget | [`rapport-fenetre-puits-attention.md`](../reports/rapport-fenetre-puits-attention.md) · [`rapport-loi-frontiere-fenetre.md`](../reports/rapport-loi-frontiere-fenetre.md) · [`rapport-budget-attention-allocation.md`](../reports/rapport-budget-attention-allocation.md) · [`rapport-politique-budget-attention.md`](../reports/rapport-politique-budget-attention.md) |
| bus de modulation | `porte-bus.sh`, `porte-bus-socket.sh` |
| E/I et gains | [`rapport-e4-ratio-signes.md`](../reports/rapport-e4-ratio-signes.md) |
| latéralité | [`rapport-c9-lateralite.md`](../reports/rapport-c9-lateralite.md) · [`rapport-c9-echange-experts.md`](../reports/rapport-c9-echange-experts.md) |
| délais, horloges, budgets | fiches 43, 44, 32, 42 · `porte-delais.sh`, `porte-horloge.sh`, `porte-budget.sh` |
| plasticité structurelle, règle locale | [`rapport-e1-e2-connectome-croissance.md`](../reports/rapport-e1-e2-connectome-croissance.md) |
| vision (Qwen2-VL, la tour et son écart) | [`rapport-vision-qwen2vl.md`](../reports/rapport-vision-qwen2vl.md) · `porte-vision.sh` (45ᵉ porte : refus · formes · tour **mesurée**, non jugée) |
| distillation (E5), et le réflexe qui propose | [`rapport-e5-distillation.md`](../reports/rapport-e5-distillation.md) · [`rapport-speculatif-reflexe.md`](../reports/rapport-speculatif-reflexe.md) |

> **E5, remesuré le 16/10 — et ses DEUX réglages critiques, que la fiche d'origine ne disait pas.**
> La distillation **fonctionne** (témoin reproduit : **25,7 %** d'accord contre 28,0 % publié ✓ ;
> direction **répliquée sur deux graines** ✓✓ : m32 **+4,6 et +4,8** points, quatre comparaisons dans le
> même sens ✓) — **mais** :
> * elle **diverge** au taux par défaut dès qu'on réduit le volume ✗ (2,7e12 en trois époques à
>   10 morceaux) : la **fenêtre est vide** ✗✓ jusqu'à ce qu'on **tronque le KL** (`--kl-tronque`,
>   fenêtre ×10 ✓) ;
> * elle **s'inverse** si le KL est trop tronqué ✗ : à **64** classes l'accord tombe à **17,1 %**
>   contre 25,7 % pour le témoin ✗✓, à **512** il monte à **30,3 %** ✓ — la cible tronquée est
>   **déformée** (renormalisée sur K classes) ;
> * le **prix est stable, le gain ne l'est pas** ✗✓ : perplexité **+148 % et +143 %** selon la graine ✓
>   (certain), accord **+4,6/+4,8** sur m32 (stable ✓) mais **+1,3 à +13,3** sur m20 ✗ (instable ✗) ;
> * le **mélange** KL + λ·CE **ne rachète rien** ✗ (chiffres identiques à λ = 0,3 et 1,0) ;
> * **limite** : il n'existe **pas** de version « petit volume » ✗ (à 10 morceaux, la distillation
>   détruit le modèle avant d'apprendre ✓).
> Et `porte-reflexe` garde désormais l'**assemblage** ✗ (refus du moteur ✓, **invariant d'identité** ✓,
> accord mesuré avant/après ✓) : les quatre pannes du fil n'étaient **pas** dans le modèle ✗✓.
| adaptation / habituation | [`rapport-habituation.md`](../reports/rapport-habituation.md) |
| le réflexe qui propose (et sa porte) · la chaîne complète, et le budget d'une décision | `tools/boucle-cerveau.sh` · `tools/carte-facultes.sh` · `tools/porte-cerveau.sh` · [`rapport-budget-decision.md`](../reports/rapport-budget-decision.md) · `porte-speculatif.sh` |
| trace globale, pannes | `porte-trace.sh`, `porte-fusion.sh`, `porte-pannes.sh` |

## 5. L'architecture qui suit — l'assemblage que les mesures IMPOSENT

Ce n'est pas un plan : c'est ce que les chiffres de cette carte laissent debout. Chaque ligne est
un choix que le dépôt a **mesuré**, et l'ordre est celui d'une décision.

**Ce qu'on allume, dans cet ordre, et pourquoi** :

1. **la profondeur d'abord** — c'est le seul levier qui déplace la métrique du plan (**×3** pour
   24 → 8 couches, **357,8 → 119,3 M paires**, exactement linéaire), et le chemin court est le seul
   endroit où la qualité tient encore (÷1,47 entraîné, `rapport-n4-porte-execution.md`) ;
2. **la fenêtre ensuite** — moitié des clés pour **+0,04 % à +7,39 %** selon le texte : elle ne
   déplace pas les paires mais divise les **clés**, donc c'est un levier de **réparti**, pas de
   calcul local (mesuré : 17,1 → 19,1 tok/s, `rapport-fenetre-puits-attention.md`) ;
3. **la mémoire de travail par TAMPON, jamais par entraînement** — R² **1,000**, **zéro paire**, et
   l'entraînement du réseau pour la retenir **échoue** (−1,09 → −2,77, `rapport-memoire-travail-n5.md`) ;
   le réseau sait seulement **lire** ce qu'une structure lui donne (+0,879 → +0,964) ;
4. **l'épisodique pour se souvenir, les poids pour savoir** — l'exemplaire bat la moyenne (**87 %**
   contre 7 % pour 11 jetons sur 2 048), et la consolidation ne transfère que la **structure
   partagée** du rejeu (mémorisation −22,5 % dans les deux cas, transfert **−7,4 %** ou **+1,2 %**) ;
5. **peu de sommeil, souvent** — 3 morceaux rejoués donnent **56 %** du gain maximal pour un coût
   indétectable, une deuxième nuit n'ajoute presque rien (−0,30 %), et doubler les époques non plus
   (+0,05 point) : **la donnée est la limite**, pas l'entraînement ;
6. **une décision par CONTENU quand la ressource rare est la bande passante** — la politique par
   texte tient la tolérance **partout** pour **−14,1 % de clés**, mais elle exige **deux passes**
   (aucun signal bon marché ne prédit la sensibilité : corrélations −0,019 et +0,096) ;
7. **et une agrégation DÉCLARÉE, jamais une somme** — deux spécialistes forts fusionnés par somme
   donnent **moins** que chacun (−4,0 % contre −7,4 % et −8,7 %).

**Ce qu'on n'allume PAS, et c'est mesuré** :

| mécanisme | ce qu'il donne | pourquoi on ne l'allume pas |
|---|---|---|
| **cycle** (boucle cortico-thalamique) | une trajectoire bornée, déterministe, ×228 plus proche après entraînement | **aucun** des quatre objectifs ne le fait converger, et le meilleur pas 4 (43,55) est **×2,4 pire qu'une passe** (18,40) pour **4× le calcul** |
| **récurrence locale** | un écho | « un écho, pas une mémoire » ; R² plafonné à **+0,104** |
| **échange d'activations entre jumeaux** | exact | gain **nul** entre jumeaux identiques (36,1307 = 36,1307), transfert nul entre experts |
| **apprentissage local** (règle hebbienne) | — | **négatif mesuré** (E7) : la règle locale *empire* l'état |
| **latéralité par duplication** | ÷2 de calcul | aucun gain mesuré (C9) |
| **effacement de l'état** | — | coûte **+41 %** (36,1307 → 51,1715) |
| **délai sur toute la pile** | — | détruit la sortie (E→E) ; le délai est bon **sur un lien**, pas partout |

**Et la chaîne complète tourne en une commande** (`tools/boucle-cerveau.sh`) : percevoir → retenir →
se souvenir → consolider → agir, chaque maillon mesuré par le moteur, avec ses chiffres publiés —
y compris celui qui dérange (le réflexe est **un autre agent** : 28 à 51 % d'accord par position,
0 à 5 jetons sur 96 en génération).

**Ce que cette carte ne dit pas** : elle ne dit pas qu'un tel cerveau **bat** un transformeur sur
une tâche — aucune mesure de ce dépôt ne le dit, et le plan le dit lui-même (§ 5). Elle dit ce
qui **existe**, ce que ça **coûte**, et où sont les trous.
