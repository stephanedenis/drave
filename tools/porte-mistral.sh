#!/bin/bash
# Porte de la famille MISTRAL — le moteur calcule-t-il le même modèle que PyTorch ?
#
# POURQUOI ELLE EXISTE. Le dépôt avait une porte pour Qwen, GLM, V4, gpt-oss et
# Kimi ; Mistral n'en avait aucune. Or `codestral-22B` a rendu **35 657** de
# perplexité sur de la prose pendant la campagne — 4 000 fois le Qwen3-30B-A3B —
# et sans porte, impossible de dire si c'était le modèle (spécialisé pour le code)
# ou le moteur (qui exécuterait mal l'architecture). La porte a tranché : le
# moteur est juste, l'écart est un décalage de tâche.
#
# CE QU'ELLE FAIT, et pourquoi ainsi :
#   · elle ENTRAÎNE un Mistral minuscule (2 couches, 64 cachés, vocabulaire
#     d'octets). Un modèle aléatoire rend des logits quasi uniformes, sur
#     lesquels une corrélation ne mesure rien : la porte passerait ou échouerait
#     au hasard ;
#   · ses dimensions sont MULTIPLES DE 32 — les blocs de quantification ggml
#     font 32 poids, et le modèle de test officiel de HuggingFace a
#     `intermediate_size = 37`, donc inexporterable ;
#   · la référence PyTorch est calculée sur les MÊMES poids quantifiés que
#     l'export, sans quoi la porte mesurerait la quantification.
#
#   tools/porte-mistral.sh          la porte (quelques dizaines de secondes)
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
D=${D:-./drave-core/target/release/drave}
T=${T:-/tmp/porte-mistral}

[ -x "$D" ] || { echo "  $D absent : construire d'abord"; exit 2; }
[ -x "$P" ] || { echo "  python d'entraînement absent ($P) : porte sautée"; exit 2; }
mkdir -p "$T"

if [ ! -f "$T/modele/config.json" ]; then
    "$P" - "$T" <<'PY' > "$T/fabrication.log" 2>&1
import sys, numpy as np, torch
from transformers import MistralConfig, MistralForCausalLM
T = sys.argv[1]
torch.manual_seed(11)
cfg = MistralConfig(vocab_size=256, hidden_size=64, num_hidden_layers=2,
                    num_attention_heads=4, num_key_value_heads=2,
                    intermediate_size=64, max_position_embeddings=512,
                    rms_norm_eps=1e-6, rope_theta=10000.0, sliding_window=4096,
                    tie_word_embeddings=False, initializer_range=0.08)
m = MistralForCausalLM(cfg)
data = np.frombuffer(open("data/corpus_en.txt", "rb").read(200_000), dtype=np.uint8).astype(np.int64)
opt = torch.optim.AdamW(m.parameters(), lr=3e-3); m.train()
for _ in range(300):
    i = np.random.randint(0, len(data) - 129, size=32)
    x = torch.from_numpy(np.stack([data[j:j + 128] for j in i]))
    perte = m(input_ids=x, labels=x).loss
    opt.zero_grad(); perte.backward(); opt.step()
m.eval()
m.save_pretrained(T + "/modele")
open(T + "/ids.txt", "w").write(",".join(str((i * 37 + 11) % 256) for i in range(64)))
print("modèle minuscule entraîné et écrit")
PY
fi

"$P" tools/porte_mistral.py --hf "$T/modele" --gguf "$T/mistral.gguf" > "$T/export.log" 2>&1
"$P" tools/porte_mistral.py --hf "$T/modele" --ids "$T/ids.txt" --logits "$T/ref.bin" \
    > "$T/reference.log" 2>&1
"$D" "$T/mistral.gguf" --ppl "$T/ids.txt" --logits-bin "$T/eng.bin" --ctx 64 --threads 4 \
    > "$T/moteur.log" 2>&1
"$P" tools/compare_logits.py "$T/eng.bin" "$T/ref.bin" "$T/ids.txt" --porte \
    > "$T/compare.log" 2>&1
code=$?

ref=$(grep -oE "perplexité [0-9.]+" "$T/reference.log" | tail -1 | grep -oE "[0-9.]+")
eng=$(grep -oE "=== perplexité [0-9.]+" "$T/moteur.log" | grep -oE "[0-9.]+" | head -1)
printf "  Mistral (2 couches, vocabulaire d'octets) : référence %s · moteur %s\n" "${ref:-?}" "${eng:-?}"
if [ "$code" = "0" ]; then
    printf "    %s\n" "$(tail -1 "$T/compare.log" | cut -c1-110)"
    exit 0
fi
printf "    %s\n" "$(tail -1 "$T/compare.log" | cut -c1-110)"
exit 1
