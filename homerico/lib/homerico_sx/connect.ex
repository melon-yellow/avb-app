defmodule HomericoSx.Connect do
  use Agent

  @pid :homerico_sx_config_state

  defp start do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  defp loop(state \\ nil) do
    receive do
      {:set, value} -> loop value
      {:get, caller} ->
        send caller, {@pid, state}
        loop state
    end
  end

  def config! do
    send @pid, {:get, self()}
    receive do
      {@pid, state} -> state
    end
  end

  def start_link(_args) do
    {:ok, pid} = Task.start_link(fn -> loop() end)
    Process.register pid, @pid
    send @pid, {:set, start()}
    {:ok, pid}
  end

end
