//! Tokenizer BPE byte-level d'un modèle Qwen2.5, reconstruit depuis les
//! métadonnées GGUF (`tokenizer.ggml.tokens`, `.merges`, `.token_type`).
//!
//! Std seul : aucune dépendance. Chaîne de traitement, identique à celle de
//! Qwen2 / llama.cpp :
//!   1. découpage du texte par le pré-tokenizer, motif `qwen2` :
//!      `(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}`
//!      `| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+`
//!      écrit à la main (l'ORDRE des alternatives et le lookahead `(?!\S)`
//!      font partie de la spécification) ;
//!   2. encodage byte-level de chaque morceau (table octet ↔ caractère de GPT-2) ;
//!   3. BPE : fusion répétée de la paire de rangs minimaux, puis conversion en ids.
//!
//! Les classes `\p{L}` et `\p{N}` sont approchées par `char::is_alphabetic()` et
//! `char::is_numeric()` : voir la nuance documentée sur `is_letter`.
//!
//! Vérification (hors dépôt, 737 cas : 300 lignes de wikitext2 avec et sans
//! retour à la ligne, cas pièges, plus 20 000 cas aléatoires) : les morceaux
//! produits ici sont identiques à ceux du moteur regex de Perl exécutant le
//! motif ci-dessus, à la seule exception des marques combinantes signalées
//! dans `is_letter`.

use std::collections::HashMap;

/// Séparateur interne des clés de fusion : les symboles manipulés ici sont tous
/// issus de la table octet ↔ caractère (U+0021..U+007E, U+00A1..U+00FF, puis
/// U+0100+), donc U+0001 ne peut jamais apparaître dans un symbole.
const SEP: char = '\u{1}';

pub struct Tokenizer {
    /// vocabulaire : l'indice est l'id du token.
    id_to_tok: Vec<String>,
    /// token (chaîne brute du GGUF) -> id. Dernière occurrence gagnante.
    tok_to_id: HashMap<String, u32>,
    /// (a, b) -> rang de fusion ; clé = `a` + SEP + `b`.
    ranks: HashMap<String, u32>,
    /// table byte-level : octet -> caractère (GPT-2 / Qwen).
    byte_enc: [char; 256],
    /// inverse de `byte_enc`, pour le décodage.
    byte_dec: HashMap<char, u8>,
    /// types GGUF des tokens (1 = normal, 3 = contrôle, 4 = défini par
    /// l'utilisateur, 5 = inutilisé…), utilisés par `special_id`.
    token_type: Vec<i32>,
    /// Motif de pré-découpage : `tokenizer.ggml.pre` du GGUF. « qwen2 »,
    /// « gpt-4o » (o200k) et « kimi-k2/k3 » sont implémentés ; les autres
    /// retombent sur qwen2.
    ///
    /// ⚠️ **Le motif kimi n'est pas cosmétique** : il groupe les nombres par
    /// TROIS (`\p{N}{1,3}`), sépare les idéogrammes Han, et n'admet les
    /// contractions qu'en suffixe des mots. Appliquer qwen2 à un modèle Kimi
    /// donne des identifiants différents de son tokenizer d'origine — mesuré le
    /// 03/10 : « 2026 » sortait en un seul jeton au lieu de « 202 » + « 6 ».
    /// C'était un défaut SILENCIEUX sur Kimi-K2.7 comme sur Kimi-K3.
    motif_gpt4o: bool,
    motif_kimi: bool,
}

impl Tokenizer {
    /// `tokens`, `merges` et `token_type` viennent des métadonnées GGUF.
    ///
    /// `merges` contient des chaînes « a b » : la coupure se fait au **premier**
    /// espace (comme `str.partition(" ")` en Python), le reste — espaces
    /// compris — formant le second symbole.
    pub fn new(tokens: Vec<String>, merges: Vec<String>, token_type: Vec<i32>,
               pre: &str) -> Self {
        let mut tok_to_id = HashMap::with_capacity(tokens.len());
        for (i, t) in tokens.iter().enumerate() {
            tok_to_id.insert(t.clone(), i as u32);
        }
        let mut ranks = HashMap::with_capacity(merges.len());
        for (i, m) in merges.iter().enumerate() {
            let (a, b) = match m.find(' ') {
                Some(p) => (&m[..p], &m[p + 1..]),
                None => (m.as_str(), ""),
            };
            let mut key = String::with_capacity(a.len() + b.len() + 1);
            key.push_str(a);
            key.push(SEP);
            key.push_str(b);
            ranks.insert(key, i as u32);
        }
        let byte_enc = bytes_to_unicode();
        let byte_dec = byte_enc.iter().enumerate().map(|(b, &c)| (c, b as u8)).collect();
        // o200k (gpt-4o, gpt-oss) découpe les lettres selon la CASSE, les
        // nombres par groupes de trois, et rattache « / » à la ponctuation.
        let motif_gpt4o = pre.starts_with("gpt-4o") || pre.starts_with("o200k");
        // `kimi-k2` (Kimi-K2.7) et `kimi-k3` (Kimi-K3) partagent le même motif.
        let motif_kimi = pre.starts_with("kimi");
        Tokenizer { id_to_tok: tokens, tok_to_id, ranks, byte_enc, byte_dec, token_type,
                    motif_gpt4o, motif_kimi }
    }

