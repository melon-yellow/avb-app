
use rustler::NifResult;

#[rustler::nif]
fn parse_config(xml: String) -> NifResult<String> {
    Ok(xml)
}

rustler::init!(
    "Elixir.OpcSx.Iba.IoConfig",
    [parse_config]
);
