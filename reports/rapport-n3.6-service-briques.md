# N3.6 — le pont, le placement et le seuil composent dans le service

> **Ligne de roadmap** : N3 · **Date** : 2026-10-30 · **Verdict** : ✅ **composition tenue**,
> avec la condition N3.2b2 — le pont **agit** dans le service, le placement reste une
> **métadonnée**, la décision à seuil est **rejouable** ; le saut de calcul, lui, n'est pas gratuit.
>
> **Dispositif** : `tools/porte-n3-service-briques.sh` ; quatre DRVM synthétiques (graine 7) :
> A (4 blocs, pont normal, `local`), B (mêmes poids, pont nul, **4 160** poids), C (mêmes poids,
> `placement=remote`), T (2 blocs, seuil) ; service `--drvm-serve` ; données
> [`n3.6-service-briques.json`](n3.6-service-briques.json).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| A deux fois | **identique** |
| A contre B (pont nul) | **différent** — le pont agit dans le service |
| A contre C (`placement=remote`) | **identique** — le placement est une métadonnée |
| seuil 0 / seuil 1 | **12/0** et **0/12**, textes différents |
| seuil 0,01, deux fois | **11/1**, rejeu identique |
| paramètres A/B/C / T | **428 504** / **132 528** |

## Le contrôle négatif

- **Pont nul** : B diffère de A — un vrai changement est détecté ; la porte ne dit pas « tout est
  identique » par construction.
- **Placement** : C est identique à A — le champ est **inerte**, comme N3.4c l'avait nommé.
- **Seuils extrêmes** : 0 → tout court, 1 → tout plein, textes différents ; 0,01 → mixte **et**
  rejouable. La décision n'est pas un tirage.

## La condition

N3.2b2 a nommé la limite : la décision à seuil calcule **les deux chemins** ; elle ne saute pas le
calcul. La profondeur 1 est plus rapide mais change le contenu, parce que les couches sautées ne
fournissent plus leurs **K/V** aux jetons suivants. Cette porte prouve la **composition** dans le
service, pas un gain de temps qui n'existe pas encore.

## Ce qui pourrait le rendre faux

- **Modèle synthétique, un prompt, 12 octets** : la comparaison prouve l'activité des briques, pas
  la qualité ;
- le pont testé est le **pont du modèle natif**, pas le lien réseau distribué ;
- le placement est un **champ de manifeste** : la porte prouve que ce champ n'active aucun chemin,
  pas qu'aucun chemin distribué n'existe ;
- le service ne teste ni le cache continu, ni une architecture par jeton.

## Ce que ça change

N3.4a composait service + profondeur + routage + comptage ; sa propre en-tête disait qu'elle ne
couvrait « ni le seuil de confiance ni le pont/placement ». N3.6 ajoute **pont + placement + seuil**
dans le même service. La composition est tenue ; les deux conditions restantes sont nommées : le
**chemin distribué** (le placement est une métadonnée) et le **saut de calcul** (N3.2b2).

## Fichiers

- `tools/porte-n3-service-briques.sh` — la porte (6,5 s).
- `reports/n3.6-service-briques.json` — les mesures.
- `reports/rapport-n3.6-service-briques.md` — cette fiche.
