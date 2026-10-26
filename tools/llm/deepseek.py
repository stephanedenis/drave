#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
  + température + max_tokens, **jamais** la clé ;
- `--dry-run` : aucune requête, réponse déterministe (tests et gate sans réseau).

Usage :
    python3 tools/llm/deepseek.py --prompt "Explique le ko au go." --json
    DEEPSEEK_API_KEY=... python3 tools/llm/deepseek.py --prompt ... --json
    python3 tools/llm/deepseek.py --prompt ... --dry-run --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

RACINE = pathlib.Path(__file__).resolve().parents[2]
CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
BASE_DEFAUT = "https://api.deepseek.com"
MODELE_DEFAUT = "deepseek-chat"


class ErreurDeepSeek(Exception):
    """Une erreur de l'API, avec la possibilité de réessayer."""

    def __init__(self, message: str, *, code: int | None = None,
                 reessayable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.reessayable = reessayable


@dataclass
class ReponseDeepSeek:
    contenu: str
    modele: str
    usage: dict = field(default_factory=dict)
    raisonnement: str | None = None
    latence_s: float = 0.0
    cache: bool = False
    brut: dict | None = None

    def __str__(self) -> str:
        return self.contenu


def _cle_env() -> str:
    """La clé, sans jamais l'écrire : variable d'environnement ou fichier 0600.

    `DEEPSEEK_API_KEY` / `DSH_API_KEY` d'abord ; sinon `DEEPSEEK_KEY_FILE` /
    `DSH_KEY_FILE` (un fichier dont la première ligne est la clé). Le fichier
    doit être hors du dépôt et lisible par l'utilisateur seul.
    """
    for var in ("DEEPSEEK_API_KEY", "DSH_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v.strip()
    for var in ("DEEPSEEK_KEY_FILE", "DSH_KEY_FILE"):
        chemin = os.environ.get(var)
        if not chemin:
            continue
        try:
            p = pathlib.Path(chemin).expanduser()
            return p.read_text(encoding="utf-8").splitlines()[0].strip()
        except (OSError, IndexError):
            continue
    return ""


def _cache_cle(modele: str, messages: list[dict], temperature: float,
               max_tokens: int) -> str:
    charge = json.dumps({"modele": modele, "messages": messages,
                         "temperature": temperature, "max_tokens": max_tokens},
                        ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(charge.encode("utf-8")).hexdigest()


def _http(url: str, entetes: dict[str, str], corps: bytes, timeout: float) -> dict:
    requete = urllib.request.Request(url, data=corps, headers=entetes, method="POST")
    try:
        with urllib.request.urlopen(requete, timeout=timeout) as r:
            texte = r.read().decode("utf-8", errors="replace")
            statut = getattr(r, "status", 200)
    except urllib.error.HTTPError as e:
        texte = e.read().decode("utf-8", errors="replace")
        raise ErreurDeepSeek(
            f"HTTP {e.code} : {texte[:400]}", code=e.code,
            reessayable=e.code in (408, 409, 425, 429, 500, 502, 503, 504)) from None
    except urllib.error.URLError as e:
        raise ErreurDeepSeek(f"réseau : {e.reason}", reessayable=True) from None
    if statut >= 400:
        raise ErreurDeepSeek(f"HTTP {statut} : {texte[:400]}", code=statut,
                             reessayable=statut in (408, 409, 425, 429, 500, 502, 503, 504))
    try:
        return json.loads(texte)
    except json.JSONDecodeError as e:
        raise ErreurDeepSeek(f"réponse non JSON : {texte[:200]}") from e


class DeepSeek:
    def __init__(self, cle: str | None = None, base_url: str | None = None,
                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
                 transport=None, sleep=time.sleep, timeout: float = 120.0,
                 essais: int = 3) -> None:
        self.cle = cle if cle is not None else _cle_env()
        self.base_url = (base_url or os.environ.get("DEEPSEEK_BASE_URL")
                         or os.environ.get("DSH_BASE_URL")
                         or BASE_DEFAUT).rstrip("/")
        self.modele = (modele or os.environ.get("DEEPSEEK_MODEL")
                       or os.environ.get("DSH_MODEL") or MODELE_DEFAUT)
        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
                                      or CACHE_DEFAUT)
        self.transport = transport or _http
        self.sleep = sleep
        self.timeout = timeout
        self.essais = max(1, essais)

    # ------------------------------------------------------------------
    def disponible(self) -> bool:
        return bool(self.cle)

    def _url(self) -> str:
        return f"{self.base_url}/chat/completions"

    def _lire_cache(self, cle: str) -> ReponseDeepSeek | None:
        chemin = self.cache_dir / f"{cle}.json"
        if not chemin.is_file():
            return None
        try:
            d = json.loads(chemin.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return ReponseDeepSeek(contenu=d.get("contenu", ""),
                               modele=d.get("modele", self.modele),
                               usage=d.get("usage", {}),
                               raisonnement=d.get("raisonnement"),
                               latence_s=float(d.get("latence_s", 0.0)),
                               cache=True, brut=d.get("brut"))

    def _ecrire_cache(self, cle: str, r: ReponseDeepSeek) -> None:
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            (self.cache_dir / f"{cle}.json").write_text(json.dumps({
                "contenu": r.contenu, "modele": r.modele, "usage": r.usage,
                "raisonnement": r.raisonnement, "latence_s": r.latence_s,
                "recu_le": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "brut": r.brut,
            }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        except OSError:
            # un cache indisponible ne doit pas faire échouer une mesure
            pass

    # ------------------------------------------------------------------
    def demande(self, prompt: str | None = None, *, system: str | None = None,
                messages: list[dict] | None = None, temperature: float = 0.0,
                max_tokens: int = 1024, dry_run: bool = False,
                cache: bool = True) -> ReponseDeepSeek:
        if messages is None:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            if prompt is None:
                raise ValueError("il faut un prompt ou des messages")
            messages.append({"role": "user", "content": prompt})
        if dry_run:
            return ReponseDeepSeek(
                contenu=f"[dry-run] {len(messages)} message(s), modèle {self.modele} ; "
                        "aucune requête réseau.",
                modele=self.modele, usage={}, latence_s=0.0, cache=False)
        if not self.cle:
            raise ErreurDeepSeek(
                "clé absente : exporter DEEPSEEK_API_KEY (ou DSH_API_KEY), "
                "ou utiliser --dry-run")
        cle = _cache_cle(self.modele, messages, temperature, max_tokens)
        if cache:
            deja = self._lire_cache(cle)
            if deja is not None:
                return deja
        corps = json.dumps({"model": self.modele, "messages": messages,
                            "temperature": temperature, "max_tokens": max_tokens,
                            "stream": False}, ensure_ascii=False).encode("utf-8")
        entetes = {"Authorization": f"Bearer {self.cle}",
                   "Content-Type": "application/json",
                   "Accept": "application/json",
                   "User-Agent": "Drave/1.0 (banc externe)"}
        dernier = None
        for essai in range(self.essais):
            t0 = time.monotonic()
            try:
                d = self.transport(self._url(), entetes, corps, self.timeout)
                latence = time.monotonic() - t0
                choix = (d.get("choices") or [{}])[0]
                message = choix.get("message") or {}
                r = ReponseDeepSeek(
                    contenu=message.get("content") or "",
                    modele=d.get("model", self.modele),
                    usage=d.get("usage") or {},
                    raisonnement=message.get("reasoning_content"),
                    latence_s=round(latence, 3), cache=False, brut=d)
                if cache:
                    self._ecrire_cache(cle, r)
                return r
            except ErreurDeepSeek as e:
                dernier = e
                if not e.reessayable or essai + 1 >= self.essais:
                    raise
                self.sleep(2 ** essai)
        raise dernier or ErreurDeepSeek("échec sans cause")


def _main() -> int:
    ap = argparse.ArgumentParser(description="le banc DeepSeek de Drave")
    ap.add_argument("--prompt", default=None)
    ap.add_argument("--system", default=None)
    ap.add_argument("--messages", default=None,
                    help="JSON d'une liste de messages (prioritaire sur prompt)")
    ap.add_argument("--modele", default=None)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    messages = json.loads(args.messages) if args.messages else None
    client = DeepSeek(base_url=args.base_url, modele=args.modele)
    try:
        r = client.demande(args.prompt, system=args.system, messages=messages,
                           temperature=args.temperature,
                           max_tokens=args.max_tokens, dry_run=args.dry_run,
                           cache=not args.no_cache)
    except ErreurDeepSeek as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"contenu": r.contenu, "raisonnement": r.raisonnement,
                          "modele": r.modele, "usage": r.usage,
                          "latence_s": r.latence_s, "cache": r.cache},
                         ensure_ascii=False, indent=1))
    else:
        print(r.contenu)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
