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

## Troisième test : session multi-tours

```
vous> Quelle est la capitale de l'Australie ?
assistant> La capitale de l'Australie est Canberra.
vous> Et combien d'habitants compte-t-elle environ ?
assistant> Canberra, la capitale de l'Australie, compte environ **450 000
habitants** (en 2023). C'est la quatrième ville du pays en population, après
Sydney, Melbourne et Brisbane.
```

La seconde question est **elliptique** : « elle » ne désigne rien sans le tour
précédent. Le modèle l'a résolu — c'est la preuve que le contexte de
conversation est bien porté d'un tour à l'autre, et pas seulement que le
gabarit est appliqué.

## Ce qui a été comblé depuis le premier bilan

| manque | état |
|---|---|
| **Pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) | ✅ 300 jetons à température 0,7 sans boucle |
| **Top-p / noyau** (`--top-p`) | ✅ s'ajoute au top-k = 40 |
| **Sortie en flux** (`--flux`) | ✅ jeton par jeton, sans couper les caractères multi-octets |
| **Session multi-tours** (`--session`) | ✅ avec troncature de sécurité du contexte |

## Ce qui n'est pas prêt

| manque | conséquence | coût du correctif |
|---|---|---|
| **gpt-oss-120b** | tourne (5 tok/s) mais la sortie est fausse (PPL 39,8 au lieu de ~6) | inconnu |
| **Contexte long** | attention en O(contexte), KV en f32 : 800 Mo à 8 k pour le 30 B, et +100 ms/jeton | moyen |
| **Vision** | le chemin image du modèle VL n'existe pas | élevé |
| **Robustesse** | pas de gestion mémoire, pas de requêtes multiples ; en session, le tour peut dépasser et divaguer si le modèle n'émet pas son jeton de fin | moyen |

## Conclusion

**Oui pour un vrai travail, y compris interactif** avec la famille Qwen :
génération de texte et de code, questions-réponses, sessions multi-tours, sortie
en flux, échantillonnage complet. Le seul frein qui reste est la vitesse —
5,6 jetons par seconde sur un 30 B MoE, ce qui est le régime d'un script ou
d'un traitement de nuit plutôt que d'une frappe au clavier.

**Non pour gpt-oss** tant que sa sortie est fausse (perplexité 39,8 au lieu de
l'ordre de 6), et **non pour la vision** : le chemin image du modèle VL n'existe
pas.
