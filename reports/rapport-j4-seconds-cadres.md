# J4 — les seconds cadres : un second annotateur ne confirme pas l'or de rôles (F1 0,71), et certains désaccords sont les erreurs de l'or

> **Ligne de roadmap** : B13 / Pensée (J4) · **Date** : 2026-11-20 (fenêtre remisée) · **Verdict** :
> l'or de rôles (`reports/or-roles-base-v1.json`, 46 textes) a été codé par **un seul annotateur**
> (« base ») — ce n'est pas un or indépendant. Un **second annotateur** (l'API) relève les mêmes
> cadres : l'accord est de **F1 0,7085** (moyenne des 7 rôles). Les rôles faciles tiennent (lieu
> 0,94, destinataire 0,94, possession 0,91), les rôles durs non (agent 0,61, prédicat 0,61,
> complément 0,28) — et **plusieurs désaccords sont des erreurs de l'or** (or-f47 : agent « c » pour
> « C'est » ; or-f45 : prédicat tronqué « n'oublie »).
>
> **Dispositif** : `tools/or_roles_second.py` (le second annotateur `deepseek-chat`, le schéma des
> 7 rôles, la comparaison par **expression normalisée** — pas par offset, le modèle ne compte pas les
> caractères) · 46 appels, `reports/or-roles-second.json` · témoin `--sans-api` : 0/46.

## Les chiffres

| rôle | F1 moyen |
|---|---:|
| lieu | 0,935 |
| destinataire | 0,935 |
| possession | 0,913 |
| temps | 0,674 |
| prédicat | 0,613 |
| agent | 0,607 |
| complément | 0,283 |
| **moyenne** | **0,7085** |

## Ce que les désaccords disent

1. **L'or a des erreurs** : or-f47 donne « c » comme agent de « C'est le meilleur film… » (l'API
   donne « j ») ; or-f45 donne « n'oublie » comme prédicat entier (l'API découpe « n'oublie
   jamais » / « sauvegarder » / « fermer »).
2. **Le périmètre des cadres diffère** : sur or-f50 (un texte de plusieurs phrases), l'or n'annote
   que la première phrase, l'API annote toutes — la comparaison par expressions pénalise l'API
   pour un travail *plus* complet.
3. **Les vrais désaccords** : « vous » de or-f03 — agent (l'or) ou destinataire (l'API) ; les deux
   se défendent, c'est le genre de cas qu'un **adjudicateur** doit trancher.
4. **Le complément est le trou** (0,28) : c'est le rôle fourre-tout, sans définition stable — le
   schéma lui-même est en cause, pas l'annotateur.

## Ce qui pourrait le rendre faux

- **L'API n'est pas un humain** : un accord de 0,71 entre un humain et un modèle ne mesure pas la
  même chose qu'entre deux humains (le modèle peut répéter les biais du gold, ou en introduire).
- La comparaison par expressions normalisées ignore les **frontières** (un NP complet contre sa
  tête) : or-f02 (« le chat de la voisine » contre « le chat de la voisine qui dort sur le toit »)
  compte comme un désaccord alors que les deux sont défendables.
- 46 textes, un seul passage : pas de barre d'erreur.

## La suite

L'**adjudication** : un troisième passage (humain ou un modèle différent) sur les **10 désaccords
les plus lourds**, pour corriger l'or avant de s'en servir comme référence. Sans cela, l'or de
rôles reste un **brouillon** — ce que l'état de S disait déjà autrement.

## Voir aussi

- [l'or de rôles](../reports/or-roles-base-v1.json) · [la restitution v3](rapport-restitution-v3.md) ·
  [les rôles de l'analyseur](rapport-s-analyseur-roles.md)
