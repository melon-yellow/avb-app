
use rustler::{NifResult};

#[rustler::nif]
fn parse(_xml: String) -> NifResult<u8> {
    Ok(0)
}

rustler::init!(
    "Elixir.OpcSx.Iba.IoConfig.Nif",
    [parse]
);
