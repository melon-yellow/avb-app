
use rustler::{Env, Term, Encoder, NifResult, Atom};

use serde::Deserialize;
use quick_xml::de;

//##########################################################################################################################

mod atoms {
    rustler::atoms! { tags, modules, names }
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
    FileModuleNr: Option<u16>,
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
        Term::map_put(
            map,
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
        map = map_put_atom(env, map, "data_type", &self.DataType)?;
        map = map_put_atom(env, map, "active", &self.Active)?;
        map = map_put_atom(env, map, "unit", &self.Unit)?;
        map = map_put_atom(env, map, "comment_1", &self.Comment1)?;
        map = map_put_atom(env, map, "comment_2", &self.Comment2)?;
        map = map_put_atom(env, map, "expression", &self.Expression)?;
        map = map_put_atom(env, map, "file_signal_id", &self.FileSignalId)?;
        map = map_put_atom(env, map, "s7_symbol", &self.S7Symbol)?;
        map = map_put_atom(env, map, "s7_operand", &self.S7Operand)?;
        map = map_put_atom(env, map, "s7_data_type", &self.S7DataType)?;
        Ok(map)
    }
}

impl Module {
    pub fn to_term<'a>(&self, env: Env<'a>) -> NifResult<Term<'a>> {
        let mut map = Term::map_new(env);
        map = map_put_atom(env, map, "name", &self.Name)?;
        map = map_put_atom(env, map, "module_nr", &self.ModuleNr)?;
        map = map_put_atom(env, map, "file_module_nr", &self.FileModuleNr)?;
        map = map_put_atom(env, map, "nr_analog_signals", &self.NrAnalogSignals)?;
        map = map_put_atom(env, map, "nr_digital_signals", &self.NrDigitalSignals)?;
        map = map_put_atom(env, map, "pccp_destination", &self.PCCP_Destination)?;
        map = map_put_atom(env, map, "cpu_name", &self.CPUName)?;
        Ok(map)
    }
}

//##########################################################################################################################

fn get_tags<'a>(
    env: Env<'a>,
    mod_nr: u32,
    sep: &str,
    list: &Vec<Signal>,
    names: Term<'a>
) -> NifResult<(Term<'a>, Term<'a>)> {
    // Index Kind
    let mut unames = names;
    let mut kind = Term::map_new(env);
    // Iterate over Tags
    for (i, signal) in list.iter().enumerate() {
        if !signal.Name.trim().is_empty() {
            kind = Term::map_put(kind,
                i.encode(env),
                signal.to_term(env)?
            )?;
            unames = Term::map_put(unames,
                signal.Name.encode(env),
                format!("{}{}{}", mod_nr, sep, i).encode(env)
            )?;
        }
    };
    Ok((kind, unames))
}

#[rustler::nif]
fn parse<'a>(env: Env<'a>, xml: &str) -> NifResult<Term<'a>> {
    // Set Variables
    let mut io = Term::map_new(env);
    let mut tags = Term::map_new(env);
    let mut names = Term::map_new(env);
    let mut modules = Term::map_new(env);
    // Parse XML
    let doc: Document = de::from_str(xml.trim()).unwrap();
    // Iterate over Modules
    for module in doc.Modules.list.iter() {
        // Add module Info
        modules = Term::map_put(modules,
            (module.ModuleNr).encode(env),
            module.to_term(env)?
        )?;
        // Index Module
        let mut tmod = Term::map_new(env);
        // Iterate over Links
        for link in module.Links.list.iter() {
            if let Some(analog) = &link.Analog {
                let (unames, kind) = get_tags(env,
                    module.ModuleNr, ":", &analog.list, names)?;
                tmod = Term::map_put(tmod, 0.encode(env), kind)?;
                names = unames;
            };
            if let Some(digital) = &link.Digital {
                let (unames, kind) = get_tags(env,
                    module.ModuleNr, ".", &digital.list, names)?;
                tmod = Term::map_put(tmod, 1.encode(env), kind)?;
                names = unames;
            };
        };
        // Index Module
        tags = Term::map_put(tags, (module.ModuleNr).encode(env), tmod)?;
    }
    // Assembly Map
    io = Term::map_put(io, atoms::tags().to_term(env), tags)?;
    io = Term::map_put(io, atoms::names().to_term(env), names)?;
    io = Term::map_put(io, atoms::modules().to_term(env), modules)?;
    Ok(io)
}

//##########################################################################################################################

rustler::init!(
    "Elixir.OpcSx.Iba.IoConfig.Nif",
    [parse]
);

//##########################################################################################################################
