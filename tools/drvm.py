#!/usr/bin/env python3
"""drvm.py — DRVM v0, le conteneur natif du modèle Drave.

DRVM n'est pas un GGUF amélioré : c'est un conteneur de **graphe** et de **blocs**.
Le manifeste porte les blocs, les ports, les routes, les têtes, le pont et la
cellule de pensée ; le payload porte les tenseurs alignés, lisibles par bloc et
mmap-ables. Le lecteur refuse une version ou un type de bloc qu'il ne connaît pas.

Structure :
  en-tête 92 o (magie, version, tailles, offsets, deux SHA-256)
  manifeste JSON canonique, aligné sur 64 o
  payload de tenseurs, chaque tenseur aligné sur 64 o

CLI :
  python3 tools/drvm.py inspect MODELE.drvm
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import os
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MAGIC = b"DRVM"
VERSION = 0
ALIGNEMENT = 64
HEADER = struct.Struct("<4sHH I Q Q 32s 32s")  # 92 octets
BLOCS_CONNUS = {
    "input", "local_mixer", "sparse_ffn", "state", "early_head",
    "thought", "bridge", "output",
}
SECTIONS = ("model", "graph", "tensors", "execution")

# Les clés sont des listes FERMÉES : une clé inconnue est refusée, jamais ignorée.
# C'est la même règle que pour `kind` (docs/theorie/modele-natif.md) : un manifeste
# à moitié compris qui s'exécute est un manifeste qui ment. Avant le 17/11, le
# lecteur déclarait `routes`, `regions`, `heads`, `thought`, `bridge` et les
# ignorait en silence ; une route est maintenant LUE, validée et exécutée par le
# moteur Rust (le moteur numpy, lui, refuse les routes).
CLES_RACINE = frozenset({"format", "version", *SECTIONS})
CLES_GRAPHE = frozenset({"blocks", "regions", "routes", "heads", "thought", "bridge"})
CLES_BLOC = frozenset({"id", "kind", "inputs", "outputs", "impl", "contrat"})
CLES_EXECUTION = frozenset({"activation", "placement", "cache", "replay", "import"})
CLES_THOUGHT = frozenset({"steps"})
CLES_REGION = frozenset({"id", "blocks"})
CLES_CONTRAT = frozenset({"version", "tolerance"})
CLES_ROUTE = frozenset({"id", "bloc", "si", "alors", "sinon"})
CLES_SI = frozenset({"kind", "seuil"})

# Les profils d'implémentation d'un bloc. Le NOM est public (il est dans le
# manifeste, donc dans le hash, donc dans la trace) ; l'ALGORITHME est privé.
#   defaut — le produit ligne par ligne, seuil net du k-WTA ;
#   bloque — le même produit accumulé par colonnes : MÊME fonction, autre ordre,
#            donc indifférent dans la tolérance déclarée par `contrat` ;
#   flou   — le seuil net remplacé par une appartenance sigmoïde : AUTRE fonction
#            sous la même signature, donc NON substituable — c'est un candidat au
#            ROUTAGE, pas à la substitution.
# Le format connaît les trois ; chaque moteur refuse celles qu'il n'implémente
# pas (le moteur numpy ne connaît que « defaut »).
IMPLS_CONNUES = frozenset({"defaut", "bloque", "flou"})
IMPLS_MOTEUR_NUMPY = frozenset({"defaut", "bloque"})


class DRVMError(ValueError):
    """Erreur de format DRVM."""


@dataclass
class TensorSpec:
    name: str
    data: bytes
    dtype: str = "f32"
    shape: tuple[int, ...] = ()
    bloc: str = ""
    quant: str | None = None
    sparsity: float = 0.0


@dataclass
class DrvmFile:
    manifest: dict[str, Any]
    _mm: mmap.mmap
    _fichier: Any
    payload_offset: int = 0
    tensors: dict[str, dict[str, Any]] = field(default_factory=dict)

    def tensor(self, name: str) -> memoryview:
        t = self.tensors.get(name)
        if t is None:
            raise DRVMError(f"tenseur inconnu : {name}")
        off = self.payload_offset + int(t["offset"])
        n = int(t["nbytes"])
        return memoryview(self._mm)[off:off + n]

    def close(self) -> None:
        try:
            self._mm.close()
        finally:
            self._fichier.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _canonique(manifest: dict[str, Any]) -> bytes:
    return json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _aligne(n: int) -> int:
    return (int(n) + ALIGNEMENT - 1) // ALIGNEMENT * ALIGNEMENT


def _objet(ou: str, valeur: Any) -> dict[str, Any]:
    if not isinstance(valeur, dict):
        raise DRVMError(f"{ou} n'est pas un objet")
    return valeur


def _cles_fermees(ou: str, obj: dict[str, Any], connues: frozenset[str]) -> None:
    inconnues = sorted(set(obj) - connues)
    if inconnues:
        raise DRVMError(f"clé inconnue dans {ou} : {', '.join(inconnues)}")


def _cle_absente(ou: str, obj: dict[str, Any], cle: str) -> Any:
    if cle not in obj:
        raise DRVMError(f"clé absente : {ou}.{cle}")
    return obj[cle]


def _chaines(ou: str, valeur: Any) -> list[str]:
    if not isinstance(valeur, list) or not all(isinstance(x, str) for x in valeur):
        raise DRVMError(f"{ou} doit être une liste de chaînes")
    return valeur


def _valide(manifest: dict[str, Any]) -> None:
    """Refuse ce que le lecteur ne sait pas exécuter — il ne l'ignore jamais."""
    _objet("le manifeste", manifest)
    _cles_fermees("le manifeste", manifest, CLES_RACINE)
    for section in SECTIONS:
        if section not in manifest:
            raise DRVMError(f"section absente : {section}")
    if manifest.get("format") != "DRVM":
        raise DRVMError("format != DRVM")
    if manifest.get("version") != VERSION:
        raise DRVMError(f"version non supportée : {manifest.get('version')}")
    modele = _objet("model", manifest["model"])
    if not isinstance(modele.get("name"), str):
        raise DRVMError("model.name absent")
    graphe = _objet("graph", manifest["graph"])
    _cles_fermees("graph", graphe, CLES_GRAPHE)
    for cle in ("blocks", "regions", "routes", "heads", "thought", "bridge"):
        _cle_absente("graph", graphe, cle)
    blocs = graphe["blocks"]
    if not isinstance(blocs, list) or not blocs:
        raise DRVMError("graphe sans bloc")
    ids = set()
    kinds = {}
    for b in blocs:
        _objet("un bloc", b)
        _cles_fermees("un bloc", b, CLES_BLOC)
        if "id" not in b or "kind" not in b:
            raise DRVMError(f"bloc incomplet : {b!r}")
        if not isinstance(b["id"], str) or not isinstance(b["kind"], str):
            raise DRVMError(f"bloc mal typé : {b!r}")
        if b["id"] in ids:
            raise DRVMError(f"bloc dupliqué : {b['id']}")
        ids.add(b["id"])
        kinds[b["id"]] = b["kind"]
        if b["kind"] not in BLOCS_CONNUS:
            raise DRVMError(f"type de bloc inconnu : {b['kind']}")
        impl = b.get("impl", "defaut")
        if not isinstance(impl, str) or impl not in IMPLS_CONNUES:
            raise DRVMError(f"impl inconnue : {impl!r} (bloc {b['id']})")
        if impl != "defaut" and b["kind"] != "local_mixer":
            raise DRVMError(
                f"impl non applicable au bloc {b['id']} ({b['kind']}) : {impl}")
        if impl != "defaut" and "contrat" not in b:
            raise DRVMError(f"contrat absent pour l'impl {impl} (bloc {b['id']})")
        if "contrat" in b:
            ou = f"contrat du bloc {b['id']}"
            contrat = _objet(ou, b["contrat"])
            _cles_fermees(ou, contrat, CLES_CONTRAT)
            version = _cle_absente(ou, contrat, "version")
            if not isinstance(version, int) or isinstance(version, bool) or version != 0:
                raise DRVMError(f"contrat.version non supportée : {version!r} (bloc {b['id']})")
            tolerance = _cle_absente(ou, contrat, "tolerance")
            if (not isinstance(tolerance, (int, float)) or isinstance(tolerance, bool)
                    or not tolerance >= 0):
                raise DRVMError(f"contrat.tolerance invalide : {tolerance!r} (bloc {b['id']})")
        for port in ("inputs", "outputs"):
            _chaines(f"{port} du bloc {b['id']}", _cle_absente("bloc", b, port))
    regions = graphe["regions"]
    if not isinstance(regions, list):
        raise DRVMError("graph.regions doit être une liste")
    vues = set()
    for r in regions:
        _objet("une région", r)
        _cles_fermees("une région", r, CLES_REGION)
        rid = _cle_absente("une région", r, "id")
        if not isinstance(rid, str):
            raise DRVMError(f"région sans id : {r!r}")
        if rid in vues:
            raise DRVMError(f"région dupliquée : {rid}")
        vues.add(rid)
        for x in _chaines(f"les blocs de la région {rid}",
                          _cle_absente("une région", r, "blocks")):
            if x not in ids:
                raise DRVMError(f"région vers un bloc inconnu : {x}")
    for h in _chaines("graph.heads", graphe["heads"]):
        if h not in ids:
            raise DRVMError(f"tête vers un bloc inconnu : {h}")
    pensee = graphe["thought"]
    if pensee is not None:
        _objet("thought", pensee)
        _cles_fermees("thought", pensee, CLES_THOUGHT)
        pas = _cle_absente("thought", pensee, "steps")
        if not isinstance(pas, int) or isinstance(pas, bool) or pas < 0:
            raise DRVMError(f"thought.steps invalide : {pas!r}")
    pont = graphe["bridge"]
    if pont is not None and (not isinstance(pont, str) or pont not in ids):
        raise DRVMError(f"pont vers un bloc inconnu : {pont}")
    routes = graphe["routes"]
    if not isinstance(routes, list):
        raise DRVMError("graph.routes doit être une liste")
    vues_routes, cibles = set(), set()
    for r in routes:
        _objet("une route", r)
        _cles_fermees("une route", r, CLES_ROUTE)
        rid = _cle_absente("une route", r, "id")
        if not isinstance(rid, str):
            raise DRVMError(f"route sans id : {r!r}")
        if rid in vues_routes:
            raise DRVMError(f"route dupliquée : {rid}")
        vues_routes.add(rid)
        bloc = _cle_absente("une route", r, "bloc")
        if not isinstance(bloc, str) or bloc not in ids:
            raise DRVMError(f"route vers un bloc inconnu : {bloc}")
        if kinds[bloc] != "local_mixer":
            raise DRVMError(f"route vers un bloc non mixeur : {bloc} ({kinds[bloc]})")
        if bloc in cibles:
            raise DRVMError(f"deux routes pour le bloc : {bloc}")
        cibles.add(bloc)
        si = _objet("si", _cle_absente("une route", r, "si"))
        _cles_fermees("si", si, CLES_SI)
        kind = _cle_absente("si", si, "kind")
        if kind != "position":
            raise DRVMError(f"condition de route inconnue : {kind}")
        seuil = _cle_absente("si", si, "seuil")
        if not isinstance(seuil, int) or isinstance(seuil, bool) or seuil < 0:
            raise DRVMError(f"si.seuil invalide : {seuil!r} (route {rid})")
        if "alors" not in r:
            raise DRVMError(f"route sans alors : {rid}")
        for cle in ("alors", "sinon"):
            if cle in r:
                v = r[cle]
                if not isinstance(v, str) or v not in IMPLS_CONNUES:
                    raise DRVMError(f"impl inconnue : {v!r} ({cle} de la route {rid})")
    execution = _objet("execution", manifest["execution"])
    _cles_fermees("execution", execution, CLES_EXECUTION)
    for cle in ("activation", "placement"):
        if not isinstance(_cle_absente("execution", execution, cle), str):
            raise DRVMError(f"execution.{cle} doit être une chaîne")
    for cle in ("cache", "replay", "import"):
        if cle in execution:
            _objet(f"execution.{cle}", execution[cle])
    if not isinstance(manifest["tensors"], list):
        raise DRVMError("section tensors absente")
    for t in manifest["tensors"]:
        if not isinstance(t, dict):
            raise DRVMError(f"tenseur mal formé : {t!r}")
        if t.get("bloc") not in ids:
            raise DRVMError(f"tenseur rattaché à un bloc inconnu : {t.get('bloc')}")
        if int(t["nbytes"]) <= 0 or int(t["offset"]) % ALIGNEMENT:
            raise DRVMError(f"tenseur mal aligné ou vide : {t.get('name')}")


