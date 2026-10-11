# E1 et E2, re-mesurés : le connectome aléatoire coûte 9 % (pas 1 %), et la croissance n'est PAS pire que le hasard

> Campagne : **biologie** · expériences : E1 (connectome inné) et E2 (croissance des connexions)
> Question : la **structure** d'un réseau peut-elle être fixée à la naissance (E1) ou **grandir**
> selon une règle locale (E2), sans payer sur la qualité ?
> Verdict : **les deux conclusions publiées changent.** Le connectome aléatoire coûte **+9,4 %**
> (pas « 1 % »), et la croissance locale est **au moins aussi bonne** qu'un masque statique de même
> densité (8,1550 contre 8,1827) — alors qu'elle était donnée « pire que le hasard ».
> **Pourquoi les chiffres changent** : le masque ne couvrait que les `nn.Linear` — **5,8 % des
> poids**, l'attention seule — et le défaut se taisait. Mesuré par l'audit du harnais
> (`tools/audit_drapeaux_harnais.py`) : « connectome inné à 25 % » laissait **83,9 %** des poids
> non nuls. Corrigé, le masque et la croissance couvrent tout tenseur ≥ 2D sauf la table d'entrée.
> Date réelle : **2026-10-11 03 h 45 HAE** (heure lue sur la machine).
> Protocole : `tools/entrainer_moteur.py` · occupation : `tools/occupation_poids.py` ·
> audit : `tools/porte-audit-drapeaux.sh`.

## 1. E1 — le connectome inné

Même entraînement partout (`--dim 192 --couches 4 --tetes 4 --experts 8 --k 2 --pas 3000
--lr 3e-4 --graine 1`), masque **aléatoire fixé à la naissance** et réappliqué à chaque pas ;
l'occupation est **lue dans le fichier exporté**, ce qui prouve la couverture :

| modèle | occupation du fichier | val (bits/octet) | perplexité (moteur) | coût |
|---|---:|---:|---:|---:|
| témoin dense | 89,2 % | 2,3533 | **7,3429** | — |
| connectome **25 %** | 24,0 % | 2,4660 | **8,0317** | **+9,4 %** |
| connectome **12,5 %** | 12,9 % | 2,6072 | **8,6970** | **+18,4 %** |

**Ce que ça dit, et ce que ça ne dit plus.** Une structure aléatoire **coûte** — 9 % à 25 % de
densité, 18 % à 12,5 % — au lieu du « 1 % » annoncé. L'ancien chiffre décrivait l'**attention
seule** : les 83 % de poids d'experts n'étaient jamais masqués. Le coût reste **modéré** (le
réseau apprend malgré une structure aléatoire), mais il n'est plus gratuit, et il **double** quand
la densité est divisée par deux.

## 2. E2 — la croissance locale

La règle est locale : à chaque étape de croissance, on ajoute une fraction des connexions
**absentes**, choisies par le **|gradient| accumulé** sur ces connexions. Le départ est un masque
aléatoire de 10 %, la cible 25 %.

| modèle | occupation finale | val (bits/octet) | perplexité | verdict |
|---|---:|---:|---:|---|
| masque **statique** 12,5 % | 12,9 % | 2,6072 | 8,6970 | — |
| **croissance** 10 % → 25 % | 20,9 % | **2,4551** | **8,1550** | — |
| masque **statique** à densité égale | 20,3 % | 2,5067 | **8,1827** | la croissance fait **mieux** de 0,3 % |

**La conclusion publiée est renversée** : la croissance locale n'est **pas** « pire que le hasard à
densité égale » — elle est **légèrement meilleure** (8,1550 contre 8,1827), et l'interpolation
entre les deux points statiques (12,9 % → 8,6970 et 24,0 % → 8,0317) place un statique à 20,9 % vers
**8,22**, soit un peu au-dessus de la croissance. L'ancien verdict (« +0,9 % pire que le hasard »)
venait du même défaut de couverture, doublé d'un second : le gradient était lu sur
`mod.weight.grad`, qui vaut `None` quand le poids est reparamétré — la croissance ne voyait
**aucun** gradient dans ce cas.

**Ce que ça ne dit pas** : la croissance n'est pas **meilleure** de façon décisive (0,3 % est dans
le bruit d'une graine). Le résultat honnête est : **à densité égale, choisir les connexions par le
gradient ne fait pas moins bien que les tirer au hasard** — la règle locale n'est pas réfutée.

## 3. Ce que ces deux re-mesures enseignent

1. **une couverture partielle qui se tait fabrique des conclusions optimistes.** « Un connectome
   aléatoire coûte 1 % » était vrai de 5,8 % du modèle — et se lisait comme une propriété du
   modèle entier ;
2. **le même défaut a produit deux verdicts faux** (E1 trop optimiste, E2 inversé) : ce n'est pas
   une erreur de mesure isolée, c'est un **instrument** qui ne mesurait pas ce qu'il annonçait ;
3. **la re-mesure ne demande pas de refaire l'expérience** : elle demande de **vérifier la
   couverture** — un chiffre lu dans le fichier exporté, à côté du chiffre annoncé.

## 4. Ce que cette fiche ne dit PAS

- **une seule graine** par point, une seule échelle (7,58 M paramètres), un corpus ;
- **les chiffres antérieurs ne sont pas effacés** : ils restent dans `reports/rapport-e2-croissance.md`
  et dans les fiches d'E1, à côté de leur portée réelle (l'attention), comme le veut la règle du
  dépôt ;
- **le coût en paires n'est pas mesuré** : une densité de 25 % ne réduit aucune paire tant que la
  représentation reste dense (manque **M9**, seconde moitié) ;
- **la croissance n'est pas testée à d'autres règles** (nouveauté, magnitude, aléatoire) : seule la
  règle « |gradient| accumulé » est mesurée ici.
