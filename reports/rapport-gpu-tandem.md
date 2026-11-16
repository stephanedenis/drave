# Les deux GPU en tandem NVLink contre le CPU — ce qui se décharge, et à quel prix

> **La question.** « Qu'est-ce qui peut être optimisé avec nos 2 GPU en tandem NVLink vs CPU ? Peut-on
> décharger le CPU du gros de sa charge, ou plus ? »
> **La réponse courte.** **Oui pour Drave** : l'entraînement (×12 à ×39 selon la charge), le
> préfill et le batch (×12), les gros modèles (le tandem) — mais **le 34 M n'utilise pas les GPU** :
> il est trop petit (le lancement des noyaux domine), et la génération est **latence-bornée par
> l'absence de cache KV**, pas par le matériel. **Le « gros » du CPU, lui, n'est pas Drave** : c'est
> `vcam3d-studio` (10 cœurs) — un GPU pourrait le décharger, mais c'est **votre** application.

## 1. Le matériel, mesuré

| élément | valeur | la mesure |
|---|---|---|
| **2 × Quadro RTX 5000** | 16 Go chacune, **compute 7.5** (Turing), FP32 ~11,2 TFLOPS, tenseurs FP16 ~89 TFLOPS | `nvidia-smi` |
| **le NVLink** | **25,78 Go/s** par lien (la fiche) — **23,1 Go/s** mesurés (une copie de 256 Mo entre les cartes) | `nvidia-smi nvlink -s` + la copie |
| le P2P | **activé** dans les deux sens | `can_device_access_peer` |
| **le CPU** | 2 × Xeon **E5-2687W v3** (20 cœurs, 40 fils, AVX2), 125 Go de RAM | `lscpu`, `free` |
| **la charge** | `load average 15/40` — **`vcam3d-studio` 1 005 %** + `kinect2-bridge` 135 % | `ps` |
| **le garde GPU** | `hauru-gpu-guard` **inactif** | `systemctl --user` |

## 2. Les mesures

### 2.1 L'entraînement du 34 M (le pas complet, 8 × 1 024 jetons)

| moteur | s/pas | jetons/s | × CPU chargé |
|---|---:|---:|---:|
| **CPU** (sous la charge actuelle) | **5,218** | 1 570 | 1× |
| CPU (à vide, d'après l'entraînement de référence) | ~0,44 | ~18 600 | — |
| **GPU 0, fp32** | **0,416** | 19 696 | **12,5×** |
| **GPU 0, fp16 (autocast)** | **0,134** | **61 156** | **39×** |
| **2 GPU en parallèle** (2 répliques) | **0,136** | **120 578** | **77×** |
| l'échange des gradients (137 Mo) | 0,0073 s | 18,8 Go/s | 5,5 % du pas |

**Lecture.** Le GPU **divise le pas par 12 à 39** — mais **surtout parce que le CPU est chargé**
(le `vcam3d` prend 10 cœurs). À vide, le CPU (~0,44 s) est **au niveau du GPU fp32** (0,416) : le
34 M est **trop petit** pour que le GPU s'impose. En fp16, le GPU garde **3,3×** à vide et **39×
sous charge** — et le **tandem double** (la réplique) pour **5,5 %** d'échange NVLink.

### 2.2 L'inférence

| mesure | CPU | GPU 0 |
|---|---:|---:|
| un pas avant, contexte 1 024 (1 séquence) | ~28 ms | **24 ms** |
| le **préfill** (le même texte en 1 passe) | ~1 500 jetons/s | **42 430 jetons/s** |
| le batch 8 / 32 | — | **49 284 / 48 315 jetons/s** |
| le contexte 32 → 1 024 (le pas) | — | 11,4 → 23,6 ms |

