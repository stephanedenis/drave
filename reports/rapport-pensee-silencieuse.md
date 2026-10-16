# PENSER SANS VERBALISER — la boucle d'état naïve détruit la prédiction, et verbaliser n'est PAS du gaspillage

> L'idée vient de **Stéphane** (16/10) : un LLM qui « réfléchit » le fait en **verbalisant** — chaque pas
> de pensée est un jeton, réinjecté dans l'entrée, re-embarqué, re-parcouru ✗. Un cerveau d'expert fait
> l'inverse : il **pense sans dialogue intérieur** ✓ (l'anecdote de César lisant sans subvocaliser ✓).
> Et réciproquement : **verbaliser** fait basculer dans un **contexte de communication** — on adapte le
> message au destinataire, on sort de la réflexion ✗. Troisième volet : étudier les **correspondances
> entre les couches prélinguistiques de sortie et les couches post-linguistiques d'entrée** des grands
> LLM ✓.
> Date réelle : **2026-10-16, 13 h 20-13 h 40 HAE** (heure lue sur la machine)
> Protocole : `tools/pensee_silencieuse.py` — un texte coupé en **amorce** (256 jetons) et **suite**
> (256), et **la perplexité de la suite** comparée entre trois réglages ✓, sur la **même** amorce et la
> **même** suite ✓. Le moteur écrit et relit ses états (`--etat-sortie` ✓, `DRAVE_ETAT_ENTREE` ✓), donc
> une « pensée sans jeton » est **exécutable** ✓.

## 1. Les chiffres

| réglage | perplexité de la suite | écart contre A |
|---|---:|---:|
| **A. lecture seule** (le témoin) | **9,6503** | — |
| **B. 1 pas silencieux** (état brut réinjecté) | **294 181** | **+3 048 315 %** ✗✗ |
| B. 2 pas silencieux | 304 146 | +3 151 570 % ✗✗ |
| B. 4 pas silencieux | 276 006 | +2 859 978 % ✗✗ |
| **B′. 1 pas silencieux, état NORMÉ** (échelle des entrées) | **292 935** | +3 035 398 % ✗✗ |
| B′. 4 pas, état normé | 284 943 | +2 952 589 % ✗✗ |
| **C. 4 jetons VERBALISÉS** (le modèle écrit, puis lit la suite) | **9,6120** | **−0,40 %** ✓ |
| **C. 16 jetons VERBALISÉS** | **9,5003** | **−1,55 %** ✓✓ |

## 2. Ce que ces chiffres disent, et dans quel ordre

* **LA BOUCLE D'ÉTAT NAÏVE DÉTRUIT LA PRÉDICTION** ✗✗ — de **cinq ordres de grandeur** (9,65 → 294 181 ✓).
  Ce n'est pas une petite dégradation, c'est une **rupture** : l'état réinjecté ne porte plus une
  entrée, il porte une **sortie** ✗ ;
