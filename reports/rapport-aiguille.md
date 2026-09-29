# L'aiguille dans la botte de foin : où en est la mesure de qualité

La perplexité ne dit **pas** si un modèle retrouve une information. Ce rapport
raconte la remise en route de la seule mesure qui le dise, et ce qu'elle a
immédiatement appris.

## 1. Ce qui n'allait pas dans la v1

La v1 (`tools/aiguille.py`, conservée dans l'historique) plantait un code dans un
contexte dont le remplissage était **la même phrase recopiée** jusqu'à la
longueur voulue, posait la question, et n'accordait que **8 jetons** de réponse.
Résultat : 6 sondes sur 6 échouaient sur Qwen2.5-0.5B, et 9,6 minutes pour un
échec sur Qwen3-30B-A3B. Le test a été arrêté à l'époque, faute de budget.

Trois défauts, tous de protocole :

1. **remplissage répété** : un modèle peut répondre en devinant la structure du
   texte, et la sonde ne teste plus la mémoire mais la régularité ;
2. **réponse trop courte** : un code peut sortir au deuxième ou troisième jeton
   d'une réponse ; s'arrêter à 8 jetons fait échouer des sondes que le modèle
   savait résoudre ;
3. **préremplissage séquentiel** : le moteur ne batchait que la perplexité, donc
   chaque sonde payait son contexte jeton par jeton.

## 2. La v2

`tools/aiguille.py` a été réécrit :

* remplissage pris dans **un vrai corpus** (`data/wikitext2_test.txt`, le jeu de
  test WikiText-2), et **fenêtre différente à chaque sonde** pour qu'elles ne
  partagent pas leur texte ;
* réponse de **40 jetons** par défaut (`--n`) ;
* préremplissage **par lots** (`--lot`) — la génération l'utilise désormais
  (`Model::lot`), ce qui n'était vrai que de la perplexité ;
* le contexte réellement construit est **relu dans la sortie du moteur**, et une
  sonde dont le moteur n'a pas démarré est signalée comme telle (« moteur
  muet ») au lieu d'être comptée comme un échec du modèle ;
* options `--gpu` / `--gpu-kv` pour mesurer aussi l'effet du KV déporté ;
* journal markdown (`--journal`) pour citer les chiffres sans les recopier.

## 3. Témoin : Qwen2.5-1.5B (le protocole est-il valable ?)

| contexte | profondeur | trouvé | secondes | contexte réel |
|---|---|---|---|---|
| 512 | 0,10 | **oui** | 87,1 | 698 jetons |
| 512 | 0,50 | **oui** | 82,9 | 698 |
| 512 | 0,90 | **oui** | 82,4 | 698 |
| 2048 | 0,10 | **oui** | 241,1 | 2 147 |
| 2048 | 0,50 | **oui** | 244,2 | 2 147 |
| 2048 | 0,90 | **oui** | 242,4 | 2 147 |

**6 sondes sur 6** sur un modèle de 1,5 milliard de paramètres — là où la v1
échouait 6 fois sur 6 avec un modèle deux fois plus petit. Le protocole mesure
donc bien ce qu'il prétend : le remplissage varié et la réponse longue suffisent
à rendre le test valide, et l'échec de la v1 était en grande partie un artefact.

## 4. Modèles capables et contexte long

Deux campagnes, mêmes profondeurs (0,1 / 0,5 / 0,9), `--n 40` :

* **Qwen3-30B-A3B-Instruct-2507** (MoE, 3 B actifs), contexte 2048, `--lot 256`,
  journal `reports/aiguille-30b.md` ;
* **gpt-oss-120b** (MXFP4, MoE 4 experts sur 128), contexte **4096**,
  `--lot 512 --gpu-kv` — le KV déporté en VRAM rend l'attention plate et donc la
  passe abordable, journal `reports/aiguille-gpt-oss.md`.

Les tableaux complets sont dans les journaux cités ; ce qui compte ici est le
taux de réussite par profondeur, parce qu'il dit si le modèle *retrouve* au fond
de la botte de foin ou seulement au début.

### Ce que la campagne a coûté, et pourquoi c'est le vrai obstacle

Une sonde de 2 048 jetons sur le 30B prend **8 à 25 minutes** selon la charge de
la machine (préremplissage à ~5 jetons/s), et une sonde de 4 096 jetons sur
gpt-oss coûte une quinzaine de minutes. Le préremplissage par lots et le KV
déporté divisent ces temps, mais **la mesure de qualité à contexte long reste
l'opération la plus chère du projet** — c'est un fait à connaître avant de
promettre des chiffres à 1 M.

## 5. Ce qui reste à faire sur ce front

1. **Étendre la grille** : 8 192 et 16 384 jetons sur gpt-oss (le corpus
   `data/wikitext2_test.txt` fait ~90 k jetons, il y a de quoi) ;
2. **Plusieurs codes par sonde** : compter combien de codes distincts un modèle
   retrouve dans le MÊME contexte donne une courbe, pas un point ;
3. **Sondes par paires** : la même information à deux profondeurs différentes
   dans le même contexte, pour séparer « le modèle a oublié » de « le modèle n'a
   pas vu » ;
4. **Attention creuse** : mesurer le taux de réussite avec `--attn-topk 256`
   (qui AMÉLIORE la perplexité à 2 048) — la question devient « la restriction
   casse-t-elle la recherche ? ».
