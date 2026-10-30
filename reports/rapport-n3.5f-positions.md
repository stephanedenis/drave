# N3.5f — la position est vérifiée à chaque pas

> **Ligne de roadmap** : N3.5f · **Date** : 2026-10-30 · **Verdict** : ✅ **une position
> sautée est refusée** (code 4), pas interprétée comme le pas suivant. Le succès normal reste
> **bit-exact**.
>
> **Dispositif** : protocole `pos` u32 par pas + statut 0/1, CLI `--drvm-serve-gen` /
> `--drvm-gen-net`, modèle 4 blocs (graine 7, 428 504 paramètres) ; porte
> `tools/porte-n3-positions.sh` ; données [`n3.5f-positions.json`](n3.5f-positions.json).

## Ce qui est mesuré

| cas | résultat |
|---|---|
| génération K=2 | **bit-exact** |
| `DRAVE_POS_DESYNC=1` (pos 1 au lieu de 0) | **REFUS, code 4** |

Le serveur compare `pos` à la position attendue **avant** de lire le hidden ; un écart écrit un
statut `0` et ferme la connexion. Le client ne reçoit aucun logit.

## Le contrôle négatif

- **Position normale** : succès et comparaison au `generer` local.
- **Position sautée** : refus explicite, code 4.
- **Le statut 0/1** évite de confondre un refus avec un logit NaN.
- **La porte N3.5e** repasse verte après le changement de protocole.

## Ce qui pourrait le rendre faux

- **Localhost, sans auth/TLS** ; une connexion = une session.
- **Le test de désync** est un hook d'environnement, pas un client indépendant.
- **Pas encore de session id** ni de reprise après refus.
- **Modèle synthétique** 4 blocs.

## Ce que ça change

N3.5a→f sont **faits** : découpage, fichier, TCP, empreinte, génération, positions. N3.6
(multi-régions/composition) reste.

## Fichiers

- `drave-core/src/main.rs` — `pos` et statut.
- `tools/porte-n3-positions.sh` — la porte.
- `reports/n3.5f-positions.json` — les mesures.
- `reports/rapport-n3.5f-positions.md` — cette fiche.
