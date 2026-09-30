# La répétition Colab, en pratique

But : faire tourner le **pilote** sur Colab et le **nœud moteur** chez vous, et
vérifier que le calcul coupé redonne exactement le calcul local (`écart : 0.00e0`
en mode dense). La recette de fond est dans `docs/colab-reparti.md` ; ici, la
mise en place.

## 1. Sur votre machine : préparer

```bash
tools/preparer_colab.sh                     # dépôt en un fichier + empreinte du modèle
```

Il produit `/tmp/drave.bundle` (≈4,5 Mo, tout l'historique git) et affiche le
SHA-256 des 24 premiers caractères du modèle. **Notez-le** : la cellule 4 du
notebook le vérifie, et c'est ce qui garantit que les deux nœuds calculent le
même modèle.

## 2. Téléverser sur Colab

Deux fichiers, et rien d'autre :

* `drave.bundle` (4,5 Mo) — via le sélecteur de fichiers ou votre Drive ;
* le GGUF, **le même des deux côtés** (507 Mo pour Qwen2.5-0.5B-Q8_0).

## 3. Monter le tunnel

Colab n'accepte aucune connexion entrante : c'est le nœud moteur local qui doit
être joignable. Trois voies, par ordre de simplicité :

| voie | commande locale | compte requis |
|---|---|---|
| ngrok | `ngrok tcp 5599` | gratuit, un authtoken |
| Tailscale | `tailscale up` des deux côtés | gratuit, un compte |
| SSH inverse | `ssh -R 5599:localhost:5599 votre-vps` | une machine publique |

Puis, en local :

```bash
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 0.0.0.0:5599 --ctx 256
ss -ltn | grep 5599          # le port écoute-t-il ?
```

## 4. Sur Colab : le notebook

`colab/Drave-reparti.ipynb` — sept cellules : environnement, chaîne Rust, clonage
depuis le bundle, vérification du modèle, compilation, banc réparti, lecture du
résultat. Remplacez `HOTE, PORT` par ce que le tunnel vous a donné.

## 5. Ce qu'on attend, et ce que ça veut dire

```
écart : 0.00e0                ← le critère. Le transport f32 est sans perte, donc
                                le découpage ne doit pas changer un chiffre.
transport : LOTS de 64 jetons · ~229 000 octets par lot
temps : ~1,6 s de calcul local par lot · ~1,6 s à attendre le pair
```

À 60 ms d'aller-retour, comptez **~8 jetons/s** contre ~60 en local : le
découpage sert à faire tenir un modèle qui ne tient pas sur une machine, pas à
accélérer. Le débit, lui, n'est jamais le problème (< 1 Mbit/s).

## Les pièges, déjà payés une fois chacun

1. **Modèle différent** d'un côté ou de l'autre : la dimension ne voyage pas, les
   deux nœuds doivent charger le même fichier (d'où l'empreinte vérifiée).
2. **Version du protocole** : un pair incompatible est refusé en la nommant —
   cloner le même commit des deux côtés.
3. **Réglages d'activation** : ils voyagent et c'est le client qui impose les
   siens ; inutile de reproduire la ligne de commande exacte sur les deux bords.
4. **Nagle** : neutralisé dans le moteur (`set_nodelay`), mais un proxy peut le
   réintroduire — il a coûté 6× le temps de calcul une fois.
5. **Pas de flux par jeton** : `--lot 64` (ou plus) regroupe le préremplissage en
   un aller-retour par lot. Sans lui, la latence est payée une fois par jeton.
