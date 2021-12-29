defmodule HomericoSx.Connect.Process do
  @pid spawn HomericoSx.Connect, :loop, nil
  def id do @pid end
end

defmodule HomericoSx.Connect do

  defp connect! do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  def loop(state \\ nil) do
    receive do
      :get -> (
        state = case state do
          nil -> connect!
          _ -> _
        end
      )
      _ -> nil
    end
    loop(state)
  end

  def config! do
    send HomericoSx.Connect.Process.id, :get
  end

end
