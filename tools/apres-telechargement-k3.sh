#!/bin/bash
# Après le téléchargement de Kimi-K3 : la séquence, dans l'ordre, automatique.
#
# Ce script existe parce que la fin d'un transfert de 1,5 To est le moment où
# l'on risque de se précipiter : on lance le modèle, il refuse, on ne sait pas
# si c'est le fichier, l'architecture ou la mémoire. Les cinq étapes ci-dessous
# sont ordonnées pour que CHAQUE échec dise lequel des trois c'est.
#
#   bash tools/apres-telechargement-k3.sh [--sans-baseline]
#
# 1. les 32 shards sont-ils tous là, à la bonne taille ?
# 2. notre moteur lit-il l'en-tête et annonce-t-il SES manques ? (`--config`)
# 3. le tokenizer est-il toujours identique à l'officiel ? (porte)
# 4. le budget par jeton est-il celui qu'on a extrapolé ? (mesure, plus d'estimation)
# 5. la référence llama.cpp-k3 tourne-t-elle, et à quelle vitesse ? (baseline)
set -u
cd "$(dirname "$0")/.."

D=./drave-core/target/release/drave
K3=${K3:-/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf}
LC=/home/stephane/Data13TB/stephane/GitHub/llama.cpp-k3
SANS_BASELINE=${1:-}

echo "=== 1. Les 32 shards sont-ils complets ? ==="
python3 - "$K3" <<'PY'
import json, os, sys, urllib.request
chemin = sys.argv[1]
dossier = os.path.dirname(chemin)
d = json.load(urllib.request.urlopen(
    "https://huggingface.co/api/models/unsloth/Kimi-K3-GGUF?blobs=true", timeout=60))
attendus = {s['rfilename']: s.get('size') or 0 for s in d['siblings']
            if s['rfilename'].startswith('UD-Q4_K_XL/') and s['rfilename'].endswith('.gguf')}
manquants, tronques, ok = [], [], 0
for nom, taille in sorted(attendus.items()):
    p = os.path.join(dossier, os.path.basename(nom))
    if not os.path.exists(p):
        manquants.append(os.path.basename(nom)); continue
    t = os.path.getsize(p)
    if t != taille:
        tronques.append(f"{os.path.basename(nom)} : {t} au lieu de {taille}")
    else:
        ok += 1
print(f"  {ok}/{len(attendus)} shards complets")
for m in manquants[:3]: print(f"  MANQUANT  {m}")
for t in tronques[:3]:  print(f"  TRONQUÉ   {t}")
sys.exit(0 if not manquants and not tronques else 1)
PY
etat=$?
[ "$etat" != "0" ] && { echo "  → transfert incomplet : on s'arrête là."; exit 1; }

echo
echo "=== 2. Ce que notre moteur annonce ==="
$D "$K3" --config 2>&1 | grep -E "architecture|couches|experts|routage|calculable"

echo
echo "=== 3. Porte du tokenizer (identifiants contre l'implémentation officielle) ==="
printf '%s\x1e' "Le ciel est bleu." "2026 et 汉字 pour finir." "def f(x): return x*2" \
  | bash tools/porte-tokenizer-kimi.sh 2>&1 | tail -1

echo
echo "=== 4. Budget par jeton, sur le fichier COMPLET ==="
timeout 1200 python3 tools/budget_execution_locale.py "$K3" --experts-par-jeton 16 2>&1 \
  | grep -E "shard|PAR JETON|experts routés|partagé|TOTAL|extrapolation|RAM, 8"

if [ "$SANS_BASELINE" = "--sans-baseline" ]; then
    echo; echo "(baseline de la référence sautée)"; exit 0
fi

echo
echo "=== 5. Baseline de la référence (llama.cpp-k3) ==="
ids=${IDS_K3:-/tmp/ids_k3_demo.txt}
if [ ! -s "$ids" ]; then
    echo "  (pas d'identifiants : en produire avec --tokenize sur un texte)"
    printf 'Le ciel est bleu et le vent tourne.' > /tmp/txt_k3_demo.txt
    $D "$K3" --tokenize --fichier /tmp/txt_k3_demo.txt --sortie "$ids" >/dev/null 2>&1
fi
echo "  ids : $(head -c 60 "$ids" 2>/dev/null)…"
/usr/bin/time -v env LD_LIBRARY_PATH=$LC/build/bin "$LC"/build/bin/llama-cli \
    -m "$K3" -f /tmp/txt_k3_demo.txt -n 8 -t 16 --no-warmup 2>&1 \
    | grep -E "eval time|tokens per second|Maximum resident|load time" | head -8
echo
echo "Si la baseline tient et que --config annonce des manques, l'étape suivante"
echo "est l'implémentation, étage par étage : docs/verification-kimi-k3.md."
