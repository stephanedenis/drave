# Parcimonie imposée à l'inférence — la frontière mesurée

*Peut-on donner à un modèle **préentraîné** le débit variable d'un réseau à
décharge, sans rien réentraîner ?* Campagne mesurée sur Qwen2.5-0.5B Q8_0, avec
deux jeux de 1 024 tokens : **A** pour le réglage, **B** (jamais vu) pour la
vérification.

Tout est déterministe : mêmes tokens, même perplexité, au chiffre près. Les
comptes d'événements et les perplexités sont donc exacts ; seule la mesure de
**temps** est bruitée (la machine tournait sous une charge de 8 à 14).

---

## 1. Pourquoi cette campagne

Le cahier des charges promet un débit **variable** selon ce qui s'active. Nous
avons mesuré le contraire sur un LLM dense : **0,00 % d'activations nulles**, donc
un débit constant, et l'argument « on ne paie que ce qui s'active » restait
théorique. Deux moyens d'imposer la parcimonie à l'inférence, tous deux inspirés
des neurones à décharge, aucun ne demandant d'entraînement :

- **seuil** : écarter les activations sous une fraction du maximum du vecteur
  (l'effet du seuil d'un neurone) ;
- **k-WTA** : ne garder que les k plus grandes (inhibition latérale).

## 2. Le seuil est catastrophique

Jeu de 512 tokens, référence 19,2647 pour 352,8 M événements :

| seuil (% du max) | événements/token | perplexité | rapport |
|---|---|---|---|
| 0,1 % | 343,8 M (−2,6 %) | 19,5750 | 1,02× |
| 0,2 % | 334,9 M (−5,1 %) | 19,6502 | 1,02× |
| 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× |
| 1,0 % | 281,1 M (−20,3 %) | 22,2286 | 1,15× |
| 2,0 % | 230,8 M (−34,6 %) | 30,5837 | 1,59× |
| 5,0 % | 145,0 M (−58,9 %) | **2264,84** | **117×** |

➡️ Économiser 11 % d'événements coûte 5 % de perplexité, et au-delà de 2 % le
modèle s'effondre. **Le seuil absolu est inutilisable.**

## 3. Le k-WTA est dix fois meilleur

Même exercice, mais en gardant une **fraction** des plus grandes magnitudes de
chaque vecteur — donc un critère relatif, qui s'adapte à l'échelle du vecteur.

| garde | événements/token | PPL (A) | PPL (B) |
|---|---|---|---|
| 100 % | 354,3 M | 23,6125 | 26,2565 |
| 90 % | 319,1 M (−9,9 %) | 23,6790 (+0,28 %) | 26,2950 (+0,15 %) |
| 85 % | 301,5 M (−14,9 %) | 23,7468 (+0,57 %) | 26,5785 (+1,23 %) |
| 80 % | 283,7 M (−19,9 %) | 23,8251 (+0,90 %) | 26,8586 (+2,29 %) |

➡️ **À sparsité comparable, le k-WTA coûte dix fois moins que le seuil** : −15 %
d'événements pour +0,6 à +1,2 % de perplexité, contre +4,6 % pour le seuil à
−11 %. La raison est simple : un seuil relatif au *maximum* coupe d'autant plus
qu'un vecteur a un maximum élevé, alors que le k-WTA garde la même proportion
partout.

## 4. Où couper compte plus que combien

En appliquant le k-WTA **projection par projection** (jeu A, référence 23,6125 /
354,3 M) :

| configuration | événements | perplexité (A) | perplexité (B) |
|---|---|---|---|
| uniforme 85 % | 301,5 M (−14,9 %) | +0,57 % | +1,23 % |
| attention seule à 90 % | 350,0 M (−1,2 %) | +0,06 % | — |
| `down` seul à 50 % | 302,9 M (−14,5 %) | +0,86 % | — |
| `gate`+`up` seuls à 80 % | 312,9 M (−11,7 %) | +1,02 % | — |
| **FFN complet à 85 %** | **308,0 M (−13,1 %)** | **−0,18 %** | **+0,46 %** |
| FFN complet à 80 % | 292,4 M (−17,5 %) | — | +1,57 % |

➡️ **Le point de fonctionnement retenu : k-WTA à 85 % sur les trois projections du
FFN, attention intacte.** −13,1 % d'événements pour +0,46 % de perplexité sur le
jeu tenu à l'écart. C'est meilleur que la parcimonie uniforme au même taux
(−14,9 % pour +1,23 %), et cela dit quelque chose de précis : **les entrées
d'attention supportent mal la coupure, celles du FFN la supportent.**

## 5. Deux idées testées et écartées

- **Renormalisation homéostatique** : après k-WTA, remettre les activations
  conservées à l'échelle pour que leur norme L1 égale celle du vecteur complet.
  Résultat : **dégrade** (+0,2 % à 90 %, +1,2 % à 85 %, +3,6 % à 80 %). Le
  modèle préfère la troncature franche à une compensation d'échelle — sa
  calibration interne compte sur les statistiques réelles.
- **Compensation par le seuil** : déjà couvert, le seuil est le mauvais outil.

## 6. Le gain de vitesse

Comptes d'événements : exacts. Temps : mesuré en temps CPU, entrelacé avec la
référence pour annuler la dérive.

| mesure | charge machine | −15 % d'événements → |
|---|---|---|
| première campagne | modérée | **−12,7 %** de CPU |
| seconde campagne | load 8-14 | **−3,0 %** de CPU |

➡️ Le gain suit la réduction d'événements **quand la machine est calme**, et se
fait manger par la contention de cache quand elle ne l'est pas. La sélection
k-WTA elle-même (un `select_nth` par produit matriciel, 168 par token) consomme
une part du gain — c'est ce qui explique qu'on ne récupère pas les 15 %.

**Fourchette honnête : entre 3 et 13 % de temps CPU pour 13-15 % d'événements
économisés.**

## 7. Ce que cette campagne établit

1. **On peut imposer de la parcimonie à un modèle préentraîné sans
   l'entraîner** — mais le budget est modeste : ~13 % d'événements pour ~0,5 %
   de perplexité.
2. **Le k-WTA (inhibition latérale) est le bon outil, le seuil est le mauvais** —
   dix fois plus efficace à sparsité égale.
3. **Le FFN est l'endroit où couper ; l'attention non.**
4. **Ce n'est pas le facteur 6,7×** qu'obtiendrait un modèle réellement entraîné à
   décharger (R̂ = 0,15 chez SpikeGPT). La différence est exactement le prix de
   l'entraînement — qui n'est pas dans ce programme.

## 8. Deux bugs attrapés par les chiffres

1. **k-WTA inversé** : `select_nth_unstable_by(k - 1, …)` gardait les k plus
   **petites** au lieu des plus grandes. Symptôme : 3,8 M événements au lieu de
   349 M — un compte absurde vaut tous les raisonnements.
2. **Options non branchées** : `--act-topk` n'existait que dans le mode
   perplexité. Le premier « gain de débit nul » mesurait donc un drapeau ignoré,
   pas un effet réel.

## 9. Reproductible

```bash
cd qtrinet-core && cargo build --release
# frontière
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_a.txt \
    --ctx 256 --abits 16 --threads 16 --act-topk 850
# point de fonctionnement retenu
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_a.txt \
    --ctx 256 --abits 16 --threads 16 --topk-gate 850 --topk-up 850 --topk-down 850
```
