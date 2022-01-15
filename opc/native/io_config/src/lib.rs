
#[rustler::nif]
fn read_io_config(path: String) -> String {
    return null
}

rustler::init!(
    "Elixir.OpcSx.IbaClient.IoConfig",
    [
        read_io_config
    ]
);
