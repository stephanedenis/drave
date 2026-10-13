# Un tableau qui ne rend pas est un tableau qui n'existe pas — 17 lignes, 9 fichiers, et une porte

> Campagne : **outillage** · expérience : la vérification des tableaux Markdown du dépôt
> Question : le premier tableau de `docs/etat-cerveau.md` s'affiche comme du **texte** dans mdserve
> (127.0.0.1:8771). Est-ce le serveur, ou le document ?
> Verdict : **le document — et il n'était pas seul.** Une seule ligne du tableau avait **4 cellules
> pour 5 colonnes** (un lien qui avait glissé d'une colonne) ; mistune refuse alors le tableau
> **entier**, sans le dire. Le balayage du dépôt en a trouvé **17 lignes** dans **9 fichiers**
> (`docs/`, `reports/`, `journal/`) : barres de valeur absolue écrites `|w|` dans une cellule
> (`|` = séparateur de colonnes), cellules manquantes, séparateur à 6 colonnes pour un en-tête à 5,
> tableau triangulaire, et des `\|` qui s'affichent **avec** leur antislash. Tout est corrigé, et
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
| `\|` qui s'affiche avec son antislash (prose ou espace de code) | 4 | barre simple en prose, `∣` dans le code |
| ligne **orpheline** (hors de son tableau, après un `---`) | 2 | remise dans son tableau, 5ᵉ cellule ajoutée |

## 3. La porte, et ce qu'elle refuse de vérifier

`tools/porte-tableaux.sh` (38ᵉ porte, ~1 s) vérifie sur **413 fichiers** : en-tête ≡ séparateur,
chaque ligne ≡ séparateur, et aucun `\|` là où il s'afficherait. Elle **vue ROUGE** sur deux
défauts volontaires (un tableau à cellules inégales, une barre échappée hors tableau).

Elle ne vérifie **pas** les tableaux « écrasés » sur une seule ligne (des retours à la ligne perdus
à l'écriture) : indétectables sans heuristique, et **un faux positif dans une porte coûte plus cher
que le défaut**. Huit cas connus sont laissés tels quels dans
`journal/2026-10-10-reprise-historique.md` (un récit historique), et c'est écrit dans l'en-tête de
la porte.

*Première version de ce contrôle, corrigée avant d'être crue* : elle criait sur **tout** `\|`, y
compris là où mistune le déséchappe légitimement (dans une cellule, hors espace de code) — 15
fausses alertes. Une porte qui crie là où tout va bien se fait ignorer : le contrôle a été
restreint aux deux cas qui s'affichent vraiment.
