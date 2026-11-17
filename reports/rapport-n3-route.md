# N3.8 — les routes sont exécutées, et leur sémantique est mesurée

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ **N3.8 tenu** — une route
> conditionnelle `position >= seuil → profil` **agit** : au seuil 0 les logits sont **bit-exacts**
> ceux du modèle pur `flou`, au seuil 10⁹ **bit-exacts** ceux du pur `defaut`, et au seuil 1 un
> **mélange déterministe** diffère des deux (5,779e-03 de `defaut`, 1,132e-05 de `flou`).
>
> **Dispositif** : [`tools/porte-n3-route.sh`](../tools/porte-n3-route.sh) · petit `drave-n0`
> (**132 720 paramètres**, `d_model` 32, 2 blocs, graine 7, **poids identiques**) écrit quatre fois :
> pur `defaut`, pur `flou`, et deux copies de `defaut` avec une route par bloc mixeur ; logits du
> dernier pas par `--drvm-pas-hex`.

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| route **toujours active** (seuil 0) vs modèle pur `flou` | **IDENTIQUE** (bit-exact) |
| route **jamais active** (seuil 10⁹) vs modèle pur `defaut` | **IDENTIQUE** (bit-exact) |
| route **mixte** (seuil 1, prompt `abc`) vs `defaut` / vs `flou` | **5,779e-03** / **1,132e-05** |
| route mixte, deux exécutions | **IDENTIQUE** (déterministe) |
| contrôle du contrôle : `defaut` vs `flou` | **5,790e-03** ≠ 0 |
| provenance | l'inspecteur affiche « position >= 0 → flou », la trace porte les 2 routes |
| moteur numpy | un manifeste à routes est **refusé** (nommé) |
| routes mal formées | 4 cas refusés et nommés (bloc inconnu, condition inconnue, sans `alors`, profil inconnu) |

## Ce que la porte établit

1. **La condition est exécutée**, pas seulement stockée : un seuil qui tombe au-delà de la séquence
   ne change **rien** (bit-exact), un seuil à 0 change **tout** (bit-exact aussi), et un seuil au
   milieu produit un état intermédiaire. C'est la définition même d'une arête conditionnelle.
2. **La sémantique est stable** : la route mixte est déterministe, et le profil d'un bloc ne dépend
   que de `(bloc, position)` — pas d'un état caché.
3. **Chaque moteur déclare ses capacités** : le Rust exécute les routes, le numpy refuse le
   manifeste au lieu de l'ignorer.

## Ce qui pourrait le rendre faux

- **Un modèle, une graine, deux blocs** : la sémantique est vérifiée sur le petit `drave-n0`, pas sur
  un modèle entraîné ; rien ne dit que la *qualité* d'un routage suit.
- **Le mélange n'est pas une interpolation** : la position 1 hérite des K/V de la position 0
  calculées sous `defaut` ; c'est ce qui rend l'écart au pur `flou` petit (1,132e-05) sans être nul.
  Un test qui attendrait une moyenne des deux serait faux.
- **Aucun coût mesuré** : la route ajoute un test par bloc et par position ; il n'est pas chronométré
  ici.
- **La politique reste ouverte** : cette porte prouve le **mécanisme**, pas qu'il faut router. R0.5 et
  R06 ont montré qu'un seuil global ne transfère pas ; une politique apprise par document est la
  condition nommée.

## Ce que ça change

`graph.routes` n'est plus la seule section inerte du manifeste : le schéma est fermé
(`{id, bloc, si {kind, seuil}, alors, sinon?}`), validé par les deux lecteurs, exécuté par le moteur
Rust, refusé par le moteur numpy, et visible dans l'inspecteur et la trace. La prochaine étape n'est
pas un nouveau mécanisme : c'est une **politique** de routage qui batte le choix fixe sur un banc —
ce que R0.5 et R06 n'ont pas obtenu.

## Voir aussi

- [la porte](../tools/porte-n3-route.sh) · [le format](../tools/drvm.py) ·
  [le moteur natif](../drave-core/src/native.rs) · [le modèle natif](../docs/theorie/modele-natif.md) ·
  [R0.5, le routeur négatif](rapport-r07-routeur.md)
