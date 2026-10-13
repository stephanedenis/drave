# Un tableau qui ne rend pas est un tableau qui n'existe pas — 17 lignes, 9 fichiers, et une porte

> Campagne : **outillage** · expérience : la vérification des tableaux Markdown du dépôt
> Question : le premier tableau de `docs/etat-cerveau.md` s'affiche comme du **texte** dans mdserve
> (127.0.0.1:8771). Est-ce le serveur, ou le document ?
> Verdict : **le document — et il n'était pas seul.** Une seule ligne du tableau avait **4 cellules
> pour 5 colonnes** (un lien qui avait glissé d'une colonne) ; mistune refuse alors le tableau
> **entier**, sans le dire. Le balayage du dépôt en a trouvé **17 lignes** dans **9 fichiers**
> (`docs/`, `reports/`, `journal/`) : barres de valeur absolue écrites `|w|` dans une cellule
> (`|` = séparateur de colonnes), cellules manquantes, séparateur à 6 colonnes pour un en-tête à 5,
> tableau triangulaire, et des `\` + `|` qui s'affichent **avec** leur antislash. Tout est corrigé, et
> `tools/porte-tableaux.sh` (38ᵉ porte) empêche la récidive.
> Date réelle : **2026-10-13, 08 h 05-08 h 40 HAE** (heure lue sur la machine)
> Protocole : `curl '127.0.0.1:8771/render?path=<fichier>'` (le HTML rendu par le serveur, pas une
> impression), puis bissection ligne par ligne ; balayage : `tools/porte-tableaux.sh`

## 1. La bissection (le serveur n'y était pour rien)

Un tableau minimal (`| a | b |` / `|---|---|` / `| 1 | 2 |`) **rend très bien** — donc le serveur
sait faire des tableaux. L'en-tête réel **plus** son séparateur rendent aussi (1 tableau). En
ajoutant les lignes du corps **une par une** : douze lignes sur treize donnent un tableau, **une
seule** (la ligne du C2 « cycle 2 régions ») le casse — elle a 4 cellules là où ses voisines en ont
5, parce que le lien `note-cycle-c2.md` a été laissé dans la 4ᵉ colonne au lieu de la 5ᵉ (« où »).

**Ce qui rend ce défaut coûteux, c'est son silence** : la ligne reste **visible** sur la page, en
texte gris, avec ses barres. Rien ne manque à l'œil — sauf le tableau. C'est la même famille que
« une porte qui rend `code 2` ressemble à un succès ».

## 2. Les 17 lignes, par cause

| cause | lignes | correction |
|---|---:|---|
| barre de valeur absolue dans une cellule (`\|gradient\|`, `\|w\|`, `\|dot\|`) | 5 | `∣` (U+2223) : rend partout, y compris **dans** un espace de code |
| cellule manquante (un lien glissé d'une colonne) | 2 | cellule remise dans sa colonne |
| séparateur à 6 colonnes pour un en-tête à 5 | 1 | séparateur aligné (et 7 lignes complétées) |
| tableau **triangulaire** (2, 3 puis 4 valeurs par ligne) | 3 | en-tête élargi à 5 colonnes, cellules vides en `—` |
| barre échappée (antislash + barre) qui s'affiche **avec** son antislash | 4 | barre simple en prose, `∣` dans le code |
| ligne **orpheline** (hors de son tableau, après un `---`) | 2 | remise dans son tableau, 5ᵉ cellule ajoutée |

## 2bis. Deuxième classe, trouvée par le lecteur : le tableau INTERROMPU

Signalé après la première correction : « maintenant c'est à partir de *Ce que « C8 » recouvre, et où
on en est* que ça dérape ». Exact — un bloc de **citation de 23 lignes** s'était glissé **au milieu**
du tableau des capacités (entre la ligne C8 et la ligne C9). Tout ce qui suivait — **C9, C9×C1, C10,
C11, C12, C12bis**, sept lignes — se retrouvait **hors du tableau**, en texte. La citation a été
déplacée **après** le tableau (elle porte sur la ligne C8, mais une note se lit après le tableau),
et les 21 lignes du tableau rendent maintenant.

Et le balayage étendu a trouvé **un second cas réel** : `docs/plan-modeles-lourds.md` portait **neuf
lignes de tableau sans en-tête ni séparateur** — elles touchaient même la citation au-dessus, donc
elles y étaient rattachées. En-tête et séparateur rendus (5 colonnes, comme ses lignes).

**La leçon, pour la porte** : vérifier les lignes *d'un* tableau ne suffit pas ; il faut aussi
vérifier qu'une ligne **qui a la forme** d'une ligne de tableau appartient bien à un tableau. La
porte le fait désormais — et elle a immédiatement attrapé **mes propres fiches**, où j'écrivais la
séquence fautive dans un espace de code pour documenter la règle (reformulée), puis une cellule de
tableau où la barre littérale redevenait un séparateur (reformulée sans le caractère).

## 3. La porte, et ce qu'elle refuse de vérifier

`tools/porte-tableaux.sh` (38ᵉ porte, ~1 s) vérifie sur **414 fichiers** : en-tête ≡ séparateur,
chaque ligne ≡ séparateur, aucune ligne de tableau **orpheline** (hors d'un tableau), et aucun
antislash-barre là où il s'afficherait. Elle **vue ROUGE** sur deux
défauts volontaires (un tableau à cellules inégales, une barre échappée hors tableau).

Elle ne vérifie **pas** les tableaux « écrasés » sur une seule ligne (des retours à la ligne perdus
à l'écriture) : indétectables sans heuristique, et **un faux positif dans une porte coûte plus cher
que le défaut**. Huit cas connus sont laissés tels quels dans
`journal/2026-10-10-reprise-historique.md` (un récit historique), et c'est écrit dans l'en-tête de
la porte.

*Première version de ce contrôle, corrigée avant d'être crue* : elle criait sur **tout** `\` + `|`, y
compris là où mistune le déséchappe légitimement (dans une cellule, hors espace de code) — 15
fausses alertes. Une porte qui crie là où tout va bien se fait ignorer : le contrôle a été
restreint aux deux cas qui s'affichent vraiment.
