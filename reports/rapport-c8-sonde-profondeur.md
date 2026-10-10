# C8 — le réflexe : l'état intermédiaire CONTIENT le prochain jeton, c'est la TÊTE qui ne sait pas le lire

> Campagne : **cerveau** · expérience : sonde linéaire sur l'état de la couche 16
> Question : un chemin court (s'arrêter à la couche 16, appliquer une tête) ne sait rien — mais
> est-ce l'**état** qui est pauvre, ou la **tête** qui ne sait pas le lire ? Autrement dit :
> **faut-il entraîner une tête par profondeur, ou C8 est-il hors de portée ?**
> Verdict : **l'information est là, et elle est LINÉAIREMENT accessible** — une sonde ridge sur
> l'état intermédiaire prédit le prochain jeton (parmi les 256 plus fréquents) avec **40,8 %** de
> justes à **16 couches** (43,1 % à 15) sur des positions **jamais vues**, contre **4,0 %** pour
> la classe majoritaire et **0,39 %** pour le hasard — **et cela dès 4 couches** (45,9 %). La tête
> empruntée, elle, rend **1 127 368** de perplexité à 16 couches contre **9,4341** pour le modèle
> complet : **le maillon faible est la tête**, et C8 a un sens. La courbe complète est au § 3.
> Date réelle : **2026-10-10 11:35 HAE**.
> Protocole : `tools/c8_sonde_lineaire.py` (capture par `drave --couches 0:15 --tete-partielle
> --etat-sortie F --etat-pos 4,5,…,1023`), Qwen2.5-0.5B-Q8_0, `ids_0.5B-Q8.txt`, 1 024 jetons.

## 1. Le fait mesuré, et il est brutal

| chemin | perplexité (1 023 jetons) |
|---|---|
| modèle complet (24 couches) | **9,4341** |
| **réflexe** : **15** couches (`--couches 0:15`), puis la tête du modèle (`--tete-partielle`) | **728 388,7546** |
| **réflexe** : **16** couches (`--couches 0:16`) | **1 127 367,6856** |

Un facteur **120 000** à 16 couches. C'était la mesure du premier pas de C8, et elle avait été lue
comme « un chemin court ne peut pas lire un état intermédiaire » (cos 0,145 entre l'état et ce que
la tête attend). **Cette lecture attribuait à l'état ce qui appartient à la tête.**

## 2. La sonde : ce que l'état contient vraiment

Protocole : capturer l'état de la couche 16 (896 canaux, juste avant la norme finale) à
1 019 positions ; cible = **le jeton suivant** du corpus ; sonde = régression ridge fermée
`W = (XᵀX + λI)⁻¹ Xᵀ Y` sur les **256 jetons les plus fréquents** ; partage **train/test par
position** (la première moitié entraîne, la seconde évalue : aucune position de test n'est vue).

| mesure | valeur |
|---|---|
| **sonde linéaire, test** | **43,1 %** |
| classe majoritaire (référence) | 4,0 % |
| hasard uniforme sur 256 classes | 0,39 % |
| fréquence du jeton le plus fréquent du corpus | 5,27 % |

**43,1 % là où la référence est à 4 %** : l'information du prochain jeton est **présente** dans
l'état de la couche 16 et elle est **linéairement décodable**. Un réflexe à cette profondeur n'est
donc pas condamné par la pauvreté de l'état.

## 3. La courbe PROFONDEUR → décodabilité : où placer un réflexe

Le pilote `tools/c8_carte_profondeur.sh` capture l'état à la sortie de N couches et lance la même
sonde, pour N = 4, 8, 12, 16, 20, 24 (1 024 jetons, 256 classes, mêmes partages) :

| couches exécutées | perplexité du chemin tronqué | sonde linéaire (test) |
|---|---|---|
| 4 / 24 | 12 401 653,7360 | 45,9 % |
| 8 / 24 | 3 776 712,4298 | 45,5 % |
| 12 / 24 | 3 282 793,4472 | 46,1 % |
| **16 / 24** | **1 127 367,6856** | **40,8 %** |
| 20 / 24 | 3 210,0126 | 37,8 % |
| **24 / 24** | **9,4341** | 34,8 % |

**Deux lectures, et elles ne disent pas la même chose — c'est important de ne pas les confondre.**

1. **La décodabilité linéaire est NETTE ET TÔT** (≈ 46 % dès 4 couches, 40,8 % à 16) : l'état
   contient le prochain jeton bien avant la fin du réseau. Un réflexe n'est donc pas condamné par
   la pauvreté de l'état à une profondeur donnée ;
2. **la qualité du chemin tronqué, elle, n'arrive que tard** : 1,1 million de perplexité à 16
   couches, 3 210 à 20, 9,43 seulement à 24. Autrement dit, **la tête du modèle ne sait lire
   qu'un état de fin de réseau** — et il faudra une tête **entraînée par profondeur** pour
   exploiter ce que la sonde voit tôt.

Contre-intuitif mais cohérent : la sonde est **meilleure tôt** (les premiers étages sont proches
des jetons, la prédiction y est presque « de bigramme ») et **moins bonne tard** (les états
profonds portent du contexte qui n'est pas aligné sur une décision restreinte à 256 classes) —
alors que le chemin complet, lui, s'améliore évidemment avec la profondeur. Les deux mesures ne
mesurent pas la même chose : **présence de l'information** d'un côté, **qualité du modèle
tronqué** de l'autre.

**Le contrôle qui valide le harnais** : `--couches 0:24 --tete-partielle` rend **9,4341**, soit
exactement le modèle entier — c'est la vérification qui a révélé le piège ci-dessous.

### Le piège attrapé par ce contrôle : `--couches a:b` EXCLUT `b`

Le premier passage du pilote étiquetait « 4/24, 8/24, 12/24, 16/24, 20/24, 24/24 » des plages
`--couches 0:3`, `0:7`, … qui exécutent **une couche de moins** : les chiffres étaient justes, les
**étiquettes fausses** d'une couche. La vérification qui l'a montré tient en une ligne —
`--couches 0:24 --tete-partielle` doit rendre **exactement** la perplexité du modèle entier
(9,4341), et `--couches 0:23` en rend 83,12 (23 couches) : la borne est **exclue**. C'est la même
famille de défaut que le reste du dépôt : un chiffre juste sous une étiquette fausse se lit comme
un chiffre faux.

## 4. Protocole, pour rejouer

```bash
# la courbe complète (4 → 24 couches), une commande :
tools/c8_carte_profondeur.sh                       # PROFONDEURS="4 8 12 16 20 24" par défaut

# une profondeur seule :
D=./drave-core/target/release/drave; M=models/Qwen2.5-0.5B-Q8_0.gguf
POS=$(seq -s, 4 1023)
$D "$M" --ppl /tmp/campagne24/ids_0.5B-Q8.txt --limit 1024 --ctx 1024 --threads 8 \
   --couches 0:16 --tete-partielle --etat-sortie /tmp/c8/etat --etat-pos "$POS"
python3 tools/c8_sonde_lineaire.py --etats /tmp/c8/etat --ids /tmp/campagne24/ids_0.5B-Q8.txt \
   --limite 1024 --classes 256
```

**Le contrôle à refaire à chaque fois** : `--couches 0:<n_layer> --tete-partielle` doit rendre la
perplexité du modèle entier. Si ce n'est pas le cas, c'est le harnais qui est faux, pas le
modèle.

Deux défauts de harnais attrapés en écrivant la sonde, tous deux du même genre (un instrument qui
ne dit rien au lieu de dire qu'il ne peut rien dire) : les `ids` de la campagne sont un **CSV sur
une ligne**, qu'un découpage sur les blancs lit comme **zéro** jeton ; et une liste d'états vide
rendait « 0 position × 896 canaux » au lieu de s'arrêter. Corrigé : lecture CSV **ou** une par
ligne, et arrêt explicite si les entrées sont vides.
