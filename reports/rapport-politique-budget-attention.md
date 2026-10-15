# Le budget d'attention a-t-il une bonne taille par texte ? — le coût de la moitié varie de ×180

> Campagne : **cerveau** · expérience : la **politique** de budget (C5 modulation, C10 budgets) —
> la conséquence pratique de la loi de frontière (`rapport-loi-frontiere-fenetre.md`).
> Question : si garder la moitié des clés coûte **de +0,4 % à +3,0 % selon le texte**, un budget
> **uniforme** est-il seulement un mauvais compromis — ou est-il **faux** ? Et une **politique par
> texte** vaut-elle ce qu'elle coûte ?
> Verdict : **le coût de la moitié varie de ×180 selon le texte, et un budget uniforme casse la
> tolérance sur 5 textes sur 8.** Mesuré sur huit morceaux de 512 jetons, tolérance **+1 %** du
> budget complet : la moitié des clés coûte **+0,04 %** (m10) à **+7,39 %** (m15) ; **3 textes sur 8
> seulement** tiennent le +1 % à la moitié. Et la politique par texte — donner à chacun ce qu'il lui
> faut — tient la tolérance **partout** pour **440 clés en moyenne contre 512** : **−14,1 % de clés à
> qualité égale**.
> Date réelle : **2026-10-15 01 h 05-01 h 25 HAE** (heure lue sur la machine)
> Protocole : `tools/politique-budget.sh` (nouveau) · huit morceaux (m5, m10, m15, m20, m25, m30,
> m31, m32) de **512 jetons**, `--ctx 512` · trois budgets : **complet** (512), **moitié**
> (fenêtre 256 + 64 puits = 320 clés), **quart** (fenêtre 128 + 64 puits = 192 clés) · perplexité du
> **moteur** · le « budget minimal » d'un texte est le plus petit des trois qui reste à ≤ +1 % du
> complet.

## 1. Les huit textes, et le budget qu'il faut à chacun

| texte | complet | moitié | quart | budget minimal ≤ +1 % |
|---|---:|---:|---:|---|
| m5 | 11,2756 | 11,4862 (**+1,87 %**) | 14,3436 (+27,21 %) | **complet** |
| m10 | 17,9935 | 18,0000 (**+0,04 %**) | 18,6225 (+3,50 %) | **moitié** |
| m15 | 14,1831 | 15,2306 (**+7,39 %**) | 17,0134 (+19,96 %) | **complet** |
| m20 | 15,4418 | 16,0361 (+3,85 %) | 16,8612 (+9,19 %) | **complet** |
| m25 | 14,2861 | 14,4186 (+0,93 %) | 16,3170 (+14,22 %) | **moitié** |
| m30 | 9,7084 | 10,0605 (+3,63 %) | 10,5925 (+9,11 %) | **complet** |
| m31 | 12,6365 | 12,8618 (+1,78 %) | 13,4797 (+6,67 %) | **complet** |
| m32 | 9,6503 | 9,6990 (+0,50 %) | 10,0053 (+3,68 %) | **moitié** |

Ce que ça dit :

* **le coût de la moitié varie de ×180** : +0,04 % sur m10, **+7,39 %** sur m15. La loi de frontière
  du 13/10 annonçait « +0,4 % à +3,0 % à N = 4 096 » ; ici, à **512 jetons**, l'étendue est **plus
  large encore** — et elle va jusqu'à **+7,4 %**, un chiffre qui n'était pas dans la fiche ;
* **un budget uniforme est donc FAUX, pas seulement coûteux** : « la moitié partout » ne tient la
  tolérance de +1 % que sur **3 des 8 textes**, et laisse les cinq autres jusqu'à **+7,39 %**. Il ne
  s'agit plus d'un compromis à accepter, mais d'une **qualité non tenue** sur 62 % des textes ;
* **la politique par texte tient partout pour −14,1 % de clés** (440 contre 512) : c'est le gain
  réel d'une allocation par texte — modeste, mais **exact**, et c'est la première mesure du dépôt où
  une **décision par contenu** (le texte) bat une constante ;
* **et le budget est très mal corrélé à la perplexité du texte** : m15 coûte +7,4 % à la moitié
  (perplexité complète 14,18) quand m20 coûte +3,85 % (15,44) et m10 +0,04 % (17,99) — **le texte le
  plus perplexe (m10) est le moins sensible**. On ne peut donc pas allouer par la difficulté
  générale : il faut **mesurer la sensibilité**, ce que le script fait (deux passes, une par budget).

