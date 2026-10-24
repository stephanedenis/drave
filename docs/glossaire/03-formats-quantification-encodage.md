# 3. Formats, quantification, encodage

> **Famille 3 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 3. Formats, quantification, encodage

**b/poids (bits par poids)** — Nombre moyen de bits nécessaires pour stocker un
poids. Un modèle 8 bits coûte 8 b/poids ; le format « liste d'événements » du
dépôt en coûte 1,98, et un encodage ternaire 0,39
(`reports/rapport-optimisations.md:37`, `reports/rapport-valeur-unaire.md:89`).
C'est la mesure qui permet de comparer un format à un autre indépendamment du
nombre de paramètres.

**BitNet b1.58** — Famille de modèles **entraînés** en ternaire (−1, 0, +1), et non
quantifiés après coup ; elle tourne autour de 50-70 % de poids non nuls. Sert de
point de comparaison : « au-delà de ~90 % de zéros, un LLM généraliste s'effondre »
si l'élagage est fait après entraînement (`reports/rapport-eparsite.md:69-71`).
**Réf.** : Ma et al., *The Era of 1-bit LLMs*, [arXiv:2402.17764](https://arxiv.org/abs/2402.17764).

**Bloc de quantification · échelle par bloc** — Les poids quantifiés sont rangés
par paquets (blocs) de 32 ou 256, chacun accompagné d'une **échelle** (un facteur
multiplicatif) qui ramène les entiers dans la dynamique réelle. « Ce n'est pas le
nombre de bits qui compte, c'est la finesse des échelles » : passer d'une échelle
par vecteur à une échelle par bloc de 32 fait tomber le coût du cache KV int8 de
+7,1 % à +1,5 % de perplexité (`docs/contexte-long.md:114-149`).
**Réf.** : Frantar et al., *GPTQ*, [arXiv:2210.17323](https://arxiv.org/abs/2210.17323).

**Dequantification (déquantification)** — Recalcul de la valeur réelle d'un poids à
partir de son entier stocké et de l'échelle de son bloc : `valeur = entier ×
échelle`. C'est l'opération qui coûte du temps à chaque lecture ; la vectoriser par
quatre a fait passer l'attention à 1 M de clés de 13,6 à 7,0 ms par couche
(`docs/contexte-long.md:241-248`).

**E2M1 · E8M0** — Les deux composants du format MXFP4 : **E2M1** est la valeur sur
4 bits (1 bit de signe, 2 d'exposant, 1 de mantisse, soit les huit magnitudes
{0, ½, 1, 1½, 2, 3, 4, 6}) ; **E8M0** est l'échelle de bloc sur 1 octet, une
puissance de deux. Tous deux lus dans le fichier gpt-oss sans requantification
(`reports/rapport-passage-a-l-echelle.md:77-79`).
**Réf.** : *Microscaling Data Formats for Deep Learning*,
[arXiv:2310.10537](https://arxiv.org/abs/2310.10537).

**Échappement · indices par écarts** — Une liste d'indices triés se comprime en
n'écrivant que l'**écart** au neurone précédent, sur un octet. La valeur 255 est
*réservée* : elle annonce un indice absolu sur les deux octets suivants
(l'« échappement »). Mesuré : 99,9997 % des écarts tiennent sur un octet, et la
trace passe de 6 à 3 octets par neurone actif sans aucune perte
(`docs/format-flux.md:43-53`).

**Entropie · Huffman · inégalité de Kraft** — L'*entropie* d'une source est le
nombre minimal de bits par symbole qu'on ne peut pas battre en moyenne ; le codage
de *Huffman* s'en approche ; l'*inégalité de Kraft* (Σ2^−l ≤ 1) est la condition
qu'un code préfixe doit respecter. Le dépôt a **retiré** un gain annoncé de ×2,17
parce que le code proposé violait Kraft (Σ2^−l ≈ 1,99 > 1) — mais un rapport
continue de le citer (`reports/rapport-valeur-unaire.md:49-57`,
`reports/bilan-multi-materiel.md:92`). **Réf.** : Cover & Thomas, *Elements of
Information Theory* — cité sans lien.

**ggml · type ggml · `ggml_blck_size` · `ggml_type_size`** — ggml est la
bibliothèque de tenseurs qui sous-tend llama.cpp, et donc la définition de
référence des types quantifiés. Chaque type déclare combien de poids tient dans un
bloc (`ggml_blck_size`) et combien d'octets pèse ce bloc (`ggml_type_size`) : un
`Q4_K` range 256 poids en 144 octets. La table du moteur est **relevée**, pas
devinée, et confrontée à `libggml` (`tools/verifier_table_types.sh`,
`docs/format-clusters.md:125-158`). **Réf.** :
[ggml-common.h](https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h).

**GGUF (GPT-Generated Unified Format)** — Format de fichier des modèles : un
en-tête de métadonnées (architecture, couches, tokenizer, hyper-paramètres) suivi
des tenseurs de poids, chacun avec son type de quantification. Le moteur le lit **en
place**, en plusieurs fichiers (multi-shards) ou en clusters
(`drave-core/src/gguf.rs`, `Gguf::open_multi`). **Réf.** : spécification officielle
ggml, [ggml/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).

**I8 · I32** — Types entiers signés du GGUF, distincts des types quantifiés. V4.1
contient deux tenseurs d'engram en `I8` (lus par déquantification générique) et
**aucun** `I32` — l'absence est vérifiée sur les deux copies du fichier
(`docs/plan-deepseek41-complet.md:71`).

**int4 · int8** — Précisions entières : 16 niveaux signés pour int4 (ou des
nibbles empaquetés), 256 pour int8. Le vocabulaire du dépôt les distingue de
`i4`/`i8` (types de stockage) et de `Q4_0`/`Q8_0` (formats ggml à échelle par
bloc). Sur le cache KV : int8 coûte +3,0 % de perplexité à 8 192 jetons, int4
+364 % (`docs/contexte-long.md:151-197`).

**IQ2_XXS · IQ1_M · IQ2_S · IQ3_XXS · IQ4_NL · IQ4_XS · IQ1_S** — Famille de types
ggml « i-quants » : des super-blocs de 256 poids à très basse précision (1 à 4
bits) utilisant des codebooks. Ce sont les formats des modèles lourds
(Kimi-K2.7 en `UD-IQ1_M`, GLM-5.3 en `UD-IQ1_S`, V4.1 en `IQ2_XXS`), et un type
absent de la table du moteur a déjà rendu un inventaire faux (8,56 Go annoncés pour
86,9 Go) (`docs/format-clusters.md:133-146`, `docs/plan-deepseek41-complet.md:71`).
**Réf.** : *QuIP#: Even Better LLM Quantization with Hadamard Incoherence and
Lattice Codebooks*, [arXiv:2402.04396](https://arxiv.org/abs/2402.04396).

**Manifeste · `mapping.tsv` · `MANIFEST.json` · `*.moe.json`** — Fichiers qui
décrivent un modèle éclaté : `mapping.tsv` relie `couche · ligne locale · expert
global · cluster` (6 144 entrées pour Qwen3-30B, volontairement en texte lisible) ;
`manifeste.json` dit le rôle de chaque fichier ; `MANIFEST.json` et `*.moe.json`
sont les formats *proposés* pour les modèles multi-shards, pas encore des fichiers
existants (`docs/format-clusters.md:31-47`, `docs/plan-modeles-lourds.md:75-82`).

**MXFP4 (Microscaling FP4 ; virgule flottante 4 bits à échelle microscopique)** —
Format 4 bits par blocs de 32, avec une échelle partagée par bloc. C'est le format
de gpt-oss-120b, lu « tel quel » par le moteur : les blocs du fichier sont les
blocs exécutés, sans copie ni requantification (`docs/convertisseur.md:26-36`,
`reports/rapport-gpt-oss-perplexite.md:6`). **Réf.** : *Microscaling Data Formats
for Deep Learning*, [arXiv:2310.10537](https://arxiv.org/abs/2310.10537).

**Nibble (quartet)** — Un demi-octet, soit 4 bits. Un poids 4 bits est un nibble ;
deux poids tiennent donc dans un octet, l'un dans les bits bas, l'autre dans les
bits hauts (`docs/convertisseur.md:26-33`).

**NVFP4** — Variante 4 bits de NVIDIA (blocs de 16 poids, échelle E4M3) présente
dans la table des types du moteur (`docs/format-clusters.md:134`).
**Réf.** : spécification OCP *Microscaling Formats (MX)* v1.0 — citée sans lien.

**PTQ (Post-Training Quantization ; quantification après entraînement)** — Réduire
la précision d'un modèle **déjà entraîné**, sans réentraînement. Tout le projet est
en PTQ — c'est précisément la limite qu'il mesure : la parcimonie ne s'impose pas,
elle s'entraîne (`reports/bilan-multi-materiel.md:86`,
`docs/programme-recherche.md:89-93`). **Réf.** : Nagel et al., *A White Paper on
Neural Network Quantization*, [arXiv:2103.13630](https://arxiv.org/abs/2103.13630).

**Q2_K · Q3_K · Q4_K · Q5_K · Q6_K · Q8_K (k-quants)** — Types ggml à
**super-blocs** de 256 poids, avec échelles et minima sur 6 bits ; `Q4_K_M` est la
quantification la plus courante des modèles publiés (Qwen3-30B, Qwen2.5-1.5B).
Un bug historique : ggml écrit les quatre quants d'un `Q6_K` en quarts successifs,
le moteur les entrelaçait — trouvé en comparant à une référence F16 des mêmes poids
(`docs/convertisseur.md:210-226`).

**Q4_0 · Q4_1 · Q5_0 · Q5_1 · Q8_0 · Q8_1** — Types ggml « legacy » à blocs de 32
poids et échelle (parfois minimum) sur 16 bits. `Q8_0` est le format de référence
du projet (tête de sortie, projections) ; `Q8_1` est le format des **activations**
chez ggml. Le moteur les lit en place, sans réencodage
(`docs/convertisseur.md:186-193`, `reports/rapport-passage-a-l-echelle.md:13`).

**QPAT** — Format du « greffon » : un en-tête `QPAT | version | couche | n | u[n] |
v[n] | d[n]` décrivant un neurone ajouté à une couche. **Où** :
`tools/make_patch.py`, `--patch` (`reports/rapport-greffon.md:19`).

**Quantification** — Stocker les poids (ou les activations, ou le cache) dans un
format plus compact que le flottant 32 bits, au prix d'une erreur. Les deux
questions du dépôt sont : *combien de bits* et *où sont les échelles* ; la seconde
compte plus que la première (`docs/vision.md:198-227`).
**Réf.** : Nagel et al., [arXiv:2103.13630](https://arxiv.org/abs/2103.13630).

**Quantification du KV** — Quantifier les clés et les valeurs du cache plutôt que
les poids. Résultat central : **tout l'écart vient des clés**, parce qu'une erreur
de clé entre dans le softmax et déplace le poids relatif d'une position entière,
alors qu'une erreur de valeur se moyenne (`docs/roadmap.md:155-194`).
**Où** : `DRAVE_KV_BITS`, `DRAVE_KV_K_F16`, `DRAVE_KV_K_F32`, `DRAVE_KV_V_F32`.

**SHA-256** — Empreinte cryptographique utilisée pour vérifier qu'un fichier
converti contient bien les mêmes octets que la source, tenseur par tenseur
(1 587 tenseurs vérifiés sur Qwen3-30B)
(`docs/format-clusters.md:60-63`). **Réf.** : FIPS 180-4,
[NIST.FIPS.180-4.pdf](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).

**Shard (fragment)** — Un modèle trop gros pour un fichier est publié en plusieurs
**shards** : le premier porte les métadonnées et aucun tenseur, les suivants portent
les poids. DeepSeek-V4-Flash en a 3, Kimi-K2.7 8, GLM-5.3 6
(`docs/plan-deepseek-v4-flash.md:36-46`, `reports/rapport-lecteur-multifichiers.md:30`).
**Où** : `Gguf::open_multi`, `tools/lire_meta_gguf.py`.

**Super-bloc** — Unité de quantification des k-quants et des i-quants : 256 poids
partageant échelles et minima. Un tenseur quantifié se lit donc « en tranches de
256 poids », ce qui rend le découpage par expert possible quand la dimension est
multiple de 256 (`docs/format-clusters.md:50-55`,
`reports/rapport-passage-a-l-echelle.md:84-91`).

**Trinaire · deux listes · plans binaires** — Cas extrême de l'encodage : au lieu
d'écrire des valeurs, on écrit **deux listes**, celle des « + » et celle des « − »,
le signe étant porté par l'appartenance. L'information est alors dans la structure,
pas dans un octet (`docs/vision.md:211-214`, `reports/rapport-encodage.md`).
Les *plans binaires* sont la variante « 4 plans de 2 bits » et le *bitmap* la forme
1 bit/poids + signe (`reports/rapport-optimisations.md:37-38`).

**Unaire (encodage)** — Représenter une valeur en répétant une adresse autant de
fois que sa magnitude : coûteux en taille (42,45 b/poids mesurés) mais donnant un
flux d'événements naturel. Mesuré « 13,7× plus cher » que le décalage-addition
(`reports/rapport-mode-listes.md:19-24`).

**varint (entier à longueur variable)** — Entier codé sur un nombre d'octets
variable selon sa taille. Le décodeur du moteur en décode huit à la fois dans un
mot de 64 bits (technique dite SWAR) ; `reports/rapport-optimisations.md:19`,
`reports/rapport-inference.md:112`.

**zstd (Zstandard)** — Compresseur sans perte. Mesuré en étape **externe** sur la
trace : `zstd -19` fait passer la trace de 45,1 Mo à 11,1 Mo, soit −79 % au total,
sans une ligne de code dans le moteur (`reports/rapport-compacite-trace.md:20-27`).
**Réf.** : RFC 8878, [rfc-editor.org/rfc/rfc8878](https://www.rfc-editor.org/rfc/rfc8878.html).

---

