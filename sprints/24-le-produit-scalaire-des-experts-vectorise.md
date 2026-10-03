# Sprint 24 — Le produit scalaire des experts, vectorisé (et ce qu'il change)

- **Début** : 06:30 · **Fin** : 08:20
- **Objectif** : le bloc 23 a mesuré que le coût par jeton de V4-Flash **croît avec le
  contexte** (3,2 s à ctx 32, 6,45 s à ctx 256, ≈60 s à ctx 1 024) et que le poste
  dominant est `proj+mlp` (les experts), pas l'attention. Il a aussi montré que le
  mode lot **n'est pas porté pour V4** (refus explicite), donc le chemin le plus
  court vers un contexte long abordable est le **débit du produit scalaire**.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. D'abord, l'hypothèse du bloc 23 est écartée (et c'est une mesure)

`proj+mlp` doublait entre ctx 32 et ctx 256. Un poste d'experts ne devrait pas
dépendre du contexte : l'hypothèse écrite était l'**empreinte des experts** (jeu de
travail qui dépasse le cache, lectures disque). Mesure :

| run | `read_bytes` (disque) |
|---|---|
| ctx 32, 31 jetons | 357 Mo |
| ctx 32, 93 jetons | **0** |

**Aucune lecture disque** : le modèle est en page cache et le coût est **CPU**.
L'hypothèse d'empreinte est écartée. Ce qui reste : le coût par jeton croît avec la
**position** (le nombre de jetons déjà traités), pas avec les octets lus.

### 2. Où passe le temps, dans le code

Le produit des experts « sans noyau » (`Vue4::matvec_dequant`) fait, par super-bloc
de 256 poids : déquantifier le bloc (AVX2), puis `for j { s += v[j] * x[j] }` —
**une seule accumulation, de gauche à droite**. 256 additions *dépendantes* à ~4
cycles de latence : ~0,25 produit par cycle, quelle que soit la largeur SIMD du
processeur. Le débit mesuré (≈0,27 FLOP/cycle/thread) colle exactement à cette
chaîne de dépendance. Et vectoriser la **déquantification** n'avait donné que ×1,07 :
le poste n'est pas la déquantification, c'est le produit.

### 3. Le noyau, et ce qu'il change

`DRAVE_SIMD_DOT=1` : quatre accumulateurs vectoriels AVX2+FMA, puis une somme
horizontale. **Le drapeau s'annonce** au premier appel, parce qu'il change une
sortie : l'ordre des additions n'est plus celui des chiffres publiés, et le FMA
n'arrondit qu'une fois au lieu de deux.

A/B sur la même fenêtre (63 jetons, ctx 64, 16 fils, charge machine identique) :

| | scalaire (défaut) | `DRAVE_SIMD_DOT=1` |
|---|---|---|
| passe complète | 271,0 s (**4,27 s/jeton**) | 131,7 s (**2,06 s/jeton**) |
| dont `proj+mlp` | 3 270,65 ms | **1 070,52 ms** (**×3,05**) |
| dont attention | 999,33 ms | 989,41 ms (inchangée) |
| perplexité | **15,2520** | **15,2747** (**+0,15 %**) |

**Ce que le SIMD change, mesuré contre notre propre scalaire** (l'instrument du
bloc 23, `tools/compare_logits.py`) : corrélation par position min **0,9822**,
moyenne **0,9981**, position 0 **exactement 1,000000**, top-1 identique 60/63
(95,2 %). Autrement dit : **le désaccord introduit par le SIMD est trois fois plus
petit que le désaccord entre le moteur et llama.cpp** (moyenne 0,9852-0,9883). Le
drapeau reste **opt-in** : l'activer par défaut changerait toutes les références
publiées (V4-Flash 8430,4966, V4.1, gpt-oss), et ce n'est pas une décision à
prendre dans un noyau.

**Non-régression du chemin par défaut** : les logits du chemin scalaire *après*
refactorisation sont **bit à bit identiques** (`cmp`) à ceux mesurés *avant*, à un
contexte différent (ctx 256 → ctx 64) — 63 × 129 280 f32 identiques.

### 4. Ce qui n'est PAS résolu, et qui est nommé

- Le mode **lot** reste refusé pour V4 (hyper-connexions non portées dans
  `forward_lot`, et les modèles MLA y retombent jeton par jeton) : c'est un
  **chantier**, pas un réglage. Il amortirait les lectures de poids sur `t` jetons ;
  le gain du SIMD, lui, est déjà là, jeton par jeton.
- L'**indexeur CSA** (`indexer.top_k` = 512) n'est pas implémenté : sans effet
  jusqu'à 512 blocs (ctx 2 048 à ratio 4), donc pas la cause du coût mesuré.
- La croissance du coût avec la **position** reste inexpliquée : elle n'est ni le
  disque, ni l'attention (qui reste à ~1 s). C'est la mesure à reprendre, et elle
  est maintenant isolée (le SIMD ne change pas la forme de la courbe, il baisse le
  niveau).

## Rétrospective — garder / changer / doute

**Garder.** Le réflexe « la première hypothèse est l'instrument » a encore payé : la
lenteur apparente d'un run (319 s au lieu de 78 s) venait d'un **processus resté
vivant** après un `timeout` (le `timeout` tue le shell, pas son enfant). Refait
proprement, l'A/B est net. Une mesure sous charge non vérifiée n'est pas une mesure.

**Garder (2).** Le drapeau qui s'annonce, et la mesure de **ce qu'il change** avec
l'outil du bloc précédent : « ×2 sur la passe » sans « voici l'écart de logits que
ça introduit » aurait été une optimisation muette — exactement ce que le mandat
interdit.

**Changer.** J'ai écrit dans le plan, au bloc 23, une **cause** (l'indexeur CSA)
avant de l'avoir mesurée, puis j'ai dû corriger le paragraphe une heure plus tard.
La règle du dépôt dit « mesurer avant de conclure » ; je l'ai appliquée au chiffre
et pas à la phrase qui l'explique. Une hypothèse s'écrit comme une hypothèse, même
dans un paragraphe de synthèse.

**Changer (2).** Le refactor du produit scalaire a modifié le chemin par défaut
(extraction d'une fonction) sans que je vérifie **immédiatement** qu'il restait
bit à bit identique. Le `cmp` l'a prouvé après coup, mais il aurait dû être le
premier geste : un refactor dans la boucle la plus chaude du moteur se prouve, il
ne s'espère pas.

**Doute.** Le seuil « 0,99 des positions ≥ 0,95 » a été calibré sur une seule
campagne (255 positions). Le SIMD, lui, donne 100 % des positions ≥ 0,95 avec un
minimum à 0,9822 : il passerait la porte. Est-ce souhaitable ? Non — la porte est
un instrument de **fidélité à la référence**, pas un laissez-passer pour nos
propres optimisations. Mélanger les deux affaiblirait l'instrument.

**Doute (2).** Le gain ×3,05 sur `proj+mlp` est mesuré sur **un** modèle
(V4-Flash, IQ1_M) et un seul format « sans noyau ». Il devrait se retrouver sur
V4.1 (Q2_K par la même voie) et sur gpt-oss (MXFP4, autre chemin) — non mesuré, donc
non affirmé.
