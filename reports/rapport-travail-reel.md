# Le moteur est-il prêt pour du vrai travail ?

> Deux tests réels, avec un modèle de 30,5 G paramètres (Qwen3-30B-A3B, MoE
> top-8, Q4_K_M) sur CPU, 16 fils, lecture en place — aucune copie.

## Les deux tests

**1. Question en français, gabarit de conversation.**

```
<|im_start|>user
Explique en trois phrases pourquoi le ciel est bleu.<|im_end|>
<|im_start|>assistant
Le ciel est bleu parce que les molécules de l'atmosphère diffusent la lumière
du soleil. La lumière bleue a une longueur d'onde plus courte que les autres
couleurs, donc elle est diffusée plus efficacement que les autres couleurs.
C'est cette diffusion de la lumière bleue dans toutes les directions qui fait
que nous voyons le ciel comme bleu.<|im_end|>
```

Trois phrases, exactes, arrêt propre sur `<|im_end|>`. 89 jetons en 15,8 s
(**5,62 tok/s**), premier jeton en 166 ms.

**2. Génération de code, réponse vérifiable.**

```
def mediane(liste):
    triee = sorted(liste)
    n = len(triee)
    if n % 2 == 1:
        return triee[n // 2]
    else:
        return (triee[n // 2 - 1] + triee[n // 2]) / 2
```

Correct, idiomatique, sans `statistics`, et **arrêt spontané après 67 jetons**
au lieu des 200 demandés — la détection de fin fonctionne.

## Ce qui est prêt

| capacité | état |
|---|---|
| Famille Qwen (0,5 B → 30 B MoE), Q4_K / Q6_K / Q8_0 / Q4_0 / MXFP4 | ✅ |
| Lecture en place, zéro copie (30 B en 17,7 Go = taille du fichier) | ✅ |
| Tokenizer du modèle, gabarit de conversation, arrêt sur fin de tour | ✅ |
| Déterministe (glouton) — reproductible au jeton près | ✅ |
| Français et anglais, texte et code | ✅ |
| Débits mesurés | 0,5 B : 32 tok/s · 1,5 B : 17 · 30 B MoE : **5,6** · 7 B : 2,8 |

## Ce qui n'est pas prêt

| manque | conséquence | coût du correctif |
|---|---|---|
| **Pénalité de répétition, top-p** | boucles sur les générations longues ; seuls des tirages courts ont été validés | quelques lignes |
| **Sortie en flux** | rien ne s'affiche avant la fin — inutilisable en interactif | faible |
| **gpt-oss-120b** | tourne (5 tok/s) mais la sortie est fausse (PPL 39,8 au lieu de ~6) | inconnu |
| **Contexte long** | attention en O(contexte), KV en f32 : 800 Mo à 8 k pour le 30 B, et +100 ms/jeton | moyen |
| **Vision** | le chemin image du modèle VL n'existe pas | élevé |
| **Robustesse** | pas de gestion mémoire, pas de session persistante, pas de requêtes multiples | moyen |

## Conclusion

**Oui pour un vrai travail par lots** — génération de texte, de code, questions
et réponses — avec la famille Qwen, sur des tâches qui tolèrent 3 à 6 jetons par
seconde. **Non pour l'interactif** tant que la sortie n'est pas en flux, et **non
pour gpt-oss** tant que sa sortie est fausse.

Trois correctifs rendraient le moteur franchement utilisable, dans cet ordre :
pénalité de répétition et top-p, sortie en flux, puis session multi-tours.
