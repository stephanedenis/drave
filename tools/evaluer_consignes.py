#!/usr/bin/env python3
import json, pathlib, sys
from tools.generer_natif import charger, generer

def main():
    m,_=charger(sys.argv[1] if len(sys.argv)>1 else '/tmp/drave-n0-consignes.pt','cpu')
    ps=[json.loads(l) for l in pathlib.Path('data/consignes_val.jsonl').read_text().splitlines() if l.strip()]
    bons=[]; det=[]
    for p in ps:
        prompt=f"Q: {p['q']}\nR:"
        b=generer(m,prompt,32)
        txt=b[len(prompt.encode()):].decode('utf-8','replace').strip()
        ok=txt.startswith(p['r'])
        bons.append(ok); det.append({"q":p['q'],"attendu":p['r'],"obtenu":txt,"ok":ok})
    out={"tenus":f"{sum(bons)}/{len(ps)}","details":det}
    pathlib.Path('reports/native-consignes.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
    print(json.dumps({"tenus":out["tenus"]},indent=1))
if __name__=='__main__': main()