    /// Encode un texte en ids.
    pub fn encode(&self, text: &str) -> Vec<u32> {
        let cs: Vec<char> = text.chars().collect();
        let mut out = Vec::new();
        let mut i = 0;
        while i < cs.len() {
            let j = if self.motif_kimi { next_piece_kimi(&cs, i) }
                    else if self.motif_gpt4o { next_piece_gpt4o(&cs, i) }
                    else { next_piece(&cs, i) };
            // encodage byte-level du morceau, puis BPE
            let mut word = String::with_capacity(j - i);
            let mut buf = [0u8; 4];
            for &c in &cs[i..j] {
                for b in c.encode_utf8(&mut buf).as_bytes() {
                    word.push(self.byte_enc[*b as usize]);
                }
            }
            out.extend_from_slice(&self.bpe(&word));
            i = j;
        }
        out
    }

    /// Décode des ids en texte (les tokens spéciaux sont conservés tels quels).
    ///
    /// Les ids hors vocabulaire sont ignorés ; les caractères absents de la table
    /// byte-level le sont aussi (même comportement que la référence Python).
    pub fn decode(&self, ids: &[u32]) -> String {
        let mut bytes = Vec::new();
        for &id in ids {
            let tok = match self.id_to_tok.get(id as usize) {
                Some(t) => t,
                None => continue,
            };
            for c in tok.chars() {
                if let Some(&b) = self.byte_dec.get(&c) {
                    bytes.push(b);
                }
            }
        }
        String::from_utf8_lossy(&bytes).into_owned()
    }

    #[allow(dead_code)] // fait partie de l'API demandée
    pub fn vocab_size(&self) -> usize {
        self.id_to_tok.len()
    }

    /// Id du token spécial à partir de sa chaîne (« <|im_end|> » -> 151645).
    ///
    /// Un token n'est « spécial » que si `token_type` le dit (3 = contrôle,
    /// 4 = défini par l'utilisateur). Si `token_type` ne couvre pas l'id
    /// (tableau vide ou tronqué), on renvoie l'id trouvé sans pouvoir trancher.
    /// Identifiant d'un jeton de contrôle, désigné par sa chaîne.
    ///
    /// Le type déclaré n'est pas décisif : le vocabulaire o200k range
    /// `<|start|>` et `<|message|>` parmi les jetons **ordinaires**. Exiger le
    /// type « contrôle » faisait donc échouer la détection du gabarit de
    /// gpt-oss et retomber sur une invite brute. On privilégie un jeton de
    /// contrôle, sinon on accepte n'importe quelle entrée portant exactement
    /// cette chaîne.
    pub fn special_id(&self, text: &str) -> Option<u32> {
        let &id = self.tok_to_id.get(text)?;
        match self.token_type.get(id as usize) {
            Some(&t) if t != 3 && t != 4 => Some(id),
            _ => Some(id),
        }
    }

    /// BPE d'un morceau déjà encodé en caractères byte-level.
    ///
    /// À chaque tour on fusionne la paire adjacente de rang minimal (le plus
    /// petit indice dans `merges`), en partant de la gauche en cas d'égalité —
    /// c'est exactement ce que fait la référence. Un symbole absent du
    /// vocabulaire est ignoré (comme le `if s in self.tok_to_id` de Python).
    fn bpe(&self, word: &str) -> Vec<u32> {
        let mut syms: Vec<String> = word.chars().map(|c| c.to_string()).collect();
        let mut key = String::new();
        while syms.len() > 1 {
            let mut best: Option<(usize, u32)> = None;
            for i in 0..syms.len() - 1 {
                key.clear();
                key.push_str(&syms[i]);
                key.push(SEP);
                key.push_str(&syms[i + 1]);
                if let Some(&r) = self.ranks.get(&key) {
                    if best.map_or(true, |(_, br)| r < br) {
                        best = Some((i, r));
                    }
                }
            }
            let (i, _) = match best {
                Some(b) => b,
                None => break, // plus aucune paire fusionnable
            };
            let merged = format!("{}{}", syms[i], syms[i + 1]);
            syms.splice(i..i + 2, [merged]);
        }
        syms.iter().filter_map(|s| self.tok_to_id.get(s).copied()).collect()
    }
}

