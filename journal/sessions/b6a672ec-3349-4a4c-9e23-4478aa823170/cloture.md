# Clôture — `b6a672ec` : le GPU bloqué, le reboot

> **Session** : `b6a672ec-3349-4a4c-9e23-4478aa823170` · **Début** : 2026-11-01 13 h 28 ·
> **Fin** : 2026-11-02 14 h 41 · **Tours** : 2 · **Messages** : 59 · **Plan** : aucun (session non
> déclarée). Clôture écrite par le hub `536cd5d6` le 02/11 16 h 09.

## Ce qui s'est passé

La session ouvre sur `git push origin`, puis dérive sur un **diagnostic GPU** : les deux Quadro
RTX 5000 ne répondent plus (`GPU requires reset`, `nvidia_drm` figé à `refcnt = -1`). Le reset
logiciel est impossible :

- `nvidia-smi -r` (même en root via `pkexec`) échoue : `failed to allocate group of reset devices:
  GPU requires reset` ;
- le déchargement des modules est bloqué (`modprobe -r` ne rend jamais la main) ;
- `nvidia-bug-report.sh` se bloque à son tour.

L'humain **annule** la question de redémarrage à 14 h 41 ; la machine est redémarrée à **15 h 06**.
Au retour, `nvidia-smi` donne **1 Mio / 16 384 Mio, 0 %** sur les deux cartes : elles sont saines.

## Ce qui est livré

- **Aucun code, aucune fiche** : un diagnostic et un reboot.
- La **cause** du blocage n'est pas identifiée ; le symptôme et les commandes qui échouent sont
  dans le [digest](digest.md) et le [rapport](rapport.md).
- La session **n'avait pas de plan** : elle n'aurait pas dû écrire de fait. Elle n'en a pas écrit.

## Ce qui reste

- **Surveiller** les deux GPU après le reboot (fait : 1 Mio, 0 %) ; si le symptôme revient, le
  reboot est la seule sortie connue.
- **Ne pas rebooter avec du travail non committé** : le reboot a laissé 67 fichiers dans l'arbre ;
  le hub les a committés après coup.
- **Déclarer les sessions de diagnostic** : celle-ci est restée hors `en-cours` et hors
  `sessions.py` ; le journal l'a vue, le pilotage non. C'est le trou que le hub corrige.

## Voir aussi

- [Rapport automatique](rapport.md) · [Digest](digest.md) · [Le 02/11](../../2026-11-02/README.md).
