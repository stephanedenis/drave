#!/usr/bin/env python3
import json, pathlib, sys, torch
from tools.generer_natif import charger, generer
from tools.sft_natif import paires

TENUES = [
    {"q":"Quelle est la capitale de la Suisse ?","r":"Berne"},
    {"q":"Combien font 9 fois 9 ?","r":"81"},
    {"q":"Quel est le contraire de rapide ?","r":"lent"},
    {"q":"Quelle est la capitale du Canada ?","r":"Ottawa"},
]

def eval_paires(m, ps):
    bons=[]; res=[]
    for p in ps:
        prompt=f"Q: {p['q']}\nR:"
        b=generer(m,prompt,16)
        txt=b[len(prompt.encode()):].decode('utf-8','replace').strip()
        ok=txt.startswith(p['r'])
        bons.append(ok); res.append({"q":p["q"],"attendu":p["r"],"obtenu":txt,"ok":ok})
    return sum(bons), len(ps), res

def main():
    modele,cfg=charger(sys.argv[1] if len(sys.argv)>1 else '/tmp/drave-n0-sft.pt','cpu')
    vus=paires('data/instructions_fr.jsonl')
    a,n,rv=eval_paires(modele,vus)
    b,m2,rt=eval_paires(modele,TENUES)
    out={"vus":f"{a}/{n}","tenus":f"{b}/{m2}","details_vus":rv,"details_tenus":rt}
    pathlib.Path('reports/native-sft-eval.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
    print(json.dumps({"vus":out["vus"],"tenus":out["tenus"]},indent=1))

if __name__=='__main__': main()
