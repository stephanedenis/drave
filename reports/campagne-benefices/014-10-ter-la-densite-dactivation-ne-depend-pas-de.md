> Campagne : **campagne-benefices** · expérience **10-ter**
> Titre : 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si

Même modèle (Qwen2.5-0.5B Q8_0), même matériel, quatre corpus, 192 jetons : la
question du batch 2 était « le bénéfice événementiel dépend-il de la tâche ? ».

| corpus | jetons/octet | PPL | **bits/octet** | paires/jeton | **densité** |
|---|---:|---:|---:|---:|---:|
| prose anglaise | 0,2385 | 15,85 | **0,951** | 495,9 M | **71 %** |
| français | 0,2783 | 11,19 | **0,969** | 495,9 M | **71 %** |
| code | 0,3117 | 7,09 | **0,881** | 495,9 M | **71 %** |
| **399 langues** (UDHR, article 1) | 0,4113 | **229,84** | **3,227** | 495,9 M | **71 %** |

**La densité est identique dans les quatre cas — 71 %, à 0,002 point près**
(67,766 / 67,767 / 67,766 / 67,764 milliards d'événements). Autrement dit : **le
bénéfice événementiel ne dépend pas de la tâche**, il dépend du **modèle**. Un
modèle dense reste dense quelle que soit l'entrée ; c'est la parcimonie
*entraînée* qui la change, et rien d'autre. L'hypothèse « telle tâche réveille
moins de neurones » est **réfutée** ici — y compris sur un corpus qui change
complètement d'écriture et de langue.

**Ce qui dépend de la tâche, c'est la qualité.** En bits/octet — la seule unité
comparable entre tokenizers — le même modèle prédit le **code mieux que la prose**
(0,881 contre 0,951) et le **français moins bien que l'anglais** (0,969 contre
0,951). Les perplexités brutes disent l'inverse (7,09 pour le code contre 15,85
pour la prose) uniquement parce que le code se tokenise en jetons plus longs :
c'est exactement le piège que la colonne bits/octet neutralise.

**Et sur 399 langues, le même modèle est 3,4× pire qu'en prose** (3,227 contre
0,951 bit/octet) — la ligne la plus défavorable du relevé. La réserve est dans la
nature du corpus : ce n'est pas *une* langue, c'est un empilement de 399 langues
dont beaucoup sont peu dotées, donc cela mesure une **couverture**, pas une
performance linguistique. C'est néanmoins la réponse à « pour tout type de
tâches » : sur cette famille, l'échelle de 0,5 B ne suffit pas, et **la densité
d'activation ne bouge pas d'un iota** — le moteur événementiel n'y gagne donc
rien de plus qu'ailleurs ; c'est le modèle qui est en défaut.

**Le seuil absolu, lui, s'effondre sur ce corpus** : `--act-thresh 0,05` fait
passer la perplexité de 229,8 à **2 542** (et l'événementiel de 67,8 à 29,2 G) —
soit ×11, alors que le k-WTA au même taux d'événements ne coûte que quelques pour
cent (§ 19). Le résultat du § 19 n'est donc pas une propriété de la prose
anglaise : il tient sur les quatre corpus.

---
