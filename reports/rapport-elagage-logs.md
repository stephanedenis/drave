# A6.3 — l'élagage guidé par les logs : aucun neurone ne s'allume jamais, mais 63 % s'allument à peine

> Mesure du 24/10/2026, Qwen2.5-0.5B Q4_0, **255 jetons** (`--profil-neurones` en mode `--ppl`, le classement
> complet dans `/tmp/neurones.txt`), **116 736 neurones** — les FFN des 24 couches (24 × 4 864). La perplexité de
> référence est celle du même run : **30,7660**.

## Le classement, en clair

| seuil d'activation | neurones | part |
|---|---:|---:|
| **exactement 0** (jamais allumés) | **0** | **0 %** |
| < 0,01 % | 2 | 0,002 % |
| < 0,1 % | **73 481** | **63,0 %** |
| < 1 % | 115 861 | 99,2 % |
| le top 10 % | 11 674 | **19 % de la masse** |

## Ce que ça dit

- **Aucun neurone mort** : le critère « ne s'allume jamais » est **inopérant** sur ce corpus — les 116 736 neurones
  s'allument au moins une fois en 255 jetons. L'élagage par le zéro est **vide**.
- **63 % s'allument à moins de 0,1 %** : les « rares » sont la vraie cible statistique — mais les retirer sans
  mesurer la perplexité serait couper **ce qui parle peu**, pas **ce qui ne parle pas**.
- **Le top 10 % porte 19 % de la masse** : la concentration est réelle, mais loin des **33 %** de la vision
  (`rapport-localite-activation.md`) — modèle et mesure différents, le chiffre de la vision n'est pas reproduit ici.

## Ce que ça ne dit pas

- **255 jetons** ne suffisent pas : un neurone qui ne s'allume pas ici peut s'allumer ailleurs. L'élagage exige un
  corpus de **calibration** beaucoup plus large, et un seuil mesuré sur plusieurs textes.
- **Les FFN seulement** : l'attention n'est pas profilée par ce classement (les 116 736 = 24 × 4 864).
- **La perplexité après élagage n'est pas mesurée** : le critère du A6.3 (« perplexité égale ») reste à faire — il
  faut un masque dans le moteur, et c'est un vrai chantier, pas un `awk`.
