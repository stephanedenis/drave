> Campagne : **campagne-benefices** · expérience **28**
> Titre : 28. La greffe d'état (C2/C6) : elle TRANSFÈRE le contenu — ma première conclusion était fausse
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 28. La greffe d'état (C2/C6) : elle TRANSFÈRE le contenu — ma première conclusion était fausse

> **CORRECTION DU 10 OCTOBRE (soir).** Ce qui suit concluait « une greffe d'état n'est pas
> une greffe de contexte ». **C'était un artefact d'un décalage d'un jeton**, pas une
> propriété du moteur : le prélèvement se faisait sur les identifiants tokenisés
> (`--tokenize`, 1 750 jetons) alors que l'inférence construit une invite d'**un jeton de
> plus** (1 751). L'état prélevé était donc celui qui prédit le dernier jeton du texte
> (« : ») au lieu de celui qui prédit le code.
>
> **Mesuré à nouveau, avec le prélèvement fait là où le calcul se fait** (`--etat-fin`,
> k-ième position depuis la fin, résolue dans la numérotation de l'inférence) :
>
> | état injecté dans une invite qui ne contient AUCUN code | réponse |
> |---|---|
> | état final de l'invite A (code `ZQ-4471-KX`) | **`ZQ3`** |
> | état final de l'invite B (code `KJ-9999-QP`) | **`K00`** |
>
> **Le contenu passe.** La greffe d'état est donc un mécanisme utilisable — et c'est le
> fondement de l'entrée de cache (C2) qui reste à construire. La leçon de méthode, elle,
> reste : **une position ne se devine pas, elle se capture là où le calcul se fait** ;
> trois mesures ont échoué pour cette raison avant que `--etat-fin` n'existe.

### 28 bis. Ce que la greffe d'état faisait vraiment (texte d'origine, conservé)

C6 sait stocker un état et le retrouver par son contenu ; C9 sait limiter ce qui
traverse un lien. Restait le **passage** : si l'on injecte l'état d'un moment vécu dans
un calcul qui ne l'a pas vécu, l'information portée est-elle encore là ? C'est ce qu'un
cerveau fait quand l'hippocampe rappelle un épisode au cortex. Mesure ajoutée par
`--fusion-etat` / `--fusion-pos` / `--fusion-alpha` (l'état brut, avant la norme
finale, est augmenté à la position choisie).

**Le protocole ne fait différer deux invites que d'une phrase** — c'est ce qui le rend
décisif : l'invite A (1 750 jetons) contient « IMPORTANT : the vault access code is
ZQ-4471-KX. », l'invite B est **le même texte, l'aiguille en moins**. Qwen2.5-0.5B-Q8
répond `ZQ-4471-K` à A et `150px` à B. On prélève l'état de la **dernière position** de
A et on l'injecte dans B, à sa dernière position.

| cas | mesure |
|---|---|
| témoin, poids **0** | sortie **identique** à B sans greffe (`220,16,20,15,…`) |
| **A + son propre état**, poids 100 | `25, 57, 48, 12, 19, 19, 22, 16` — **le contenu de A est toujours là** |
| **B + l'état de A**, poids 1 / 2 / 4 / 10 / 100 | **jamais le code** (`220,16,20,15,…` puis `25,16,20,15,…`) |
| B + l'état de A à **toutes** les positions, poids 100 | `25,25,25,25,…` — dégénéré |

**Ce qui est établi, en trois points :**

1. **l'injection est branchée** — un poids de 0 ne change rien (à la sortie près, au
   jeton près), et A greffé de son propre état conserve le contenu de A. Le mécanisme
   n'est donc pas en cause ;
2. **une greffe d'état n'est pas une greffe de contexte** : le code n'apparaît à AUCUN
   poids, ni même en injectant à toutes les positions (ce qui dégénère la sortie) ;
3. **et la cause est mesurée** : le **premier** jeton change (`220 → 25`, il vient de
   l'état injecté) mais **la suite reste celle de B** (`16, 20, 15`). Les jetons
   suivants sont **re-dérivés par l'attention sur le cache KV**, que la greffe ne touche
   pas. Un état résiduel est une **direction pour la tête**, pas un souvenir que le
   modèle peut relire.

**Conséquence, et elle est nette** : pour qu'une mémoire **serve** le calcul, ce qu'elle
rend doit entrer comme **contenu** (des jetons que le modèle peut lire — c'est le RAG
ordinaire) ou comme **entrée de cache** (un état rangé comme clé/valeur que l'attention
peut interroger). Le moteur n'a aujourd'hui **aucune prise sur le cache KV** : c'est un
manque, écrit comme tel, et non un réglage à trouver.

**Ce que la mesure ne dit pas** : elle porte sur un modèle de 0,5 B, une invite de
1 750 jetons, et une seule position d'injection (la dernière). Une injection à une
position *antérieure* du contexte, ou une injection **répétée à chaque pas** (un état
maintenu, comme le ferait un cache), n'ont pas été essayées — la seconde est
précisément ce qu'un cache mémoire demanderait.
