#!/usr/bin/env python3
"""test_contamination.py — LE BANC UDHR EST-IL CONTAMINÉ ? (le test de la substitution absurde, sur phrases).

LE PROBLÈME ✗✗. La Déclaration universelle des droits de l'homme est **publique, célèbre, et traduite
officiellement dans 448 langues** : elle est certainement dans les données d'entraînement des grands modèles ✓✗.
Si le modèle a **mémorisé** les couples source→référence, un chrF élevé ne mesure pas sa **qualité de traducteur**
mais sa **mémoire** ✓✗ — et une courbe « la qualité vient avec la taille » pourrait n'être qu'une courbe
« le rappel vient avec la taille » ✓✗.

LE TEST (décideur ✓✓). On travaille sur **une phrase** (la phrase de l'article qui porte le mot substitué), et on
**substitue un mot absurde** à un endroit où la grammaire le supporte (« en dignité et en droits » → « en dignité
et en couleur ») ✓. On demande la traduction de cette phrase seule :
  - si la sortie contient la traduction du mot **substitué** ✓✓ → le modèle **traduit** ce qu'il lit ;
  - si la sortie contient le mot **canonique** à la place ✗✗ → le modèle **récite** la référence.
Le contrôle **positif** (deux phrases inventées, jamais vues) vérifie que le modèle sait transporter un mot nouveau
✓ : sans lui, un échec sur les phrases ne prouverait rien ✓✓.

⚠️ LA PREMIÈRE VERSION (sur articles entiers) ÉTAIT AMBIGUË ✗✗ : le mot canonique pouvait apparaître **ailleurs**
dans l'article ✓✗ (art. 7 : « loi » deux fois) et le modèle pouvait produire **les deux** mots ✓✗. La phrase isolée
lève l'ambiguïté ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, re, unicodedata

# article : (mot français remplacé, mot français substitué, attendu anglais, canonique anglais)
SUBSTITUTIONS = {
    1: ("droits", "couleur", r"\bcolou?rs?\b", r"\brights?\b"),
    2: ("religion", "moustache", r"\bmoustaches?\b", r"\breligion\b"),
    3: ("sûreté", "soupe", r"\bsoups?\b", r"\bsafety\b|\bsecurity\b"),
    4: ("servitude", "confiture", r"\bjams?\b", r"\bservitude\b|\bslavery\b"),
    5: ("torture", "musique", r"\bmusic\b", r"\btorture\b"),
    6: ("personnalité juridique", "collection de timbres", r"\bstamp collection\b", r"\blegal personality\b"),
    7: ("loi", "lune", r"\bmoon\b", r"\blaw\b"),
    8: ("recours effectif", "bicyclette", r"\bbicycles?\b|\bbikes?\b", r"\beffective remed(y|ies)\b"),
    9: ("exilé", "embrassé", r"\bkissed\b|\bembraced\b", r"\bexile(d)?\b"),
    10: ("cause", "salade", r"\bsalads?\b", r"\bcause\b"),
}

CONTROLES = [
    ("Le zorblax vert compte les nuages violets.", r"\bzorblax\b", r"\bgreen\b"),
    ("La bibliothécaire de Saturne collectionne les parapluies en fer.", r"\bsaturn\b", r"\bumbrellas?\b"),
]


def nz(t: str) -> str:
    return " ".join(unicodedata.normalize("NFC", t).lower().split())


def phrases(t: str):
    """Découpe en phrases — assez brut, mais UDHR est propre ✓."""
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", t.strip()) if p.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--dtype", default="bfloat16", choices=["float32", "bfloat16"])
    ap.add_argument("--max-jetons", type=int, default=200)
    ap.add_argument("--sortie", default="reports/contamination.json")
    ap.add_argument("--litteral", action="store_true",
                    help="consigne de traduction LITTÉRALE (« ne corrige rien ») : la mémoire est-elle "
                         "désactivable par consigne ? ✓✓")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    par = {}
    for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines():
        x = json.loads(l)
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]

    def genere(texte: str) -> str:
        if a.litteral:
            demande = ("Translate the following sentence into English. Translate literally and do not correct "
                       "or normalise anything, even if it seems strange. Answer with the translation only.\n\n"
                       + texte)
        else:
            demande = ("Translate the following sentence into English. Answer with the translation only.\n\n"
                       + texte)
        prompt = tok.apply_chat_template([{"role": "user", "content": demande}], tokenize=False,
                                         add_generation_prompt=True)
        ids = tok(prompt, return_tensors="pt").to(m.device)
        with torch.no_grad():
            g = m.generate(**ids, max_new_tokens=a.max_jetons, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)

    res = []
    for art, (vieux, neuf, attendu, canonique) in SUBSTITUTIONS.items():
        fr_p, en_p = phrases(par["fra"][art]), phrases(par["eng"][art])
        if len(fr_p) != len(en_p):
            print(f"  ⚠ article {art} : {len(fr_p)} phrases FR contre {len(en_p)} EN — appariement par position")
        # la phrase française qui porte le mot à substituer ✓
        i = next((k for k, p in enumerate(fr_p) if re.search(re.escape(vieux), p, re.I)), None)
        if i is None or i >= len(en_p):
            print(f"  ✗ article {art} : phrase introuvable"); continue
        phrase_fr, phrase_en = fr_p[i], en_p[i]
        m2 = re.search(re.escape(vieux), phrase_fr, re.I)
        if not m2:
            print(f"  ✗ article {art} : position introuvable"); continue
        modifiee = phrase_fr[:m2.start()] + neuf + phrase_fr[m2.end():]
        sortie = genere(modifiee)
        sortie_canon = genere(phrase_fr)
        s = nz(sortie)
        porte_neuf = bool(re.search(attendu, s))
        porte_vieux = bool(re.search(canonique, s))
        # combien la sortie ressemble à la phrase canonique ? (récitation → très haut ✓✗)
        import difflib
        ratio = difflib.SequenceMatcher(None, s, nz(phrase_en)).ratio()
        # LE CONTRÔLE DÉCISIF ✓✓ : si la source change et que la SORTIE NE CHANGE PAS, le modèle n'a pas lu la
        # source — il a récité ✓✗. C'est plus robuste que la recherche d'un mot ✓✓.
        identique = (s == nz(sortie_canon))
        sim_sorties = difflib.SequenceMatcher(None, s, nz(sortie_canon)).ratio()
        verdict = ("TRADUIT" if porte_neuf and not porte_vieux else
                   "MÉLANGE" if porte_neuf and porte_vieux else
                   "RÉCITE" if porte_vieux else "RÉPARE")
        res.append({"litteral": a.litteral, "article": art, "vieux": vieux, "neuf": neuf, "attendu": attendu,
                    "canonique": canonique, "phrase_modifiee": modifiee, "phrase_canonique_en": phrase_en,
                    "sortie": sortie, "sortie_canonique": sortie_canon,
                    "porte_le_neuf": porte_neuf, "porte_le_canonique": porte_vieux,
                    "identique_malgre_la_source": identique, "similarite_sorties": round(sim_sorties, 3),
                    "ressemblance_canonique": round(ratio, 3), "verdict": verdict})
        print(f"  art. {art:2d} · {neuf:22s} → {verdict:8s} · neuf={porte_neuf!s:5s} canonique={porte_vieux!s:5s} "
              f"· sorties identiques={identique!s:5s} (sim {sim_sorties:.2f}) · ressemblance {ratio:.2f}")
    for phrase, attendu1, attendu2 in CONTROLES:
        sortie = genere(phrase)
        s = nz(sortie)
        ok1, ok2 = bool(re.search(attendu1, s)), bool(re.search(attendu2, s))
        res.append({"controle": phrase, "sortie": sortie, "porte_mot_rare": ok1, "porte_adjectif": ok2})
        print(f"  contrôle · “{phrase[:40]}…” → rare={ok1} adjectif={ok2} · {sortie[:90]}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    n = [r for r in res if "article" in r]
    if n:
        print(f"  → {sum(r['verdict'] == 'TRADUIT' for r in n)}/{len(n)} TRADUISENT · "
              f"{sum(r['verdict'] == 'RÉCITE' for r in n)} RÉCITENT · "
              f"{sum(r['verdict'] == 'MÉLANGE' for r in n)} MÉLANGENT · "
              f"{sum(r['verdict'] == 'RÉPARE' for r in n)} RÉPARENT · "
              f"{sum(r['identique_malgre_la_source'] for r in n)}/{len(n)} SORTIES IDENTIQUES malgré la source · "
              f"sim moyenne {sum(r['similarite_sorties'] for r in n) / len(n):.2f} · {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
