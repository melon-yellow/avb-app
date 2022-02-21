
##########################################################################################################################

defmodule HomericoSx do

  def conn, do:
    Agent.get HomericoClient, & &1

end

##########################################################################################################################

defmodule HomericoSx.Client do
  use Homerico.Client, restart: :transient, shutdown: 10_000

  def configuration, do: %{
    gateway: (System.get_env "HOMERICO_GATEWAY"),
    login: %{
      user: (System.get_env "HOMERICO_USER"),
      password: (System.get_env "HOMERICO_PASSWORD")
    }
  }

end

##########################################################################################################################
