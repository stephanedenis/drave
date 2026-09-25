# Qtrinet

Inférence de LLM en **ternaire / multi-bits** sur un cluster de cartes **Stratix V**
(Microsoft Storey Peak) — 100 % logique, sans DSP.

Le cahier des charges d'origine est dans [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md).
⚠️ **Il a été audité et corrigé** : voir la section « Écarts avec le CDC » ci-dessous.

---

## État du projet

| Étape | État |
|-------|------|
| Audit du cahier des charges | ✅ (corrections ci-dessous) |
| **Test de principe : quantification d'un modèle minimal** | ✅ **fait** → [`reports/rapport-minimal.md`](reports/rapport-minimal.md) |
| Modèle ternaire *entraîné* (BitNet b1.58) | ⬜ à faire |
| Extracteur GGUF → plans ternaires | ⬜ à faire |
| Format binaire + schéma partagé Python/RTL | ⬜ à faire |
| RTL : PE ternaire + décodeur | ⬜ à faire |

Le matériel est prêt de son côté : voir le dépôt
[`FPGA-Stratix-V`](../FPGA-Stratix-V) — carte détectée (Gen3 ×8), JTAG validé
(`0x029070dd`), Quartus Prime Standard 21.1 opérationnel, bitstream produit.

---

## Test de principe (`run_quantify.py`)

Un MLP minimal (32→64→10) est **entraîné** en numpy (aucune dépendance ML), puis
quantifié selon plusieurs formats. Trois questions, chiffres en main :

**1. Le chemin entier est-il exact ?** Oui — écart avec le calcul flottant :
**4,2e-07** (couche 1) et **1,9e-06** (couche 2), soit de l'arrondi flottant pur.
Le principe « que des additions/soustractions, aucun DSP » est validé. Le biais
s'ajoute à la remise à l'échelle, hors du réseau de MAC.

**2. Le ternaire préserve-t-il le modèle ?**

| Format | b/poids | Accuracy |
|--------|---------|----------|
| float32 | 32 | 76,07 % |
| int8 | 8 | 76,27 % |
| int4 | 4 | 74,12 % |
| **ternaire 1,58 b (dense 2 b)** | **2** | **49,71 %** |
| multi 2 plans | 4 | 73,44 % |
| multi 3 plans | 6 | 74,12 % |
| multi 4 plans | 8 | 75,98 % |

➡️ La quantification ternaire **a posteriori** détruit la fonction (−26 pt). Ce n'est
pas un verdict contre BitNet : les modèles b1.58 sont **entraînés** avec la contrainte.
Le découpage en plans (multi-bits) dégrade au contraire très progressivement.

**3. Combien coûte chaque encodage ?**

| Encodage | Ternaire | 4 plans |
|----------|----------|---------|
| dense (1 bit/plan) | **2,0 b/poids** | **4,0 b/poids** |
| bitmap + signe | — | 8,0 b/poids |
| **CSR par plan (le CDC)** | **10,1 b/poids** | **61,8 b/poids** |

➡️ Le CSR coûte **5 à 15× le dense** en trafic mémoire. Sur un système borné par la
DDR3, cela divise directement le débit.

**4. Débit projeté** (débits **mesurés** : DDR3 9,66 Go/s, fmax 124 MHz) :

| Modèle | Encodage | tok/s par carte |
|--------|----------|-----------------|
| 7B | ternaire dense 2 b | **5,5** |
| 7B | 4 bits | 2,8 |
| 7B | ternaire CSR | 0,6 |

➡️ **312 voies de MAC suffisent** (≈ 9 400 ALM, 5 % du FPGA) pour saturer la DDR3.
Le projet est un projet **système mémoire**, pas un projet de PE.

---

## Écarts avec le CDC d'origine

| Point du CDC | Réalité vérifiée |
|---|---|
| « transceivers 40 Gbps » | Aucun transceiver Stratix V GS ne dépasse 12,5 Gbps : le 40G = 4 × 10,3125 Gbps via QSFP+ |
| « NVLink entre les 2 RTX 5000 » | ✅ **exact** — mesuré à 25,78 Go/s par lien |
| « M20K en lecture combinatoire » | Le M20K est **synchrone** (1-2 cycles) ; l'asynchrone, c'est le MLAB |
| « CSR pour éliminer les zéros » | Coûte 5-15× le dense (cf. §3) et impose des accès aléatoires aux activations |
| « 1,58 bit » | Vrai pour un ternaire **entraîné** ; faux pour un Q4 bit-slicé |
| DMA « VFIO ou XDMA » | Ni l'un ni l'autre : l'IP DMA + driver existent déjà (6,5 Go/s mesurés) |

---

## Structure

```
Qtrinet-bootstrap.md    cahier des charges d'origine (à lire avec les écarts ci-dessus)
src/ternary.py          quantification ternaire/multi-bits, plans, encodages, MAC entier
src/tiny_model.py       MLP minimal + entraînement numpy (aucune dépendance ML)
src/roofline.py         projection matérielle (constantes mesurées de la carte)
run_quantify.py         orchestrateur : entraîne, quantifie, mesure, écrit le rapport
reports/                rapports générés
```

## Lancer

```bash
python3 run_quantify.py --epochs 400      # ~10 s, numpy seul
```

Aucune dépendance hors `numpy`. (`torch`/`gguf`/`transformers` seront nécessaires
plus tard, pour les modèles réels — pas pour le test de principe.)

---

## Prochaines étapes

1. **Modèle ternaire entraîné** : implémenter un entraînement avec poids ternaires
   (straight-through estimator) ou récupérer un petit modèle BitNet b1.58 pour
   trancher la question « le ternaire suffit-il ? ».
2. **Extracteur** : GGUF/safetensors → plans → format binaire packé, avec un
   **schéma unique** générant à la fois le packer Python et le paquet SystemVerilog
   (contrainte de cohérence des largeurs de bus du CDC).
3. **RTL** : PE ternaire (mux + add/sub + accumulateur 24 bits) et décodeur, puis
   mesure réelle du débit sur la carte.
