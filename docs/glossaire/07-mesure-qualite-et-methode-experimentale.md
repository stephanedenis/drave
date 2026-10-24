# 7. Mesure, qualité et méthode expérimentale

> **Famille 7 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 7. Mesure, qualité et méthode expérimentale

**Amplification chaotique** — Explication d'un écart de continuation entre deux
chemins de calcul pourtant à perplexité identique : une différence de 1e-5 sur un
logit peut faire basculer l'`argmax`, et la suite diverge. « La perplexité est
identique, pas la continuation » (`docs/contexte-long.md:315-318`,
`reports/rapport-aiguille-topk.md:136-139`).

**Banc dégénéré · « un banc qui passe ne prouve pas qu'il mesure »** — Un banc dont
les données rendent le résultat vrai pour de mauvaises raisons. Exemple consigné :
un banc de scores GPU où toutes les positions partageaient la même clé, ce qui a
donné 1,03e-7 au lieu de 1,60-2,25e-7 (`reports/rapport-gpu-scores.md:27-36`,
`docs/sprints.md:69-73`).

**Cohérence des documents (audits)** — Trois rapports passent le corpus au crible et
classent chaque affirmation en OK / PÉRIMÉ / CONTRADICTOIRE / MANQUANT, avec
`fichier:ligne` : `reports/rapport-coherence-docs.md` (80 affirmations, 38
périmées), `reports/rapport-coherence-docs-2.md` (66 affirmations, 27 tiennent) et
`reports/rapport-coherence-vision.md` (les 18 documents de `docs/`).
**Où** : à lire avant de citer un chiffre ancien.

**Corrélation · différence symétrique · accord top-1** — Trois façons de comparer
deux exécutions : la *corrélation* des logits (0,999024 entre le moteur et
llama.cpp sur GLM-5.3), la *différence symétrique* des ensembles retenus (0 sur
14/14 lignes pour le top-k GPU), l'*accord top-1* (497 jetons sur 511 gardent le
même argmax) (`reports/rapport-mla-experts.md:106-113`,
`reports/rapport-logits-gpu-vs-cpu.md:40-44`).

**Croisement push/pull (≈22 %)** — La densité d'activation à laquelle le coût des
deux chemins s'égale : en dessous, le push gagne (×2,1 à 10 %, ×8,3 à 1 %) ;
au-dessus, le dense gagne (×4,7 à 100 %). Le seuil `seuil_push` a été corrigé de
0,15 à **0,22** après une première campagne fausse
(`reports/rapport-croisement-push-pull.md:43-48`,
`reports/rapport-mur-memoire-4bits.md:53-57`).

**Densité d'activation · sparsité · parcimonie · creux** — Fraction des neurones
dont l'activation n'est pas nulle (ou dépasse un seuil). Le projet mesure 17,9 % à
seuil 5 % du max sur Qwen2.5-0.5B, et 100 % (aucun zéro exact) à seuil nul ; c'est
cette densité qui décide du chemin d'exécution
(`docs/vision.md:44-55`, `reports/rapport-localite-activation.md:43-47`).
La densité **par couche** varie de 20 % à 56 %, donc la décision push/pull est une
propriété de la couche, pas du modèle (`docs/roadmap.md:28`).

**Diff par couche** — Comparaison de deux traces couche par couche, jeton par jeton,
pour localiser une divergence au lieu de la constater : « KV f32 contre int8 →
première divergence couche 1, jeton 0, couche la plus touchée FFN 2 »
(`docs/roadmap.md:16`, `tools/diff_flux.py`).

**Écart relatif · RMS · écart max** — Façons de chiffrer une erreur. L'*écart max
relatif* est utilisé pour comparer des tenseurs (1e-7, 5,2e-7, 1,8e-6) ; le *RMS*
(root mean square) pour une erreur répartie (0,085 % du max de la liste pour la
trace v3) ; la *tolérance* du dépôt pour un noyau GPU est 1e-6
(`docs/format-flux.md:62-65`, `reports/rapport-gpu-scores.md:50-52`).

**Fidélité (bit à bit · exact · équivalent)** — Trois niveaux définis par le dépôt :
*bit à bit* (même forme d'exécution, même résultat), *exact* (aucun réencodage : les
octets du fichier sont ceux exécutés), *équivalent* (même perplexité à l'arrondi
près). Un convertisseur qui réencode doit prouver « exact » ou renoncer au nom
« haute fidélité » (`docs/convertisseur.md:150-163`).

**Gini · Jaccard · η² · R² · r · exposant de Heaps** — Statistiques employées pour
tester une hypothèse : le *Gini* mesure la concentration d'un routage d'experts par
couche ; le *Jaccard* le recouvrement de deux ensembles d'experts ; *η²* et *R²* la
part de variance expliquée ; *r* une corrélation ; l'*exposant de Heaps* (~0,21) la
croissance du vocabulaire d'un corpus. Ce sont eux qui ont infirmé la piste des
« motifs d'expertise » (R² hors échantillon = +0,007)
(`reports/rapport-empreinte-memoire.md:114`, `reports/rapport-programme-evolutif.md:36-42`).

**Localité d'activation · réorganisation contiguë** — Les neurones qui s'allument
ensemble sont-ils voisins en mémoire ? Un élagage *contigu* est 30 % plus rapide
qu'un élagage *dispersé* à taux égal, et grouper les neurones co-actifs est la
piste de gain la plus proche du programme (`reports/rapport-inference.md:285-288`,
`docs/programme-recherche.md:219-221`).

