> Campagne : **toutes-langues** · expérience **71**
> Titre : 71. Blanchir l'entrée par langue : écarté — et un chiffre qui tombe
> Date réelle : **2026-10-07 00:13 HAE** (source : commit `2a70119`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 71. Blanchir l'entrée par langue : écarté — et un chiffre qui tombe

### 71.1 L'idée, et pourquoi elle découlait du §70

Le §70 a établi que l'axe de langue vient de **l'entrée**, et que le réservoir ne fait
que l'amplifier. Sous les contraintes du projet, `A` et `B` sont aléatoires et **gelés** :
on ne peut pas *apprendre* la transformation manquante. Mais on peut **changer ce qu'on
donne à lire**.

Le §64 avait retiré le **premier moment** de l'entrée (le jeton moyen) : +28 % de
rapport. Restait le **second moment** — la structure de covariance, elle aussi
massivement propre à la langue. On la retire par un **blanchiment par langue** :
`E' = (E − m_L)·C_L^(−α/2)`, entièrement déployable (la covariance s'estime sur le texte
d'entrée lui-même).

### 71.2 Le résultat : ça explose

| α | fid TEST | P_lang | P_cont | RAPPORT |
|---:|---:|---:|---:|---:|
| **0,00** | **0,5437** | 57,1 | 83,6 | **1,466** |
| 0,25 | 0,3434 | 761,2 | 1 054,8 | 1,386 |
| 0,50 | **0,1701** | **16 922** | **27 185** | 1,606 |

**Les énergies explosent** (`P_lang` 57 → 16 922, soit ×296) et **la fidélité
s'effondre** (0,5437 → 0,1701).

La raison est claire : blanchir **amplifie les directions de faible variance** de
l'entrée — qui contiennent à la fois du bruit et du détail propre à la langue. Donner
cela à lire à un réservoir à poids aléatoires fait diverger les énergies sans rien
démêler. **Écarté**, et nettement.

### 71.3 Le chiffre qui tombe, et il est marquant

**À α = 0 — l'entrée centrée seule, ZÉRO neurone — la fidélité vaut 0,5437.** C'est la
**meilleure fidélité de toute la série des §57-§71** :

| modèle | fidélité TEST |
|---|---:|
| **entrée centrée seule, 0 neurone** | **0,5437** |
| entrée + états du réservoir | 0,5309 |
| entrée seule, non centrée | 0,5161 |
| **états du réservoir seuls** | **0,4751** |

**Une régression linéaire-quadratique sur l'entrée centrée du professeur, sans un seul
neurone, bat tout ce que le pont construit.** Et son rapport contenu/langue (1,466) est
meilleur que celui du réservoir seul (1,354).

C'est la **quatrième** mesure indépendante qui mène au même constat — après le §29
(« une lecture sans aucun neurone bat le réservoir de 40 neurones »), le §34 (le
réservoir ne rattrape qu'avec l'entrée par-dessus) et le §70 (le réservoir abaisse le
rapport de 1,698 à 1,354).

### 71.4 Ce que les quatre mesures disent ensemble

| § | mesure | ce qu'elle montre |
|---|---|---|
| 29 | 40 neurones contre l'entrée seule | +0,0564 pour l'entrée seule |
| 34 | un gros réservoir **avec** l'entrée | le réservoir n'ajoute que +0,0073 à 40 neurones |
| 70 | caractéristiques emboîtées | le réservoir **abaisse** le rapport (1,698 → 1,354) |
| **71** | entrée centrée seule | **0,5437 — la meilleure fidélité de la série** |

**Quatre chemins indépendants, un même constat : la dynamique récurrente à poids
aléatoires gelés n'apporte rien que l'entrée ne portait déjà, et elle retire de la
structure contenu/langue.** Ce n'est plus une observation isolée, c'est un résultat
établi par quatre mesures de protocoles différents.

### 71.5 Et cela referme la boucle avec la mission

La mission demande d'**émuler les premières couches** d'un gros modèle par un **modèle
récurrent n-couches**. Les §58-§71 établissent que :

1. la transformation qui **crée** la séparation contenu/langue entre la couche 0 et la
   couche 8 **n'est pas reproduite** par un réservoir aléatoire gelé (§70) ;
2. aucune transformation **linéaire** de la sortie ne la rattrape sans payer 0,12 à 0,23
   de fidélité (§69) ;
3. et le réservoir **coûte** en fidélité comme en structure (§29, §34, §70, §71).

**Le réservoir aléatoire gelé n'est pas le bon mécanisme pour cette transformation.**
C'est une conclusion négative, elle est mesurée quatre fois, et elle désigne précisément
ce qu'il faut remplacer.


---
