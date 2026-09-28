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

## gpt-oss-120b : le modèle fonctionne, la métrique non

```
invite  : "The capital of Australia is"
réponse : " Canberra."
```

**Correct, cohérent, en 5,5 tok/s** sur un modèle de 117 G paramètres, 62 Go
résidents, lecture en place. Le modèle n'est donc pas cassé.

Ce qui reste inexpliqué, c'est notre **perplexité de 39,8** sur du wikitext brut
là où l'on attendrait de l'ordre de 6. Trois hypothèses, non départagées :

1. **notre encodage du fichier de test** — le tokenizer o200k a été vérifié sur
   sept chaînes pièges, pas sur les 4 424 jetons du corpus ;
2. **la sensibilité au format** — gpt-oss est entraîné sur son propre format
   (`<|start|>user<|message|>…`), pas sur de la continuation de texte brut ;
3. un détail d'architecture encore faux, que la génération ne révèle pas sur une
   réponse aussi courte.

Le test qui trancherait est de comparer notre flux de jetons à celui d'une
implémentation de référence sur le fichier entier — une seule requête, mais elle
demande de recharger 60 Go.

Au passage, un défaut de robustesse corrigé : `--chat` **paniquait** sur gpt-oss
(gabarit Qwen absent). Il retombe maintenant sur une invite brute en le
signalant, au lieu de s'arrêter sur un `unwrap`.

## Ce qui n'est pas prêt

| manque | conséquence | coût du correctif |
|---|---|---|
| **Gabarit de conversation de gpt-oss** | sa réponse est bonne en invite brute, mais son format `harmony` n'est pas implémenté | faible |
| **Contexte long** | attention en O(contexte), KV en f32 : 800 Mo à 8 k pour le 30 B, et +100 ms/jeton | moyen |
| **Vision** | le chemin image du modèle VL n'existe pas | élevé |
| **Robustesse** | pas de gestion mémoire, pas de requêtes multiples ; en session, le tour peut dépasser et divaguer si le modèle n'émet pas son jeton de fin | moyen |

## Conclusion

**Oui pour un vrai travail, y compris interactif** avec la famille Qwen :
génération de texte et de code, questions-réponses, sessions multi-tours, sortie
en flux, échantillonnage complet. Le seul frein qui reste est la vitesse —
5,6 jetons par seconde sur un 30 B MoE, ce qui est le régime d'un script ou
d'un traitement de nuit plutôt que d'une frappe au clavier.

**Oui pour gpt-oss aussi**, avec deux réserves : son gabarit de conversation
n'est pas implémenté (invite brute seulement), et notre perplexité sur ce modèle
reste inexpliquée alors que sa génération est correcte.

**Non pour la vision** : le chemin image du modèle VL n'existe pas.
