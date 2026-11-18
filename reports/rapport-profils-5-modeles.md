# Les profils sur cinq modèles entraînés — ce qui est stable, ce qui dépend du modèle

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ mesuré sur **cinq** modèles
> entraînés (34,3 M, fenêtres 256 · 256 · 512 · 1 024 · 2 048), même texte de 2 055 octets, quatre
> profils à poids identiques : `bloque` **±0,04 %** (aucun biais — le contrat tient), `flou`
> **+1,07 à +6,99 %** (toujours une perte, 5/5), `court` **−12,13 à +4,57 %** (le **sens dépend du
> modèle**, pas de la fenêtre déclarée).
>
> **Dispositif** : [`bench/drvm_profils.py`](../bench/drvm_profils.py) · cinq `drave-n0` de 34,3 M
> (384 dimensions, 6 blocs) réécrits à poids identiques pour chaque profil · perplexité native sur
> 2 055 octets de `data/corpus_mixte.txt` · données
> [`profils-5-modeles.json`](profils-5-modeles.json).

## La table

| modèle | fenêtre | `defaut` | `bloque` Δ | `flou` Δ | `court` Δ |
|---|---:|---:|---:|---:|---:|
| base-en-34m | 256 | 12,3656 | **+0,00 %** | **+1,94 %** | **+1,46 %** |
| base-multi-34m | 256 | 13,2374 | **+0,00 %** | **+1,07 %** | **+3,09 %** |
| mix1024-60k | 1 024 | 23,7480 | **+0,04 %** | **+2,09 %** | **−0,70 %** |
| propre512-8k | 512 | 133,6858 | **−0,04 %** | **+6,99 %** | **−12,13 %** |
| rope2048-20k | 2 048 | 18,5578 | **+0,00 %** | **+3,09 %** | **+4,57 %** |

*Les PPL absolues ne sont pas comparables entre modèles (données et étapes différents) ; seuls les
deltas internes le sont.*

## Ce que ça dit

1. **`bloque` ne biaise pas** : ±0,04 % sur cinq modèles, **des deux signes**. Le décalage est du
   bruit d'ordre de sommation (f32), pas une dérive systématique. C'est la meilleure preuve qu'on
   puisse donner du contrat de substitution : sur cinq modèles réels, il ne change pas le modèle.
2. **`flou` est toujours une perte** : +1,07 à +6,99 %, **5/5**. Une route vers `flou` a donc un
   **prix** en qualité, jamais un gain — le seul intérêt serait un gain de coût, et il n'y en a pas
   (le sigmoïde coûte plus cher qu'un seuil).
3. **`court` change de signe** : −12,13 % sur propre512-8k, +4,57 % sur rope2048-20k, +1,46 % sur
   base-en-34m. Le « `court` est gratuit » mesuré sur mix1024-60k était une **exception**, pas une
   règle. L'effet dépend du **modèle** (ce qu'il a appris à utiliser), pas de la fenêtre déclarée :
   propre512-8k (PPL 133, mal entraîné) *gagne* 12 % à couper sa fenêtre — une fenêtre courte qui
   régularise, hypothèse non testée ici ; rope2048-20k *perd* 4,6 % à la couper, parce qu'il s'en
   sert.

## Contrôles

- **Même texte, même limite, mêmes poids** : les quatre profils sont des réécritures du même
  manifeste ; seule la ligne `impl` change.
- **Sur le vrai modèle (34 M), les deux moteurs sont d'accord** : Rust ↔ numpy, mêmes logits à
  **1,526e-05** (≤ 1e-4) sur 64 octets — 50× plus que sur le petit modèle (3e-07), ce qui est
  attendu (384 dimensions, 6 blocs, ordres de sommation différents) mais reste sous le contrat.
- **Les deux cartes** (P1b) donnent le même plateau : la mesure n'est pas liée à une carte.

## Ce qui pourrait le rendre faux

- **Un seul texte, 2 055 octets, PPL par octet** : le texte est en distribution pour « mixte », pas
  nécessairement pour les quatre autres modèles ; un autre texte peut changer l'ampleur (pas le
  signe de `flou`, probablement).
- **Cinq modèles, une graine de données** : ils partagent la même architecture et sans doute la même
  graine d'initialisation ; ils ne couvrent pas la variété des modèles réels.
- **Les temps ne sont pas dans cette table** : la machine était partagée pendant le banc ; le seul
  chiffre de temps valide reste le banc contrôlé de N3.10 (0,694× pour `court`).
- **`flou` est un prototype précis** : le +1 à +7 % mesure cette sigmoïde-là, pas « le flou ».

## Ce que ça change

La politique de routage ne peut pas se concevoir **à partir du nom du profil** : `bloque` est
substituable partout (mesuré sur 5 modèles), `flou` coûte toujours, et `court` peut aider ou nuire
selon le modèle. **Toute route doit donc être mesurée sur le modèle et le corpus où elle sert** —
c'est exactement la leçon de R0.5/R06, étendue des seuils aux profils.

## Voir aussi

- [le banc](../bench/drvm_profils.py) · [les données](profils-5-modeles.json) ·
  [un modèle](rapport-profils-modele.md) · [court](rapport-n3-court.md) ·
  [les deux moteurs](rapport-n3-moteurs.md)
