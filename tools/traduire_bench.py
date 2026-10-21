#!/usr/bin/env python3
"""traduire_bench.py — LA QUALITÉ DE TRADUCTEUR, MESURÉE (chrF contre traduction humaine).

POURQUOI CE BANC. Les mesures de la série UDHR testaient le **retrieval** (retrouver le même article) — une
propriété de l'état, pas une qualité de **traduction** ✓✗. Ici, on demande au modèle de **traduire** ✓, et on
compare sa sortie à la **traduction humaine de référence** ✓✓ (les 448 langues UDHR sont des traductions humaines
alignées ✓ ; Verne et Alice donnent les domaines littéraires ✓).

LA MÉTRIQUE. **chrF** (Popović 2015 ✓) : F-score de n-grammes de **caractères** (n = 1..6, β = 2 ✓), insensible à
la tokenisation ✓ — c'est la métrique standard pour les langues à morphologie riche et les écritures non latines
✓✓. On rapporte aussi deux **bornes** : la source elle-même comparée à la référence ✓ (le plancher : « ne rien
traduire » ✓✗) et une référence **mélangée** ✓ (le hasard ✓).

⚠️ CE QUE CE BANC NE DIT PAS ✗ : chrF mesure la **ressemblance de surface** avec UNE référence humaine ✓✗ — une
bonne traduction peut différer ; et le modèle est petit ✓, les scores seront bas ✓✓ : c'est un **classement relatif**
entre tailles, domaines et paires, pas une note absolue ✓.

⚠️ LES DEUX PIÈGES DE LA PREMIÈRE VERSION (mesures 50-58), trouvés en 61 ✗✗ :
  1. **pas de gabarit de conversation** : on donnait la consigne en texte brut à un modèle *instruct* ✓✗ — le
     même piège que la première version de `marqueur_bruit.py` ✓✓. `--chat` passe par `apply_chat_template` ;
  2. **sortie coupée à 160 jetons** : les articles longs (2, 4...) ne tenaient pas ✗✗ — on mesurait la troncature
     autant que la traduction ✓✗. Le défaut est maintenant **400**, et le taux de troncature est **rapporté** ✓✓.

CE QUE CHAQUE LIGNE DE JSON PORTE ✓✓ : les scores **par article** (d'où l'IC bootstrap ✓), la **longueur** de la
sortie contre la référence (détecte la troncature ✓), et la **sortie brute** (pour l'audit humain des pièges ✓).
"""
from __future__ import annotations
import argparse, json, pathlib, random, re, unicodedata
from collections import Counter
import numpy as np


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    """chrF : F-beta sur les n-grammes de caractères (n=1..6) ✓."""
    hyp = " ".join(unicodedata.normalize("NFC", hyp).split())
    ref = " ".join(unicodedata.normalize("NFC", ref).split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, len(H)))
        rec.append(inter / max(1, len(R)))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def ic_bootstrap(scores, n_tirages: int = 5000, graine: int = 0):
    """IC à 95 % de la moyenne, par rééchantillonnage des ARTICLES ✓ (n=6 : l'IC est large, il faut le voir ✓✓)."""
    if len(scores) < 2:
        return (float(scores[0]) if scores else 0.0,) * 2
    rng = np.random.default_rng(graine)
    x = np.asarray(scores, dtype=float)
    m = np.array([rng.choice(x, size=len(x), replace=True).mean() for _ in range(n_tirages)])
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def nettoie(sortie: str) -> str:
    """Retire les préambules que le modèle instruct ajoute parfois (« Here is the translation: ») ✓.

    On ne retire QUE le préambule (première ligne qui finit par « : » et ne contient pas de phrase), jamais le
    corps de la traduction ✓✓ — sinon on s'attribuerait le travail du modèle ✗.
    """
    s = sortie.strip()
    m = re.match(r"^(?:here is|here's|voici|traduction|translation)\b[^\n]{0,120}:\s*\n?", s, re.I)
    if m and len(m.group(0)) < 160:
        s = s[m.end():].strip()
    s = s.strip().strip('"“”«»').strip()
    return s


