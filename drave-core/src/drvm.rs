//! DRVM v0 — lecteur du conteneur natif de modèle Drave.
//!
//! Ce n'est pas un GGUF amélioré : le manifeste porte un **graphe** (blocs,
//! ports, routes, têtes, pont) et le payload porte des tenseurs alignés par
//! bloc. Le lecteur refuse une version, un type de bloc ou une section qu'il ne
//! connaît pas ; il n'exécute jamais un fichier à moitié compris.
//!
//! Le crate reste **std seul** : le JSON minimal est analysé à la main.

use std::collections::BTreeSet;
use std::fs;
use std::path::Path;

pub const MAGIC: &[u8; 4] = b"DRVM";
pub const VERSION: u16 = 0;
pub const HEADER_SIZE: usize = 92;
pub const ALIGNEMENT: usize = 64;
pub const BLOCS_CONNUS: &[&str] = &[
    "input", "local_mixer", "sparse_ffn", "state", "early_head",
    "thought", "bridge", "output",
];

#[derive(Debug, Clone)]
pub enum Json {
    Null,
    Bool(bool),
    Nombre(f64),
    Chaine(String),
    Tableau(Vec<Json>),
    Objet(Vec<(String, Json)>),
}

impl Json {
    pub fn get(&self, cle: &str) -> Option<&Json> {
        match self {
            Json::Objet(v) => v.iter().find(|(k, _)| k == cle).map(|(_, v)| v),
            _ => None,
        }
    }
    pub fn as_str(&self) -> Option<&str> {
        if let Json::Chaine(s) = self { Some(s) } else { None }
    }
    pub fn as_u64(&self) -> Option<u64> {
        if let Json::Nombre(n) = self { Some(*n as u64) } else { None }
    }
    pub fn as_f64(&self) -> Option<f64> {
        if let Json::Nombre(n) = self { Some(*n) } else { None }
    }
    pub fn as_array(&self) -> Option<&[Json]> {
        if let Json::Tableau(v) = self { Some(v) } else { None }
    }
}

/// Les clés sont des listes FERMÉES : une clé inconnue est refusée, jamais
/// ignorée. C'est la règle déjà appliquée à `kind` (`docs/theorie/modele-natif.md`) :
/// un manifeste à moitié compris qui s'exécute est un manifeste qui ment. Avant
/// le 17/11, le lecteur DÉCLARAIT `routes`, `regions`, `heads`, `thought`,
/// `bridge` dans son en-tête et les IGNORAIT en silence.
const CLES_RACINE: &[&str] = &["format", "version", "model", "graph", "tensors", "execution"];
const CLES_GRAPHE: &[&str] = &["blocks", "regions", "routes", "heads", "thought", "bridge"];
const CLES_BLOC: &[&str] = &["id", "kind", "inputs", "outputs"];
const CLES_EXECUTION: &[&str] = &["activation", "placement", "cache", "replay", "import"];
const CLES_THOUGHT: &[&str] = &["steps"];
const CLES_REGION: &[&str] = &["id", "blocks"];

fn cles_fermees(ou: &str, obj: &Json, connues: &[&str]) -> Result<(), ErreurDrvm> {
    match obj {
        Json::Objet(v) => {
            let inconnues: Vec<&str> = v.iter().map(|(k, _)| k.as_str())
                .filter(|k| !connues.contains(k)).collect();
            if inconnues.is_empty() { Ok(()) } else {
                Err(ErreurDrvm(format!("clé inconnue dans {ou} : {}", inconnues.join(", "))))
            }
        }
        _ => Err(ErreurDrvm(format!("{ou} n'est pas un objet"))),
    }
}

fn verifie_racine(m: &Json) -> Result<(), ErreurDrvm> {
    cles_fermees("le manifeste", m, CLES_RACINE)?;
    for s in CLES_RACINE {
        if m.get(s).is_none() {
            return Err(ErreurDrvm(format!("section absente : {s}")));
        }
    }
    if m.get("format").and_then(Json::as_str) != Some("DRVM") {
        return Err(ErreurDrvm("format != DRVM".into()));
    }
    if m.get("version").and_then(Json::as_u64) != Some(VERSION as u64) {
        return Err(ErreurDrvm("version du manifeste non supportée".into()));
    }
    if m.get("model").and_then(|x| x.get("name")).and_then(Json::as_str).is_none() {
        return Err(ErreurDrvm("model.name absent".into()));
    }
    Ok(())
}

