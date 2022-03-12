
use rustler::{
    Env,
    Term,
    Encoder,
    NifResult,
    Atom,
    MapIterator
};

use rayon::prelude::*;
use serde::Deserialize;
use quick_xml::de;

//##########################################################################################################################

mod atoms {
    rustler::atoms! { tags, names, config }
}

//##########################################################################################################################

#[allow(non_snake_case)]
#[derive(Debug, Deserialize, PartialEq)]
struct Signal {
    Name: String,
    DataType: usize,
    Active: bool,
    Unit: Option<String>,
    Comment1: Option<String>,
    Comment2: Option<String>,
    Expression: Option<String>,
    FileSignalId: Option<String>,
    S7Symbol: Option<String>,
    S7Operand: Option<String>,
    S7DataType: Option<String>
}

#[derive(Debug, Deserialize, PartialEq)]
struct SignalList {
    #[serde(rename = "Signal", default)]
    list: Vec<Signal>
}

#[allow(non_snake_case)]
#[derive(Debug, Deserialize, PartialEq)]
struct Link {
    Analog: Option<SignalList>,
    Digital: Option<SignalList>
}

#[derive(Debug, Deserialize, PartialEq)]
struct LinkList {
    #[serde(rename = "Link", default)]
    list: Vec<Link>
}

#[allow(non_snake_case)]
#[derive(Debug, Deserialize, PartialEq)]
struct Module {
    Name: String,
    ModuleType: usize,
    Enabled: bool,
    ModuleNr: usize,
    Links: LinkList,
    FileModuleNr: Option<usize>,
    NrAnalogSignals: Option<usize>,
    NrDigitalSignals: Option<usize>,
    PCCP_Destination: Option<String>,
    CPUName: Option<String>
}

#[derive(Debug, Deserialize, PartialEq)]
struct ModuleList {
    #[serde(rename = "Module", default)]
    list: Vec<Module>
}

#[allow(non_snake_case)]
#[derive(Debug, Deserialize, PartialEq)]
struct Document {
    Modules: ModuleList
}

//##########################################################################################################################

fn map_put_atom<'a, T: Encoder>(
    map: mut Term<'a>,
    atom: &str,
    value: &T
) -> NifResult<Term<'a>> {
    let env = map.get_env();
    let atom = Atom::from_str(env, atom)?;
    Ok(
        Term::map_put(map,
            atom.encode(env),
            value.encode(env)
        )?
    )
}

//##########################################################################################################################

fn map_merge<'a>(
    map: mut Term<'a>,
    origin: Term<'a>
) -> NifResult<Term<'a>> {
    if let Some(iter) = MapIterator::new(origin) {
        for (key, value) in iter {
            map = Term::map_put(map, key, value)?;
        };
    };
    Ok(map)
}

//##########################################################################################################################

impl Signal {
    pub fn to_term<'a>(&self, env: Env<'a>) -> NifResult<Term<'a>> {
        let mut map = Term::map_new(env);
        map = map_put_atom(map, "name", &self.Name)?;
        map = map_put_atom(map, "unit", &self.Unit)?;
        map = map_put_atom(map, "active", &self.Active)?;
        map = map_put_atom(map, "data_type", &self.DataType)?;
        map = map_put_atom(map, "comment_1", &self.Comment1)?;
        map = map_put_atom(map, "comment_2", &self.Comment2)?;
        map = map_put_atom(map, "s7_symbol", &self.S7Symbol)?;
        map = map_put_atom(map, "s7_operand", &self.S7Operand)?;
        map = map_put_atom(map, "expression", &self.Expression)?;
        map = map_put_atom(map, "s7_data_type", &self.S7DataType)?;
        map = map_put_atom(map, "file_signal_id", &self.FileSignalId)?;
        Ok(map)
    }
}

impl Module {
    pub fn to_term<'a>(&self, env: Env<'a>) -> NifResult<Term<'a>> {
        let mut map = Term::map_new(env);
        map = map_put_atom(map, "name", &self.Name)?;
        map = map_put_atom(map, "cpu_name", &self.CPUName)?;
        map = map_put_atom(map, "module_nr", &self.ModuleNr)?;
        map = map_put_atom(map, "file_module_nr", &self.FileModuleNr)?;
        map = map_put_atom(map, "pccp_destination", &self.PCCP_Destination)?;
        map = map_put_atom(map, "nr_analog_signals", &self.NrAnalogSignals)?;
        map = map_put_atom(map, "nr_digital_signals", &self.NrDigitalSignals)?;
        Ok(map)
    }
}

//##########################################################################################################################

// Make Buffer
fn tag_buffer<'a>(
    env: Env<'a>
) -> NifResult<(Term<'a>, Term<'a>)> {
    Ok((
        Term::map_new(env),
        Term::map_new(env)
    ))
}

//##########################################################################################################################

