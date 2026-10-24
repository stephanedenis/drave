# 8. Points relevés, non corrigés

> **Famille 8 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 8. Points relevés, non corrigés

Ces points ont été croisés en rédigeant ce glossaire. **Aucun autre fichier n'a été
modifié** : ils sont listés ici, avec leur chemin et leur citation, pour qu'un
lecteur ne s'y trompe pas.

1. **L'attribution de l'écart int8 se contredit dans le même document.**
   `docs/contexte-long.md:399-401` : « L'écart de +3,0 % contre +0,8 % à 8 192 vient
   donc d'ailleurs : probablement la quantification des VALEURS et la précision du
   softmax, pas l'arrondi des clés. » — alors que le §4.bis.3 du même fichier
   (`:176-197`) et `docs/roadmap.md:30` concluent l'inverse : « tout l'écart est
   dans les CLÉS ».

2. **Un paragraphe barré « CORRIGÉ » subsiste au milieu d'une section.**
   `docs/contexte-long.md:241-248` : « ~~Le format ne change presque rien au temps
   GPU (13,2 à 15,0 ms à 1 M) : le noyau est borné par la déquantification
   scalaire.~~ **CORRIGÉ** ». La phrase fausse reste lisible ; la valeur corrigée
   est 6,5-7,4 ms.

3. **Les phases P1 à P5 du plan V4.1 sont écrites deux fois.**
   `docs/plan-deepseek41-complet.md` porte deux titres « P1 », deux « P2 », deux
   « P3 », deux « P4 », deux « P5 » : une version « **FAIT** (02/10) » (`:164-169`)
   suivie de la version « à faire » (`:171-186`). Le statut se contredit à la
   lecture linéaire.

4. **Le mode 4 est dit « à écrire » alors qu'il est mesuré.**
   `docs/plan-prefill-reparti.md:421` : « **Le lot en listes** : c'est le mode 4, à
   écrire quand le débit gênera. » — contredit par `docs/format-flux.md:88-125` et
   `docs/plan-mode4-lot-listes.md:6` (« L'implémentation est faite »). Le préambule
   (`:3-11`) prévient que le corps du plan n'est pas réécrit, mais la phrase reste
   fausse telle quelle.

5. **Deux perplexités « clusters » sans rappel du contexte.**
   `docs/format-clusters.md:116` : « origine 15,2789 · clusters 15,2789 (mêmes
   63 jetons) » ; `docs/format-clusters.md:167-173` : « 8 | **799,8557** »
   (mêmes 7 jetons). 799,8557 est aussi la porte de non-régression citée partout
   (`docs/sprints.md:39`) : le lecteur qui ne voit qu'un des deux chiffres croit à
   une contradiction.

6. **Le bandeau de statut casse le tableau des modèles lourds.**
   `docs/plan-modeles-lourds.md:23-29` insère un bloc « Où en est ce plan (02/10) »
   entre la ligne d'en-tête (`:20-21`) et les lignes de données (`:30-38`) : le
   tableau n'a plus d'en-tête, et les colonnes ne sont plus lisibles.

7. **Trois durées par jeton pour le même modèle.**
   `docs/plan-modeles-lourds.md:92` : « ~73 s/jeton » (Kimi-K2.7) ;
   `reports/rapport-mla-experts.md:110` : « **53 s par jeton** » ;
   `reports/rapport-mla-experts.md:236` : « le moteur met ~190 s par jeton ». Aucune
   datation ne permet de savoir laquelle fait foi.

8. **Une affirmation que le corpus qualifie lui-même de fausse est reprise.**
   `reports/bilan-multi-materiel.md:96` : « il est **8 % plus rapide** que le dense
   (15,8 contre 14,7 tok/s) » — or `reports/rapport-croisement-push-pull.md:66-71`
   écrit : « **C'est faux, et je l'ai mesuré deux fois** », le pull corrigé valant
   **36,4 tok/s**.

9. **Le croisement push/pull est donné à deux densités différentes.**
   `reports/rapport-analyse-flux.md:14` : « Le croisement push/pull du projet est
   mesuré à **~10 % de densité** » — contredit par
   `reports/rapport-croisement-push-pull.md:43` : « Les deux architectures se
   croisent à **~22 % de densité d'activation**, pas à 10 % », et par
   `docs/vision.md:44-46`.

10. **Une accuracy de 4 971 % dans un tableau.**
    `reports/rapport-encodage.md:42` : « | 2.00 | **4971.00 %** | 5.5 | dense
    ternaire (référence CDC) | » — une exactitude supérieure à 100 % est impossible
    (49,71 % attendu, cf. `reports/rapport-minimal.md:12`).

11. **Le `mmap` est annoncé « pas fait » dans un rapport qui le dit fait ailleurs.**
    `reports/rapport-lecteur-multifichiers.md:267-268` : « Le **mmap** :
    `read_to_end` charge tout le fichier. DeepSeek-V4.1-Flash fait 366 Go, il
    restera hors de portée sans lui. » — contredit par `:171-186` du même fichier
    (« Les fichiers sont maintenant **mappés** », 9,32 s / 6,35 Go) et par
    `docs/format-clusters.md:181-186`.

12. **Le top-k GPU est dit « pas encore branché » après avoir été branché.**
    `reports/rapport-gpu-topk-selection.md:347-349` : « Le top-k GPU n'est donc
    **pas encore branché dans le moteur** [...] jusqu'à l'étape 3. » — contredit par
    `:164-171` du même rapport (« ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) ») et par
    `docs/plan-gpu-topk.md:99`.

