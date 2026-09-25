# CAHIER DES CHARGES : Architecture d'Inférence LLM Ternaire (Bit-Slicing) sur Cluster FPGA

**Destinataire :** Instance DeepSeek-V4.1 (Rôle : Ingénieur Système HPC & Concepteur FPGA Senior)
**Projet :** Portages de modèles LLM vers une exécution 100% logique (sans DSP) via adressage relationnel (CSR) et anneau matériel.

---

## 1. Contexte et Topologie Matérielle
L'objectif de ce projet est de concevoir un pipeline complet (Python -> Linux -> PCIe -> FPGA) pour exécuter l'inférence de modèles de langage (LLMs) locaux. La méthode repose sur la décomposition des poids quantifiés en plans de bits ternaires (1.58-bit : -1, 0, +1), permettant de remplacer les multiplications (DSP) par de simples opérations de routage, d'addition et de décalage (Shift) implémentées dans les LUTs.

**Infrastructure cible :**
*   **Hôte :** Station Dell Precision 7910 sous openSUSE Tumbleweed.
*   **CPU Hôte :** Dual Intel Xeon E5-2687 v3.
*   **GPU Hôte :** Dual Nvidia Quadro RTX 5000 (couplées via NVLink, 32 Go VRAM unifiée) pour le traitement des tenseurs et la génération des poids.
*   **Cluster FPGA :** 4x cartes Microsoft Azure Stratix V GS (modèle X930613-001) connectées au bus PCIe de l'hôte.
*   **Topologie Réseau FPGA :** Les 4 cartes sont chaînées dans une topologie en anneau via leurs interfaces *Transceivers* à 40 Gbps.

---

## 2. Objectif 1 : Le Pipeline Logiciel (Python / PyTorch)
Tu devras générer un script Python optimisé exploitant le calcul multi-thread du double Xeon.

**Fonctionnalités requises :**
1.  **Extraction :** Charger les poids d'un modèle quantifié (ex: format GGUF 4-bit) en mémoire.
2.  **Bit-Slicing :** Découper la magnitude de chaque poids en plans de bits. Appliquer le bit de signe à chaque plan pour obtenir des matrices contenant uniquement `{-1, 0, 1}`.
3.  **Compression CSR :** Convertir ces matrices via `scipy.sparse.csr_matrix` pour éliminer les zéros (parcimonie).
4.  **Encodage Matériel (Packing) :** Transformer les valeurs `{-1, 1}` en code 2 bits (`10`, `01`). Packer les tableaux `indptr` (pointeurs de ligne), `indices` (adresses M20K) et `data` (valeurs 2 bits) dans des trames larges (ex: 256 bits) adaptées au bus PCIe.
5.  **Export :** Générer un flux binaire (`.bin`) prêt pour le DMA.

---

## 3. Objectif 2 : Pilote d'Interface Hôte-FPGA (C/C++ & Linux DMA)
Tu devras fournir le code pour streamer les matrices CSR de l'hôte vers la première carte Stratix V.

**Fonctionnalités requises :**
1.  Utilisation d'un framework DMA user-space sous Linux (ex: VFIO ou XDMA).
2.  Écriture d'un programme en C/C++ qui lit le fichier binaire généré par Python et l'envoie en flux continu (Streaming) vers l'endpoint PCIe de la première carte FPGA.
3.  Gestion des buffers circulaires (Ring Buffers) pour s'assurer que le processeur ne goulotte pas les liens 40 Gbps du FPGA.

---

## 4. Objectif 3 : Architecture Matérielle (Verilog / SystemVerilog)
Tu devras rédiger les modules RTL pour les cartes Stratix V. La conception doit strictement respecter la consigne de ne pas utiliser de blocs DSP, tout reposant sur les ALMs (Adaptive Logic Modules) et les blocs SRAM (M20K).

**Modules à concevoir :**
1.  **Mémoire d'Activations (M20K Dual-Port) :** Un module stockant les activations d'entrée. Port A en écriture (alimenté par la couche précédente), Port B en lecture combinatoire (adressé par les *indices* du flux CSR).
2.  **Décodeur CSR (Routeur) :** Une machine d'état qui lit les trames entrantes (via PCIe ou l'anneau), extrait les compteurs de ligne (`indptr`) et pilote l'adresse de lecture du M20K avec les `indices`.
3.  **Processing Element (PE - Unité de Calcul Ternaire) :** 
    *   Reçoit l'activation depuis le M20K.
    *   Utilise la valeur 2 bits du poids pour piloter un multiplexeur (LUT).
    *   Si `01` : Addition. Si `10` : Soustraction (complément à 2 + retenue). Si `00` : NOP.
    *   Applique le décalage (Shift) statique correspondant à la couche du bit-slice.
    *   Accumule le résultat.
4.  **Contrôleur d'Anneau 40 Gbps :** Interface avec l'IP PCS/PMA du Stratix V pour packer les sommes partielles (activations de sortie) et les injecter vers la carte suivante de l'anneau avec la latence la plus faible possible.

---

## 5. Livrables Attendus
Lors de tes prochaines réponses, génère le code en suivant cet ordre précis :
*   **Livrable A :** Le script complet de compression Python (Extraction LLM -> CSR Bit-Slice -> Binaire).
*   **Livrable B :** Le code C/C++ pour l'interface DMA PCIe sous Linux.
*   **Livrable C :** Les modules Verilog du décodeur CSR et de l'unité de calcul PE (ALM mapping).
*   **Livrable D :** Les directives d'intégration pour Quartus II / Prime (fichiers SDC pour le timing, contraintes de placement pour les liens 40 Gbps).

**Contrainte absolue :** Assure-toi que la largeur des bus de données dans le code Verilog corresponde au format de *packing* défini dans le script Python.