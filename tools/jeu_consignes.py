#!/usr/bin/env python3
"""jeu_consignes.py — N4.8 : consignes courtes procédurales, mots tenus à l'écart."""
import json, pathlib, random
MOTS = ["chat","chien","maison","arbre","livre","table","porte","fenêtre","jardin","route",
        "fleur","soleil","lune","étoile","mer","rivière","montagne","ville","village","pays",
        "ami","frère","sœur","père","mère","enfant","homme","femme","jour","nuit",
        "matin","soir","pain","eau","lait","pomme","fleur","oiseau","poisson","cheval",
        "vache","mouton","poule","canard","lapin","souris","loup","renard","ours","tigre"]
TENUS = ["nuage","orage","neige","vent","forêt","plage","désert","île","pont","tour"]

def paire(t, mot):
    if t == 0: return {"q":f"Mets en majuscules : {mot}","r":mot.upper()}
    if t == 1: return {"q":f"Mets en minuscules : {mot.upper()}","r":mot.lower()}
    if t == 2: return {"q":f"Répète : {mot}","r":mot}
    return {"q":f"Écris deux fois : {mot}","r":f"{mot} {mot}"}

def main():
    rng=random.Random(0)
    train=[]; val=[]
    for mot in MOTS:
        for t in range(4):
            for _ in range(10): train.append(paire(t,mot))
    for mot in TENUS:
        for t in range(4): val.append(paire(t,mot))
    rng.shuffle(train); rng.shuffle(val)
    pathlib.Path('data/consignes_train.jsonl').write_text('\n'.join(json.dumps(p,ensure_ascii=False) for p in train)+'\n')
    pathlib.Path('data/consignes_val.jsonl').write_text('\n'.join(json.dumps(p,ensure_ascii=False) for p in val)+'\n')
    print(len(train),len(val))
if __name__=='__main__': main()
