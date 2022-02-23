
use rustler::{Env, Term, Encoder, NifResult, Atom};

use serde::Deserialize;
use quick_xml::de;

//##########################################################################################################################

mod atoms {
    rustler::atoms! { tags, modules, names }
}

//##########################################################################################################################

#[derive(Debug, Deserialize, PartialEq)]
struct Signal {
    Name: String,
    DataType: u8,
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

#[derive(Debug, Deserialize, PartialEq)]
struct Link {
    Analog: SignalList,
    Digital: SignalList
}

#[derive(Debug, Deserialize, PartialEq)]
struct LinkList {
    #[serde(rename = "Link", default)]
    list: Vec<Link>
}

#[derive(Debug, Deserialize, PartialEq)]
struct Module {
    Name: String,
    ModuleType: u16,
    Enabled: bool,
    ModuleNr: u8,
    Links: LinkList,
    FileModuleNr: Option<u16>,
    NrAnalogSignals: u16,
    NrDigitalSignals: u16,
    PCCP_Destination: Option<String>,
    CPUName: Option<String>
}

#[derive(Debug, Deserialize, PartialEq)]
struct ModuleList {
    #[serde(rename = "Module", default)]
    list: Vec<Module>
}

#[derive(Debug, Deserialize, PartialEq)]
struct IoConfig {
    Modules: ModuleList
}

#[derive(Debug, Deserialize, PartialEq)]
struct Document {
    IOConfiguration: IoConfig
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

#[rustler::nif]
fn parse<'a>(env: Env<'a>, xml: &str) -> NifResult<Term<'a>> {
    // Set Variables
    let mut io = Term::map_new(env);
    let mut tags = Term::map_new(env);
    let mut names = Term::map_new(env);
    let mut modules = Term::map_new(env);
    // Parse XML
    let doc: Document = de::from_str(xml).unwrap();
    // Iterate over Modules
    for module in doc.IOConfiguration.Modules.list.iter() {
        modules = Term::map_put(
            modules,
            (module.ModuleNr).encode(env),
            module.to_term(env)?
        )?;
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
