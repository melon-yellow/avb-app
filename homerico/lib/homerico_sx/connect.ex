defmodule HomericoSx.Connect do
  use Agent

  defp connect do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  def start_link(_args) do
    try do
      {:ok, pid} = HomericoSx.Connect.State.start_link
      connect() |> HomericoSx.Connect.State.set
      IO.inspect HomericoSx.Connect.State.get
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def config, do: HomericoSx.Connect.State.get

end

defmodule HomericoSx.Connect.State do

  @pid :homerico_sx_config_pid

  defp loop(state) do
    receive do
      {:set, value} -> loop value
      {:get, caller} ->
        send caller, {@pid, state}
        loop state
    end
  end

  def start_link do
    try do
      {:ok, pid} = Task.start_link(fn -> loop nil end)
      Process.register pid, @pid
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  def set(value) do
    send @pid, {:set, value}
  end

  def get do
    send @pid, {:get, self()}
    receive do {@pid, state} -> state end
  end

end
