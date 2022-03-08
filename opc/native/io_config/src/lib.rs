
use rustler::{
    Env,
    Term,
    Encoder,
    NifResult,
    Atom,
    MapIterator
};

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
    map: Term<'a>,
    atom: &str,
    value: &T
) -> NifResult<Term<'a>> {
    let env = map.get_env();
    let _atom = Atom::from_str(env, atom)?;
    Ok(
        Term::map_put(map,
            _atom.encode(env),
            value.encode(env)
        )?
    )
}

//##########################################################################################################################

fn map_merge<'a>(
    dest: Term<'a>,
    origin: Term<'a>
) -> NifResult<Term<'a>> {
    if let Some(iter) = MapIterator::new(origin) {
        for (key, value) in iter {
            dest = Term::map_put(dest, key, value)?;
        };
    };
    Ok(dest)
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

// Get Tags From Signal-List
fn get_tags<'a>(
    env: Env<'a>,
    prefix: (usize, &str),
    list: &Vec<Signal>
) -> NifResult<(Term<'a>, Term<'a>)> {
    // Set Buffer
    let mut tags = Term::map_new(env);
    let mut names = Term::map_new(env);
    // Iterate over Tags
    for (i, signal) in list.iter().enumerate() {
        if !signal.Name.trim().is_empty() {
            tags = Term::map_put(tags,
                i.encode(env),
                signal.to_term(env)?
            )?;
            names = Term::map_put(names,
                signal.Name.encode(env),
                format!("{}{}{}", prefix.0, prefix.1, i).encode(env)
            )?;
        };
    };
    // Return Ok
    Ok((tags, names))
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
        // Set Buffer
        let mut analogs = Term::map_new(env);
        let mut digitals = Term::map_new(env);
        // Iterate over Links
        for link in module.Links.list.iter() {
            if let Some(analog) = &link.Analog {
                let (_tags, _names) = get_tags(env,
                    (module.ModuleNr, ":"),
                    &(analog.list)
                )?;
                analogs = map_merge(analogs, _tags);
                names = map_merge(names, _names);
            };
            if let Some(digital) = &link.Digital {
                let (_tags, _names) = get_tags(env,
                    (module.ModuleNr, "."),
                    &(digital.list)
                )?;
                digitals = map_merge(digitals, _tags);
                names = map_merge(names, _names);
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
