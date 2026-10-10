> Campagne : **campagne-benefices** · expérience **22-bis**
> Titre : 22 bis. Ce que le nouveau matériel change, d'après ces mesures
> Date réelle : **2026-10-09 07:33 HAE** (source : commit `838c511`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 22 bis. Ce que le nouveau matériel change, d'après ces mesures

La machine va recevoir une carte 4×NVMe (4 Patriot P320 256 Go, Gen3 ×4) en RAID,
sur l'autre processeur, plus une carte AMD 6 mini-DP pour l'affichage
(`docs/configuration-nvme-raid-amd.md`). Ce que la campagne permet de dire de
l'effet attendu — et ce qu'elle ne permet pas :

| mesure de la campagne | ce que le RAID change |
|---|---|
| **8,6 Mo/s** de lecture en mmap sur disque dur contre 243 Mo/s en séquentiel (§ 12 bis) | **c'est le poste le plus amélioré** : le même moteur sur NVMe tient déjà 140-300 Mo/s (§ 12 bis). Les 90 minutes d'une passe gpt-oss et les 21 minutes de chargement du codestral deviennent des minutes |
| **le lot ne divise pas les lectures sur un MoE** (§ 14 bis) | inchangé : c'est la **structure** (union des experts touchés par une passe) qui le veut, pas le disque |
| **les experts ne passent pas par les listes** (format Q4_0, noyau absent) | inchangé — c'est du code, pas du matériel |
| **la parcimonie apprise divise les paires lues par 4** (§ 5 ter) | **amplifié** : des lectures plus rapides ne rendent pas la parcimonie inutile, elles déplacent le seuil de rentabilité du chemin par listes vers des densités plus élevées |
| **répartir paie si le calcul dépasse 3,4 ms × RTT** (§ 8 bis) | inchangé : la règle ne dépend pas du disque mais du réseau et de la taille du modèle |
| **20 threads saturés, 2 sockets, NUMA asymétrique** (`docs/numa-segregation.md`) | le RAID sur l'autre socket ajoute un chemin PCIe sans retirer de voies au GPU — c'était le but du plan |

**Ce que ces mesures ne disent pas** : rien n'a été mesuré sur le RAID lui-même
(il n'est pas installé). Les chiffres ci-dessus sont des **attendus dérivés** de la
comparaison HDD/NVMe de la campagne, pas des mesures du nouveau matériel — et la
première chose à faire quand il arrivera est de refaire **la même mesure de débit
`dd` et la même passe à froid**, pour vérifier que l'écart tient.

---
