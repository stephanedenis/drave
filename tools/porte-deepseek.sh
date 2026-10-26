#!/bin/bash
# porte-deepseek.sh — le banc externe, sans réseau et sans clé.
#
# CE QU'ELLE VERROUILLE :
#   1. les tests de l'adaptateur, du corpus professeur et de la distillation
#      (transport factice, aucun appel réseau, aucune clé réelle) ;
#   2. le dry-run de l'adaptateur : réponse déterministe, pas de requête ;
#   3. les 60 prompts publics : 50 traductions UDHR + 10 questions de jeux ;
#   4. le dry-run du corpus professeur : il écrit, mais `distillation.py`
#      l'ignore — un faux professeur ne devient jamais un corpus d'entraînement.
#
# La mesure **live** est opt-in : `DEEPSEEK_API_KEY=... DEEPSEEK_LIVE=1
# bash tools/porte-deepseek.sh`. Sans clé, la porte est verte et le dit.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"
T="${JOURNAUX:-/tmp}/deepseek-porte"
rm -rf "$T"; mkdir -p "$T"

echo "  === tests (adaptateur, corpus, distillation) ==="
python3 -m unittest discover -s tools/llm/tests -t tools || exit 1

echo "  === dry-run de l'adaptateur ==="
python3 tools/llm/deepseek.py --prompt "test de la porte" --dry-run --json > "$T/dry.json" || exit 1
python3 - "$T/dry.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert "[dry-run]" in d["contenu"], d
assert d["usage"] == {}, d
print("     dry-run déterministe, aucune requête")
PY

echo "  === prompts publics ==="
python3 - "$PWD/tools/llm/prompts_publics.jsonl" "$PWD/tools/llm/prompts_publics_300.jsonl" <<'PY'
import json, sys
for chemin, attendu, trad_attendu in ((sys.argv[1], 60, 50), (sys.argv[2], 310, 300)):
    lignes = [json.loads(l) for l in open(chemin, encoding="utf-8") if l.strip()]
    assert len(lignes) == attendu, (chemin, len(lignes))
    trad = sum(1 for p in lignes if p["meta"]["categorie"] == "traduction")
    jeux = sum(1 for p in lignes if p["meta"]["categorie"] == "jeu")
    assert (trad, jeux) == (trad_attendu, 10), (chemin, trad, jeux)
    assert all(p.get("id") and p.get("prompt") and p.get("system") for p in lignes)
    print(f"     {len(lignes)} prompts : {trad} traductions UDHR, {jeux} jeux ({chemin.rsplit('/', 1)[-1]})")
PY

echo "  === dry-run du corpus professeur (ignoré par la distillation) ==="
python3 tools/llm/enseignant.py --sortie "$T/enseignant-dry.jsonl" --limite 2 --dry-run >/dev/null || exit 1
python3 tools/llm/distillation.py --entree "$T/enseignant-dry.jsonl" --sortie "$T/dist" >/dev/null
python3 - "$T/dist/meta.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert d["exemples"] == 0, d
print("     dry-run ignoré : 0 exemple de distillation")
PY

if [ -n "${DEEPSEEK_API_KEY:-${DSH_API_KEY:-}}" ] && [ "${DEEPSEEK_LIVE:-0}" = "1" ]; then
  echo "  === appel live (1 prompt, 32 jetons) ==="
  python3 tools/llm/deepseek.py --prompt "Réponds par le mot « vivant »." \
      --max-tokens 32 --json > "$T/live.json" || exit 1
  python3 - "$T/live.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert d["contenu"].strip(), d
print(f"     live : {d['usage'].get('total_tokens', '?')} jetons, "
      f"{d['latence_s']} s, cache={d['cache']}")
PY
else
  echo "  (live ignoré : pas de clé ou DEEPSEEK_LIVE!=1)"
fi

echo "  ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation."