**Magnitude · quantile · « top 10 % »** — La *magnitude* est la valeur absolue
d'une activation ; le *quantile* Q d'une trace est le seuil qui retient une fraction
donnée. Mesure clé du projet : les 10 % de neurones les plus forts portent **33,1 %**
de la magnitude, et seuls **0,08 %** sont « chauds » plus de 90 % du temps — donc un
préchargement statique ne paie pas (`docs/vision.md:79-81`,
`reports/rapport-localite-activation.md:43-47`).

**Moindres carrés · span linéaire · monômes quadratiques · rang effectif · valeur
singulière** — Outils de l'étape d'apprentissage sans rétropropagation :
*moindres carrés* pour ajuster une lecture sur le journal, *span linéaire* pour
savoir si une direction est déjà dans l'espace des poids, *monômes quadratiques*
(401 856 produits `x_i·x_j`) comme candidats non linéaires, *rang effectif* et
*valeurs singulières* pour mesurer la saturation d'une projection. Conclusion
mesurée : un nœud linéaire ne peut rien ajouter à 69,2 % des poids
(`docs/programme-recherche.md:123-127`, `reports/rapport-capteur-hebbien.md:44-92`).

**p50 · p90 · p95 · médiane · max** — Quantiles d'une distribution d'écarts :
« |ΔNLL| médian 0,076, max 1,49 », « p90 0,0017 ». Le dépôt préfère la médiane et le
p90 au maximum seul, parce qu'un jeton atypique peut porter tout l'écart
(`reports/rapport-gpt-oss-perplexite.md:76`, `reports/rapport-aiguille-topk.md:133`).

**Porte de format** — Vérification que chaque type quantifié est déquantifié
correctement, comparé à `libggml` au bit près : « 19 formats lisibles, 17 à la
porte » (`tools/portes_formats.sh`, `docs/format-clusters.md:148-158`,
`reports/rapport-coherence-vision.md:145-146`).

**Profilage par neurone · `--ppl-profil`** — Compter quels neurones s'allument, à
quelle fréquence, avec quelle magnitude, couche par couche (`--profil-neurones`,
`--neurones-sortie`) ; le temps par poste, lui, s'imprime à chaque `--ppl` (pas de
drapeau), et `--ppl-profil` ajoute la **perte par tranche de 256 positions**. C'est l'axe 1
de la vision : « un flux de listes est observable par construction »
(`docs/vision.md:62-89`, `docs/roadmap.md:129-149`).

**Profondeur de sonde · fenêtre · taux de récupération** — Vocabulaire du test de
l'aiguille : le code à retrouver est planté à une *profondeur* relative (0,1 = tout
au début, 0,9 = tout à la fin), chaque essai est une *sonde*, et le *taux de
récupération* est la fraction de sondes réussies. La perplexité ne dit pas si le
modèle **retrouve** une information : c'est pourquoi ce test existe
(`docs/contexte-long.md:533-550`, `reports/rapport-aiguille.md:74`).

**Référence indépendante (numpy)** — Seconde implémentation de la **même formule**,
écrite dans un autre langage, pour valider un chemin : « une seconde implémentation
de la même formule, pas une seconde exécution de la même implémentation ». C'est
ainsi que MLA (5,2e-7), les patchs de vision (5,4e-7) et le projecteur (1,7e-6) ont
été validés (`docs/vision.md:182-190`, `docs/plan-mla-vision.md:8-16`,
`src/transformer_np.py`).

**Reproduit · non reproduit** — Mention explicite du dépôt quand un chiffre n'a pas
été re-mesuré depuis sa première publication : « valeurs du 30/09, non reproduites
depuis : seul l'écart A/B fait foi » (`docs/contexte-long.md:565-567`,
`docs/plan-gpu-topk.md:86-90`). Un chiffre « non reproduit » ne doit pas être cité
comme acquis.

**Seuil absolu · seuil relatif** — Un seuil *absolu* coupe les activations sous une
valeur fixe ; un seuil *relatif* les coupe sous une fraction du maximum du vecteur.
Mesure : le seuil absolu est **10× moins efficace** que le k-WTA à sparsité égale
(`reports/rapport-parcimonie-imposee.md:47`, `docs/roadmap.md:139-141`).

**Test de l'aiguille (« l'aiguille dans la botte de foin »)** — Banc de
récupération : on plante un code (`AZUR-7391`) dans un long remplissage et on
vérifie que le modèle le ressort. Version 2 : remplissage Wikitext-2, réponses de
40 jetons, préremplissage par lots — **12 sondes sur 12** trouvées
(`docs/contexte-long.md:533-550`, `reports/rapport-aiguille.md:74`,
`tools/aiguille.py`). **Réf.** : Hsieh et al., *RULER: What's the Real Context Size
of Your Long-Context Language Models?*, [arXiv:2404.06654](https://arxiv.org/abs/2404.06654).

**Trace · mesure · recalcul** — Distinction de méthode : une trace est un
enregistrement, une mesure est un chiffre obtenu en exécutant, un recalcul est une
conséquence arithmétique du code. L'audit prévient : « les chiffres recalculables
(3 663, 917 583, 1 419) sont des conséquences arithmétiques du code, pas des mesures
neuves » (`reports/rapport-coherence-docs.md:205-211`).

---

