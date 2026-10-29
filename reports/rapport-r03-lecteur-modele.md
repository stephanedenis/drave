# R0.3 (première tranche) — le lecteur modèle : 0,500 contre 0,400, et le GPU

> **Ligne de roadmap** : R0.3 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **mesure
> indicative** — le contrôleur domine la troncature naïve (**0,500** contre **0,400**) et le
> hasard (**0,000**) à fenêtre égale, sur **10 questions** et un modèle de **0,5 B** : l'écart
> agrégé vaut une question.
>
> **Dispositif** : 10 questions (2 par type), 5 types ; Qwen2.5-0.5B sur **GPU** via
> `llama-cli` CUDA (greedy) ; fenêtre de 1 200 caractères ; `tools/lecteur_modele.py` +
> `tools/banc_lecture.py --lecteur modele` ; JSON bruts
> [`r03-lecteur-modele.json`](r03-lecteur-modele.json) (BM25) et
> [`r03-lecteur-modele-couverture.json`](r03-lecteur-modele-couverture.json) (couverture) ;
> spec [`banc-lecture.md`](../docs/implantation/banc-lecture.md) § 6.

## La question

Le lecteur **extractif** de R0.2 plafonne : même en lisant tout, il ne trouve la valeur que
dans **25 à 75 %** des cas. Ce plafond est-il celui du **lecteur** ou celui du **document** ?
On branche un modèle qui lit le contexte sélectionné et on compare, à **fenêtre égale**, trois
façons de remplir la fenêtre : le **contrôleur** (les passages qu'il a choisis, par score), la
**troncature naïve** (les premiers passages, dans l'ordre de lecture), le **hasard**.

## Le dispositif (et pourquoi le GPU)

Le premier passage a utilisé le `--infer` du moteur Drave, qui est **CPU** (20 fils) : ~8 à
15 s par génération, et deux bancs lancés en double ont saturé **~38 cœurs** pendant que les
deux GPU restaient à **0 %**. C'était un mauvais usage de la machine, et il est corrigé :

- **le lecteur tourne sur GPU** : `llama-cli` (build CUDA) lit le même GGUF à **1 409 t/s** de
  prompt et **273 t/s** de génération, soit **1,9 s par appel** — douze fois moins ;
- **un seul GPU** (`CUDA_VISIBLE_DEVICES=0`) : l'autre reste libre pour N2 ;
- **le CPU est rendu au moteur et aux portes**, qui sont ses vrais clients.

**Le prompt** : « Contexte : … Question : … Réponse : », génération **greedy** (`--temp 0`).
Le contexte est borné à 1 200 caractères (~300 jetons) : la fenêtre coupe, et c'est justement
pour cela que la sélection compte.

## Ce qui est mesuré

Taux de réponses qui contiennent la **valeur** attendue (0 = aucune des deux questions du type) :

| type | contrôleur | début | hasard | closed-book |
|---|---:|---:|---:|---:|
| technique | **1,00** | 0,50 | 0,00 | 0,00 |
| tableau | **0,50** | 0,00 | 0,00 | 0,00 |
| juridique | 0,50 | 0,50 | 0,00 | 0,00 |
| prose | 0,50 | 0,50 | 0,00 | 0,00 |
| code | 0,00 | **0,50** | 0,00 | 0,00 |
| **agrégat** | **0,500** | **0,400** | **0,000** | **0,000** |

**Contrôleur devant 2 types, à égalité 2, derrière 1** (le code, où la troncature prend la
première moitié du document et tombe sur le manifeste JSON). L'écart agrégé vaut **une
question** : indication, pas mesure.

**Le critère de sélection, testé et non concluant.** Le contrôleur de R0.2 et le lecteur
extractif partagent BM25 : c'est un biais. Le critère **couverture** (BM25 + 2 × la fraction des
mots de la question présents dans le passage) est branché (`--critere couverture`) et donne
**exactement les mêmes chiffres** : 0,500 / 0,400 / 0,000. Sur dix questions, le banc ne
départage pas les critères. Il faut le banc complet, ou des questions plus dures, pour cela.

## Ce que la mesure a corrigé (et qui vaut d'être noté)

Quatre fautes, toutes invisibles sans le modèle — et trois étaient des fautes **du banc**, pas
du contrôleur :

1. **Le mode « début » tombait sur la lecture intégrale** (un `startswith` manquant) : il lisait
   tout, puis la fenêtre le tronquait — il semblait battre le contrôleur avec dix fois son
   budget.
2. **Le contexte était donné dans l'ordre de lecture** : les meilleurs passages du contrôleur,
   plus loin, étaient coupés par la fenêtre. Corrigé : priorité par score.
3. **L'extraction laissait passer le bandeau de llama.cpp** : deux réponses du « hasard »
   contenaient « build 11017 » et marquaient faussement. Corrigé : on coupe sur la troncature
   de l'écho ou la fin du prompt, sinon **réponse vide** — jamais un bandeau compté comme une
   réponse.
4. **« 3,663 » contre « 3 663 »** : un modèle juste était compté faux. La comparaison des
   valeurs unifie maintenant les séparateurs de nombres.

Et une question **ambiguë** : « Que désigne le mot *drave* ? » a **deux** réponses valides dans
le document (le bus d'événements, et les billots). Le modèle répondait la première ; le gold
attendait la seconde. La question est devenue « Que désignait la drave **sur la rivière** ? ».

## Ce qui pourrait le rendre faux

- **10 questions** : un cas vaut 0,5 ; l'écart contrôleur/début est d'une question.
- **Un modèle de 0,5 B** : il hallucine et répond partiellement. Le classement contrôleur/début
  reste valable (même modèle des deux côtés) ; le taux absolu ne dit rien d'un grand modèle.
- **Le runtime fait partie du dispositif** : le même GGUF, le même prompt et le même greedy
  donnaient **0,6** sur le moteur CPU et **0,5** sur `llama-cli` — BOS, pénalité de répétition
  et découpage du prompt diffèrent. Aucun chiffre de lecteur ne se cite sans son runtime.
- **La fenêtre de 1 200 caractères est un réglage** : plus large, la troncature gagne du
  terrain ; plus étroite, la sélection compte davantage.
- **Banc choisi par l'auteur** (5 documents du dépôt) : pas un échantillon.
- **Le critère n'est pas départagé** : à 10 questions, couverture = BM25.

## Ce que ça change

1. **Le banc doit grossir et durcir** : 30 documents, 300 questions, et des questions qui ne
   partagent pas les mots du passage — sinon le modèle répond 5 fois sur 10 et tous les
   critères se ressemblent.
2. **Le runtime est un paramètre du résultat** : la fiche doit le nommer (CPU/GPU, moteur ou
   `llama-cli`), et les chiffres ne se comparent pas d'un runtime à l'autre.
3. **Le GPU est le bon instrument** pour un banc de lecture ; le CPU reste au moteur.

## Fichiers

- `tools/lecteur_modele.py` — le modèle comme lecteur (llama-cli CUDA, greedy, extraction stricte).
- `tools/lecteur_controleur.py` — `--critere couverture` (BM25 + couverture).
- `tools/banc_lecture.py --lecteur modele --critere …` — les trois façons de remplir la fenêtre ; `--depuis` relit un JSON.
- `reports/r03-lecteur-modele.json`, `reports/r03-lecteur-modele-couverture.json` — mesures brutes.
- `docs/implantation/banc-lecture.md` § 6 — le dispositif et ses limites.