* **ET CE N'EST PAS UN PROBLÈME D'ÉCHELLE** ✗✓ : remettre l'état à la **norme des embeddings** (moyenne
  nulle, norme 1 ✓) ne change **rien** (292 935 contre 294 181, soit **0,4 %** d'écart entre les deux ✗✓).
  L'hypothèse « il suffit de recaler l'amplitude » est **réfutée** en une mesure ✓ ;
* **donc c'est une question de SÉMANTIQUE, pas d'unités** ✓ : le résidu **avant la norme finale** (ce que
  `--etat-sortie` capture ✓, et c'est la couche **prélinguistique** ✗) est l'**état** du modèle après
  24 couches — le réinjecter à l'**entrée** revient à **appliquer le réseau à sa propre sortie** ✗✓.
  C'est très exactement la **correspondance prélinguistique ↔ post-linguistique** que Stéphane pose ✓✓ :
  **elle n'est pas l'identité**, et cette fiche la **chiffre** : à l'échelle près, l'écart est nul ✓ ;
* **ET VERBALISER N'EST PAS DU GASPILLAGE** ✓✓ — c'est le résultat qui va **contre** l'intuition de départ
  ✓ : écrire **4** jetons **améliore** la prédiction de la suite de **0,40 %**, en écrire **16**
  l'améliore de **1,55 %** ✓ — et l'effet est **monotone** en le nombre de jetons écrits ✓✓. Autrement
  dit : *le dialogue intérieur n'est pas une perte, c'est un **pont** — il remet l'état dans un espace
  que le modèle sait relire* ✓✓ (le jeton est précisément l'interface **post-linguistique** ✓) ;
* **et cela rejoint le cycle, mesuré la même nuit** ✓ : le pas d'état est **expansif** (λ local ≥ 3,7e4 ✓,
  `rapport-cycle-c2.md` § 7 ✓) et l'entraînement **réduit λ sans le soumettre** (206 → 136 ✓). Une boucle
  de pensée silencieuse **naïve** ne peut donc pas converger ✗✓ — **les deux mesures se confirment** ✓✓.

## 3. Ce que cela NE dit pas (et qui doit être dit avant qu'on s'enthousiasme)

* **ce n'est pas une mesure d'« intelligence »** ✗ mais de **prédiction de la suite** ✓ : une pensée
  silencieuse peut nuire à la prédiction **et** aider à raisonner ✗✓ — le protocole ne tranche pas cela ✓ ;
* **la boucle essayée est la plus NAÏVE possible** ✗ : le même réseau, appliqué à sa propre sortie, sans
  aucune adaptation ✓. Ce qui est réfuté, c'est **cette** boucle ✗ — pas la **pensée latente** en général ✓ ;
* **la comparaison B/C n'est pas parfaitement appariée** ✗ : en C, le modèle lit la suite **après k jetons
  écrits** (donc avec k jetons de contexte en plus ✓), tandis qu'en B il lit la **même** longueur ✓. Une
  partie du gain de C vient donc du contexte **supplémentaire** ✗✓ — la mesure **sépare mal** ces deux
  effets, et c'est nommé ✓ (un contrôle propre : verbaliser k jetons **sans** les garder en contexte ✗) ;
* **une seule amorce, un seul texte, un seul modèle** ✗ (m32, 256 jetons, Qwen2.5-0.5B ✗) — c'est une
  **première** mesure ✓, pas une loi ✓.

## 4. Le programme que cette fiche ouvre, dans l'ordre de ce qu'il coûte

1. **Le pont entraîné** ✗ — un **adaptateur** état → entrée (le dépôt a déjà la machinerie ✓ : les
   adaptateurs de sortie d'E5 ✓, entraînés sur des états gelés ✓). C'est **la** réponse à la question de
   la correspondance ✓ : si un pont **appris** rend la boucle utile, alors la correspondance existe mais
   n'est **pas linéaire** ✓✓ ; sinon, elle n'existe pas ✗✓ — dans les deux cas, c'est une mesure ✓ ;
2. **Le contrôle apparié de C** ✗ — verbaliser k jetons **sans** les laisser dans le contexte ✓ (les
   écrire, capturer l'état, **effacer** les jetons ✓) : cela sépare « le pont linguistique » ✗ de « plus
   de contexte » ✓✓ — c'est la mesure qui dirait **pourquoi** verbaliser aide ✓ ;
3. **Le même protocole sur le CYCLE ENTRAÎNÉ** ✗ (`rapport-cycle-entraine.md` ✓) : la boucle apprise
   aide-t-elle la prédiction, elle qui **dompte** la divergence sans la soumettre ✓ ? C'est la question
   « pensée silencieuse **entraînée** » ✓, et elle est à une commande ✓ ;
4. **Le mode COMMUNICATION contre le mode RÉFLEXION** ✗ (le deuxième volet de l'idée ✓) : la même
   question posée à un **destinataire** contre la même question posée « pour soi » ✓ — mesurable par une
   **sonde linéaire** sur les états ✓ (`tools/c8_sonde_lineaire.py` existe ✓) : les deux modes sont-ils
   **séparables** dans le résidu ✗, et **où** (quelle couche ✗) ? C'est la mesure qui dirait si
   « verbaliser = se mettre en mode communication » est **vrai dans les poids** ✓✓.

## 5. LE LANGAGE ABSTRAIT : appris, il bat le jeton — et l'état porte la suite bien au-delà du mot

La phrase de Stéphane (« si un LLM peut répéter intégralement un énoncé, tu as ce qu'il te faut dans les
couches intermédiaires » ✓) est **testable sans supposer** ✓ : on apprend, pour chaque **couche** L et
chaque **horizon** k, un mapping `h_p^(L) → embedding(jeton p+k)` ✓ et on regarde ce que l'état sait ✓.
`tools/pont_abstrait.py --couches … --horizons …` ✓ (ridge linéaire, 896 × 896, 4 000 positions ✓) :

| couche | k = 1 | k = 4 | k = 16 | **témoin : le JETON choisi** (k = 1) |
|---:|---:|---:|---:|---:|
| 2 | 72,9 % | 82,8 % | 84,7 % | **122,9 %** |
| 6 | 72,9 % | 82,9 % | 84,8 % | 122,9 % |
| 12 | 73,0 % | 83,0 % | 84,6 % | 122,9 % |
| 18 | **70,0 %** | 82,7 % | 84,7 % | 122,9 % |
| 23 | **68,6 %** | **82,7 %** | 84,9 % | 122,9 % |

*(écart relatif du mapping appris vers l'embedding du vrai jeton suivant ✓ ; le « témoin jeton » est
l'embedding du jeton que le **modèle aurait choisi** ✗ — le repli sur le mode jeton ✗✓.)*

* **LE LANGAGE ABSTRAIT EXISTE, ET IL BAT LE JETON** ✓✓ : l'état mappé prédit l'embedding du prochain
  jeton avec **68,6 à 73 %** d'écart, quand **le mot que le modèle aurait dit** en est à **122,9 %** ✗✓
  — c'est-à-dire **pire que l'embedding moyen** du corpus (97,1 % ✗, § mesuré plus haut ✓). Autrement
  dit : *le mot est un très mauvais représentant de ce qui vient, et l'état en est un bien meilleur* ✓✓ ;
* **ET L'ÉTAT PORTE LA SUITE BIEN AU-DELÀ DU PROCHAIN MOT** ✓✓ : à **16 jetons d'avance**, le mapping
  garde **84,6 à 84,9 %** — à peine plus mauvais qu'à 1 jeton (68,6-73 % ✓) et **très** loin devant le
  mot (122,9 % ✗). Ce que l'état contient n'est donc **pas** « le mot suivant » ✗ mais **une trajectoire**
  ✓ — ce qui est exactement ce qu'il faut pour **penser sans verbaliser** ✓✓ ;
* **et les couches intermédiaires suffisent** ✓ : de la couche **2** à la couche **23**, l'écart ne bouge
  que de **4 points** (72,9 → 68,6 ✓). Le contenu est **là, à toutes les profondeurs** ✓✓ — la phrase de
  Stéphane est **confirmée par la mesure** ✓ (et « couches intermédiaires » est même **optimiste** : la
  couche 2 fait presque aussi bien que la dernière ✓).

## 6. Et pourtant la boucle échoue encore — avec le pont appris

Le pont **appris** a été branché dans la boucle silencieuse (`--pont` ✓, appliqué à l'état avant
l'injection ✓) :

| réglage (amorce 256, suite 256) | perplexité de la suite | écart |
|---|---:|---:|
| A. lecture seule | **9,6503** | — |
| B. 1 pas silencieux, **PONT** appris | **453 609** | **+4 700 367 %** ✗✗ |
| B. 4 pas, PONT appris | 368 834 | +3 821 897 % ✗✗ |
| C. 16 jetons verbalisés | 9,5003 | **−1,55 %** ✓✓ |

* **le pont appris ne sauve pas la boucle** ✗✓ (453 609 contre 294 181 sans pont : **pire** ✗) — et ce
  n'est **pas** contradictoire avec le § 5 ✓ : le mapping est un **lecteur** ✓ (il *résume* l'état en
  une entrée plausible ✓, avec 69 % d'écart ✗), pas un **inverse** ✗✓. Une boucle exige que l'erreur ne
  s'accumule pas ✗ — or elle s'accumule ✓, et la mesure du **cycle** (§ `rapport-cycle-c2.md` : λ ≥ 3,7e4,
  pas expansif **du tout** ✗) dit **pourquoi** : *le pas d'état amplifie* ✗✓ ;
* **la conclusion des deux fiches se rejoint** ✓✓ : **lire** la pensée dans l'état est **facile** ✓
  (linéaire, à toutes les couches, jusqu'à 16 jetons d'avance ✓✓) ; **la faire tourner sur elle-même**
  est **difficile** ✗ (il faut une dynamique **contractante** ✗, et le modèle n'en a pas ✓). C'est
  exactement la différence entre **lire** et **penser** ✓✓ ;
* **la cible devient donc précise, et elle est chiffrée** ✓ : un langage abstrait n'est utile en boucle
  que si son évolution est **stable** ✗ — donc il faut apprendre **le pas** (état → état ✓), pas
  seulement **le pont** (état → entrée ✗). Le pont, lui, est **acquis** : il existe, il est linéaire, et
  il bat le jeton ✓✓.
