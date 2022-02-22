
use rustler::NifResult;

#[rustler::nif]
fn parse(xml: String) -> NifResult<String> {
    Ok(xml)
}

rustler::init!(
    "Elixir.OpcSx.Iba.IoConfig",
    [parse]
);
