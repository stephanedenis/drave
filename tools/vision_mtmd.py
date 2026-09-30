#!/usr/bin/env python3
"""Référence de vision : interroger libmtmd d'ollama, sans en-têtes.

C'est la SEULE vérification qui tranche d'un coup la rotation 2-D, la fenêtre
locale et la fusion 2 × 2 du ViT de Qwen2.5-VL : elle compare la sortie complète
de l'implémentation de référence (llama.cpp, embarquée par ollama) aux 3 584
valeurs du projecteur du moteur.

Aucun en-tête n'est installé, donc les prototypes sont déclarés ici. La structure
de paramètres est déclarée OPAQUE et GÉNÉREUSE (256 octets) : au-delà de 16
octets, l'ABI SysV passe la structure sur la pile et l'appelé ne lit que ce dont
il a besoin — une déclaration plus grande que la réelle est sans danger. Les
valeurs par défaut viennent de `*_default_params()`, pas d'un tampon à zéro.

Usage : vision_mtmd.py <modele.gguf> <mmproj.gguf> [sortie.bin]
"""
import ctypes
import os
import struct
import sys

OLLAMA = "/usr/lib/ollama"
MODELE = "/home/stephane/FastNVMe/models/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
MMPROJ = "/home/stephane/FastNVMe/models/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf"
TAILLE_PARAMS = 256


class Params(ctypes.Structure):
    _fields_ = [("b", ctypes.c_ubyte * TAILLE_PARAMS)]


def charger():
    llama = ctypes.CDLL(f"{OLLAMA}/libllama.so", mode=ctypes.RTLD_GLOBAL)
    mtmd = ctypes.CDLL(f"{OLLAMA}/libmtmd.so")
    # « no backends are loaded » : llama.cpp ne charge plus ggml tout seul, il
    # faut le lui demander — sinon le chargement du modèle échoue.
    try:
        ggml = ctypes.CDLL(f"{OLLAMA}/libggml.so", mode=ctypes.RTLD_GLOBAL)
        # `load_all` cherche les greffons à côté de l'EXÉCUTABLE (python3), où il
        # n'y en a pas : on charge explicitement le backend CPU de la machine
        # (Xeon E5 v3 = haswell).
        ggml.ggml_backend_load.restype = ctypes.c_void_p
        ggml.ggml_backend_load.argtypes = [ctypes.c_char_p]
        for nom in ("libggml-cpu-haswell.so", "libggml-cpu-alderlake.so",
                    "libggml-cpu-sandybridge.so"):
            if os.path.exists(f"{OLLAMA}/{nom}"):
                b = ggml.ggml_backend_load(f"{OLLAMA}/{nom}".encode())
                print(f"backend {nom} :", "chargé" if b else "ÉCHEC")
                break
    except (OSError, AttributeError) as e:
        print("chargement des backends ggml impossible :", e)
    # --- backend et modèle de texte
    llama.llama_backend_init.restype = None
    llama.llama_backend_init()
    llama.llama_model_default_params.restype = Params
    pm = llama.llama_model_default_params()
    llama.llama_model_load_from_file.restype = ctypes.c_void_p
    llama.llama_model_load_from_file.argtypes = [ctypes.c_char_p, Params]
    modele = sys.argv[1] if len(sys.argv) > 1 else MODELE
    mmproj = sys.argv[2] if len(sys.argv) > 2 else MMPROJ
    print(f"chargement du modèle de texte : {modele}")
    m = llama.llama_model_load_from_file(modele.encode(), pm)
    if not m:
        print("échec du chargement du modèle")
        return None
    # --- contexte multimodal
    mtmd.mtmd_context_params_default.restype = Params
    cp = mtmd.mtmd_context_params_default()
    mtmd.mtmd_init_from_file.restype = ctypes.c_void_p
    mtmd.mtmd_init_from_file.argtypes = [ctypes.c_char_p, ctypes.c_void_p, Params]
    ctx = mtmd.mtmd_init_from_file(mmproj.encode(), m, cp)
    print("contexte mtmd :", "ok" if ctx else "ÉCHEC")
    return (llama, mtmd, m, ctx)