## 1bis. Aucun signal BON MARCHÉ ne prédit la sensibilité — la politique exige deux passes

Une politique n'est utile **en ligne** que si l'on peut décider **sans payer** : s'il existait un
signal peu coûteux qui prédise « ce texte a besoin de ses clés », la décision se prendrait en une
passe. Deux candidats évidents, et ils ne marchent pas — corrélations sur les **huit** textes :

| signal (disponible avant de décider) | corrélation avec la sensibilité au budget |
|---|---:|
| **perplexité du texte au budget complet** (sa difficulté) | **−0,019** |
| **perplexité au budget réduit** (ce qu'on paie de toute façon) | **+0,096** |

* **aucune des deux n'est corrélée** : ni la difficulté du texte, ni ce qu'il rend à budget réduit ne
  dit s'il **supporterait** la réduction. Le texte le plus perplexe (m10, 17,99) est le **moins**
  sensible (+0,04 %) et le plus sensible (m15, +7,39 %) a une perplexité **plus basse** (14,18) ;
* **conséquence nette** : la politique par texte **ne peut pas** se décider en une passe. Elle exige
  de **payer deux fois** (mesurer la sensibilité, puis servir le texte au budget choisi) — et c'est
  le coût qui borne son intérêt : **2× le calcul** pour **−14,1 % de clés**. Elle n'est donc
  rentable que si la ressource rare est la **bande passante** (réparti) et non le calcul local ;
* **et c'est une réponse au 🟡 « modulation » de la carte des facultés** : le signal scalaire qui
  manquait depuis le 10/10 n'est pas *introuvable par hasard* — il **n'existe pas** dans les deux
  statistiques les plus naturelles. La métacognition utile ici est une **mesure**, pas un signal.

## 2. Ce que ça change pour le cerveau

* **la modulation a enfin un signal qui paie** : non pas un scalaire abstrait (les cinq modulateurs
  mesurés sont inertes ou nuisibles, `docs/cerveau-facultes.md` § modulation), mais une **décision
  par texte** — « ce texte supporte-t-il la moitié des clés ? » — qui se **mesure** et qui
  **rapporte** 14 % du budget de clés à qualité tenue ;
* **c'est une faculté de MÉTACOGNITION** : le système doit savoir ce qu'il ne sait pas (ou plutôt
  ce qu'il ne peut pas se permettre de ne pas regarder). Le script en donne la version la plus
  simple : deux passes de mesure, puis un choix ;
* **et le coût de la politique est nommé** : mesurer la sensibilité demande **deux exécutions** par
  texte (une complète, une à la moitié) — soit 2× le calcul avant de savoir. La politique n'est donc
  rentable que si le texte est **long** (le coût de mesure s'amortit sur les jetons qui suivent), et
  c'est un calcul qui n'est pas fait ici.

## 3. Ce que cette fiche ne dit pas

* **huit textes, une tolérance (+1 %), deux budgets de réduction** : la courbe complète
  (512 → 384 → 320 → 256 → 192 clés) dirait *où* chaque texte décroche, et elle n'est pas faite —
  c'est le prolongement naturel ;
* **la sensibilité est mesurée par texte entier**, pas par région du texte : un même texte peut
  avoir des passages faciles et difficiles, et une politique **par jeton** (ce que le plan C5
  appellerait une modulation) n'est pas mesurée — elle demanderait une décision *en ligne* ;
* **les puits sont fixes** (64) dans les trois budgets : leur nombre change la qualité
  (`rapport-fenetre-puits-attention.md`), donc « 320 clés » n'est qu'**une** façon de dépenser la
  moitié ;
* **rien n'est mesuré en temps** : la moitié des clés n'accélère presque pas en local (mesuré le
  13/10 : 17,1 → 19,1 tok/s), donc l'intérêt du budget est en **paires et en octets répartis**, pas
  en vitesse locale — et c'est cohérent avec ce que la fiche de la fenêtre disait déjà ;
* **le coût de la mesure préalable (2×) n'est pas amorti** dans le −14,1 % : le chiffre est le gain
  sur l'**allocation**, pas sur le calcul total.
