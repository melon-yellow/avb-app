
##########################################################################################################################

defmodule HomericoSx do

  def connect do
    try do
      config = System.get_env("HOMERICO_GATEWAY")
        |> Homerico.Connect.gateway!
        |> Homerico.Connect.login!(
          System.get_env("HOMERICO_USER"),
          System.get_env("HOMERICO_PASSWORD")
        )
      {:ok, config}
    catch _, reason -> {:error, reason}
    end
  end

  def config, do:
    HomericoSx.State.get

end

##########################################################################################################################

defmodule HomericoSx.State do
  use SimpleState

  def start_link(_init_arg) do
    try do
      {:ok, config} = HomericoSx.connect
      SimpleState.start_link(__MODULE__, value: config)
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
