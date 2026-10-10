> Campagne : **campagne-benefices** · expérience **42**
> Titre : 42. C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9)
> Date réelle : **2026-10-10 09:10 HAE** (source : commit `4767b22`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 42. C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9)

Le troisième volet est livré : `budget_paires` dans la topologie du lien, comparé au compte que
**le nœud annonce** dans chaque trame (protocole v8), avec un plafond `budget × pas` puisque le
compte du nœud est **cumulatif**.

| volet | unité | code d'arrêt | mesure |
|---|---|---|---|
| octets | octets par pas | **6** | 1 860 octets pour un budget de 975 ⇒ arrêt au pas 0 |
| latence | ms par pas (aller-retour) | **8** | 20,1 ms pour un budget de 1 ms |
| **paires** | paires du nœud par pas | **9** | **178 913 280** paires annoncées pour un budget de **1 000 000** par pas ⇒ arrêt **au pas 0** |

**Et la leçon du round précédent est appliquée** : le contrôle est **dans la boucle**, au pas où
le dépassement se produit. Placé après elle, il laissait **calculer et afficher la perplexité**
avant de refuser — le résultat partiel que ce dépôt refuse. C'est **la porte** qui l'avait
signalé, par son assertion « aucune perplexité ne doit être rendue ».

**Détail qui se recoupe** : le compte annoncé au premier pas (178 913 280) est exactement la
valeur par pas mesurée sur la session entière (178,9 M) — le nœud dit la même chose au premier
pas qu'à la fin, ce qui est le comportement attendu d'un compteur cumulatif lu une fois.

**Ce que C10 apporte à la distribution** : les trois coûts d'un lien sont désormais **déclarables
et vérifiés** — le temps, les octets, et le **calcul déporté**, qui est le seul que ce moteur
compte vraiment (`paires = poids non nuls × activations vivantes`). Un lien qui ne peut pas
porter un demi-modèle se voit refuser **au premier pas**, au lieu de le découvrir à la fin.