def image_deterministe(cote=84):
    """Exactement l'image du banc Rust : dégradé + carré central."""
    buf = (ctypes.c_ubyte * (cote * cote * 3))()
    for y in range(cote):
        for x in range(cote):
            carre = cote // 3 <= x < 2 * cote // 3 and cote // 3 <= y < 2 * cote // 3
            for c in range(3):
                v = 1.0 if carre else (x + y + c) / (2.0 * cote)
                buf[(y * cote + x) * 3 + c] = max(0, min(255, int(v * 255)))
    return buf, cote


def main():
    charge = charger()
    if charge is None:
        return 1
    _, mtmd, _, ctx = charge
    buf, cote = image_deterministe()
    mtmd.mtmd_bitmap_init.restype = ctypes.c_void_p
    mtmd.mtmd_bitmap_init.argtypes = [ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.POINTER(ctypes.c_ubyte)]
    bmp = mtmd.mtmd_bitmap_init(cote, cote, buf)
    print("bitmap :", "ok" if bmp else "ÉCHEC")
    mtmd.mtmd_default_marker.restype = ctypes.c_char_p
    marqueur = mtmd.mtmd_default_marker()
    print("marqueur d'image :", marqueur)
    mtmd.mtmd_input_chunks_init.restype = ctypes.c_void_p
    mtmd.mtmd_input_chunks_init.argtypes = []
    chunks = mtmd.mtmd_input_chunks_init()
    print("conteneur de morceaux :", "ok" if chunks else "ÉCHEC")
    bitmaps = (ctypes.c_void_p * 1)(bmp)
    mtmd.mtmd_tokenize.restype = ctypes.c_int32
    mtmd.mtmd_tokenize.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                   ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p),
                                   ctypes.c_size_t]
    # Le seul marqueur ne suffit pas (tokenize rendait std::bad_alloc, rc=2) :
    # on lui donne une invite complète, marqueur compris.
    invite = b"<|im_start|>user\n" + marqueur + b"\ndecris cette image<|im_end|>\n<|im_start|>assistant\n"
    rc = mtmd.mtmd_tokenize(ctx, chunks, invite, bitmaps, 1)
    mtmd.mtmd_input_chunks_size.restype = ctypes.c_size_t
    mtmd.mtmd_input_chunks_size.argtypes = [ctypes.c_void_p]
    n = mtmd.mtmd_input_chunks_size(chunks)
    print(f"tokenize rc={rc} · {n} morceaux")
    mtmd.mtmd_input_chunks_get.restype = ctypes.c_void_p
    mtmd.mtmd_input_chunks_get.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    mtmd.mtmd_input_chunk_get_type.restype = ctypes.c_int32
    mtmd.mtmd_input_chunk_get_type.argtypes = [ctypes.c_void_p]
    mtmd.mtmd_input_chunk_get_n_tokens.restype = ctypes.c_size_t
    mtmd.mtmd_input_chunk_get_n_tokens.argtypes = [ctypes.c_void_p]
    mtmd.mtmd_encode_chunk.restype = ctypes.c_int32
    mtmd.mtmd_encode_chunk.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    mtmd.mtmd_get_output_embd.restype = ctypes.POINTER(ctypes.c_float)
    mtmd.mtmd_get_output_embd.argtypes = [ctypes.c_void_p]
    for i in range(n):
        ch = mtmd.mtmd_input_chunks_get(chunks, i)
        typ = mtmd.mtmd_input_chunk_get_type(ch)
        ntok = mtmd.mtmd_input_chunk_get_n_tokens(ch)
        print(f"  morceau {i} : type {typ} · {ntok} jetons")
        if typ == 1:                      # 1 = image
            rc = mtmd.mtmd_encode_chunk(ctx, ch)
            print(f"  encode_chunk rc={rc}")
            ptr = mtmd.mtmd_get_output_embd(ctx)
            if not ptr:
                print("  pas d'embeddings")
                continue
            # 3 584 valeurs attendues (projection_dim du mmproj)
            vals = [ptr[k] for k in range(3584)]
            norme = sum(v * v for v in vals) ** 0.5
            print(f"  embeddings : 3 584 valeurs · |v| = {norme:.4f} · 4 premières "
                  f"{[round(v, 5) for v in vals[:4]]}")
            if len(sys.argv) > 3:
                with open(sys.argv[3], "wb") as f:
                    f.write(struct.pack("<i", len(vals)))
                    f.write(struct.pack(f"<{len(vals)}f", *vals))
                print("  écrit dans", sys.argv[3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