def recopie(sortie: str, ref: str) -> bool:
    """Le modèle a-t-il RECOPIÉ la référence (mémorisation) plutôt que traduit ? ✓✗

    Contrôle grossier mais utile : 40 caractères normalisés consécutifs de la référence présents dans la sortie ✓.
    """
    def nz(t):
        return " ".join(unicodedata.normalize("NFC", t).lower().split())
    s, r = nz(sortie), nz(ref)
    if len(r) < 40:
        return False
    for i in range(0, len(r) - 40, 10):
        if r[i:i + 40] in s:
            return True
    return False


def charger_udhr():
    arts = [json.loads(l) for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines()]
    par = {}
    for x in arts:
        par.setdefault(x["iso3"], {})[int(x["art"])] = x["texte"]
    return par


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--paires", default="fra:eng,eng:fra,fra:deu,fra:spa,fra:cmn")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--max-jetons", type=int, default=400,
                    help="400 par défaut ✓ ; 160 était le réglage des mesures 50-58, qui TRONQUAIT les articles "
                         "longs ✗✗ (mesure 61)")
    ap.add_argument("--sortie", default="reports/traduction-legal.json")
    ap.add_argument("--corpus", choices=["udhr", "verne", "verne_align", "eurlex", "presse", "onu"], default="udhr",
                    help="udhr : le domaine juridique, MAIS CONTAMINE (mesure 61) ✗✗ ; eurlex : un reglement "
                         "europeen POST-CUTOFF, aligne par structure, non memorisable ✓✓ ; verne_align : le "
                         "litteraire ALIGNE ET VALIDE (mesure 63, 3397 paires) ✓✓ ; presse : le registre "
                         "QUOTIDIEN (15 communiques UE de 2026, EN/FR/DE alignes par paragraphe) ✓✓ ; onu : les "
                         "resolutions 2026 en 5 langues (EN/FR/ES/RU/ZH) ✓✓ ; verne : l'ancien mode invalide "
                         "(mesure 59) ✗")
    ap.add_argument("--celex", default="32025R1106", help="le reglement EUR-Lex (corpus_eurlex.py) ✓")
    ap.add_argument("--dtype", default="float32", choices=["float32", "bfloat16", "float16"],
                    help="bfloat16 pour un modele qui ne tient pas en fp32 ✓ (7 B : 14 Go en bf16)")
    ap.add_argument("--chat", action="store_true",
                    help="passer par le gabarit de conversation du modèle instruct ✓✓ (le défaut historique ne le "
                         "faisait pas ✗ — piège de la mesure 61)")
    ap.add_argument("--nettoie", action="store_true",
                    help="retirer le préambule (« Here is the translation: ») avant chrF ✓")
    ap.add_argument("--repartir", action="store_true",
                    help="device_map=auto : répartir un modèle plus gros que 16 Go sur les deux cartes ✓✓")
    ap.add_argument("--graine", type=int, default=0, help="graine du hasard (référence mélangée) ✓")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    charge = dict(dtype=getattr(torch, a.dtype))
    if a.repartir:
        charge["device_map"] = "auto"
        m = AutoModelForCausalLM.from_pretrained(a.hf, **charge).eval()
    else:
        m = AutoModelForCausalLM.from_pretrained(a.hf, **charge).to(device).eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    if a.corpus == "verne":
        # le domaine LITTERAIRE : les chapitres du Tour du monde, francais (original) et anglais (traduction) ✓
        base = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified/around_world_80_days")
        fr = (base / "around_world_80_days_fr.txt").read_text(errors="ignore")
        en = (base / "around_world_80_days_en.txt").read_text(errors="ignore")
        # ⚠️ LA TABLE DES MATIÈRES FAIT DOUBLON ✗✗ : 84 sections françaises contre 37 anglaises ✓✗. On écarte les
        # entrées de TOC par leur LONGUEUR ✓✓ (une entrée de TOC est suivie d'une autre entrée, donc son segment
        # est minuscule ✓ ; un chapitre du corps fait des milliers de caractères ✓).
        en_c = [p.strip() for p in re.split(r"(?im)^\s*CHAPTER\s+[IVXLC0-9]+\.?", en)[1:] if len(p.strip()) > 2000]
        fr_c = [p.strip() for p in re.split(r"(?im)^\s*[IVXLC]+\s+[A-ZÀ-Ý]", fr)[1:] if len(p.strip()) > 2000]
        n = min(len(en_c), len(fr_c))
        # on lit le même endroit RELATIF dans chaque chapitre ✓ (20 % du chapitre, 400 caractères ✓)
        def extrait(x):
            d = max(0, len(x) // 5)
            return x[d:d + 400]
        par = {"fra": {i + 1: extrait(fr_c[i]) for i in range(n)},
               "eng": {i + 1: extrait(en_c[i]) for i in range(n)}}
        print(f"  litteraire : {len(fr_c)} chapitres français · {len(en_c)} anglais · {n} appariés")
    elif a.corpus == "verne_align":
        # LE LITTÉRAIRE, ALIGNÉ ET VALIDÉ (tools/aligneur_litteraire.py, 93,2 % des ancres à ±2 contre 0,3 % au
        # contrôle négatif) : on ne garde que les paires 1:1 STRICTES ✓✓ (2570 paires), pour que la phrase source
        # et la phrase cible disent exactement la même chose ✓.
        import json as _json
        data = _json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
        pp = [p for p in data["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
        par = {"fra": {i: p["fr"] for i, p in enumerate(pp)},
               "eng": {i: p["en"] for i, p in enumerate(pp)}}
        ordre = list(range(len(pp)))
        print(f"  litteraire aligne : {len(pp)} paires 1:1 strictes ({len(data['paires'])} paires au total)")
    elif a.corpus == "onu":
        # LES GRANDES LANGUES HORS UE : résolutions de l'Assemblée générale 2025-2026, alignées par les
        # paragraphes numérotés ✓✓ (5 langues : EN/FR/ES/RU/ZH ; l'arabe est écarté, pdftotext le déchiquette).
        import json as _json
        data = _json.loads(pathlib.Path("data/onu/onu_2026.json").read_text())
        par = {lg: {} for lg in data["langues"]}
        ordre = []
        for u in data["unites"]:
            for lg in data["langues"]:
                par[lg][u["id"]] = u["textes"][lg]
            ordre.append(u["id"])
        print(f"  ONU 2026 : {len(ordre)} unités alignées ({len(data['langues'])} langues, "
              f"{len(data['documents'])} résolutions)")
    elif a.corpus == "presse":
        # LE REGISTRE QUOTIDIEN : des communiqués de presse UE de 2026, alignés par paragraphe ✓✓ (structure
        # identique dans les trois langues, vérifiée par tools/corpus_presse.py) ✓.
        import json as _json
        data = _json.loads(pathlib.Path("data/presse/presse_2026.json").read_text())
        par = {lg: {} for lg in data["langues"]}
        ordre = []
        for u in data["unites"]:
            for lg in data["langues"]:
                par[lg][u["id"]] = u["textes"][lg]
            ordre.append(u["id"])
        print(f"  presse 2026 : {len(ordre)} unités alignées ({len(data['langues'])} langues, "
              f"{len(data['documents'])} communiqués)")
    elif a.corpus == "eurlex":
        # le corpus POST-CUTOFF : les règlements publiés après la coupure du modèle ✓✓, alignés par structure ✓
        import json as _json
        data = _json.loads(pathlib.Path(f"data/eurlex/{a.celex}.json").read_text())
        par = {lg: {} for lg in data["langues"]}
        ordre = []
        for u in data["unites"]:
            for lg in data["langues"]:
                par[lg][u["id"]] = u["textes"][lg]
            ordre.append(u["id"])
        print(f"  eurlex {a.celex} : {len(ordre)} unités alignées ({len(data['langues'])} langues)")
    else:
        par = charger_udhr()
    noms = {"fra": "French", "eng": "English", "deu": "German", "spa": "Spanish", "ita": "Italian",
            "cmn": "Chinese", "rus": "Russian", "jpn": "Japanese", "pol": "Polish", "nld": "Dutch",
            "por": "Portuguese", "zho": "Chinese", "ara": "Arabic", "bul": "Bulgarian", "ces": "Czech", "dan": "Danish", "ell": "Greek",
            "est": "Estonian", "fin": "Finnish", "gle": "Irish", "hrv": "Croatian", "hun": "Hungarian",
            "lav": "Latvian", "lit": "Lithuanian", "mlt": "Maltese", "ron": "Romanian", "slk": "Slovak",
            "slv": "Slovenian", "swe": "Swedish"}
    resultats = []
    for paire in a.paires.split(","):
        src, dst = paire.split(":")
        if src not in par or dst not in par:
            print(f"  ✗ {paire} : langue absente"); continue
        communes = set(par[src]) & set(par[dst])
        # l'ordre du corpus (eurlex) ou l'ordre numérique (udhr) ✓ ; --n 0 = tout ✓
        if a.corpus in ("eurlex", "verne_align", "presse", "onu"):
            arts = [x for x in ordre if x in communes]
            if 0 < a.n < len(arts):
                # on ÉTALE l'échantillon sur TOUT le corpus ✓✓, par positions régulières (linspace) : ni les 200
                # premiers (le chapitre 1 ✗), ni un pas entier qui surestique le début ✗✓.
                idx = [round(i * (len(arts) - 1) / (a.n - 1)) for i in range(a.n)]
                arts = [arts[i] for i in dict.fromkeys(idx)]
        else:
            arts = sorted(communes)[: a.n] if a.n > 0 else sorted(communes)
        scores, plancher, hasard, tronque, recopies, ratios, details = [], [], [], [], [], [], []
        rng = random.Random(a.graine)
        for n in arts:
            texte = par[src][n]
            demande = (f"Translate the following text into {noms.get(dst, dst)}. "
                       f"Answer with the translation only.\n\n{texte}")
            if a.chat:
                messages = [{"role": "user", "content": demande}]
                prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                prompt = demande
            ids = tok(prompt, return_tensors="pt").to(m.device)
            with torch.no_grad():
                g = m.generate(**ids, max_new_tokens=a.max_jetons, do_sample=False,
                               pad_token_id=tok.eos_token_id)
            nouvelles = g[0][ids["input_ids"].shape[1]:]
            sortie = tok.decode(nouvelles, skip_special_tokens=True)
            brut = sortie
            if a.nettoie:
                sortie = nettoie(sortie)
            ref = par[dst][n]
            s = chrf(sortie, ref)
            scores.append(s)
            plancher.append(chrf(texte, ref))                 # « ne rien traduire » ✓✗
            autres = [par[dst][k] for k in par[dst] if k != n]
            hasard.append(chrf(sortie, rng.choice(autres)))   # référence mélangée ✓
            tronque.append(bool(len(nouvelles) >= a.max_jetons))
            recopies.append(recopie(sortie, ref))
            ratios.append(len(sortie) / max(1, len(ref)))
            details.append({"article": n, "chrf": round(s, 2), "plancher": round(plancher[-1], 2),
                            "hasard": round(hasard[-1], 2), "sortie": brut,
                            "longueur_sortie": len(sortie), "longueur_ref": len(ref),
                            "tronque": tronque[-1], "recopie": recopies[-1]})
        bas, haut = ic_bootstrap(scores, graine=a.graine)
        resultats.append({"paire": paire, "n": len(scores), "chrf": float(np.mean(scores)),
                          "ic95": [round(bas, 1), round(haut, 1)],
                          "plancher_source": float(np.mean(plancher)), "hasard": float(np.mean(hasard)),
                          "tronque": sum(tronque), "recopie": sum(recopies),
                          "ratio_longueur": round(float(np.mean(ratios)), 2),
                          "chat": a.chat, "max_jetons": a.max_jetons,
                          "details": details})
        print(f"  {paire:9s} · chrF {np.mean(scores):5.1f} [{bas:4.1f}, {haut:4.1f}] · "
              f"plancher {np.mean(plancher):5.1f} · hasard {np.mean(hasard):5.1f} · "
              f"tronqué {sum(tronque)}/{len(scores)} · recopié {sum(recopies)} · {len(scores)} articles")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(resultats, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
