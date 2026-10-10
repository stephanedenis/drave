# Modularisation et parallélisme — ce que la mesure dit de faire

> 9 octobre 2026. Réponse à « faut-il diviser en submodules et paralléliser sur
> plusieurs cœurs ? ». La réponse est **oui pour paralléliser, non pour les
> submodules** — et les deux moitiés sont chiffrées ci-dessous.

---

## 1. Le dépôt est publié

`https://github.com/stephanedenis/drave` (**privé**), remote `origin` en SSH
(`git@github.com:stephanedenis/drave.git`), branche `master` suivie.
469 fichiers, 32 Mo d'historique, journaux de session compris.

**⚠️ Un jeton d'accès personnel (`ghp_…`) a été retrouvé dans le magasin
d'identifiants de git et est apparu en clair dans le transcript de la session.**
Il devrait être **révoqué et remplacé** — il n'est pas nécessaire au
fonctionnement : la clé SSH `~/.ssh/id_ed25519_github` suffit pour pousser, et la
configuration globale réécrit déjà `https://github.com/…` en SSH.

---

## 2. Submodules : non. Espace de travail Cargo : oui

Un **submodule** sert à épingler un **dépôt séparé** dans un autre. Il n'a jamais
servi à découper du code dans un même dépôt — pour cela, l'outil est l'**espace de
travail Cargo** (`[workspace]` + plusieurs caisses), qui donne :

- la **compilation parallèle** des caisses indépendantes ;
- des **frontières vérifiées par le compilateur** (une caisse ne peut pas toucher
  aux entrailles d'une autre sans le déclarer) ;
- moins de **conflits** quand deux personnes travaillent en parallèle ;
- et, plus tard, des versions indépendantes si l'envie vient.

**Ce qui mérite un vrai submodule**, en revanche : le **journal de sessions**
(9 Mo de transcriptions, 3 fichiers de 1 à 9 Mo, qui grossissent tout seuls et
n'ont aucun rapport avec le code), et les **dépendances externes épinglées**.
Le journal est le seul candidat sérieux aujourd'hui.

### Le découpage proposé, d'après les dépendances réelles

Mesuré sur les 28 758 lignes du crate unique et sur les `crate::` internes :

| caisse proposée | modules actuels | lignes | dépend de |
|---|---|---:|---|
| `drave-formats` | `gguf` (2 357) · `formats` (2 901) | 5 258 | rien |
| `drave-tokenizer` | `tokenizer` (731) | 731 | rien |
| `drave-list` | `list` (1 597) | 1 597 | formats |
| `drave-model` | `model` (9 343) | 9 343 | formats, list |
| `drave-k3` | `kimi_k3` (1 866) | 1 866 | formats, list, model |
| `drave-runtime` | `engine` (1 029) · `gpu` (1 573) · `clusters` (506) · `materiel` (478) · `engram` (408) | 3 994 | formats, list, model |
| `drave-cli` | `main` (5 969) | 5 969 | tout |

**Deux fichiers portent 53 % du code** (`model.rs` 9 343 + `main.rs` 5 969) : c'est
là que le découpage rapporte — et c'est aussi là que deux intervenants se marchent
dessus aujourd'hui. `main.rs` est le premier à sortir : 5 969 lignes de modes, de
drapeaux et d'analyse d'arguments n'ont rien à faire dans le même fichier que le
noyau.

**Contrainte à préserver** : le crate est aujourd'hui **std seul, sans aucune
dépendance** (`Cargo.toml` : *« aucune : std seul, pour rester sans dépendance
réseau »*). Le découpage ne doit pas l'entamer — un espace de travail de caisses
`std` reste sans dépendance externe.

---

## 3. Paralléliser la compilation : ×3 disponible, mesuré

Recompilation du crate, machine sous charge de fond :

| profil | temps | CPU utilisé |
|---|---:|---:|
| **actuel** (`lto = true`, `codegen-units = 1`) | **37,98 s** | **100 %** — un seul cœur |
| `codegen-units = 16`, `lto = "thin"` | **12,64 s** | 385 % |
| `codegen-units = 16`, `lto = false` | 11,67 s | 319 % |

**Le profil de release actuel compile sur un cœur**, sur une machine à 40 threads.
C'est un choix explicite (binaire plus rapide), et il se paie à chaque itération.

**La règle à inscrire, et elle n'est pas négociable** : le profil `release` est
celui du **binaire de mesure**. Toutes les mesures du dépôt — 0,210 ns par
événement, croisement push/pull à 22-25 %, débits — sont attachées à ce binaire.
Donc :

1. on **ajoute** un profil d'itération (`[profile.rapide]` : `codegen-units = 16`,
   `lto = "thin"`) pour le développement et les tests — 12 s au lieu de 38 ;
2. on **garde** `release` tel quel pour les mesures ;
3. et **toute promotion vers `release` se paie d'un passage de TOUTES les portes**
   (`tools/toutes-les-portes.sh`), parce
   qu'elle change les nombres.

Les 77 tests, eux, tournent déjà en 12 s : les exécuter en parallèle d'un
entraînement ne coûte rien.

---

## 4. Paralléliser le travail : par RESSOURCE, pas par cœur

La campagne a mesuré la contrainte, et elle n'est pas le nombre de cœurs :
**deux lecteurs du même fichier de 63 Go font tomber le débit effectif à 8,6 Mo/s**
(contre 243 Mo/s en séquentiel), et les deux tentatives de porte gpt-oss ont expiré
pour cette raison. Le schéma qui marche :

| ressource | règle |
|---|---|
| **VRAM (16 Go)** | **1 entraînement à la fois** — c'est le vrai facteur limitant |
| **disque des modèles** | **au plus 1 lecteur lourd** — la ressource rare, à utiliser comme sémaphore |
| **processeur** | N mesures en parallèle sans risque : elles sont **déterministes** (perplexité, événements, paires) |
| **compilation / tests** | toujours possibles en parallèle (ni disque de modèles, ni VRAM) |

**Et une leçon de mise en œuvre** : les chaînes de cette session sérialisaient leur
travail par un `pgrep` sur un motif de ligne de commande — qui **s'est mordu la
queue trois fois** (le motif apparaît dans la ligne de commande de l'appelant). Un
**fichier verrou par ressource** (`flock`) est la bonne primitive ; c'est ce qu'il
faut écrire avant de multiplier les travailleurs.

---

## 5. Ce qu'il faut faire, dans l'ordre

1. **Révoquer le jeton** qui a fuité, et ne garder que la clé SSH.
2. **Extraire `main.rs`** dans une caisse `drave-cli` (5 969 lignes → le noyau
   respire), puis `formats`/`tokenizer`/`list` — les trois couches sans dépendance
   croisée, donc sans risque.
3. **Ajouter le profil `rapide`** et l'utiliser par défaut en développement ;
   garder `release` pour les mesures, avec passage des portes à chaque promotion.
4. **Remplacer les gardes `pgrep` par des verrous** (`flock`) dans les chaînes.
5. **Sortir le journal** en submodule (ou en dépôt séparé) le jour où il gêne —
   pas avant.

**Ce que ce plan ne fait pas** : il ne rend pas le moteur plus rapide. La
modularisation est une affaire de **débit de développement**, pas de performance —
et confondre les deux serait la seule vraie erreur ici.
