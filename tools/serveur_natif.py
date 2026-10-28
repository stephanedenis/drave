#!/usr/bin/env python3
"""serveur_natif.py — N4.2 : service local minimal pour `drave-n0`.

HTTP stdlib, pas de dépendance : `GET /sante`, `POST /generer` avec
`{"prompt": "...", "n": 64}`. Génération greedy, déterministe. Ce n'est pas un
service de production : pas d'authentification, pas de cache KV, un seul modèle.
"""
from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tools.generer_natif import charger, generer

VERROU = threading.Lock()
MODELE = None


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path == "/sante":
            self._json(200, {"ok": True, "parametres": MODELE.nb_parametres()})
        else:
            self._json(404, {"erreur": "chemin inconnu"})

    def do_POST(self):
        if self.path != "/generer":
            self._json(404, {"erreur": "chemin inconnu"}); return
        n = int(self.headers.get("Content-Length", "0"))
        try:
            d = json.loads(self.rfile.read(n) or b"{}")
            prompt = str(d.get("prompt", "La France"))
            k = max(1, min(int(d.get("n", 64)), 512))
        except Exception as e:
            self._json(400, {"erreur": f"json invalide : {e}"}); return
        with VERROU:
            b = generer(MODELE, prompt, k)
        self._json(200, {"prompt": prompt, "octets": len(b),
                         "texte": b.decode("utf-8", errors="replace")})

    def log_message(self, *_):
        pass


def main() -> None:
    global MODELE
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="/tmp/drave-n0-distille.pt")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    MODELE, _ = charger(a.modele, "cpu")
    s = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"service natif sur http://127.0.0.1:{a.port} · {MODELE.nb_parametres()} paramètres", flush=True)
    s.serve_forever()


if __name__ == "__main__":
    main()
