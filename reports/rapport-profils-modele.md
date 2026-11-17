# Les profils sur un modèle entraîné — ce que le contrat garantit, et ce qu'il ne garantit pas

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ mesuré — sur un modèle
> **entraîné** (34 301 224 paramètres, fenêtre 1 024), à poids identiques : `bloque` déplace la
> perplexité de **+0,04 %** (le contrat tient sur les logits, pas sur la perplexité), `flou` de
> **+2,09 %** (une dégradation réelle), `court` de **−0,70 %** (la fenêtre longue n'est pas utilisée
> ici). Les temps de cette passe ne sont **pas** interprétables (bruit).
>
> **Dispositif** : [`bench/drvm_profils.py`](../bench/drvm_profils.py) ·
> `work/n2ac/mix1024-60k.drvm` (384 dimensions, 6 blocs, 8 experts, fenêtre 1 024, 34,3 M de
> paramètres) réécrit à poids identiques pour chaque profil ; perplexité native sur **2 055 octets**
> de `data/corpus_mixte.txt` (in distribution) ; données [`profils-34m.json`](profils-34m.json).

## Ce qui est mesuré

| profil | perplexité | Δ vs `defaut` | temps (bruité) |
|---|---:|---:|---:|
| `defaut` | **23,7480** | — | 74,3 s |
| `bloque` (même fonction, somme tuilée) | **23,7585** | **+0,04 %** | 61,6 s |
| `flou` (seuil du k-WTA → sigmoïde) | **24,2443** | **+2,09 %** | 76,9 s |
| `court` (fenêtre / 4) | **23,5824** | **−0,70 %** | 69,6 s |

## Ce que ça établit — et la nuance qui compte

1. **Le contrat de substitution tient sur un vrai modèle** : `bloque` ne change pas le corps ; les
   logits diffèrent de ~5e-7, sous la tolérance déclarée (1e-4). **Mais la perplexité, elle, bouge
   de 0,04 %** : c'est une fonction **non linéaire** de tous les logits, et un décalage de 5e-7 par
   position s'y accumule. L'indifférence se juge sur le **corps**, pas sur les agrégats — et il faut
   le dire, sinon on promet une invariance qui n'existe pas.
2. **`flou` coûte +2,09 % de perplexité** : une variante floue n'est pas gratuite. C'est le prix
   mesuré d'une autre fonction, sur ce modèle et ce texte.
3. **`court` ne coûte rien ici (−0,70 %)** : la fenêtre de 1 024 n'est pas utilisée au-delà de 256
   sur ce modèle — résultat cohérent avec la fiche N3.10.

## Ce qui pourrait le rendre faux

- **Un texte, un modèle, un découpage** : 2 055 octets du début de `corpus_mixte.txt` ; la
  perplexité est par octet ; un autre texte ou un autre modèle peut inverser `court` et changer
  l'ampleur de `flou`.
- **Les temps ne sont pas exploitables ici** : `bloque` (coût identique à `defaut`) varie de −17 % à
  +4 % selon la passe — la machine était partagée. Les chiffres de temps valides sont ceux du banc
  contrôlé (N3.10 : **0,694×** sur 11 passes alternées).
- **Le drift de perplexité dépend du nombre de positions** : plus le texte est long, plus le
  décalage de 5e-7 par logit s'accumule ; 0,04 % à 2 055 octets n'est pas une borne.
- **`flou` est une différence *conçue*** : le +2,09 % mesure ce prototype précis, pas « le flou » en
  général.

## Ce que ça change

Le catalogue de profils a maintenant une **lecture de qualité sur un modèle entraîné** : une
substitution qui tient (sur le corps), une dégradation chiffrée (`flou`, +2,09 %), une coupe
gratuite ici (`court`, −0,70 %). Pour un routage, cela donne le prix à payer en face du gain de
temps — mais le gain de temps n'existe que pour `court`, et seulement là où l'attention domine.

## Voir aussi

- [le banc](../bench/drvm_profils.py) · [les données](profils-34m.json) ·
  [les variantes](rapport-n3-variante.md) · [court](rapport-n3-court.md) ·
  [les deux moteurs](rapport-n3-moteurs.md)
