# N2 — La porte < 2,5 sur le corpus propre, attaquée avec la fenêtre

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-03 · **Verdict** :
> la porte **< 2,5 n'est pas atteinte** : le meilleur point est **2,7856** en
> validation et **2,8566** en test (fenêtre 512, contexte 1 024) — il manque **0,29**. Mais la
> fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),
> la fenêtre 512 fait **2,9726 → 2,8443 → 2,7856** de 128 à 1 024 octets, quand la fenêtre 128
> fait **2,9027 → 3,0464 → 3,1107** : elle gagne à courte longueur, puis elle est **0,33
> derrière** à 1 024.
> Les deux bras battent la chaîne honnête de N2.h (val **3,0904**, test **3,1960**).

## La question

La porte de N2 est **PPL < 2,5 sur le corpus propre**, tenu à l'écart par construction (N2.h :
corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec
la recette à fenêtre 128 ; la porte était à **0,59**. Depuis, la nuit a montré que la **fenêtre
entraînée** est le levier de longueur (fiches [`n2-fenetre`](rapport-n2-fenetre.md),
[`n2-r12-2048`](rapport-n2-r12-2048.md)) : la même recette à fenêtre 1 024 a donné **2,9955** en
domaine wiki à 128 octets, **2,6256** à 1 000 et **2,5429** à 4 000. La question de cette fiche :
**la fenêtre rapproche-t-elle la porte 2,5 sur son propre corpus ?**

## Le dispositif

- **Corpus** : `data/corpus_propre/` — train **3 244 858 octets**, val **180 224**, test 180 224 ;
  canal recalculé par `tools/canal_structure.py` (une classe par octet).
- **Deux bras à octets égaux** (33 Mo vus), RoPE, 34,3 M, lot 8, lr 3e-4, graine 1, init
  `base-wiki-45m` (un modèle de wikipédia : le corpus propre lui est **doublement étranger**) :
  1. **fenêtre 512**, 8 000 pas × 8 × 512 ;
  2. **fenêtre 256** (seq 128), 32 000 pas × 8 × 128.
- **Mètre** : `eval_longueurs.py --val data/corpus_propre --rope` (val et test du corpus propre,
  canal fourni), et le protocole N2.h pour la comparaison à 3,0904.

## Ce qui est mesuré

Validation (`val`, 180 224 octets) et test (`test`, 180 224 octets) du corpus propre, canal
fourni, PPL par longueur :

| bras (33 Mo vus) | val 128 | val 256 | val 512 | val 1 024 | test 128 | test 512 | test 1 024 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **fenêtre 128** (32 000 pas) | **2,9027** | 2,9034 | 3,0464 | 3,1107 | **3,0150** | 3,1104 | 3,1876 |
| **fenêtre 512** (8 000 pas) | 2,9726 | **2,8988** | **2,8443** | **2,7856** | 3,0649 | **2,8875** | **2,8566** |
| N2.h, chaîne honnête (référence) | 3,0904 | — | — | — | 3,1960 | — | — |
| **porte** | **2,5** | | | | | | |


## Lecture

1. **La porte n'est pas atteinte, et elle n'est pas loin.** Le meilleur chiffre de la nuit sur le
   corpus propre est **2,7856** (val, contexte 1 024) et **2,8566** (test) : il manque **0,29** en
   validation. C'est **moins** que les 0,59 de N2.h, et c'est obtenu avec **33 Mo vus** — 8 000
   pas, 28 minutes de GPU.
2. **La fenêtre est le seul levier qui fait descendre la courbe.** Le bras 512 vaut 2,9726 à 128
   octets et **2,7856** à 1 024 : il **gagne** 0,19 en regardant plus loin. Le bras 128 vaut
   2,9027 à 128 octets et **3,1107** à 1 024 : il **perd** 0,21. Sur un corpus de 3,24 Mo, la
   fenêtre reste le levier de longueur — le corpus n'y change rien.
3. **À courte longueur, la fenêtre 128 est meilleure** (2,9027 contre 2,9726) : la fenêtre large
   paie son démarrage à froid, exactement comme sur le wiki. Le classement s'inverse dès 256
   octets.
4. **Les deux bras battent la chaîne honnête de N2.h** (3,0904 val / 3,1960 test) : à 2,9027 et
   3,0150 pour le bras 128, la recette RoPE + init `base-wiki-45m` est **meilleure de 0,19** sur
   le même corpus propre, sans distillation. La comparaison est indicative (l'init diffère), mais
   l'écart est du même ordre que le gain de la fenêtre.
5. **Le prix de la porte ne se paie plus en octets.** Il reste 0,29 à gagner ; sur le wiki,
   +144 Mo vus ont acheté −0,37 à 128 octets, mais ici le corpus fait **3,24 Mo** et nous l'avons
   vu **dix fois** : allonger le run, c'est de la mémorisation, pas de la donnée. La suite est la
   **capacité** (34,3 M aujourd'hui) ou un **corpus propre plus large** — pas un run plus long.

## Ce qui pourrait le rendre faux

- **L'initialisation est un modèle de wiki** : les deux bras partent de `base-wiki-45m`, donc ils
  apprennent le corpus propre en **affinage**, pas depuis zéro. N2.h partait d'un point différent ;
  la comparaison à 3,0904 est **indicative**, la comparaison entre les deux bras est contrôlée.
- **3,24 Mo de train pour 33 Mo vus** : environ **10 époques**. C'est peu pour mémoriser, assez
  pour surapprendre ; la val est disjointe par chunks (0 % de fuite vérifié), donc la mesure tient,
  mais la marge est mince.
- **Un lancement par bras**, comme partout cette nuit.
- **La porte se mesure sur le corpus propre avec un modèle entraîné dessus** ; si elle n'est pas
  atteinte ici, elle ne dit rien des autres corpus.

## Fichiers

- Modèles : `work/n2ac/propre512-8k.pt`, `work/n2ac/propre128-32k.pt`.
- Bancs : `work/n2ac/entrainer_rope.py`, `eval_longueurs.py`, `chaine_porte.sh`.
- Mesures : `reports/n2-porte-propre.json` ; fiches amont
  [`n2-propre`](rapport-n2-propre.md), [`n2-fenetre`](rapport-n2-fenetre.md).
