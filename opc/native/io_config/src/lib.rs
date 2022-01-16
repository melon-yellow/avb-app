
use std::fs::File;
use std::io::Read;
use rustler::NifResult;

#[rustler::nif]
fn read_xml(path: String) -> NifResult<Vec<u8>> {
    let mut file = File::open(&path).unwrap();
    let mut contents: Vec<u8> = Vec::with_capacity(
        file.metadata().unwrap().len() as usize
    );
    file.read_to_end(&mut contents).unwrap();
    Ok(contents)
}

#[rustler::nif]
fn parse_config(xml: String) -> NifResult<String> {
    Ok(xml)
}

rustler::init!(
    "Elixir.OpcSx.IbaClient.IoConfig",
    [read_xml, parse_config]
);