// Map Tags in Link
fn map_tags<'a>(
    env: Env<'a>,
    pfx: &str,
    i: &usize
    signal: &Signal
) -> NifResult<(Term<'a>, Term<'a>)> {
    let mut (tags, names) = tag_buffer(env)?;
    // Apply Signal
    if !signal.Name.trim().is_empty() {
        tags = Term::map_put(tags,
            i.encode(env),
            signal.to_term(env)?
        )?;
        names = Term::map_put(names,
            signal.Name.encode(env),
            format!("{}{}", pfx, i).encode(env)
        )?;
    };
    // Return Data
    Ok((tags, names))
}

//##########################################################################################################################

// Reduce Tags in Link
fn reduce_tags<'a>(
    upstr: (Term<'a>, Term<'a>),
    dnstr: (Term<'a>, Term<'a>)
) -> NifResult<(Term<'a>, Term<'a>)> {
    Ok((
        map_merge(upstr.0, dnstr.0)?,
        map_merge(upstr.1, dnstr.1)?
    ))
}

//##########################################################################################################################

// Get Tags in Link
fn get_tags<'a>(
    env: Env<'a>,
    prefix: (&usize, &str),
    list: &Vec<Signal>
) -> NifResult<(Term<'a>, Term<'a>)> {
    let pfx = format!("{}{}", prefix.0, prefix.1);
    // Iterate over Signals
    let reduced = list.par_iter().enumerate()
        .map(|(i, signal)| map_tags(env, pfx, i, signal)?)
        .reduce(|| tag_buffer(env)?, |u, d| reduce_tags(u, d)?);
    // Return Data
    Ok(reduced)
}

//##########################################################################################################################

// Map Links in Module
fn map_links<'a>(
    env: Env<'a>,
    modnr: &usize,
    link: &Link
) -> NifResult<((Term<'a>, Term<'a>), Term<'a>)> {
    let mut (analogs, digitals) = tag_buffer(env)?;
    let mut names = Term::map_new(env);
    // Apply Link
    if let Some(analog) = link.Analog {
        let (_tags, _names) = get_tags(env,
            (modnr, ":"), &analog.list
       )?;
        analogs = map_merge(analogs, _tags)?;
        names = map_merge(names, _names)?;
    };
    if let Some(digital) = link.Digital {
        let (_tags, _names) = get_tags(env,
            (modnr, "."), &digital.list
        )?;
        digitals = map_merge(digitals, _tags)?;
        names = map_merge(names, _names)?;
    };
    // Return Data
    Ok(((analogs, digitals), names))
}

//##########################################################################################################################

// Reduce Links in Module
fn reduce_links<'a>(
    upstr: ((Term<'a>, Term<'a>), Term<'a>),
    dnstr: ((Term<'a>, Term<'a>), Term<'a>)
) -> NifResult<((Term<'a>, Term<'a>), Term<'a>)> {
    Ok((
        (
            map_merge(upstr.0.0, dnstr.0.0)?,
            map_merge(upstr.0.1, dnstr.0.1)?
        ),
        map_merge(upstr.1, dnstr.1)?
    ))
}

//##########################################################################################################################

// Get Links in Module
fn get_links<'a>(
    env: Env<'a>,
    modnr: &usize,
    list: &Vec<Link>
) -> NifResult<((Term<'a>, Term<'a>), Term<'a>)> {
    let reduced = list.par_iter()
        .map(|link| map_links(env, modnr, link)?)
        .reduce(|| tag_buffer(env)?, |u, d| reduce_links(u, d)?);
    // Return Data
    Ok(reduced)
}

//##########################################################################################################################

#[rustler::nif]
fn parse<'a>(env: Env<'a>, xml: &str) -> NifResult<Term<'a>> {
    // Parse XML
    let doc: Document = de::from_str(xml).unwrap();
    // Set Buffer
    let mut tags = Term::map_new(env);
    let mut names = Term::map_new(env);
    // Iterate over Modules
    for module in doc.Modules.list.iter() {
        // Get Links in Module
        let ((analogs, digitals), _names) = get_links(env,
            &module.ModuleNr, &module.Links.list
        )?;
        // Assembly Module
        let mut _mod = Term::map_new(env);
        _mod = Term::map_put(_mod, 0.encode(env), analogs)?;
        _mod = Term::map_put(_mod, 1.encode(env), digitals)?;
        _mod = Term::map_put(_mod,
            atoms::config().to_term(env),
            module.to_term(env)?
        )?;
        // Assign Names
        names = map_merge(names, _names);
        // Assign Module
        tags = Term::map_put(tags,
            module.ModuleNr.encode(env),
            _mod
        )?;
    };
    // Assembly Data
    let mut io = Term::map_new(env);
    io = Term::map_put(io, atoms::tags().to_term(env), tags)?;
    io = Term::map_put(io, atoms::names().to_term(env), names)?;
    // Return Ok
    Ok(io)
}

//##########################################################################################################################

rustler::init!(
    "Elixir.OpcSx.Iba.IoConfig.Nif",
    [parse]
);

//##########################################################################################################################
