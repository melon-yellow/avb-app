
use rustler::{Env, Term, Encoder, NifResult, Atom};

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
    DataType: u32,
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
    ModuleType: u32,
    Enabled: bool,
    ModuleNr: u32,
    Links: LinkList,
    FileModuleNr: Option<u32>,
    NrAnalogSignals: Option<u32>,
    NrDigitalSignals: Option<u32>,
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
    env: Env<'a>,
    map: Term<'a>,
    atom: &str,
    value: &T
) -> NifResult<Term<'a>> {
    Ok(
        Term::map_put(map,
            Atom::from_str(env, atom)?.encode(env),
            value.encode(env)
        )?
    )
}

//##########################################################################################################################

impl Signal {
    pub fn to_term<'a>(&self, env: Env<'a>) -> NifResult<Term<'a>> {
        let mut map = Term::map_new(env);
        map = map_put_atom(env, map, "name", &self.Name)?;
        map = map_put_atom(env, map, "unit", &self.Unit)?;
        map = map_put_atom(env, map, "active", &self.Active)?;
        map = map_put_atom(env, map, "data_type", &self.DataType)?;
        map = map_put_atom(env, map, "comment_1", &self.Comment1)?;
        map = map_put_atom(env, map, "comment_2", &self.Comment2)?;
        map = map_put_atom(env, map, "s7_symbol", &self.S7Symbol)?;
        map = map_put_atom(env, map, "s7_operand", &self.S7Operand)?;
        map = map_put_atom(env, map, "expression", &self.Expression)?;
        map = map_put_atom(env, map, "s7_data_type", &self.S7DataType)?;
        map = map_put_atom(env, map, "file_signal_id", &self.FileSignalId)?;
        Ok(map)
    }
}

impl Module {
    pub fn to_term<'a>(&self, env: Env<'a>) -> NifResult<Term<'a>> {
        let mut map = Term::map_new(env);
        map = map_put_atom(env, map, "name", &self.Name)?;
        map = map_put_atom(env, map, "cpu_name", &self.CPUName)?;
        map = map_put_atom(env, map, "module_nr", &self.ModuleNr)?;
        map = map_put_atom(env, map, "file_module_nr", &self.FileModuleNr)?;
        map = map_put_atom(env, map, "pccp_destination", &self.PCCP_Destination)?;
        map = map_put_atom(env, map, "nr_analog_signals", &self.NrAnalogSignals)?;
        map = map_put_atom(env, map, "nr_digital_signals", &self.NrDigitalSignals)?;
        Ok(map)
    }
}

//##########################################################################################################################

// Get Tags From Signal-List
fn get_tags<'a>(
    env: Env<'a>,
    prefix: (u32, &str),
    list: &Vec<Signal>,
    buffer: (Term<'a>, Term<'a>)
) -> NifResult<(Term<'a>, Term<'a>)> {
    // Set Buffer
    let mut _kind = buffer.0;
    let mut _names = buffer.1;
    // Iterate over Tags
    for (i, signal) in list.iter().enumerate() {
        if !signal.Name.trim().is_empty() {
            _kind = Term::map_put(_kind,
                i.encode(env),
                signal.to_term(env)?
            )?;
            _names = Term::map_put(_names,
                signal.Name.encode(env),
                format!("{}{}{}", prefix.0, prefix.1, i).encode(env)
            )?;
        };
    };
    // Return Ok
    Ok((_kind, _names))
}

//##########################################################################################################################

#[rustler::nif]
fn parse<'a>(env: Env<'a>, xml: &str) -> NifResult<Term<'a>> {
    // Parse XML
    let doc: Document = de::from_str(xml.trim()).unwrap();
    // Set Buffer
    let mut tags = Term::map_new(env);
    let mut names = Term::map_new(env);
    // Iterate over Modules
    for module in doc.Modules.list.iter() {
        // Set Buffer
        let mut analogs = Term::map_new(env);
        let mut digitals = Term::map_new(env);
        // Iterate over Links
        for link in module.Links.list.iter() {
            if let Some(analog) = &link.Analog {
                let (_analogs, _names) = get_tags(
                    env,
                    (module.ModuleNr, ":"),
                    &analog.list,
                    (analogs, names)
                )?;
                analogs = _analogs;
                names = _names;
            };
            if let Some(digital) = &link.Digital {
                let (_digitals, _names) = get_tags(
                    env,
                    (module.ModuleNr, "."),
                    &digital.list,
                    (digitals, names)
                )?;
                digitals = _digitals;
                names = _names;
            };
        };
        // Set Module Info
        let mut _mod = Term::map_new(env);
        _mod = Term::map_put(_mod, 0.encode(env), analogs)?;
        _mod = Term::map_put(_mod, 1.encode(env), digitals)?;
        _mod = Term::map_put(_mod,
            atoms::config().to_term(env),
            module.to_term(env)?
        )?;
        // Index Module
        tags = Term::map_put(tags,
            (module.ModuleNr).encode(env),
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
