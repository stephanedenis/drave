# Campagne « parcimonie imposée » — synthèse

*Peut-on exécuter un modèle **préentraîné** de façon radicalement plus creuse,
sans rien réentraîner ?* Campagne complète sur Qwen2.5-0.5B Q8_0, deux jeux de
1 024 tokens (A pour le réglage, **B tenu à l'écart** pour la vérification), plus
un contrôle en contexte 512 et sur 2 040 tokens.

Toutes les mesures de perplexité et de comptes d'événements sont **déterministes**
— mêmes tokens, même résultat au chiffre près. Seules les mesures de **temps**
sont bruitées (la machine tournait sous une charge de 8 à 22).

---

## 1. Ce qui survit à la coupure, et ce qui n'y survit pas

| où l'on coupe | tolérance mesurée | verdict |
|---|---|---|
| **poids d'attention** (top-k clés) | **améliore** de 0,5 à 1,2 % | ✅ à garder |
| activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |
| activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |
| entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |
| **Q et K** (après RoPE) | ×2,2 à 50 %, ×36 à 25 % | ❌ intouchable |
| activations du FFN (seuil absolu) | ×117 à 5 % du max | ❌ inutilisable |

➡️ **La frontière est nette** : ce qui est *surabondant* (les poids d'attention,
dont la plupart sont négligeables) se coupe sans mal ; ce qui est *porteur* (Q, K,
les activations du FFN) ne se coupe pas.

## 2. Le résultat net : une configuration qui gagne des deux côtés

**Attention à 32 clés + projection `gate` à 85 %.**

| | événements/token | perplexité A | perplexité B |
|---|---|---|---|
| référence | 354,3 M | 23,6125 | 26,2565 |
| attention 32 clés seule | 354,3 M | 23,3279 (**−1,21 %**) | 26,1178 (**−0,53 %**) |
| **+ `gate` à 85 %** | **338,8 M (−4,4 %)** | 23,2811 (**−1,40 %**) | 26,1417 (**−0,44 %**) |

➡️ **On améliore la qualité de 0,4 à 1,4 % tout en réduisant le flux
d'événements de 4,4 %.** Ce n'est pas un compromis : les deux vont dans le même
sens, et le résultat se reproduit sur des tokens jamais vus.

## 3. Composants testés et écartés

| idée | résultat |
|---|---|
| seuil absolu plutôt que relatif | **10× moins efficace** à sparsité égale — le seuil coupe d'autant plus que le vecteur a un grand maximum |
| renormalisation homéostatique après k-WTA | **dégrade** (+0,2 à +3,6 %) : le modèle préfère la troncature franche |
| k-WTA uniforme sur toutes les projections | moins bon que FFN-seul, puis que `gate`-seul |
| FFN complet à 85 % + attention creuse | **non additif, défavorable** (+0,19 % en B) |
| creuser Q et K pour accélérer les scores | **catastrophique** (×2,2 à 50 %) |
| espérer un gain de temps de l'attention creuse | **nul** : le coût est dans le calcul des scores, que le top-k ne peut pas éviter |

## 4. Le fait qui borne tout

Les trois papiers neuromorphiques (SpikeGPT, Spikformer, Spikingformer)
obtiennent des taux de décharge de **R̂ ≈ 0,15** — 6,7× moins d'événements — avec
une qualité comparable. Nous plafonnons à **−4 à −15 % d'événements** pour
+0,5 % de perplexité.

**L'écart est exactement le prix de l'entraînement.** Un réseau *entraîné* à
décharger place son information dans les quelques neurones qui tirent ; un réseau
dense entraîné à tout utiliser répartit son information partout, et couper après
coup détruit du signal.

C'est la conclusion principale de la campagne, et elle est cohérente avec tout ce
que ce projet a mesuré : élaguer après coup détruit (11 points sur les poids),
tronquer les activations coûte, et seule la parcimonie **structurellement
surabondante** (les poids d'attention) se coupe gratuitement.

## 5. Ce que ça implique pour le programme

1. **La parcimonie ne s'impose pas, elle s'entraîne.** Toute la suite « apprendre
   avec moins de couches, faire des grappes, récurser » suppose un modèle qui a
   appris à être creux — c'est-à-dire un entraînement, qui n'est pas dans ce
   programme.
2. **Ce qui reste acquis sans entraînement** : l'attention creuse (qualité + poids
   listables) et la réduction de 4,4 % du flux d'événements. C'est modeste mais
   c'est net, vérifié, et cela ne coûte rien.
3. **Le verrou est confirmé** : sans gradient, on ne peut pas fabriquer la
   parcimonie qui rendrait l'architecture événementielle payante à l'échelle
   promise.

## 6. Reproductible

```bash
cd drave-core && cargo build --release
# configuration gagnante
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_b.txt \
    --ctx 256 --abits 16 --threads 16 --attn-topk 32 --topk-gate 850
```
