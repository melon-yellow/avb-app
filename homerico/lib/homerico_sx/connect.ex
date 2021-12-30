
defmodule HomericoSx.Connect do
  use Agent

  defp start! do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  defp loop(term \\ nil) do
    receive do
      {:get, caller} ->
        send caller, term
        term |> loop()
      {:put, value} ->
        value |> loop()
    end
  end

  def start_link(_arg) do
    {:ok, pid} = Task.start_link(fn -> loop() end)
    send pid, {:put, start!()}
    Process.register(pid, :stack)
    {:ok, :stack}
  end

  def config! do
    send :stack, {:get, self()}
  end

end