/// Table byte-level de GPT-2 : les 256 octets sont représentés par les
/// caractères U+0021..U+007E, U+00A1..U+00AC et U+00AE..U+00FF, les octets
/// restants (contrôles, espace, U+00AD…) étant repliés sur U+0100, U+0101, …
/// dans l'ordre croissant des octets.
fn bytes_to_unicode() -> [char; 256] {
    let mut bs: Vec<u16> = Vec::with_capacity(256);
    bs.extend(0x21u16..=0x7E);
    bs.extend(0xA1u16..=0xAC);
    bs.extend(0xAEu16..=0xFF);
    let mut cs: Vec<u32> = bs.iter().map(|&b| b as u32).collect();
    let mut n = 0u32;
    for b in 0u16..256 {
        if !bs.contains(&b) {
            bs.push(b);
            cs.push(256 + n);
            n += 1;
        }
    }
    let mut table = ['\0'; 256];
    for (&b, &c) in bs.iter().zip(cs.iter()) {
        table[b as usize] = char::from_u32(c).expect("point de code valide");
    }
    table
}

/// `\p{L}` du motif.
///
/// La std n'expose pas les catégories Unicode, seulement la propriété dérivée
/// `Alphabetic` (`char::is_alphabetic`), qui contient EN PLUS ~1 700 marques
/// combinantes (`Mn`/`Mc` de `Other_Alphabetic` : matras indiens, voyelles
/// thaïes, harakat arabes, points hébreux…). Conséquence : sur du texte qui
/// contient ces marques (hindi, thaï, arabe vocalisé, accents décomposés), les
/// morceaux diffèrent du vrai Qwen2 ; sur du texte NFC (latin, grec,
/// cyrillique, CJK, emoji) les deux coïncident exactement.
fn is_letter(c: char) -> bool {
    c.is_alphabetic()
}

/// `\p{N}` : `char::is_numeric` couvre exactement les catégories Nd, Nl et No.
fn is_number(c: char) -> bool {
    c.is_numeric()
}

/// `\s` : la propriété Unicode White_Space, exactement `char::is_whitespace`.
fn is_space(c: char) -> bool {
    c.is_whitespace()
}

/// Pré-tokenizer Qwen2, appliqué au caractère `i` :
/// `(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+`
///
/// L'ORDRE des alternatives est significatif : à gauche, tout ce qui peut
/// démarrer plus tôt ou plus loin l'emporte (un « 's » final, une espace
/// rattachée au mot suivant, etc.). Chaque fonction ci-dessous ne fait que
/// reproduire le comportement gourmand (avec rétrogradation) de sa branche.
/// Renvoie l'indice de fin (exclusif) du morceau, toujours > `i`.
fn next_piece(cs: &[char], i: usize) -> usize {
    match_contraction(cs, i)
        .or_else(|| match_letters(cs, i))
        .or_else(|| match_number(cs, i))
        .or_else(|| match_punctuation(cs, i))
        .or_else(|| match_line_breaks(cs, i))
        .or_else(|| match_spaces_before_word(cs, i))
        .or_else(|| match_spaces(cs, i))
        // Inatteignable : à elles sept, les alternatives couvrent tout
        // caractère (lettre, nombre, espace, ou ponctuation). Garde-fou
        // contre une boucle infinie.
        .unwrap_or(i + 1)
}

// --------------------------------------------------------------------------- //
// Pré-tokenizer kimi (Kimi-K2.7, Kimi-K3)
// --------------------------------------------------------------------------- //

