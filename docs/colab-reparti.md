# Répétition Colab — la phase 3.4, pas à pas

Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.

Ce document est la recette ; l'état du protocole et les chiffres qui la
dimensionnent sont dans `docs/format-flux.md` et
`reports/rapport-transport-liste.md`.

## Ce qui est déjà vérifié, et ce qui ne l'est pas

| point | état |
|---|---|
| fidélité du découpage | ✅ écart **0,00e0** entre local et deux nœuds (40 et 200 jetons) |
| version du protocole | ✅ dans chaque en-tête ; un pair incompatible est refusé en le disant |
| réglages qui changent les chiffres | ✅ niveaux, seuil, top-k, renorm voyagent dans l'en-tête |
| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |
| au-delà de localhost | ✅ testé sur l'IP du réseau local (`--flux-serveur 0.0.0.0:PORT`) |
| **deux machines avec le même fichier GGUF** | ❌ les deux nœuds chargent le modèle ENTIER (`Model::load` lit tout le fichier) — le découpage porte sur le CALCUL |
| **préremplissage par lots sur le fil** | ❌ un flux par jeton aujourd'hui, donc séquentiel |

Les deux ❌ sont des limites assumées, pas des oublis : elles disent ce que la
démonstration peut prétendre. Un petit modèle tient sur les deux machines ; le
préremplissage par lots est le chantier suivant.

## Dimensionnement (mesuré)

* **Débit** : 3 623 octets par flux en dense, 1 989 en listes à échelle par bloc
  (68 % d'activité). À 20 jetons/s : **moins de 1 Mbit/s**. Le débit n'est pas le
  problème, même sur un lien domestique.
* **Latence** : chaque jeton paie un aller-retour. Un aller-retour Colab ↔
  connexion domestique se compte en dizaines de millisecondes ; le calcul distant
  de 12 couches de Qwen2.5-0.5B coûte ~15 ms sur ce serveur. À 40 ms d'aller-
  retour, le banc réparti sera ~2,5× plus lent que le local — et c'est normal :
  **le découpage sert à faire tenir un modèle qui ne tient pas sur une machine,
  pas à accélérer.**

## Topologie recommandée : le nœud moteur EN LOCAL, le pilote sur Colab

Colab n'accepte aucune connexion entrante. Un tunnel est donc nécessaire dans un
sens ou dans l'autre, et il est plus simple de le tenir sur la machine qu'on
administre :

```
   [ Colab ]                                    [ votre machine ]
   pilote : couches 0..12                       nœud moteur : couches 12..24
   --ppl-reparti <hôte-public>:PORT  ─────────▶ --flux-serveur 0.0.0.0:PORT
                                    ◀─────────  flux résultant
```

Le tunnel (au choix) : `cloudflared tunnel --url tcp://localhost:5599`,
`ssh -R`, ou un Tailscale des deux côtés (`--flux-serveur 100.x.y.z:5599`).

### Côté local

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --flux-serveur 0.0.0.0:5599 --ctx 256
# puis, dans un autre terminal, le tunnel vers 5599
```

### Côté Colab

```python
!git clone <votre-dépôt> drave && cd drave/drave-core && cargo build --release -q
# le MÊME fichier GGUF que le nœud moteur (0,57 Go pour Qwen2.5-0.5B)
!cd drave && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl-reparti <hôte-public>:5599 --couches-locales 12 --limit 200 --ctx 256
```

### Ce qu'on lit dans la sortie

```
  référence locale  : perplexité ...       <- le même modèle, calculé entièrement sur Colab
  deux nœuds        : perplexité ...       <- 12 couches sur Colab, 12 en local
  écart             : 0.00e0               <- le critère de la phase 3.4
  transport         : ... octets par flux ...
  temps             : ... ms en local · ... ms à attendre le pair
```

Le critère de succès de la phase 3.4 est **l'écart**, pas la vitesse : les mêmes
logits qu'en local, à 1e-5 près. En mode dense il doit être **exactement** nul
(le transport est du f32, donc sans perte) ; en mode listes, il dépend du seuil —
utiliser `--flux-blocs --act-thresh 0.02` (÷2 sur le fil pour 0,2 %).

## Les pièges déjà payés, pour ne pas les repayer

1. **Même build des deux côtés** : la version est dans chaque en-tête, un
   désaccord est refusé avec un message clair — mais autant cloner le même commit.
2. **Même fichier GGUF** : les deux nœuds chargent le modèle entier. Un GGUF
   différent (quantification, version) donne des calculs différents.
3. **`--act-thresh` identique** : il voyage désormais dans l'en-tête, donc le
   client impose le sien — mais c'est le client qui gagne, pas le serveur.
4. **Nagle** : déjà neutralisé dans le code (`set_nodelay(true)`), mais si un
   proxy s'intercale, vérifier qu'il ne réintroduit pas de mise en tampon — c'est
   6× le temps de calcul qu'on a perdu une fois.
5. **Contexte du nœud moteur** : `--ctx` est respecté des deux côtés depuis peu.
   Un nœud moteur en contexte 4096 pour un banc en 256 payait des tampons seize
   fois trop grands.
