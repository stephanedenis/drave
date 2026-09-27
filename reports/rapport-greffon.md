# Greffon : plomberie d'apprentissage

Première brique de la boucle d'apprentissage : **charger un modèle augmenté de
nœuds, sans réentraînement**, et mesurer la perplexité avant/après. C'est ce qui
rend l'étape A du [programme de recherche](../docs/programme-recherche.md)
exécutable.

---

## 1. Le mécanisme

Un greffon ajoute **un neurone** à une couche, à la forme SwiGLU du réseau :

```
a = silu(u · x) · (v · x)          contribution ajoutée au flux résiduel : a · d
```

`--patch <fichier.bin>` charge `(u, v, d)` pour une couche. Format binaire :
`QPAT | version | couche | n | u[n] | v[n] | d[n]`, en f32 little-endian.

Pourquoi c'est intéressant malgré le verdict hebbien : **le produit de deux
formes linéaires est quadratique.** Prendre `u` sur une ligne existante de `gate`
et `v` sur une **autre** ligne de `up` fabrique une caractéristique que le réseau
n'a jamais calculée — les 4 864 neurones d'origine n'apparient que `gate[i]` avec
`up[i]`. Le produit croisé `gate[i] · up[j]`, `i ≠ j`, est hors de l'espace des
neurones existants.

*(C'est la version exploitable de la conclusion du capteur hebbien : un nœud
linéaire est redundant, un nœud-produit ne l'est pas.)*

## 2. Validation

Perplexité sur 1 020 tokens de WikiText-2, couche 12, greffon croisé
`gate[0] × up[7]`, `d` pris sur la colonne correspondante de `down` :

| Greffon | Perplexité | Écart |
|---|---|---|
| **aucun** (référence) | **23,6125** | — |
| **nul** (`u = v = d = 0`) | **23,6125** | **0,0000** ✅ transparent |
| croisé, échelle 0,1 | 23,6123 | −0,0002 |
| croisé, échelle 1,0 | 23,6156 | +0,0031 |
| croisé, échelle 5,0 | 23,6253 | +0,0128 |

➡️ Le greffon nul donne **exactement** la perplexité de base : la plomberie ne
perturbe rien. Un greffon non trivial la change, et **proportionnellement à son
échelle** : le nœud est bien dans le circuit, et le mécanisme est sain.

## 3. Ce qui reste pour fermer la boucle

Le greffon est **posé mais pas ajusté** : `d` vient de la colonne `down`
d'origine, ce qui est un point de départ, pas un optimum — d'où la dégradation
observée. Trouver `(u, v, d)` qui *améliore* demande un objectif, et l'objectif
qui compte (la perte) n'est accessible que par gradient.

Trois chemins, par ordre de coût croissant :

1. **Recherche par échelle et par appariement** : balayer les couples `(i, j)` et
   les échelles avec le banc à 100 évaluations/heure. Grossier, mais sans
   gradient — et 2 400 évaluations par jour couvrent un balayage utile.
2. **Ajustement de `d` par moindres carrés** sur un objectif de substitution
   (reconstruire la contribution de la couche suivante), ce qui reste de
   l'algèbre linéaire.
3. **Rétropropagation** : aucune capacité d'autogradage dans la pile aujourd'hui.
   C'est le seul point du programme qui demande une brique extérieure.

## 4. Reproductible

```bash
cd qtrinet-core && cargo build --release
cd .. && python3 tools/make_patch.py croise 12 /tmp/p.bin --i 0 --j 7 --scale 1.0
cd qtrinet-core && ./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl /tmp/wt2_ids.txt --ctx 256 --abits 16 --threads 16 --limit 1024 --patch /tmp/p.bin
```