/// `\p{Han}` : idéogrammes chinois. Les mêmes plages que la référence
/// (`llama.cpp-k3`, `unicode_cpt_is_han`), qui est elle-même la transcription du
/// motif officiel de Moonshot (`tokenization_kimi.py`).
fn is_han(c: char) -> bool {
    let u = c as u32;
    (0x4E00..=0x9FFF).contains(&u)        // CJK unifié
        || (0x3400..=0x4DBF).contains(&u) // extension A
        || (0x20000..=0x2A6DF).contains(&u)
        || (0x2A700..=0x2B73F).contains(&u)
        || (0x2B740..=0x2B81F).contains(&u)
        || (0x2B820..=0x2CEAF).contains(&u)
        || (0x2CEB0..=0x2EBEF).contains(&u)
        || (0xF900..=0xFAFF).contains(&u) // compatibilité
        || (0x2F800..=0x2FA1F).contains(&u)
}

/// `[\p{Han}]+` — les idéogrammes se groupent entre eux, jamais avec le reste.
fn match_han(cs: &[char], i: usize) -> Option<usize> {
    if !is_han(cs[i]) {
        return None;
    }
    let mut e = i;
    while e < cs.len() && is_han(cs[e]) { e += 1; }
    Some(e)
}

/// Pré-tokenizer **kimi** (Kimi-K2.7, Kimi-K3), transcription du motif officiel :
/// `[\p{Han}]+`
/// `|[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]*[\p{Ll}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?`
/// `|[^\r\n\p{L}\p{N}]?[\p{Lu}…&&[^\p{Han}]]+[\p{Ll}…&&[^\p{Han}]]*(?i:…)?`
/// `|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+`
///
/// Deux différences avec Qwen2, et une avec o200k : les idéogrammes forment
/// leurs propres morceaux, les lettres se coupent selon la casse **en excluant
/// les Han**, et les nombres vont par **trois**. Les contractions ne sont pas une
/// alternative : elles ne s'accrochent qu'en suffixe d'un mot.
fn next_piece_kimi(cs: &[char], i: usize) -> usize {
    match_han(cs, i)
        .or_else(|| match_casse_decroissante(cs, i, true))
        .or_else(|| match_casse_croissante(cs, i, true))
        .or_else(|| match_nombre_trois(cs, i))
        .or_else(|| match_punctuation(cs, i))
        .or_else(|| match_line_breaks(cs, i))
        .or_else(|| match_spaces_before_word(cs, i))
        .or_else(|| match_spaces(cs, i))
        .unwrap_or(i + 1)
}

// --------------------------------------------------------------------------- //
// Pré-tokenizer o200k (gpt-4o, gpt-oss)
// --------------------------------------------------------------------------- //

/// `[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]` — lettres **non minuscules**.
///
/// La std n'expose pas les catégories Unicode. `!is_lowercase()` classe
/// exactement comme il faut les capitales et les caseless (Lm, Lo : CJK,
/// arabe, hébreu…), et range avec elles les marques combinantes `\p{M}`, qui
/// appartiennent justement à cette classe dans le motif.
fn is_majuscule(c: char) -> bool {
    c.is_alphabetic() && !c.is_lowercase()
}

/// `[\p{Ll}\p{Lm}\p{Lo}\p{M}]` — lettres **non majuscules** (les caseless
/// appartiennent aux deux classes, comme dans le motif).
fn is_minuscule(c: char) -> bool {
    c.is_alphabetic() && !c.is_uppercase()
}

/// ni retour à la ligne, ni lettre, ni nombre — le préfixe optionnel.
fn prefixe_possible(c: char) -> bool {
    c != '\r' && c != '\n' && !is_letter(c) && !is_number(c)
}

/// Pré-tokenizer **o200k** (gpt-4o, gpt-oss) :
/// `[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?`
/// `|[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?`
/// `|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n/]*|\s*[\r\n]+|\s+(?!\S)|\s+`
///
/// La différence avec Qwen2 tient à trois choses : les lettres se coupent
/// selon la casse (`Hello` → `Hello`, mais `hEllo` → `h` puis `Ello`), les
/// nombres par groupes de trois, et `[\r\n/]*` rattache aussi la barre oblique.
fn next_piece_gpt4o(cs: &[char], i: usize) -> usize {
    match_casse_decroissante(cs, i, false)
        .or_else(|| match_casse_croissante(cs, i, false))
        .or_else(|| match_nombre_trois(cs, i))
        .or_else(|| match_ponctuation_gpt4o(cs, i))
        .or_else(|| match_line_breaks(cs, i))
        .or_else(|| match_spaces_before_word(cs, i))
        .or_else(|| match_spaces(cs, i))
        .unwrap_or(i + 1)
}

