# S — La banque s'arrête à 81 lectures / 65 phrases : l'arbre manque de profondeur, les référents ne sont pas résolus

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : la validation humaine s'est
> arrêtée après **142 verdicts sur 71 phrases** : **81 lectures acceptées sur 65 phrases**
> (71 `resolu`, 10 `compatible`, 1 `double sens`) et **60 `exclu`**. Le motif, verbatim :
> « il manque trop souvent de profondeur » et « les référents ne semblent pas résolus avant que
> je tranche ». La mesure le chiffre : **277/369 candidats** ont une profondeur maximale de
> **1** (82 de 2, 10 de 0), et **170/207 phrases** portent un pronom/possessif — **371 formes,
> 0 antécédent proposé**. La banque est **partielle**, pas fausse : l'export `--mode banque`
> donne **81 lignes / 65 phrases**, SHA-256
> `2d27b712269735d01ad091303f76bfba34cf491d7775c84c2cc63ad460297525`, spans et restitution
> vérifiés.

## Le dispositif

- **Banc** : 7 phrases du banc + 200 phrases réelles de la littérature → **207 phrases,
  369 candidats** ; le serveur `serveur.py` (port 8765) ; verdicts append-only dans
  `donnees/validations.jsonl`.
- **Validation** : un humain, les quatre statuts (`resolu`, `compatible`, `exclu`,
  `double sens`), une note libre ; arrêt spontané.
- **Mesure des bloqueurs** : `mesure_arbre.py` — la profondeur d'indentation (`niveau`) par
  candidat et les pronoms/possessifs sans antécédent proposé.
- **Export** : `exporter_corpus.py --mode banque` (dernier verdict, spans vérifiés, manifeste) ;
  `verifier_corpus.py`.

## Les chiffres

| ce qui est mesuré | valeur |
|---|---:|
| verdicts | **142** sur **71 phrases** (141 candidats distincts) |
| lectures acceptées | **81** sur **65 phrases** |
| statuts | **71** `resolu`, **10** `compatible`, **1** `double sens` |
| exclues | **60** |
| export de la banque | **81 lignes / 65 phrases**, SHA `2d27b712…` |
| arbre : profondeur max par candidat | **277/369 à 1**, 82 à 2, 10 à 0 |
| arbre : niveaux des segments | 1 444 à 0, 888 à 1, 82 à 2 |
| référents | **170/207 phrases**, **371 formes**, **0 antécédent proposé** |

Les formes les plus fréquentes : `y` (109), `en` (67), `se` (44), `me` (19), `il` (18),
`son` (18), `elle` (9), `je` (9), `vous` (9) — les clitiques `y`/`en` gonflent le décompte ; le
chiffre est un **majorant**, pas une liste d'anaphores.

## Le retour humain, verbatim

> « pour ce qui est de la validation de la banque, après moins de 20 %, j'arrête car j'ai trop de
> doutes sur l'arbre syntaxique car il manque trop souvent de profondeur et les référents ne
> semblent pas résolus avant que je tranche »

Une note de validation : p002-c2, `compatible` — « il est préférable de dire l'homme au
télescope ». Elle est conservée : la banque n'est pas un juge, c'est une trace.

## Le négatif nommé

**La banque n'est pas validable à l'échelle tant que l'outil ne montre pas un arbre réel et des
référents résolus.** Le chiffre le dit : trois candidats sur quatre s'arrêtent à une profondeur de
1, et l'outil ne propose **aucun** antécédent pour 371 formes pronominales. L'humain ne peut pas
trancher une lecture dont la structure est plate et dont les référents manquent : ce n'est pas une
banque « fausse », c'est une **banque partielle** avec un **bloqueur d'outil** nommé.

## Les contrôles négatifs

- **le dernier verdict gagne** : 60 `exclu` ne sortent pas ; l'export ne garde que les lectures
  acceptées ; `verifier_corpus.py` recalcule l'empreinte, les comptes, les spans et la
  **restitution** ;
- **le partiel contre le prévu** : 65 phrases sur 207 ; la banque n'est pas complète, et l'export
  le dit (81 lignes, pas 200) ;
- **le majorant des référents** : `y`/`en`/`se` sont des clitiques qui ne sont pas tous
  anaphoriques ; le vrai besoin d'antécédent est plus petit que 371 — mais il n'est pas nul ;
- **la profondeur** est celle de l'indentation actuelle, pas d'un arbre linguistique : le chiffre
  mesure le **plat** de l'outil, pas la langue.

## Ce qui pourrait le rendre faux

- **Un seul humain** : le retour dit la difficulté d'un valideur, pas une propriété de la banque ;
- **200 phrases** : un échantillon de littérature, pas un corpus ; les verdicts sont utilisables
  comme banque partielle, pas comme vérité ;
- **les référents** : le décompte inclut les clitiques non anaphoriques ; le besoin réel est plus
  petit, mais l'outil n'en propose **aucun** ;
- **la profondeur** : un arbre plus profond n'est pas forcément juste ; c'est la **condition** de
  la validation, pas sa preuve ;
- **la banque partielle** : elle est une trace de 142 décisions humaines ; elle vaut pour ce
  qu'elle est, pas pour ce qu'elle n'a pas validé.

## Le miroir entrée/sortie

- **entrée** : 207 surfaces → 369 structures candidates ; 142 verdicts humains ;
- **sortie** : `data/structures/banque-validee.jsonl`, **81 lignes**, SHA `2d27b712…`, spans et
  restitution vérifiés — une banque **partielle** qui se relit.

La fluidité (un candidat qui s'affiche) n'est pas la fidélité (un humain qui tranche) : l'arrêt le
montre.

## Fichiers

- Sous-module : commit **`51b6aaf`** — `donnees/validations.jsonl` (142 verdicts),
  `mesure_arbre.py`, `donnees/mesure-arbre.json`, README ; **47 tests**.
- Export : `data/structures/banque-validee.jsonl` (81 lignes) ;
  manifeste committé : `reports/s-banque-validee.json`.
- Fiche : celle-ci ; état et roadmap S mis à jour.

## La suite (ligne S)

1. **Arbre réel** : parent/enfant, `profondeur` explicite, rendu indenté — et une mesure de la
   profondeur sur les 200 phrases ;
2. **Référents** : proposer les antécédents (pronom/possessif → GN, sujet, GP), les faire
   **résoudre avant** le verdict de structure ; le verdict garde les référents ;
3. **Reprendre la validation** sur les 200 phrases avec l'outil corrigé, puis exporter la banque
   complète ;
4. `h050`/`h053` (verbe hors lexique, nom après adjectif en fin de phrase) restent les limites de
   l'analyseur, à mesurer sur une nouvelle vague.