**Lecture — le résultat qui compte.** La **génération** (1 octet à la fois) coûte **~24 ms/octet**
sur le GPU comme sur le CPU : ce n'est **pas** le matériel, c'est **l'absence de cache KV** (le
modèle recalcule les 1 024 positions à chaque octet). Le **batch** (le préfill, l'analyse) donne
**12×** au GPU ; la **génération** ne bouge pas tant que le cache n'existe pas.

### 2.3 Le tandem (le NVLink)

- **Le P2P** : actif ; la copie **23,1 Go/s** (vs le PCIe 3.0 ~6–8 Go/s — **~3×**).
- **Le data-parallel** : les 2 répliques, **120 578 jetons/s** (le double) ; l'échange des gradients
  (137 Mo, l'aller) coûte **7,3 ms** = **5,5 %** du pas — le NVLink suffit largement.
- **Le tensor-parallel** (le modèle coupé en deux) : inutile pour le 34 M (il tient dans 16 Go) ;
  utile pour **1 Md+** (les 2 × 16 Go = 32 Go, les poids + l'optimiseur).

## 3. Ce qui se décharge — et ce qui ne se décharge pas

| charge | qui la porte | le GPU peut-il la prendre ? | le gain |
|---|---|---|---|
| **l'entraînement natif** (34 M : 3,7 h) | CPU | **oui**, et le tandem double | **12–39×** (3,7 h → 10–20 min), **×77** en tandem |
| **le préfill / l'analyse en lot** | CPU | **oui** (le batch) | **×12** |
| **la génération** (1 octet à la fois) | CPU/GPU | **non** — c'est le cache KV qui manque | ×20–50 **sans GPU** (le cache) |
| **les bancs** (136 générations) | CPU | oui (le batch) | ×10 |
| **l'autotest, la passe** | CPU | partiellement (les portes neurales) | ×2–5 |
| **`vcam3d-studio`** (10 cœurs) | CPU (votre app) | **oui, en principe** (la 3D est GPU) | à voir avec son code |
| **le bloc linguistique** (`analyser`, 0,8 s/10 000 mots) | CPU | non (le GPU serait plus lent) | — |

## 4. Les recommandations

1. **Le cache KV d'abord** : c'est le levier **×20–50** de la génération, sans GPU. Le banc
   (`generer_natif`, `drvm_infere`) recalcule tout le contexte à chaque octet — le cache le
   ramènerait à **~1 ms/octet** (le pas d'un jeton).
2. **L'entraînement sur le GPU** : le pas du 34 M en fp16 = **0,134 s** (vs 5,2 s chargé) ; le
   palier 1 (100–150 M) sera **impossible en CPU** sous la charge actuelle — le GPU est la
   condition, pas l'option.
3. **Le tandem pour le palier 2** (300–600 M) : les 2 × 16 Go + le data-parallel (×2) ou le
   tensor-parallel (le modèle coupé) ; le NVLink (23 Go/s) suffit (5 % d'échange).
4. **Le préfill en lot** pour les analyses massives (les 612 phrases, les 50 textes) : ×12 au GPU.
5. **`vcam3d`** : si son rendu est du GPU, le décharger libérerait **10 cœurs** — c'est votre code.

## 5. Les limites

- **La règle 11** : les GPU sont **réservés à Drave** ; `vcam3d` n'en fait pas partie — le
  décharger serait une **exception** à décider.
- **Le garde** `hauru-gpu-guard` est **inactif** : rien ne protège les GPU aujourd'hui ; le
  réactiver serait prudent.
- **Le 34 M est trop petit** : le GPU est **sous-utilisé** (11 ms de lancement pour 11 ms de
  calcul) ; le gain vient des **gros modèles** et du **batch**, pas du petit.
- **Le compute 7.5 (Turing)** : pas de TF32, pas de BF16 — le fp16 avec l'échelle de perte est le
  seul mode rapide ; les noyaux récents (FlashAttention 3) ne tournent pas.
- **Le mode fp16** n'a pas été validé sur la convergence : le banc mesure la vitesse, pas la
  qualité d'un entraînement fp16.

## 6. Fichiers

- Les bancs : `/tmp/bench_gpu.py`, `/tmp/bench_2gpu.py`, `/tmp/bench_ar.py`, `/tmp/bench_inf.py`
  (les mesures du jour ; à promouvoir en `tools/` si le sujet avance).
- Le rapport : ce document.
