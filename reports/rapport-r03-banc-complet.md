# R0.3 — le banc complet : 249 questions, 30 documents, et le modèle sur GPU

> **Ligne de roadmap** : R0.3 · **Date** : 2026-10-29 · **Verdict** : ✅ **la sélection est
> validée à l'échelle** — le contrôleur est **5,5× meilleur** que la troncature naïve
> (**0,231** contre **0,042**) et gagne sur les **5 types** ; ⚠️ mais le **modèle de 0,5 B
> répond moins bien que le lecteur extractif** sur les valeurs (0,23 contre 0,72–1,00), parce
> qu'il **paraphrase** au lieu d'extraire.
>
> **Dispositif** : 30 documents, 5 types, **249 questions** générées à valeur numérique ;
> lecteur **extractif** (R0.2) et lecteur **modèle** (Qwen2.5-0.5B, `llama-cli` **CUDA**,
> 1,9 s/appel) ; budgets 10/30/50 % ; JSON bruts
> [`r03-banc-extractif.json`](r03-banc-extractif.json) et [`r03-banc-modele.json`](r03-banc-modele.json) ;
> spec [`banc-lecture.md`](../docs/implantation/banc-lecture.md) § 7.

## La question

Le banc pilote (20 questions main) ne faisait pas un taux : un cas valait 0,25. À l'échelle de
30 documents, la sélection tient-elle encore ? Et que fait un **modèle** dans la boucle — le
plafond de 25–75 % du lecteur extractif était-il celui du lecteur ou du document ?

## Le corpus et les questions

**30 documents** (5 types × 6) : prose (théorie), technique (implantation), tableau (pilotage),
juridique (résolutions ONU), code (documents à blocs de code). **249 questions** construites par
`tools/banc_complet.py` : un passage qui porte une **valeur numérique**, deux **mots rares** du
passage pour la demander, le passage pour gold, la valeur pour réponse.

**Ce que le gabarit ne peut pas faire** : une question générée partage des mots avec son gold,
donc la sélection y est plus facile qu'une paraphrase. C'est écrit avant les chiffres : le banc
complet mesure la **couverture**, le pilote la **difficulté**.

**Le corpus juridique est latin à dessein** : le tokeniseur du lecteur ne lit ni le cyrillique
ni le CJK — les PDF russes et chinois ne produisent **aucune ancre**. C'est une limite du
lecteur, pas un choix du banc ; R5.2 en hérite.

## Ce qui est mesuré — le lecteur extractif (249 questions, 3 s)

| type | récup. 10 % | récup. 30 % | récup. 50 % | valeur 30 % | valeur 100 % | aléatoire 30 % |
|---|---:|---:|---:|---:|---:|---:|
| code | 0,89 | **1,00** | 1,00 | 0,72 | 0,72 | 0,39 |
| juridique | 0,87 | **1,00** | 1,00 | 1,00 | 1,00 | 0,20 |
| prose | 1,00 | **1,00** | 1,00 | 0,76 | 0,76 | 0,33 |
| tableau | 0,98 | **1,00** | 1,00 | 0,93 | 0,93 | 0,29 |
| technique | 1,00 | **1,00** | 1,00 | 0,90 | 0,90 | 0,30 |