13. **Un état « reste à faire » survit à l'état « fait » dans le plan MLA.**
    `docs/plan-mla-vision.md:104-106` : « Ce qui reste : **le chemin MLA dans le
    moteur** » — alors que la section précédente (`:55-72`) annonce « MLA EST FAIT
    ET VALIDÉ ». Les sections d'états successifs cohabitent sans être datées.

14. **Une valeur non reproduite est citée comme un acquis dans la vision.**
    `docs/vision.md:82-86` cite `--attn-topk 256` : « 234,88 contre 298,56 » ;
    `docs/contexte-long.md:565-567` précise que ces valeurs « ne sortent pas du
    binaire courant » et que « seul l'écart A/B fait foi », et
    `docs/plan-gpu-topk.md:86-90` ajoute qu'elles « n'[ont] pas été reproduite[s]
    depuis ».

15. **Des mesures de dispersion manifestement fausses restent dans un rapport.**
    `reports/rapport-cpu-aer.md:17-18` : « dispersion (`np.bincount`) :
    **183999808.87 G événements/s** » et « **364797216.41 G** » — soit ~1,8·10¹⁷
    événements/s, incompatibles avec les 18,1 G événements/s du GPU ; le rapport
    signale lui-même (`:62-65`) que ces chiffres ne sont pas exploitables.

16. **Le coût de la journalisation est donné pour deux artefacts différents.**
    `docs/programme-recherche.md:29` : « Journaliser les listes d'activations
    (1,2 Mo/token, **+3,0 %**) » — le +3,0 % est celui du **capteur hebbien**
    (`reports/rapport-programme-evolutif.md:17`), tandis que la trace de flux coûte
    **+8 % de temps** et 258 ko/jeton (`docs/roadmap.md:15`). Les deux chiffres sont
    exacts séparément, mais la phrase les associe au même objet.

17. **Le périmètre annoncé ne correspond pas au disque.**
    La demande de glossaire décrit « une centaine de rapports » dans `reports/` ;
    le dossier en contient **60** (plus 9 fichiers dans `sprints/`). Les 18
    documents de `docs/` sont, eux, exacts (`reports/rapport-coherence-vision.md:3`
    parle aussi de « 18 documents »).

18. **Des termes attendus sont absents du corpus.**
    `Hadamard`, `MTP` (hors la mention `dspark_*`), `SparseVec` hors des rapports
    d'optimisation, `speculative decoding` en toutes lettres, `MTok/s`, `Gbit/s`,
    `p50/p95` (seul p90 apparaît) ne figurent **pas** dans `docs/` ni dans
    `reports/`. `MTP` n'apparaît que dans `journal/sessions/.../rapport.md:2545`
    (« MTP | `dspark` : 128 experts top-3 sur les couches 37-39 »), fichier hors du
    périmètre de ce glossaire. Les entrées correspondantes ci-dessus sont donc
    explicitées comme telles.

19. **Un drapeau présenté comme existant n'existe pas.**
    `docs/vision.md:74` liste, dans le tableau « Ce qui existe déjà, et qui a
    servi » : « `--ppl-profil` | le temps par poste (projections, rope, attention,
    FFN, tête) » — et `docs/contexte-long.md:520` s'appuie dessus. Or
    `reports/rapport-drapeaux-ignores.md:97` classe déjà ce drapeau « **jamais
    lu** », et le code courant ne le reconnaît pas : il reste un champ mort
    (`drave-core/src/main.rs:541`, jamais alimenté par `analyser()`), donc tout
    usage est traité comme drapeau inconnu.

20. **Un drapeau dit inexistant existe désormais.**
    `reports/rapport-drapeaux-ignores.md:196-198` recommande `--options-actives`
    « (et `--options-strict`) » tout en précisant ailleurs que la variante
    `--options-strict` **n'existe pas** ; l'arbre courant l'implémente pourtant
    (`drave-core/src/main.rs:619`). Le rapport est daté du 30/09 : toute citation
    croisée doit être datée.

21. **Un rapport de sprint déclare « aucun poids ouvert » pour un modèle que le
    dépôt télécharge.** `sprints/07-cloture-de-la-nuit.md:138-142` :
    « **DeepSeek-V4.1-Flash est un modèle d'API** … **aucun poids ouvert**, donc
    rien à télécharger » — contredit par `tools/manifeste_modeles_lourds.json`
    (entrée `DeepSeek-V4.1-Flash-Q2`, 365,7 Go), par `tools/portes_formats.sh:38`
    et par `sprints/09:5`. `sprints/` est hors du périmètre initial de ce
    glossaire, mais le fichier est dans le dépôt et la contradiction est frontale.

---

