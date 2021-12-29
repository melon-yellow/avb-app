defmodule HomericoSx.Connect do

  @config (
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  )

  def config! do @config end

end
