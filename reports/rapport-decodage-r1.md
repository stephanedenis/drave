# Le décodage du 73 M à 13 000 pas : top-40 à T=0,5 bat le greedy sur tous les axes

> **Ligne de roadmap** : N4 (l'usage du natif) · **Date** : 2026-11-18 · **Verdict** : ✅ mesuré — sur
> le checkpoint r1 (73 M, 13 000 pas), le **greedy** donne 0,902 de mots valides mais **5,7 de
> répétition**, 0,149 d'écho et 0,329 de diversité ; **top-40 à T=0,5** donne **0,907** de mots
> valides, **1,7 de répétition**, 0,075 d'écho et **0,835** de diversité. Le critère du palier 1
> (« répétition ≤ 3 ») est **atteint** — et le greedy n'est pas le régime à retenir.
>
> **Dispositif** : [`bench/balayage_decodage.py`](../bench/balayage_decodage.py) · 10 régimes
> (greedy + top_k ∈ {20, 40, 80} × T ∈ {0,5, 0,8, 1,0}) · 20 prompts, 128 octets, graine 1234,
> même banc et mêmes métriques que la fiche du 34 M · données
> [`balayage-decodage-r1.json`](balayage-decodage-r1.json).

## La grille

| régime | mots/texte | mots valides | distinct-2 | répétition | écho |
|---|---:|---:|---:|---:|---:|
| greedy | 27,1 | 0,902 | 0,329 | **5,7** | **0,149** |
| **top-40 / 0,5** | 24,1 | **0,907** | 0,835 | **1,7** | 0,075 |
| top-20 / 0,5 | 25,6 | 0,897 | 0,888 | 1,4 | 0,079 |
| top-20 / 0,8 | 22,8 | 0,871 | 0,979 | **1,1** | 0,035 |
| top-40 / 0,8 | 22,8 | 0,817 | 0,974 | 1,1 | 0,035 |
| top-80 / 0,5 | 25,4 | 0,875 | 0,825 | 2,4 | 0,094 |
| top-80 / 0,8 | 22,9 | 0,862 | 0,963 | 1,1 | 0,033 |
| top-20 / 1,0 | 21,5 | 0,806 | 0,995 | 1,0 | 0,037 |
| top-40 / 1,0 | 20,9 | 0,706 | 0,991 | 1,0 | 0,028 |
| top-80 / 1,0 | 20,6 | 0,704 | 0,995 | 1,0 | 0,019 |

## Lecture

1. **Le greedy n'est pas un régime, c'est un piège** : 0,902 de mots valides mais une répétition de
   5,7, un écho de 0,149 (il recopie le prompt) et une diversité de 0,329. Les mots sont bons, la
   phrase ne l'est pas.
2. **top-40 à T=0,5 domine le greedy sur tous les axes** : +0,005 de mots valides, **×2,5 de
   diversité**, **÷3,4 de répétition**, **÷2 d'écho**. C'est le régime à retenir par défaut.
3. **La température est le levier de diversité, pas le top-k** : à T=0,5, d2 ≈ 0,83–0,89 ; à T=0,8,
   d2 ≈ 0,96–0,98 ; à T=1,0, d2 ≈ 0,99 mais les mots valides tombent à 0,70–0,81.
4. **Le critère du palier 1 est atteint en échantillonnage** : répétition 1,1–2,4 ≤ 3 pour tous les
   réglages sauf le greedy (5,7). La formulation du critère doit nommer le décodage.

## Les contrôles

- **Le même banc que le 34 M** (20 prompts, 128 octets, mêmes métriques, même graine) : la
  comparaison avec la fiche du 34 M est directe.
- **Le greedy est le point de référence** dans la grille : si le balayage ne faisait que reproduire
  le banc à trois réglages, il ne dirait rien ; il ajoute 7 régimes et **un** gagnant clair.
- **Les métriques se contredisent exprès** : le taux de mots valides sature (~0,90) et ne discrimine
  plus ; ce sont la répétition, l'écho et la diversité qui séparent les régimes. Un banc qui ne
  regarderait que les mots valides conclurait « le greedy est le meilleur ».

## Ce qui pourrait le rendre faux

- **Un checkpoint, 20 prompts, 2 560 octets par régime** : le classement peut bouger avec d'autres
  prompts ; la grille de températures est grossière (0,5 / 0,8 / 1,0).
- **Les métriques sont lexicales** : ni grammaticalité ni sens ; la fiche de grammaticalité montre
  que GV et ciment mesurent surtout la classe du token de boucle.
- **Le tirage multinomial n'est pas reproductible au bit** : la graine est fixée, mais deux
  exécutions peuvent différer légèrement (les chiffres sont des moyennes sur 20 textes).
- **Aucun coût mesuré** : les 10 régimes tournent à ~125 octets/s sur GPU, le décodage n'est pas le
  goulot.

## Ce que ça change

Le produit (`drave generer`, le service) doit passer au **top-40 / T=0,5** par défaut : le greedy
n'est bon qu'en apparence. Et le critère du palier 1 devient mesurable : « répétition ≤ 3 en
échantillonnage top-40/0,5 » est **tenu** à 13 000 pas, ce qui déplace la question vers la
**grammaticalité** et la **composition**, pas vers la boucle.

## Voir aussi

- [le banc](../bench/balayage_decodage.py) · [les données](balayage-decodage-r1.json) ·
  [r1](rapport-r1-13000-pas.md) · [la grammaticalité](rapport-grammaticalite-100m.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