/// Vérifie les sections descriptives du graphe : régions, têtes, pensée, pont et
/// routes. Elles sont **croisées** avec les blocs : une région, une tête ou un
/// pont qui nomme un bloc absent est refusé. Une route non vide est refusée
/// **parce que le moteur ne sait pas l'exécuter** — l'implémenter, pas l'ignorer,
/// est la prochaine étape.
fn verifie_graphe(g: &Json, ids: &BTreeSet<String>) -> Result<(), ErreurDrvm> {
    let regions = g.get("regions").and_then(Json::as_array)
        .ok_or_else(|| ErreurDrvm("graph.regions doit être une liste".into()))?;
    let mut vues = BTreeSet::new();
    for r in regions {
        cles_fermees("une région", r, CLES_REGION)?;
        let rid = r.get("id").and_then(Json::as_str)
            .ok_or_else(|| ErreurDrvm("région sans id".into()))?;
        if !vues.insert(rid.to_string()) {
            return Err(ErreurDrvm(format!("région dupliquée : {rid}")));
        }
        let bl = r.get("blocks").and_then(Json::as_array)
            .ok_or_else(|| ErreurDrvm(format!("région sans blocs : {rid}")))?;
        for x in bl {
            let s = x.as_str().ok_or_else(|| ErreurDrvm(format!("bloc non typé dans la région {rid}")))?;
            if !ids.contains(s) {
                return Err(ErreurDrvm(format!("région vers un bloc inconnu : {s}")));
            }
        }
    }
    let heads = g.get("heads").and_then(Json::as_array)
        .ok_or_else(|| ErreurDrvm("graph.heads doit être une liste".into()))?;
    for h in heads {
        let s = h.as_str().ok_or_else(|| ErreurDrvm("tête non typée".into()))?;
        if !ids.contains(s) {
            return Err(ErreurDrvm(format!("tête vers un bloc inconnu : {s}")));
        }
    }
    if let Some(th) = g.get("thought") {
        if !matches!(th, Json::Null) {
            cles_fermees("thought", th, CLES_THOUGHT)?;
            let pas = th.get("steps").and_then(Json::as_f64)
                .ok_or_else(|| ErreurDrvm("clé absente : thought.steps".into()))?;
            if pas < 0.0 || pas.fract() != 0.0 {
                return Err(ErreurDrvm(format!("thought.steps invalide : {pas}")));
            }
        }
    }
    if let Some(br) = g.get("bridge") {
        if !matches!(br, Json::Null) {
            let s = br.as_str().ok_or_else(|| ErreurDrvm("pont non typé".into()))?;
            if !ids.contains(s) {
                return Err(ErreurDrvm(format!("pont vers un bloc inconnu : {s}")));
            }
        }
    }
    let routes = g.get("routes").and_then(Json::as_array)
        .ok_or_else(|| ErreurDrvm("graph.routes doit être une liste".into()))?;
    if !routes.is_empty() {
        return Err(ErreurDrvm(format!(
            "routes non exécutées : {} route(s) — le lecteur refuse ce qu'il ne sait pas exécuter",
            routes.len())));
    }
    Ok(())
}

fn verifie_execution(m: &Json) -> Result<(), ErreurDrvm> {
    let ex = m.get("execution").ok_or_else(|| ErreurDrvm("section execution absente".into()))?;
    cles_fermees("execution", ex, CLES_EXECUTION)?;
    for c in ["activation", "placement"] {
        if ex.get(c).and_then(Json::as_str).is_none() {
            return Err(ErreurDrvm(format!("execution.{c} absent")));
        }
    }
    for c in ["cache", "replay", "import"] {
        if let Some(v) = ex.get(c) {
            if !matches!(v, Json::Objet(_)) {
                return Err(ErreurDrvm(format!("execution.{c} doit être un objet")));
            }
        }
    }
    Ok(())
}

#[derive(Debug, Clone)]
pub struct Bloc {
    pub id: String,
    pub kind: String,
}

