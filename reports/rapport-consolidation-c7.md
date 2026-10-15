# C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**)

> Campagne : **cerveau** · expérience : la consolidation (plan § C7 : « rejouer une trace →
> calculer la perte → mettre à jour les poids »), et la seule question du plan : **la perplexité
> baisse-t-elle sur un jeu NON rejoué ?**
> Question : le rejeu d'une journée d'expérience (dix morceaux de texte) met-il quelque chose dans
> les poids — et ce quelque chose sert-il **ailleurs** que sur ce qui a été rejoué ?
> Verdict : **oui en domaine, non hors domaine.** Après deux époques sur 10 morceaux (~10 000
> jetons), le MOTEUR rend, sur des textes **jamais rejoués** : m20 **19,1247 → 15,9804**
> (**−16,4 %**), m32 **7,4250 → 6,9333** (**−6,6 %**) — et sur un **autre corpus** (corpus_en_val,
> jamais vu) **17,2679 → 17,4919** (**+1,3 %**). La consolidation **spécialise** : elle paie là où
> l'expérience ressemble au monde, elle coûte ailleurs. Le contrôle « rejeu mélangé » fait
> exploser la validation (15,97 → 130,5) et l'époque choisie est **0** — le protocole refuse de
> publier un modèle dégradé (0,00 %).
> Date réelle : **2026-10-14 21 h 05-22 h 40 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein` (LoRA sur les 8 premières couches,
> `W ← W + (α/r)·B·A`, rang 8 = **360 448 paramètres, 0,07 % du modèle**), puis
> `tools/exporter_gguf_dense.py` (fusion + GGUF) et `drave --ppl` (le chiffre publié est celui du
> **moteur**) · rejeu m0..m9 · validation m10+m11 (époque choisie : **2**) · tests m20 et m32
> (jamais rejoués) · hors domaine : `data/corpus_en_val.txt`, 1 024 jetons à la position 300 000.

## 1. Les chiffres, et ils sont ceux du moteur

| jeu | avant (moteur) | après consolidation (moteur) | écart | torch (avant → après) |
|---|---:|---:|---:|---:|
| **m20** (même domaine, jamais rejoué) | 19,1247 | **15,9804** | **−16,4 %** | 18,4607 → 15,4351 (−16,4 %) |
| **m32** (même domaine, jamais rejoué) | 7,4250 | **6,9333** | **−6,6 %** | 7,1787 → 6,7052 (−6,6 %) |
| **hors domaine** (autre corpus) | 17,2679 | 17,4919 | **+1,3 %** | 16,7324 → 16,9753 (+1,5 %) |

* **le moteur retrouve torch à 3 %** (quantification Q8_0, le même écart que partout ailleurs) :
  la consolidation est un chiffre du dépôt, pas un chiffre de banc ;
* **les deux textes en domaine s'améliorent, et pas du même facteur** (−16,4 % et −6,6 %) : le
  gain dépend du texte, comme tout le reste de ces mesures ;
* **le hors-domaine se dégrade légèrement** (+1,3 %) : c'est peu, mais c'est le **signe** qui
  compte — l'expérience rejouée n'est pas neutre pour le reste du monde.

## 2. Les contrôles (sans eux, un gain ne veut rien dire)

| contrôle | ce qu'il devait montrer | mesuré |
|---|---|---|
| **LoRA nul fusionné** (B = 0) | l'invariant du plan C7 : « à taux nul, le modèle est **bit à bit** identique » | le GGUF exporté est **identique au bit** (`cmp`, 531 068 480 octets) |
| **LoRA aléatoire** fusionné (même forme) | que la fusion agit — sinon le contrôle précédent ne prouverait rien | fichier **différent**, et perplexité moteur **17,4268 → 17,1655** (×0,985) |
| **lecteur de sortie seul** (dessin A) | que le lecteur appris ne touche pas le modèle complet | GGUF **identique au bit** |
| **rejeu MÉLANGÉ** (mêmes jetons, ordre détruit) | que le gain vient de la **séquence**, pas du volume de données | la validation explose (**15,97 → 17,4 → 39,8 → … → 130,5**), l'époque choisie est **0** ⇒ chiffres **inchangés (0,00 %)** |

**Le contrôle du LoRA aléatoire est le plus instructif, et il borne le résultat** : une
perturbation **aléatoire** de même forme améliore déjà la perplexité de **1,5 %** sur ce texte.
Autrement dit, il existe un « gain gratuit » de l'ordre du pour cent dès qu'on touche aux poids.
Le **−16,4 %** de la consolidation est **dix fois** au-dessus de cette borne — mais toute mesure
future de consolidation devra citer la sienne, sinon elle publiera du bruit déguisé en
apprentissage.

Et le contrôle du **rejeu mélangé** montre autre chose, qui vaut d'être gardé : le protocole
(époque choisie sur la validation) **refuse** le modèle dégradé et rend exactement le modèle de
départ. Un entraînement qui ne vaut rien ne se publie pas ici — c'est la règle de sélection qui
le garantit, pas la prudence de l'opérateur.

## 3. Ce que ça change pour le cerveau

* **la faculté « consolidation » existe maintenant dans Drave**, avec sa mesure : c'est la
  première fois qu'une expérience **modifie durablement les poids** et que l'effet est lu par le
  moteur ;
* **le mécanisme le plus efficient à cette échelle** est un LoRA de rang 8 sur les **8 premières
  couches** — 0,07 % des paramètres, deux époques, 10 morceaux : le reste du modèle ne bouge pas,
  et le fichier exporté reste un GGUF ordinaire de 0,53 Go ;
* **mais la consolidation n'est pas gratuite** : elle **spécialise**. Le plan du cerveau doit donc
  la lire comme un arbitrage (adapter vs oublier), pas comme un gain — et c'est exactement ce que
  la mémoire épisodique (C6) évite : elle **ajoute** un magasin sans toucher aux poids. Le choix
  « consolider ou se souvenir » est donc un vrai choix de conception, et il est désormais chiffré
  des deux côtés ;
* **le moteur n'entraîne toujours pas** (manque **M6**) : la boucle est **rejeu (moteur) →
  mise à jour (torch) → mesure (moteur)**. Ce qui est nouveau, c'est que la boucle est **complète
  et vérifiée** : le rejeu est exact (DRVF, 0,00e0), la fusion est exacte (LoRA nul ⇒ fichier
  identique au bit), et la mesure est celle du moteur.

## 4. Ce que cette fiche ne dit pas

* **une seule graine, un seul volume de rejeu** (10 morceaux) : ni la courbe « plus de rejeu »,
  ni la variabilité entre exécutions (mesurée à ±10 % pour les bras qui rétropropagent,
  `reports/rapport-n4-porte-execution.md` § 4) ne sont ici ;
* **la consolidation n'est pas comparée à la mémoire épisodique** sur la même expérience : les
  deux mécanismes sont mesurés séparément (C6 : rappel 96,3 %, round-trip exact), pas côte à côte
  sur une tâche qui aurait besoin des deux ;
* **le hors-domaine n'est qu'un texte** (1 024 jetons d'`corpus_en_val`) : le « +1,3 % » est un
  signe, pas une loi d'oubli — il faudrait plusieurs corpus et plusieurs tailles de rejeu ;
* **rien n'est mesuré sur la génération** : la consolidation améliore une perplexité, pas
  (encore) une réponse ;
* **le rang, la profondeur du LoRA et le taux d'apprentissage ne sont pas balayés** : rang 8 / 8
  couches / 1e-3 est un réglage, pas un optimum — la question « quel est le modèle le plus
  efficient pour consolider » demanderait la courbe.
