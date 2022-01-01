
defmodule HomericoSx.Connect do
  use Agent

  @pid :homerico_app_state

  defp start do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  defp loop(dnstr \\ nil) do
    receive do
      {:get, caller} ->
        send caller, {@pid, dnstr}
        loop dnstr
      {:set, upstr} -> loop upstr
      _ -> loop dnstr
    end
  end

  def config! do
    send @pid, {:get, self()}
    receive do
      {@pid, upstr} -> upstr
      _ -> nil
    end
  end

  def start_link(_args) do
    {:ok, pid} = Task.start_link &loop/0
    Process.register pid, @pid
    send @pid, {:set, start()}
    {:ok, pid}
  end

end
