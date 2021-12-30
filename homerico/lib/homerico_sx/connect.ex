
defmodule HomericoSx.Connect do
  use Agent

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
        send caller, {:stack, dnstr}
        dnstr |> loop()
      {:put, upstr} ->
        upstr |> loop()
      _ ->
        dnstr |> loop()
    end
  end

  def config! do
    send :stack, {:get, self()}
    receive do
      {:stack, upstr} -> upstr
      _ -> nil
    end
  end

  def start_link(_args) do
    {:ok, pid} = Task.start_link(fn -> loop() end)
    Process.register(pid, :stack)
    send :stack, {:put, start()}
    {:ok, pid}
  end

end