def write_drvm(path: str | os.PathLike, manifest: dict[str, Any],
               tensors: list[TensorSpec]) -> str:
    """Écrit un DRVM et retourne le SHA-256 du fichier."""
    manifest = json.loads(json.dumps(manifest))  # copie
    manifest.setdefault("format", "DRVM")
    manifest.setdefault("version", VERSION)
    if not tensors:
        raise DRVMError("aucun tenseur")
    noms = set()
    specs = []
    offset = 0
    for t in tensors:
        if t.name in noms:
            raise DRVMError(f"tenseur dupliqué : {t.name}")
        noms.add(t.name)
        if not t.data:
            raise DRVMError(f"tenseur vide : {t.name}")
        offset = _aligne(offset)
        specs.append({
            "name": t.name, "bloc": t.bloc, "dtype": t.dtype,
            "shape": list(t.shape), "offset": offset, "nbytes": len(t.data),
            "quant": t.quant, "sparsity": t.sparsity,
        })
        offset += len(t.data)
    manifest["tensors"] = specs
    _valide(manifest)
    mj = _canonique(manifest)
    mj_pad = mj + b"\0" * (_aligne(len(mj)) - len(mj))
    payload = bytearray()
    for t in tensors:
        payload.extend(b"\0" * (_aligne(len(payload)) - len(payload)))
        payload.extend(t.data)
    header = HEADER.pack(
        MAGIC, VERSION, HEADER.size, len(mj), HEADER.size + len(mj_pad),
        HEADER.size + len(mj_pad) + len(payload),
        hashlib.sha256(mj).digest(), hashlib.sha256(payload).digest(),
    )
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("wb") as f:
        f.write(header); f.write(mj_pad); f.write(payload)
    os.replace(tmp, p)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_drvm(path: str | os.PathLike, verifier: bool = True) -> DrvmFile:
    """Lit un DRVM, vérifie l'en-tête, le manifeste et le payload (SHA-256)."""
    p = Path(path)
    f = p.open("rb")
    try:
        raw = f.read(HEADER.size)
        if len(raw) != HEADER.size:
            raise DRVMError("fichier trop court pour l'en-tête")
        magic, version, hsize, mlen, poff, total, msha, psha = HEADER.unpack(raw)
        if magic != MAGIC:
            raise DRVMError(f"mauvaise magie : {magic!r}")
        if version != VERSION:
            raise DRVMError(f"version non supportée : {version}")
        if hsize != HEADER.size or poff < hsize + mlen or poff > total:
            raise DRVMError("en-tête incohérent")
        if total != p.stat().st_size:
            raise DRVMError("taille de fichier incohérente")
        f.seek(hsize)
        mj = f.read(mlen)
        if hashlib.sha256(mj).digest() != msha:
            raise DRVMError("hash du manifeste invalide")
        try:
            manifest = json.loads(mj.decode("utf-8"))
        except Exception as e:
            raise DRVMError(f"manifeste JSON invalide : {e}") from e
        _valide(manifest)
        f.seek(0)
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if verifier and hashlib.sha256(mm[poff:]).digest() != psha:
            mm.close()
            raise DRVMError("hash du payload invalide")
    except Exception:
        f.close()
        raise
    return DrvmFile(manifest=manifest, _mm=mm, _fichier=f, payload_offset=poff,
                    tensors={t["name"]: t for t in manifest["tensors"]})


def inspecter(path: str | os.PathLike) -> dict[str, Any]:
    with read_drvm(path) as d:
        return {
            "fichier": str(path),
            "manifest_sha256": hashlib.sha256(_canonique(d.manifest)).hexdigest(),
            "modele": d.manifest["model"],
            "blocs": [b["id"] for b in d.manifest["graph"]["blocks"]],
            "tenseurs": len(d.manifest["tensors"]),
            "octets_payload": sum(int(t["nbytes"]) for t in d.manifest["tensors"]),
            "version": d.manifest["version"],
        }


def main() -> None:
    ap = argparse.ArgumentParser(description="DRVM v0 — conteneur natif Drave")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inspect")
    i.add_argument("fichier")
    a = ap.parse_args()
    if a.cmd == "inspect":
        print(json.dumps(inspecter(a.fichier), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