#[derive(Debug, Clone)]
pub struct Tenseur {
    pub name: String,
    pub bloc: String,
    pub offset: u64,
    pub nbytes: u64,
    pub dtype: String,
    pub shape: Vec<u64>,
}

#[derive(Debug, Clone)]
pub struct Drvm {
    pub manifeste: Json,
    pub blocs: Vec<Bloc>,
    pub tenseurs: Vec<Tenseur>,
    payload_offset: usize,
    data: Vec<u8>,
}

#[derive(Debug)]
pub struct ErreurDrvm(pub String);

impl std::fmt::Display for ErreurDrvm {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "DRVM invalide : {}", self.0)
    }
}

fn u16le(b: &[u8], o: usize) -> u16 {
    u16::from_le_bytes(b[o..o + 2].try_into().unwrap())
}
fn u32le(b: &[u8], o: usize) -> u32 {
    u32::from_le_bytes(b[o..o + 4].try_into().unwrap())
}
fn u64le(b: &[u8], o: usize) -> u64 {
    u64::from_le_bytes(b[o..o + 8].try_into().unwrap())
}

struct P<'a> { b: &'a [u8], i: usize }

impl<'a> P<'a> {
    fn ws(&mut self) {
        while self.i < self.b.len() && matches!(self.b[self.i], b' ' | b'\n' | b'\r' | b'\t') {
            self.i += 1;
        }
    }
    fn attend(&mut self, c: u8) -> Result<(), ErreurDrvm> {
        self.ws();
        if self.i < self.b.len() && self.b[self.i] == c {
            self.i += 1; Ok(())
        } else {
            Err(ErreurDrvm(format!("attendu '{}' à {}", c as char, self.i)))
        }
    }
    fn valeur(&mut self) -> Result<Json, ErreurDrvm> {
        self.ws();
        if self.i >= self.b.len() { return Err(ErreurDrvm("JSON tronqué".into())); }
        match self.b[self.i] {
            b'{' => {
                self.i += 1; let mut v = Vec::new();
                self.ws();
                if self.i < self.b.len() && self.b[self.i] == b'}' { self.i += 1; return Ok(Json::Objet(v)); }
                loop {
                    let k = self.chaine()?;
                    self.attend(b':')?;
                    let val = self.valeur()?;
                    v.push((k, val));
                    self.ws();
                    if self.i < self.b.len() && self.b[self.i] == b',' { self.i += 1; continue; }
                    self.attend(b'}')?; break;
                }
                Ok(Json::Objet(v))
            }
            b'[' => {
                self.i += 1; let mut v = Vec::new();
                self.ws();
                if self.i < self.b.len() && self.b[self.i] == b']' { self.i += 1; return Ok(Json::Tableau(v)); }
                loop {
                    v.push(self.valeur()?);
                    self.ws();
                    if self.i < self.b.len() && self.b[self.i] == b',' { self.i += 1; continue; }
                    self.attend(b']')?; break;
                }
                Ok(Json::Tableau(v))
            }
            b'"' => Ok(Json::Chaine(self.chaine()?)),
            b't' => { self.mot("true")?; Ok(Json::Bool(true)) }
            b'f' => { self.mot("false")?; Ok(Json::Bool(false)) }
            b'n' => { self.mot("null")?; Ok(Json::Null) }
            _ => self.nombre(),
        }
    }
    fn mot(&mut self, m: &str) -> Result<(), ErreurDrvm> {
        if self.b[self.i..].starts_with(m.as_bytes()) { self.i += m.len(); Ok(()) }
        else { Err(ErreurDrvm(format!("attendu {m} à {}", self.i))) }
    }
    fn chaine(&mut self) -> Result<String, ErreurDrvm> {
        self.ws();
        if self.i >= self.b.len() || self.b[self.i] != b'"' { return Err(ErreurDrvm("chaîne attendue".into())); }
        self.i += 1; let mut out = String::new();
        while self.i < self.b.len() {
            let c = self.b[self.i]; self.i += 1;
            match c {
                b'"' => return Ok(out),
                b'\\' => {
                    if self.i >= self.b.len() { break; }
                    let e = self.b[self.i]; self.i += 1;
                    match e {
                        b'"' => out.push('"'), b'\\' => out.push('\\'),
                        b'/' => out.push('/'), b'b' => out.push('\u{8}'),
                        b'f' => out.push('\u{c}'), b'n' => out.push('\n'),
                        b'r' => out.push('\r'), b't' => out.push('\t'),
                        b'u' => {
                            if self.i + 4 > self.b.len() { return Err(ErreurDrvm("\\u tronqué".into())); }
                            let h = std::str::from_utf8(&self.b[self.i..self.i + 4])
                                .map_err(|_| ErreurDrvm("\\u invalide".into()))?;
                            let n = u32::from_str_radix(h, 16).map_err(|_| ErreurDrvm("\\u invalide".into()))?;
                            out.push(char::from_u32(n).unwrap_or('\u{fffd}'));
                            self.i += 4;
                        }
                        _ => return Err(ErreurDrvm("échappement JSON inconnu".into())),
                    }
                }
                _ => {
                    let start = self.i - 1;
                    let len = std::str::from_utf8(&self.b[start..]).map(|s| s.chars().next().map(|c| c.len_utf8()).unwrap_or(1)).unwrap_or(1);
                    let s = std::str::from_utf8(&self.b[start..start + len])
                        .map_err(|_| ErreurDrvm("UTF-8 invalide".into()))?;
                    out.push_str(s); self.i = start + len;
                }
            }
        }
        Err(ErreurDrvm("chaîne non terminée".into()))
    }
    fn nombre(&mut self) -> Result<Json, ErreurDrvm> {
        let start = self.i;
        if self.i < self.b.len() && (self.b[self.i] == b'-' || self.b[self.i] == b'+') { self.i += 1; }
        while self.i < self.b.len() && matches!(self.b[self.i], b'0'..=b'9' | b'.' | b'e' | b'E' | b'-' | b'+') { self.i += 1; }
        let s = std::str::from_utf8(&self.b[start..self.i]).map_err(|_| ErreurDrvm("nombre invalide".into()))?;
        let n = s.parse::<f64>().map_err(|_| ErreurDrvm(format!("nombre invalide : {s}")))?;
        Ok(Json::Nombre(n))
    }
}

