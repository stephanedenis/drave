> Campagne : **campagne-benefices** · expérience **14**
> Titre : 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages
> Date réelle : **2026-10-08 23:27 HAE** (source : commit `8db69e8`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages

Batch 5, Qwen3-30B-A3B depuis le NVMe, `--lot` de 1 à 64 :

| lot | PPL | tok/s | octets lus | mur |
|---:|---:|---:|---:|---:|
| 1 | 7,6139 | 0,4 | **10 954 Mio** | 345 s |
| 4 | 7,6098 | 1,4 | 0 | 118 s |
| 8 | 7,6098 | 1,4 | 0 | 118 s |
| 32 | 7,6098 | 1,2 | 0 | 138 s |
| 64 | 7,6098 | 1,2 | 0 | 135 s |

**Le protocole a mesuré le cache de pages, pas le lot** : seule la première passe
a lu (10,9 Go, à froid) ; les suivantes ont tout trouvé en mémoire (0 octet lu) et
durent toutes ~2 minutes. La comparaison lot 1 / lot 4 n'est donc **pas** une
mesure du lot — c'est une mesure de « à froid contre à chaud ». Les PPL, elles,
sont identiques (7,6098 à partir du lot 4), ce qui confirme au moins que **le lot
ne change pas le résultat**.

Pour mesurer le lot, il faut un modèle plus gros que la mémoire — ce que le § 12
donne — ou vider le cache entre les passes, ce que la campagne ne peut pas faire
sans root.

### 14 bis. Le protocole corrigé : éviction sans root, et le résultat n'est pas celui qu'on attendait

`posix_fadvise(POSIX_FADV_DONTNEED)` jette les pages d'un fichier hors du cache
**sans être root** : c'est ce qui manquait. `tools/mesure_lot_disque.sh` évince le
modèle avant **chaque** réglage — le journal le confirme (« cache du modèle
évincé : 17,3 Go ») — puis lit les octets réellement lus dans `File system inputs`.

Qwen3-30B-A3B depuis le NVMe, 192 jetons, ctx 512, à froid à chaque passe :

| `--lot` | PPL | **octets lus** | mur | tok/s |
|---:|---:|---:|---:|---:|
| 1 | 7,4244 | **12 586 Mio** | 2 min 06 | 2,1 |
| 2 | 7,4228 | 17 520 Mio | 2 min 14 | 1,9 |
| 4 | 7,4228 | **21 006 Mio** | 4 min 12 | 0,9 |
| 8 | 7,4228 | 17 338 Mio | 4 min 03 | 0,9 |
| 16 | 7,4228 | 13 360 Mio | 1 min 18 | 3,8 |

**La perplexité est invariante au lot** (7,4228 dès le lot 2 — 0,02 % d'écart avec
le lot 1) : c'est le résultat net, et il confirme le § 20 sur un second modèle.

**Les octets lus, eux, ne baissent pas** — ils montent, puis redescendent, pour un
fichier de 17,3 Go. Le mécanisme est visible dans les compteurs du moteur : les
paires d'experts **par jeton** valent 1 840,7 M au lot 1 et 1 821,4 M au lot 16,
soit **le même chiffre** — le moteur regroupe bien les jetons par expert et ne
relit pas un expert pour chaque jeton du lot. Ce qui change avec le lot, c'est
**l'union des experts touchés par une passe** : sur 48 couches à 128 experts et
4 experts par jeton, une passe de 192 jetons finit par ouvrir **presque tous les
experts de toutes les couches**, quel que soit le découpage en lots. Le disque
n'est donc pas un levier de lot sur un MoE : il l'est sur un modèle **dense**, où
chaque passe relit les mêmes poids — et là, c'est le nombre de **jetons par passe**
qui amortit la lecture, pas la taille du lot.

**Ce que cette mesure ne dit pas** : les temps. Ils varient de 78 s à 252 s pour la
même quantité de calcul, sous une charge de fond de 30 à 40 (d'autres lectures de
modèles tournaient). La colonne tok/s n'est publiable qu'avec cette réserve, et
l'ordre de grandeur seul est utilisable.

**Et le seul modèle plus gros que la RAM REFUSE le lot — explicitement.** Restait à
faire la mesure dans le régime où le lot devrait le plus payer : V4.1-Flash,
365,7 Go sur 125 Go. Mesure à `--lot 1` d'abord : **39 216 Mio lus**, 129 s.
Puis `--lot 16` :

    chemin par LOTS et hyper-connexions : ce chemin n'est pas porté (le résidu y est
    additionné au lieu d'être remélangé par `hc_post`) — utilisez `--lot 1`, ou
    implémentez-le. Le lot n'est pas neutre ici : il change le modèle

**Le moteur refuse plutôt que de rendre un chiffre faux**, et il dit pourquoi : sur
un modèle à hyper-connexions, une passe par lots additionnerait le résidu au lieu
de le remélanger, donc **ce n'est pas le même modèle** qui serait mesuré. C'est le
comportement voulu, et c'est le seul résultat possible aujourd'hui : **le seul
modèle plus gros que la RAM de cette machine ne peut pas être exécuté par lots**.
La question « le lot amortit-il les lectures du disque quand le modèle ne tient
pas en mémoire » reste donc **ouverte**, et ce n'est pas un oubli : c'est un
chemin de code qui n'existe pas (le § 23 le porte comme manque).

---
