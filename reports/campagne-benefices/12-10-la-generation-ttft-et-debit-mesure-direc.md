> Campagne : **campagne-benefices** · expérience **10**
> Titre : 10. La génération : TTFT et débit, mesure directe
> Date réelle : **2026-10-08 22:04 HAE** (source : commit `2d57177`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 10. La génération : TTFT et débit, mesure directe

| modèle | invite | TTFT | débit de génération |
|---|---:|---:|---:|
| Qwen2.5-0.5B Q8_0 | 11 jetons en 0,307 s | **27,9 ms** | **29,0 tok/s** |
| r1-distill-1.5B Q4_K_M | 11 jetons en 1,260 s | 114,6 ms | 7,1 tok/s |
| r1-distill-14B Q4_K_M | *en cours* | | |
| Qwen3-30B-A3B | *en cours* | | |
| gpt-oss-120b MXFP4 | *en cours* | | |

Ces chiffres-là portent la **latence perçue** d'un usage réel, que la perplexité
ne donne pas : un premier jeton en 28 ms et 29 jetons/s sur un 0,5 B, c'est un
assistant utilisable ; 7 jetons/s, c'est déjà pénible.

---
