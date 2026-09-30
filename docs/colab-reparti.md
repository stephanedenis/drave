# Répétition Colab — la phase 3.4, pas à pas

Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.

Ce document est la recette ; l'état du protocole et les chiffres qui la
dimensionnent sont dans `docs/format-flux.md` et
`reports/rapport-transport-liste.md`.

## Mise en place, concrètement

`tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo
avec tout l'historique) et affiche l'empreinte SHA-256 du modèle — les deux nœuds
doivent charger le même GGUF, la dimension ne voyage pas. `colab/README.md` donne
la marche à suivre (tunnel, téléversements) et `colab/Drave-reparti.ipynb` est le
notebook prêt à ouvrir, avec la vérification d'empreinte et la lecture du résultat.

## Ce qui est déjà vérifié, et ce qui ne l'est pas

| point | état |
|---|---|
| fidélité du découpage | ✅ écart **0,00e0** entre local et deux nœuds (40 et 200 jetons) |
| version du protocole | ✅ dans chaque en-tête ; un pair incompatible est refusé en le disant |
| réglages qui changent les chiffres | ✅ niveaux, seuil, top-k, renorm voyagent dans l'en-tête |
| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |
| au-delà de localhost | ✅ testé sur l'IP du réseau local (`--flux-serveur 0.0.0.0:PORT`) |
| **deux machines avec le même fichier GGUF** | ❌ les deux nœuds chargent le modèle ENTIER (`Model::load` lit tout le fichier) — le découpage porte sur le CALCUL |
| **préremplissage par lots sur le fil** | ✅ mode 3, `--lot T` : 256 jetons en 4 lots, écart **0,00e0** (`reports/rapport-prefill-reparti.md`) |

La limite qui reste est assumée, pas oubliée : **les deux nœuds chargent le
modèle entier**. Un petit modèle tient sur les deux machines ; c'est le
préremplissage par lots (fait depuis) qui manquait pour que la démonstration ne
paie pas la latence 256 fois.

## Dimensionnement (mesuré)

* **Débit** : 3 663 octets par flux en dense (en-tête v4 compris), ≈ 1 419 en
  listes à échelle par bloc à 68 % d'activité. En **lots** (`--lot 64`), c'est
  229 455 octets par lot de 64 jetons, soit **3,5 ko par jeton** — et surtout UN
  aller-retour par lot. À 20 jetons/s : **moins de 1 Mbit/s**. Le débit n'est pas
  le problème, même sur un lien domestique.
* **Latence** : chaque jeton paie un aller-retour, et c'est le seul poste qui
  compte. Mesuré avec un relais retardateur (`tools/proxy_latence.py`, 256 jetons,
  12 couches par nœud) : `attente ≈ calcul distant + 3,2 × (latence par message)`.
  Concrètement,

  | latence ajoutée | attente par jeton | rapport au calcul local |
  |---|---|---|
  | 0 ms (localhost) | 16,8 ms | 1,01× |
  | 5 ms | 33,0 ms | 1,99× |
  | 20 ms | 81,8 ms | 4,89× |

  Un aller-retour Colab de 60 ms donne donc ≈ 112 ms par jeton, soit ~8 jetons/s
  au lieu de ~60 en local — et la fidélité, elle, ne bouge pas (0,00e0 partout).
  **Le découpage sert à faire tenir un modèle qui ne tient pas sur une machine,
  pas à accélérer** ; c'est ce que la démonstration devra montrer, et le tableau
  ci-dessus dit d'avance ce qu'elle mesurera.

  **Le mode lot change l'ordre de grandeur du préremplissage** : mesuré avec un
  relais qui ajoute 20 ms par message (64 jetons, 12 couches par nœud), un seul
  lot prend **2,6 s** là où un flux par jeton en prend **47,6 s** — 18×, à
  fidélité identique. C'est pourquoi le notebook lance le banc avec `--lot 64` :
  sans lui, la démonstration paierait 63 fois la latence du lien.

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
utiliser `--flux-blocs --act-thresh 0.01` (÷2,3 sur le fil pour 1,3 % à 1 024 jetons).

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