fn parse_json(b: &[u8]) -> Result<Json, ErreurDrvm> {
    let mut p = P { b, i: 0 };
    let v = p.valeur()?;
    p.ws();
    if p.i != b.len() { return Err(ErreurDrvm("octets après le JSON".into())); }
    Ok(v)
}

impl Drvm {
    pub fn open<P: AsRef<Path>>(path: P) -> Result<Self, ErreurDrvm> {
        let b = fs::read(path).map_err(|e| ErreurDrvm(format!("lecture : {e}")))?;
        if b.len() < HEADER_SIZE { return Err(ErreurDrvm("fichier trop court".into())); }
        if &b[0..4] != MAGIC { return Err(ErreurDrvm("mauvaise magie".into())); }
        let version = u16le(&b, 4);
        if version != VERSION { return Err(ErreurDrvm(format!("version non supportée : {version}"))); }
        let hsize = u16le(&b, 6) as usize;
        let mlen = u32le(&b, 8) as usize;
        let poff = u64le(&b, 12) as usize;
        let total = u64le(&b, 20) as usize;
        if hsize != HEADER_SIZE || poff < hsize + mlen || total != b.len() {
            return Err(ErreurDrvm("en-tête incohérent".into()));
        }
        if poff > b.len() { return Err(ErreurDrvm("payload hors fichier".into())); }
        let manifeste = parse_json(&b[hsize..hsize + mlen])?;
        verifie_racine(&manifeste)?;
        let mut blocs = Vec::new();
        let graph = manifeste.get("graph").ok_or_else(|| ErreurDrvm("section graph absente".into()))?;
        cles_fermees("graph", graph, CLES_GRAPHE)?;
        for cle in CLES_GRAPHE {
            if graph.get(cle).is_none() {
                return Err(ErreurDrvm(format!("clé absente : graph.{cle}")));
            }
        }
        let arr = graph.get("blocks").and_then(Json::as_array)
            .ok_or_else(|| ErreurDrvm("graph.blocks absent".into()))?;
        let mut ids = BTreeSet::new();
        for x in arr {
            cles_fermees("un bloc", x, CLES_BLOC)?;
            let id = x.get("id").and_then(Json::as_str).ok_or_else(|| ErreurDrvm("bloc sans id".into()))?;
            let kind = x.get("kind").and_then(Json::as_str).ok_or_else(|| ErreurDrvm("bloc sans kind".into()))?;
            if !ids.insert(id.to_string()) { return Err(ErreurDrvm(format!("bloc dupliqué : {id}"))); }
            if !BLOCS_CONNUS.contains(&kind) {
                return Err(ErreurDrvm(format!("type de bloc inconnu : {kind}")));
            }
            for port in ["inputs", "outputs"] {
                let p = x.get(port).and_then(Json::as_array)
                    .ok_or_else(|| ErreurDrvm(format!("clé absente : bloc.{port}")))?;
                if p.iter().any(|v| v.as_str().is_none()) {
                    return Err(ErreurDrvm(format!("{port} non typés : {id}")));
                }
            }
            blocs.push(Bloc { id: id.to_string(), kind: kind.to_string() });
        }
        if blocs.is_empty() { return Err(ErreurDrvm("graphe sans bloc".into())); }
        verifie_graphe(graph, &ids)?;
        verifie_execution(&manifeste)?;
        let mut tenseurs = Vec::new();
        let arr = manifeste.get("tensors").and_then(Json::as_array)
            .ok_or_else(|| ErreurDrvm("section tensors absente".into()))?;
        for x in arr {
            let name = x.get("name").and_then(Json::as_str).ok_or_else(|| ErreurDrvm("tenseur sans nom".into()))?;
            let bloc = x.get("bloc").and_then(Json::as_str).ok_or_else(|| ErreurDrvm("tenseur sans bloc".into()))?;
            let offset = x.get("offset").and_then(Json::as_u64).ok_or_else(|| ErreurDrvm("tenseur sans offset".into()))?;
            let nbytes = x.get("nbytes").and_then(Json::as_u64).ok_or_else(|| ErreurDrvm("tenseur sans nbytes".into()))?;
            let dtype = x.get("dtype").and_then(Json::as_str).unwrap_or("f32");
            let shape: Vec<u64> = x.get("shape").and_then(Json::as_array)
                .map(|a| a.iter().filter_map(Json::as_u64).collect()).unwrap_or_default();
            if !ids.contains(bloc) { return Err(ErreurDrvm(format!("bloc inconnu pour {name}"))); }
            if nbytes == 0 || offset % ALIGNEMENT as u64 != 0 {
                return Err(ErreurDrvm(format!("tenseur mal aligné : {name}")));
            }
            if poff + offset as usize + nbytes as usize > b.len() {
                return Err(ErreurDrvm(format!("tenseur hors payload : {name}")));
            }
            tenseurs.push(Tenseur { name: name.to_string(), bloc: bloc.to_string(),
                                    offset, nbytes, dtype: dtype.to_string(), shape });
        }
        Ok(Drvm { manifeste, blocs, tenseurs, payload_offset: poff, data: b })
    }