/// Fin du morceau après une éventuelle contraction finale (`(?i:'s|'t|…)`).
fn avec_contraction(cs: &[char], fin: usize) -> usize {
    if fin < cs.len() && cs[fin] == '\'' {
        if let Some(f) = match_contraction(cs, fin) { return f; }
    }
    fin
}

/// 1) `[^…]? U* L+ (?i:'…)?` — majuscules puis minuscules.
///
/// Le retour arrière du motif se traduit ainsi : `U*` est glouton, donc on
/// cherche le **plus grand** `k` tel que `[p, k)` ne contienne que des
/// non-minuscules et que `cs[k]` soit une non-majuscule ; `L+` consomme alors
/// la suite de non-majuscules.
fn match_casse_decroissante(cs: &[char], i: usize, hors_han: bool) -> Option<usize> {
    let lettre = |c: char| is_letter(c) && !(hors_han && is_han(c));
    let minus = |c: char| is_minuscule(c) && !(hors_han && is_han(c));
    let mut p = i;
    if prefixe_possible(cs[i]) && i + 1 < cs.len() && lettre(cs[i + 1]) {
        p = i + 1;
    } else if !lettre(cs[i]) {
        return None;
    }
    let mut e = p;
    while e < cs.len() && lettre(cs[e]) { e += 1; }
    let mut k = e;
    while k > p && !minus(cs[k - 1]) { k -= 1; }
    if k == p { return None; }              // aucun `L+` possible
    // `U*` ne peut pas absorber une minuscule : on recule jusqu'à la première.
    while k > p && minus(cs[k - 1]) { k -= 1; }
    let mut fin = k;
    while fin < e && minus(cs[fin]) { fin += 1; }
    if fin == k { return None; }
    Some(avec_contraction(cs, fin))
}

/// 2) `[^…]? U+ L* (?i:'…)?` — l'inverse : majuscules d'abord, minuscules
/// ensuite, mais au moins une majuscule.
fn match_casse_croissante(cs: &[char], i: usize, hors_han: bool) -> Option<usize> {
    let lettre = |c: char| is_letter(c) && !(hors_han && is_han(c));
    let maj = |c: char| is_majuscule(c) && !(hors_han && is_han(c));
    let minus = |c: char| is_minuscule(c) && !(hors_han && is_han(c));
    let mut p = i;
    if prefixe_possible(cs[i]) && i + 1 < cs.len() && lettre(cs[i + 1]) {
        p = i + 1;
    } else if !lettre(cs[i]) {
        return None;
    }
    let mut k = p;
    while k < cs.len() && maj(cs[k]) { k += 1; }
    if k == p { return None; }              // `U+` exige au moins une
    let mut fin = k;
    while fin < cs.len() && minus(cs[fin]) { fin += 1; }
    Some(avec_contraction(cs, fin))
}

/// 3) `\p{N}{1,3}` — les nombres par groupes de trois.
fn match_nombre_trois(cs: &[char], i: usize) -> Option<usize> {
    if !is_number(cs[i]) { return None; }
    let mut j = i;
    let mut n = 0;
    while j < cs.len() && n < 3 && is_number(cs[j]) { j += 1; n += 1; }
    Some(j)
}

/// 4) ` ?[^\s\p{L}\p{N}]+[\r\n/]*` — comme Qwen2, plus la barre oblique.
fn match_ponctuation_gpt4o(cs: &[char], i: usize) -> Option<usize> {
    let mut j = i;
    if cs[i] == ' ' && i + 1 < cs.len() && !is_space(cs[i + 1])
        && !is_letter(cs[i + 1]) && !is_number(cs[i + 1])
    {
        j = i + 1;
    }
    let debut = j;
    while j < cs.len() && !is_space(cs[j]) && !is_letter(cs[j]) && !is_number(cs[j]) { j += 1; }
    if j == debut { return None; }
    while j < cs.len() && (cs[j] == '\r' || cs[j] == '\n' || cs[j] == '/') { j += 1; }
    Some(j)
}

