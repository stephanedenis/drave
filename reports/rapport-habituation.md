# L'habituation (soustraire le passé) n'apporte RIEN — le réseau calcule déjà la différence

> Campagne : **cerveau** · expérience : **l'adaptation** — une faculté que le plan ne nommait pas
> et que la biologie impose (un récepteur qui s'habitue ne transmet plus la valeur, mais le
> **changement**). Ici, elle a une implémentation évidente dans le moteur : le **tampon** de la
> mémoire de travail, avec un **gain négatif** (`--entree-memoire K`, gain −1 : le passé est
> **soustrait** au lieu d'être recopié) — un filtre passe-haut.
> Question : un gain **négatif** rend-il le **changement** plus lisible que la valeur ?
> Verdict : **non — et le contrôle le dit.** À retard 1, avec **les deux** valeurs présentes dans
> l'entrée (`v[t]` et `v[t−1]`), le changement `v[t] − v[t−1]` est déjà lisible à **R² +0,921**
> avec le gain **positif**, et le gain **négatif** le rend **moins** lisible (**+0,817**). Le réseau
> **calcule la différence lui-même** ; la soustraire explicitement ne fait que **retirer de
> l'information** (la valeur). L'habituation est donc **inutile** ici : ce qui compte est d'avoir la
> fenêtre du passé, pas son signe.
> Date réelle : **2026-10-15 02 h 30-03 h 00 HAE** (heure lue sur la machine)
> Protocole : `tools/memoire_travail.py --tampon --changement` (une cible de plus : `v[t] − v[t−1]`,
> sonde **ridge** sur la première moitié de la séquence, mesurée sur la seconde) · quatre réglages ·
> signal de bruit uniforme `U(−2, 2)` sur le canal 0, jeton de base fixe, 4 époques d'entraînement
> du bras entraîné (les chiffres cités sont ceux du bras **gelé**, qui ne dépend pas de l'entraînement).

## 1. Les quatre réglages

| tampon | gain | retard | cible **changement** `v[t] − v[t−1]` | cible mémoire `v[t−k]` | cible présent `v[t]` |
|---|---|---:|---:|---:|---:|
| — (sans tampon) | — | — | **−0,183** | −0,183 *(k = 8)* | +0,992 |
| oui | **+1** | 8 | −0,183 | +0,831 | +0,921 |
| oui | **−1** | 8 | **+0,211** | +0,457 | +0,920 |
| oui | **+1** | 1 | **+0,921** | +0,853 | +0,962 |
| oui | **−1** | 1 | **+0,817** | +0,850 | +0,888 |

Ce que ça dit :

* **le retard est ce qui décide, pas le signe** : à retard 1, le changement est lisible (**+0,921**)
  parce que `v[t]` et `v[t−1]` sont **tous les deux** dans l'entrée ; à retard 8, il ne l'est pas
  (−0,183), parce que la différence d'un pas n'est pas dans l'entrée (on y a mis celle de huit pas) ;
* **le gain négatif DÉGRADE** ce que le gain positif donnait (0,921 → 0,817), et il dégrade aussi la
  valeur (le passé : 0,853 → 0,850 ; le présent : 0,962 → 0,888). **Soustraire, c'est jeter** : la
  différence est une fonction linéaire des deux canaux, donc **la sonde la trouve** quand les deux
  sont là — et elle ne la trouve plus quand l'un des deux a été retiré ;
* **le seul cas où le signe négatif « aide »** (retard 8 : −0,183 → +0,211) est un **artefact de
  mesure** : la cible (différence d'un pas) et le tampon (différence de huit pas) ne portent pas la
  même chose. Il est écrit ici plutôt que présenté comme un gain ;
* **conséquence pour la carte** : l'adaptation n'est **pas** une faculté à ajouter — c'est une
  **conséquence** de la mémoire de travail (avoir la fenêtre du passé). Le cerveau qui a le tampon
  n'a pas besoin d'un filtre passe-haut : le réseau fait la soustraction, et il la fait mieux seul.

## 2. Ce que ça change pour le cerveau

* **« donner la fenêtre » bat « prétraiter la fenêtre »** : c'est la **quatrième** mesure de la nuit
  dans ce sens (la mémoire de travail est une structure et non un entraînement ; la sélection du
  rejeu pèse moins que son volume ; l'allocation du budget d'attention est de second ordre ;
  maintenant, la transformation du signal d'entrée est un moins-disant) ;
* **et c'est un argument d'architecture** : chaque prétraitement ajouté est une **perte
  d'information**, et un réseau assez large **refait** la transformation — donc la règle du dépôt
  (« le mécanisme le plus efficient pour chaque faculté ») donne ici : **le tampon brut, aucun
  filtre** ;
* **ce qui reste ouvert, et c'est le vrai test de l'habituation** : un signal **très long** (où
  garder tout le passé coûte des canaux) ou **à forte dynamique** (où la valeur sature et où seule
  la variation compte) n'est pas mesuré — l'habituation pourrait payer **là**, et pas ici.

## 3. Ce que cette fiche ne dit pas

* **une seule forme d'habituation** (le gain linéaire négatif du tampon) : une habituation
  **adaptative** (gain qui décroît avec la répétition, constante de temps réglable) n'existe pas
  dans le moteur et n'est pas mesurée ;
* **un seul type de signal** (bruit uniforme i.i.d.) : sur un signal **lisse** (où le changement est
  petit devant la valeur), la conclusion pourrait s'inverser — c'est la première expérience à
  refaire, et elle est facile ;
* **une seule sonde** (ridge linéaire) : une sonde non linéaire lirait peut-être la différence même
  à retard 8 ;
* **4 époques, une graine** pour le bras entraîné (les chiffres cités sont gelés, donc la
  conclusion ne dépend pas de l'entraînement) ;
* **rien en génération** : la faculté est mesurée comme une **lecture**, comme partout dans cette
  famille de fiches.