    pub fn bloc(&self, id: &str) -> Option<&Bloc> { self.blocs.iter().find(|b| b.id == id) }

    pub fn tenseur(&self, name: &str) -> Option<&[u8]> {
        let t = self.tenseurs.iter().find(|t| t.name == name)?;
        let a = self.payload_offset + t.offset as usize;
        Some(&self.data[a..a + t.nbytes as usize])
    }

    pub fn resume(&self) -> String {
        format!("DRVM v{} · {} blocs · {} tenseurs · payload {} o",
                VERSION, self.blocs.len(), self.tenseurs.len(),
                self.data.len() - self.payload_offset)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn graphe_valide(bloc: &str) -> String {
        format!(
            r#"{{"blocks":[{{"id":"b0","kind":"{bloc}","inputs":[],"outputs":[]}}],"regions":[{{"id":"r0","blocks":["b0"]}}],"routes":[],"heads":[],"thought":null,"bridge":null}}"#
        )
    }

    fn manifeste_graphe(graphe: &str) -> String {
        format!(
            r#"{{"format":"DRVM","version":0,"model":{{"name":"t"}},"graph":{graphe},"tensors":[{{"name":"b0.w","bloc":"b0","dtype":"f32","shape":[1],"offset":0,"nbytes":4,"quant":null,"sparsity":0.0}}],"execution":{{"activation":"DRVF","placement":"local"}}}}"#
        )
    }

    fn entete(version: u16, manifeste: &str) -> Vec<u8> {
        let mlen = manifeste.len();
        let mut m = manifeste.as_bytes().to_vec();
        while m.len() % ALIGNEMENT != 0 { m.push(0); }
        let poff = HEADER_SIZE + m.len();
        let mut b = vec![0u8; HEADER_SIZE];
        b[0..4].copy_from_slice(MAGIC);
        b[4..6].copy_from_slice(&version.to_le_bytes());
        b[6..8].copy_from_slice(&(HEADER_SIZE as u16).to_le_bytes());
        b[8..12].copy_from_slice(&(mlen as u32).to_le_bytes());
        b[12..20].copy_from_slice(&(poff as u64).to_le_bytes());
        b[20..28].copy_from_slice(&((poff + 4) as u64).to_le_bytes());
        b.extend(m); b.extend([1u8, 2, 3, 4]);
        b
    }

    fn fichier(version: u16, bloc: &str) -> Vec<u8> {
        entete(version, &manifeste_graphe(&graphe_valide(bloc)))
    }

    /// Refuse un manifeste et vérifie que l'erreur **nomme** la cause — un refus
    /// muet ne vaut pas mieux qu'un silence.
    fn refuse(nom: &str, manifeste: &str, attendu: &str) {
        let d = std::env::temp_dir().join(format!("drave_drvm_refus_{nom}.bin"));
        std::fs::write(&d, entete(VERSION, manifeste)).unwrap();
        let e = match Drvm::open(&d) {
            Err(e) => e.to_string(),
            Ok(_) => panic!("{nom} : le lecteur a accepté ce qu'il n'exécute pas"),
        };
        assert!(e.contains(attendu), "{nom} : « {e} » ne nomme pas « {attendu} »");
        let _ = std::fs::remove_file(&d);
    }

    #[test]
    fn lit_et_refuse() {
        let d = std::env::temp_dir().join("drave_drvm_test.bin");
        std::fs::write(&d, fichier(VERSION, "input")).unwrap();
        let m = Drvm::open(&d).unwrap();
        assert_eq!(m.tenseur("b0.w"), Some(&[1, 2, 3, 4][..]));
        assert!(m.bloc("b0").is_some());
        std::fs::write(&d, fichier(99, "input")).unwrap();
        assert!(Drvm::open(&d).is_err());
        std::fs::write(&d, fichier(VERSION, "quantum")).unwrap();
        assert!(Drvm::open(&d).is_err());
        std::fs::write(&d, &fichier(VERSION, "input")[..40]).unwrap();
        assert!(Drvm::open(&d).is_err());
        let _ = std::fs::remove_file(&d);
    }

    /// Le contrôle négatif du contrat : tout ce que le lecteur ne sait pas
    /// exécuter est refusé, et le refus nomme la clé, la route ou le bloc.
    #[test]
    fn refuse_ce_quil_ne_lit_pas() {
        let g = graphe_valide("input");
        let m = manifeste_graphe(&g);
        refuse("route", &manifeste_graphe(&g.replace(
            r#""routes":[]"#,
            r#""routes":[{"id":"r1","de":"b0","vers":"b0"}]"#)), "routes non exécutées");
        refuse("cle_graphe", &manifeste_graphe(&g.replace(
            r#""bridge":null"#,
            r#""bridge":null,"quota":1"#)), "clé inconnue dans graph : quota");
        refuse("cle_bloc", &manifeste_graphe(&g.replace(
            r#""inputs":[]"#,
            r#""inputs":[],"poids":1"#)), "clé inconnue dans un bloc : poids");
        refuse("region", &manifeste_graphe(&g.replace(
            r#""blocks":["b0"]}"#,
            r#""blocks":["b1"]}"#)), "région vers un bloc inconnu : b1");
        refuse("tete", &manifeste_graphe(&g.replace(
            r#""heads":[]"#,
            r#""heads":["b1"]"#)), "tête vers un bloc inconnu : b1");
        refuse("pont", &manifeste_graphe(&g.replace(
            r#""bridge":null"#,
            r#""bridge":"b1""#)), "pont vers un bloc inconnu : b1");
        refuse("pensee", &manifeste_graphe(&g.replace(
            r#""thought":null"#,
            r#""thought":{"steps":-1}"#)), "thought.steps invalide");
        refuse("pensee_absente", &manifeste_graphe(&g.replace(
            r#","thought":null"#, "")), "clé absente : graph.thought");
        refuse("execution", &m.replace(
            r#""placement":"local""#,
            r#""placement":"local","regime":"eager""#), "clé inconnue dans execution : regime");
        refuse("racine", &m.replace(
            r#""format":"DRVM""#,
            r#""format":"DRVM","extra":1"#), "clé inconnue dans le manifeste : extra");
    }
}

impl Drvm {
    /// Reconstruit un GGUF complet **en mémoire** à partir du DRVM.
    /// Aucun fichier temporaire : `Gguf::depuis_octets` le lit directement.
    pub fn en_gguf(&self) -> Result<Vec<u8>, ErreurDrvm> {
        let kv = self.tenseur("__gguf_kv")
            .ok_or_else(|| ErreurDrvm("tenseur __gguf_kv absent".into()))?;
        let imp = self.manifeste.get("execution").and_then(|e| e.get("import"))
            .ok_or_else(|| ErreurDrvm("execution.import absent".into()))?;
        let version = imp.get("version").and_then(Json::as_u64).unwrap_or(3) as u32;
        let n_kv = imp.get("n_kv").and_then(Json::as_u64)
            .ok_or_else(|| ErreurDrvm("import.n_kv absent : régénérer le DRVM".into()))?;
        let align = imp.get("alignement").and_then(Json::as_u64).unwrap_or(32) as usize;
        let tensors: Vec<&Tenseur> = self.tenseurs.iter()
            .filter(|t| t.name != "__gguf_kv").collect();
        let mut out: Vec<u8> = Vec::new();
        out.extend_from_slice(b"GGUF");
        out.extend_from_slice(&version.to_le_bytes());
        out.extend_from_slice(&(tensors.len() as u64).to_le_bytes());
        out.extend_from_slice(&n_kv.to_le_bytes());
        out.extend_from_slice(kv);
        for t in &tensors {
            let nom = t.name.as_bytes();
            out.extend_from_slice(&(nom.len() as u64).to_le_bytes());
            out.extend_from_slice(nom);
            let shape = self.manifeste.get("tensors").and_then(Json::as_array)
                .and_then(|a| a.iter().find(|x| x.get("name").and_then(Json::as_str) == Some(t.name.as_str())))
                .and_then(|x| x.get("shape")).and_then(Json::as_array)
                .ok_or_else(|| ErreurDrvm(format!("shape absente : {}", t.name)))?;
            out.extend_from_slice(&(shape.len() as u32).to_le_bytes());
            for d in shape.iter().rev() {
                out.extend_from_slice(&d.as_u64().unwrap_or(0).to_le_bytes());
            }
            let ttype: u32 = t.dtype.trim_start_matches("gguf_").parse()
                .map_err(|_| ErreurDrvm(format!("type GGUF illisible : {}", t.dtype)))?;
            out.extend_from_slice(&ttype.to_le_bytes());
            out.extend_from_slice(&t.offset.to_le_bytes());
        }
        while out.len() % align != 0 { out.push(0); }
        let data_start = out.len();
        let total = self.tenseurs.iter().filter(|t| t.name != "__gguf_kv")
            .map(|t| t.offset as usize + t.nbytes as usize).max().unwrap_or(0);
        out.resize(data_start + total, 0);
        for t in &tensors {
            let src = self.tenseur(&t.name).ok_or_else(|| ErreurDrvm(format!("tenseur absent : {}", t.name)))?;
            let a = data_start + t.offset as usize;
            out[a..a + src.len()].copy_from_slice(src);
        }
        Ok(out)
    }
}
