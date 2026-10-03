# La réutilisation des experts, mesurée

> Question posée par la cible elle-même (`docs/plan-kimi-k3.md`) : un jeton de
> Kimi-K3 lit **24,7 Go d'experts routés** (16 sur 896). Aucun placement ne rend
> cette lecture interactive — sauf si **les mêmes experts reviennent**. C'est la
> mesure qui décide si un cache peut servir à quelque chose, et elle manquait.
>
> Relevés du 03/10 (bloc 30), sur **Qwen3-30B-A3B** (48 couches, **128 experts,
> 8 par jeton**, routage softmax), **trois textes** : 48 jetons de wikitext,
> 128 jetons du même texte, et 128 jetons de **code** (le module de matvec du
> dépôt). Le texte est écrit par le tokenizer du modèle, jamais un autre.
> Instrument : `DRAVE_TRACE_EXPERTS` (trace du moteur, une ligne par
> (couche, jeton)) + `tools/analyse_reutilisation_experts.py` (neuf).

## 1. Ce que la trace dit

| mesure | wikitext 48 | wikitext 128 | **code 128** |
|---|---|---|---|
| experts distincts touchés (par couche) | 128/128 | 128/128 | 128/128 |
| **réutilisation immédiate** (t−1 → t) | 46,9 % | **47,9 %** | **48,8 %** |
| fenêtre de 2 jetons | 54,7 % | 57,1 % | 60,4 % |
| fenêtre de 4 | 63,9 % | 68,5 % | 72,9 % |
| fenêtre de 8 | 72,8 % | 78,1 % | 82,3 % |
| fenêtre de 16 | 78,8 % | 84,5 % | 88,2 % |
| sur tout l'historique | 82,7 % | 93,1 % | 93,9 % |

**Près d'un expert sur deux est déjà là au jeton précédent** — et c'est vrai sur
les trois textes (46,9 · 47,9 · 48,8 %), donc la dépendance au texte est faible
sur cette mesure. Le plafond de réutilisation (93 %) est atteint avec une fenêtre
d'une quinzaine de jetons ; au-delà, le routage va chercher des experts « froids »
et ne les revoit plus.

## 2. Ce qu'un cache LRU rend, mesuré

| capacité du cache (experts par couche) | part des experts | taux de succès |
|---|---|---|
| 8 | 6 % | 33,7 % |
| 16 | 13 % | 58,5 % |
| **32** | **25 %** | **74,8 %** |
| 64 | 50 % | 82,3 % |
| 128 | 100 % | 82,7 % |

Le rendement est **très favorable au début** : un quart des experts en cache
(32 sur 128) sert **de 75 à 87 % des lectures** selon le texte, et la moitié en
sert 92 à 93 %. C'est exactement la forme qu'il
faut pour un modèle « trop gros pour le local » : on ne garde pas tout, on garde
le quart le plus chaud et on divise le trafic par quatre.

## 3. Ce que ça change pour Kimi-K3 — et ce que ça ne dit pas

Transposition, **avec ses réserves** : Kimi-K3 a 896 experts (7× plus), 16 par
jeton (2× plus) et un routage **sigmoïde** (celui de Qwen3-30B est softmax) — la
courbe de réutilisation y sera **différente**, et c'est le jalon M6 de la
mesurer sur le modèle lui-même. Mais l'ordre de grandeur, lui, change tout :

- trafic d'experts sans cache : **24,7 Go/jeton** ;
- avec un cache qui capte 80 % (le quart le plus chaud) : **5,1 Go/jeton** ;
- à 3,4 Go/s (NVMe, 4 flux **mesurés**), cela fait 1,5 s/jeton au lieu de 7,3 ;
- et la partie dense (62 Go, résidente) coûte 1,6 s/jeton à 40 Go/s (RAM à
  8 fils, **mesurée**) : **≈ 3,1 s/jeton** au lieu de 9 s, sans rien changer au
  moteur qu'un cache.

> Les deux débits utilisés ici ont été **remesurés** au bloc 30 : le dépôt citait
> « 20 Go/s » pour la RAM ; la mesure donne 9,6 Go/s à un fil et **40,3 Go/s** à
> huit — et 2,26 → 3,39 Go/s pour le NVMe selon le nombre de flux.

Autrement dit : **la réutilisation est le levier**, et le chiffre à vérifier en
premier sur Kimi-K3 est le même que celui-ci — pas la peine d'écrire un cache
avant de l'avoir.

## 4. Réserves, nommées

1. **Un seul modèle, deux textes, 48 et 128 jetons.** Les deux textes donnent la
   même réutilisation immédiate (47-49 %), mais ils sont tous les deux de la
   prose/code technique : le dialogue, le multilingue et le très long contexte
   restent à mesurer. Les gros MoE (Kimi-K2.7 à 384 experts, Qwen3-235B à 128)
   suivront **quand le disque sera libre** (un téléchargement de 1,5 To écrit
   dessus en ce moment, et il fait tomber le débit des lectures — mesuré : le
   premier jeton de Qwen3-235B n'est pas sorti en 13 minutes).
2. **Le routage par TABLE (`tid2eid`, V4) n'est pas concerné** : il ne dépend que
   de l'identifiant du jeton, donc sa réutilisation se lit dans le fichier sans
   rien calculer. Ce sera un contrôle croisé gratuit.
3. **Le taux de succès n'est pas le gain de temps** : un cache ajoute de la
   gestion et de la mémoire. Le cache RAM d'experts a déjà été mesuré **plus
   lent** sur V4.1 (+4 % à 4 Go, +21 % à 32 Go) — mais c'était un cache *sans
   hiérarchie de stockage* : le noyau servait déjà tout depuis le `buff/cache`.
   Ici, l'enjeu est de **ne pas relire le NVMe**, ce qui est une autre question.