À **30 %** du budget, le passage gold est lu dans **100 %** des cas sur les cinq types — la
courbe est plate entre 30 et 50 %, et commence à mordre à 10 % (0,87–1,00). Le **hasard** reste
à 0,20–0,39. Le taux de réponse est **exactement** celui de la lecture intégrale : c'est
structurel (le lecteur est le même, ancré sur l'index du document entier), et c'est le contrôle
qui dit que la sélection ne coûte rien.

## Ce qui est mesuré — le modèle sur GPU (249 questions, ~13 min)

| type | contrôleur 30 % | début 30 % | closed-book |
|---|---:|---:|---:|
| code | **0,204** | 0,056 | 0,000 |
| juridique | **0,167** | 0,100 | 0,000 |
| prose | **0,265** | 0,000 | 0,000 |
| tableau | **0,220** | 0,017 | 0,000 |
| technique | **0,298** | 0,035 | 0,000 |
| **agrégat** | **0,231** | **0,042** | **0,000** |

**Le contrôleur gagne sur les 5 types, par un facteur 5,5.** C'est la validation à l'échelle :
à fenêtre égale, sélectionner vaut mieux que prendre le début du document.

**Mais le taux absolu est bas, et il faut le dire** : 0,231. Le modèle ne répond pas « 4833 »
ou « 65 536 » ; il **paraphrase la question** (« Le document associe les valeurs *activations*
et *couche* à… »). Un modèle de 0,5 B n'est pas un extracteur.

**Et le lecteur extractif fait mieux sur ces questions** (0,72–1,00 contre 0,23) : il **rend le
passage**, qui contient le nombre. Pour une réponse **numérique**, rendre le passage bat générer
— à cette taille de modèle. C'est une conclusion de dispositif, pas de doctrine : un plus grand
modèle peut renverser la comparaison, et c'est R0.3 « durci » qui le dira.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **passages aléatoires** | nettement plus bas que le contrôleur | ✅ 0,20–0,39 (récup.) · valeurs aléatoires 0,000 |
| **closed-book** | aucune réponse | ✅ 0,000 sur les cinq types |
| **troncature naïve** | perdre face à la sélection | ✅ 0,042 contre 0,231 |
| **sans but** (pilote) | ne pas répondre | ✅ 0,000 |

## Ce qui pourrait le rendre faux

- **Questions gabarit** : elles partagent les mots du gold ; la récupération y est plus facile
  qu'en paraphrase. Le banc complet ne remplace pas le pilote, il le complète.
- **La valeur est le premier nombre du passage** : parfois un identifiant (« 4833 ») et non la
  valeur saillante. C'est une imprécision du générateur, pas du lecteur.
- **Modèle de 0,5 B** : il paraphrase, donc le taux absolu (0,231) ne dit rien d'un grand modèle.
  La comparaison contrôleur/début reste valable (même modèle des deux côtés).
- **Tokeniseur latin** : ni cyrillique ni CJK ; les PDF ru/zh sont hors banc.
- **Le banc est adossé à des documents vivants** : réécrire un document invalide ses golds
  (attrapé en cours de route sur `banc-lecture.md`). Régénérer avec `tools/banc_complet.py`
  avant tout passage.
- **Le runtime fait partie du dispositif** : les chiffres CPU et GPU du même modèle ne se
  comparent pas (0,6 contre 0,5 sur le pilote).

## Ce que ça change

1. **La sélection est acquise** : à 30 % du budget, le contrôleur lit le bon passage dans 100 %
   des cas sur 249 questions et 5 types. R0.2 n'a plus besoin d'être amélioré pour cela.
2. **Pour les valeurs, rendre le passage bat générer** à 0,5 B. Le pipeline de lecture doit
   donc être **extractif par défaut**, génératif seulement quand la question demande une
   synthèse — et c'est au modèle de le mériter, pas au banc de le supposer.
3. **La paraphrase est la prochaine difficulté** : le banc complet mesure la couverture, pas la
   compréhension. R0.3 « durci » (paraphrases, deux sauts) est la suite.

## Fichiers

- `tools/banc_complet.py` — le corpus de 30 documents et le générateur de questions (249).
- `tools/banc_lecture.py --banc … --lecteur modele` — les deux lecteurs, les modes, les contrôles.
- `tools/lecteur_modele.py` — `llama-cli` CUDA, extraction stricte (jamais le bandeau).
- `reports/r03-banc-extractif.json`, `reports/r03-banc-modele.json` — mesures brutes.
- `docs/implantation/banc-lecture.md` § 7 — le banc complet et ses limites.
