"""Tokenizer officiel de Kimi-K3 en pur Python (pat_str du dépôt + BPE tiktoken),
pour comparer aux identifiants de notre moteur. Aucune dépendance hors `regex`."""
import base64, sys, regex

ranks = {}
for ligne in open('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tokenizer_kimi/tiktoken.model'):
    p = ligne.split()
    if len(p) == 2:
        ranks[base64.b64decode(p[0])] = int(p[1])

PAT = regex.compile("|".join([
    r"""[\p{Han}]+""",
    r"""[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]*[\p{Ll}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?""",
    r"""[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]+[\p{Ll}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?""",
    r"""\p{N}{1,3}""",
    r""" ?[^\s\p{L}\p{N}]+[\r\n]*""",
    r"""\s*[\r\n]+""",
    r"""\s+(?!\S)""",
    r"""\s+""",
]), regex.V1)

def bpe(morceau: bytes):
    parts = [bytes([b]) for b in morceau]
    while len(parts) > 1:
        meilleur, ou = None, -1
        for i in range(len(parts) - 1):
            r = ranks.get(parts[i] + parts[i + 1])
            if r is not None and (meilleur is None or r < meilleur):
                meilleur, ou = r, i
        if ou < 0:
            break
        parts = parts[:ou] + [parts[ou] + parts[ou + 1]] + parts[ou + 2:]
    return parts

def encoder(texte: str):
    ids = []
    for m in PAT.finditer(texte):
        for p in bpe(m.group().encode('utf-8')):
            ids.append(ranks[p])
    return ids

if __name__ == '__main__':
    texte = sys.stdin.read()
    print(','.join(str(i) for i in encoder(texte)))
