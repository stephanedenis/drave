# Phase 3.4 — le préremplissage par LOTS sur le fil

**En une ligne** : un préremplissage de 256 jetons traverse désormais le réseau en
**4 lots** (ou un seul) au lieu de 255 flux, et le calcul coupé redonne exactement
le calcul local — **écart 0,00e0**.

## Le problème

Le transport était séquentiel : un flux par jeton, donc un aller-retour par jeton.
Un préremplissage de N jetons payait N fois la latence, alors que la latence est
précisément le seul poste qui compte (`attente ≈ calcul distant + 3,2 × latence
par message`, mesuré dans `reports/rapport-transport-liste.md`). Avec 60 ms
d'aller-retour, 256 jetons coûtaient 15 secondes d'attente pure.

## Le mode 3 du protocole

```
en-tête   magie u32 · version u8 (4) · mode u8 (3 = LOT) · plage (2 × u32)
          position u32 (celle du PREMIER jeton) · n u32 (nombre d'ÉTATS)
          échelle f32 · et le contrat d'activation (niveaux, seuil, top-k,
          renorm, 7 top-k par projection, attn/qk/moe top-k)
corps     n × dimension × f32        ← la dimension ne voyage pas
```

`n` est le nombre d'**états**, pas de canaux : chaque nœud connaît la dimension
par son modèle, et les deux doivent charger le même GGUF. La réponse est encodée
comme la demande, et la position transmise est celle du premier jeton du lot (les
positions suivantes sont contiguës par contrat).

Côté modèle, une seule addition : `emb_imposee_lot`, le pendant de `emb_imposee`
pour tout un lot. `forward_lot` part des états reçus au lieu des identifiants de
jetons — et c'est ce qui rend le découpage possible sans que le nœud distant ait
jamais vu le texte.

## Mesuré

Qwen2.5-0.5B-Q8_0, 256 jetons de WikiText-2, 12 couches par nœud, deux processus :

| découpage | lots | écart local/réparti |
|---|---|---|
| 256 jetons en lots de 64 | 4 | **0,00e0** (18,0851 = 18,0851) |
| 256 jetons en UN lot de 917 583 octets | 1 | **0,00e0** |
| contrôle `--lot 1` (un flux par jeton) | 255 | **0,00e0** (18,0206 = 18,0206) |

Le critère est l'égalité **à lot égal** : la référence locale est découpée de la
même façon que le chemin réparti, sinon l'écart mesurerait la différence entre
deux ordres de sommation (le par-lots contre le jeton par jeton donne ~1e-4 sur
Qwen, ce qui n'est pas un défaut du découpage).

## Sur un lien latent : 18× (c'est là que le mode lot paie)

`tools/proxy_latence.py` ajoute 20 ms par message, comme le ferait un lien
distant. 64 jetons de préremplissage, 12 couches par nœud :

| | échanges | temps local | attente du pair | total |
|---|---|---|---|---|
| **en UN lot de 64** | 1 | 1 145 ms | 1 488 ms | **2,6 s** |
| un flux par jeton | 63 | 350 ms/jeton | 394 ms/jeton | **47,6 s** |

Même calcul, même fidélité (0,00e0 des deux côtés) : **18×**. Chaque aller-retour
coûte ~4 × 20 ms de latence pure, et le mode lot en supprime 62 sur 63. C'est
l'argument de la phase 3.4, et ce que la démonstration Colab doit montrer : sur un
lien rapide le mode lot ne change presque rien, sur un lien distant il change tout.

## Le lot est aussi plus RAPIDE, machine au repos

Chronométré sur 256 jetons, deux processus locaux, machine au repos (12 couches
par nœud) :

| découpage | temps par lot | temps par jeton |
|---|---|---|
| un flux par jeton | 116,7 ms | **116,7 ms** |
| lots de 16 | 358,0 ms | 22,4 ms |
| lots de 64 | 1 185,3 ms | 18,5 ms |
| **un seul lot de 256** | 4 255,6 ms | **16,6 ms** |

**7× plus rapide par jeton** — et ce n'est pas la latence (localhost), c'est le
produit matrice-matrice : le chemin par lots lit chaque ligne de poids une fois
pour tout le lot, celui par jeton la relit 256 fois. Le mode lot gagne donc sur
les deux tableaux : moins d'allers-retours sur un lien distant (18× à 20 ms), et
moins de lectures de poids en local.

## Ce que ça coûte, et ce que ça n'économise pas

Le lot voyage en **f32 dense, 3 663 octets par jeton en mode dense** — le mode
liste par état n'existe pas encore (c'est le mode 4 décrit, non écrit). Ce qui est
gagné n'est pas du débit mais de la **latence** : un aller-retour par lot au lieu
d'un par jeton. À 20 jetons/s le débit demandé reste sous 1 Mbit/s.

## Les deux pièges, tous les deux payés

1. **L'en-tête d'un octet trop long** : `envoyer_lot` écrivait 40 octets pour un
   `TAILLE_TETE` de 39 (un `push(0)` hérité d'une expérience annulée). Tout le
   corps se décalait d'un octet — des f32 valides, faux — et la désynchronisation
   n'apparaissait qu'au flux SUIVANT, sous la forme « magie de flux absente ». Les
   deux émetteurs portent maintenant un `assert_eq!(tete.len(), TAILLE_TETE)`.
   Trouvé par la spécification déléguée, pas par le banc.
2. **L'entrée normée** : envoyer `norme(résidu)` au lieu du résidu pour mieux le
   quantifier casse la connexion résiduelle (`x = x + attention(norme(x))`) — le
   banc de contrôle en mode dense l'a dit tout de suite : 5,61e0 au lieu de
   0,00e0. Voir `reports/rapport-transport-liste.md`.

## Reste à faire

Le **lot en listes** (mode 4) : chaque état en liste creuse au lieu de f32 dense,
soit ÷2,3 sur le fil à 2,7 % d'écart — la même recette que le mode 2, répétée par
état et auto-délimitée.