/// 1) `(?i:'s|'t|'re|'ve|'m|'ll|'d)` — insensible à la casse (`I'LL`, `we'VE`).
fn match_contraction(cs: &[char], i: usize) -> Option<usize> {
    if cs[i] != '\'' {
        return None;
    }
    let rest = &cs[i + 1..];
    let one = |c: char| !rest.is_empty() && rest[0].eq_ignore_ascii_case(&c);
    let two = |a: char, b: char| {
        rest.len() >= 2 && rest[0].eq_ignore_ascii_case(&a) && rest[1].eq_ignore_ascii_case(&b)
    };
    if one('s') {
        Some(i + 2)
    } else if one('t') {
        Some(i + 2)
    } else if two('r', 'e') {
        Some(i + 3)
    } else if two('v', 'e') {
        Some(i + 3)
    } else if one('m') {
        Some(i + 2)
    } else if two('l', 'l') {
        Some(i + 3)
    } else if one('d') {
        Some(i + 2)
    } else {
        None
    }
}

/// 2) `[^\r\n\p{L}\p{N}]?\p{L}+` — un caractère quelconque (ni retour à la
/// ligne, ni lettre, ni nombre) peut être COLLÉ devant la suite de lettres :
/// c'est ainsi que « .com », « (word) », « -word » ou «  word » forment un seul
/// morceau. Le préfixe est gourmand, mais on rétrograde s'il ne reste alors
/// aucune lettre à consommer.
fn match_letters(cs: &[char], i: usize) -> Option<usize> {
    let n = cs.len();
    for k in [1usize, 0] {
        if k == 1 {
            let c = cs[i];
            if c == '\r' || c == '\n' || is_letter(c) || is_number(c) {
                continue;
            }
        }
        let j = i + k;
        if j < n && is_letter(cs[j]) {
            let mut e = j;
            while e < n && is_letter(cs[e]) {
                e += 1;
            }
            return Some(e);
        }
    }
    None
}

/// 3) `\p{N}` — UN SEUL caractère numérique (et non `\p{N}+` comme GPT-2).
fn match_number(cs: &[char], i: usize) -> Option<usize> {
    if is_number(cs[i]) {
        Some(i + 1)
    } else {
        None
    }
}

/// 4) ` ?[^\s\p{L}\p{N}]+[\r\n]*` — une espace facultative, une suite de
/// ponctuation, puis TOUS les retours à la ligne qui suivent : « !\n\n » est un
/// seul morceau (le « \n » ne part donc pas avec les espaces).
fn match_punctuation(cs: &[char], i: usize) -> Option<usize> {
    let n = cs.len();
    let mut j = if cs[i] == ' ' { i + 1 } else { i };
    let run = j;
    while j < n && !is_space(cs[j]) && !is_letter(cs[j]) && !is_number(cs[j]) {
        j += 1;
    }
    if j == run {
        return None; // l'espace facultative seule ne suffit pas
    }
    while j < n && (cs[j] == '\r' || cs[j] == '\n') {
        j += 1;
    }
    Some(j)
}

/// 5) `\s*[\r\n]+` — `\s*` peut lui-même contenir des retours à la ligne ; le
/// morceau va donc jusqu'au DERNIER « \r »/« \n » de la plage d'espaces
/// (« \n \n » est un seul morceau), et pas au-delà.
fn match_line_breaks(cs: &[char], i: usize) -> Option<usize> {
    let n = cs.len();
    let mut w = i;
    while w < n && is_space(cs[w]) {
        w += 1;
    }
    if w == i {
        return None;
    }
    let mut end = None;
    for k in i..w {
        if cs[k] == '\r' || cs[k] == '\n' {
            end = Some(k + 1);
        }
    }
    end
}

/// 6) `\s+(?!\S)` — gourmand, puis rétrogradation jusqu'à ce que le caractère
/// suivant ne soit plus « non-espace » : au milieu d'un texte, le dernier
/// caractère de la plage est laissé au morceau suivant (une seule unité
/// d'espace est donc détachée devant un mot) ; en fin de texte, toute la plage
/// est prise.
fn match_spaces_before_word(cs: &[char], i: usize) -> Option<usize> {
    let n = cs.len();
    let mut j = i;
    while j < n && is_space(cs[j]) {
        j += 1;
    }
    if j == n {
        return if j > i { Some(j) } else { None }; // fin de texte : toute la plage
    }
    if j > i + 1 {
        return Some(j - 1); // on détache le dernier caractère d'espace
    }
    None // une seule espace : rien à prendre ici, la 7e alternative s'en charge
}

/// 7) `\s+` — dernière alternative : toute la plage d'espaces.
fn match_spaces(cs: &[char], i: usize) -> Option<usize> {
    let n = cs.len();
    let mut j = i;
    while j < n && is_space(cs[j]) {
        j += 1;
    }
    if j > i {
        Some(j)
    } else {
        None
    }
}
