"""
Qtrinet — projection matérielle sur la carte Storey Peak (Stratix V GS D5).

Toutes les constantes viennent de mesures réelles, consignées dans
FPGA-Stratix-V/docs/carte-storey-peak.md et docs/journal-bringup.md :

  DDR3 lecture            9,66 Go/s   (mesuré, blog part 6)
  PCIe Gen3 x8            6,50 Go/s   (mesuré, blog part 8)
  QSFP+ 40GbE             4,80 Go/s   (théorique, jamais démontré)
  NVLink GPU↔GPU         25,78 Go/s   (mesuré sur Hauru)
  M20K                    2 014 blocs × 20 Kbit = 5,03 Mo   (Quartus)
  ALM                       172 600
  DSP                         1 590  (inutilisés dans la voie ternaire)
  fmax mesuré (Kernel 1)   ~124 MHz  (slack −3,056 ns à 200 MHz)
"""

from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Constantes carte (mesurées)
# --------------------------------------------------------------------------- #

CARD = {
    "ddr3_read_Bps": 9.66e9,      # octets/s
    "pcie_x8_Bps": 6.50e9,
    "qsfp40_Bps": 4.80e9,
    "nvlink_Bps": 25.78e9,
    "m20k_bytes": 2014 * 20480 / 8,
    "alms": 172_600,
    "dsps": 1_590,
    "f_clk_hz": 124e6,            # fmax réellement atteint par le Kernel 1
    "f_clk_target_hz": 200e6,     # cible du SDC
}


@dataclass
class Projection:
    label: str
    params: int
    bits_per_weight: float
    weight_bytes: float
    macs: int
    t_memory_s: float          # temps imposé par la lecture des poids
    lanes_needed: int          # voies de MAC pour saturer la mémoire
    alms_for_lanes: int        # estimation ALM (≈30 ALM/voie)
    fits_m20k: bool
    fits_ddr3: bool


def lanes_needed(bits_per_weight: float, bw_Bps: float, f_clk_hz: float) -> int:
    """Nombre de voies de MAC nécessaires pour suivre le débit mémoire.

    Chaque voie consomme 1 poids par cycle ; la mémoire fournit
    bw / (bits/8) poids par seconde.
    """
    weights_per_s = bw_Bps / (bits_per_weight / 8.0)
    return int(round(weights_per_s / f_clk_hz))


def project(params: int, bits_per_weight: float, label: str = "",
            macs_per_param: float = 1.0, alms_per_lane: int = 30) -> Projection:
    """Projette un modèle sur UNE carte."""
    weight_bytes = params * bits_per_weight / 8.0
    macs = int(params * macs_per_param)
    t_mem = weight_bytes / CARD["ddr3_read_Bps"]
    lanes = lanes_needed(bits_per_weight, CARD["ddr3_read_Bps"], CARD["f_clk_hz"])
    return Projection(
        label=label or f"{params/1e9:.2f}G params @ {bits_per_weight:.2f} b",
        params=params,
        bits_per_weight=bits_per_weight,
        weight_bytes=weight_bytes,
        macs=macs,
        t_memory_s=t_mem,
        lanes_needed=lanes,
        alms_for_lanes=lanes * alms_per_lane,
        fits_m20k=weight_bytes <= CARD["m20k_bytes"],
        fits_ddr3=weight_bytes <= 4e9,
    )


def report_line(p: Projection) -> str:
    tok_s = 1.0 / p.t_memory_s if p.t_memory_s > 0 else float("inf")
    return (
        f"{p.label:<34} {p.weight_bytes/1e6:9.1f} Mo  "
        f"{p.t_memory_s*1e3:9.3f} ms/token  {tok_s:8.1f} tok/s  "
        f"{p.lanes_needed:6d} voies  {p.alms_for_lanes:7d} ALM"
    )
