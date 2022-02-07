import Unsafe.Handler

##########################################################################################################################

defmodule OpcSx.Iba.Utils do
  use Unsafe.Generator, handler: :bang!

  @unsafe [
    node_from_tag: 1,
    node_from_tagname: 1,
  ]

  @node_prefix %{ns: 3, s: "V:0.3"}
  @tag_regex ~r/([0-9]+)((.|:){1})([0-9]+)/

  defp throw_tag!(valid) when valid, do: true
  defp throw_tag!(_), do: throw "invalid tag"

  defp check_tag!(text), do:
    text |> String.match?(@tag_regex) |> throw_tag!

  defp split_tag!(tag), do: if String.contains?(tag, ":"),
    do:   [0 | String.split(tag, ":")],
    else: [1 | String.split(tag, ".")]

  defp set_node!([d, m, s]), do: OpcSx.Utils.node_from!(
    ns: @node_prefix.ns, s: @node_prefix.s <> ".#{m}.#{d}.#{s}"
  )

  def node_from_tag(tag) when is_binary(tag) do
    try do
      check_tag! tag
      nid = tag |> split_tag! |> set_node!
      {:ok, nid}
    catch _, reason -> {:error, reason}
    end
  end

  defp tag_from_name!(tagname), do:
    OpcSx.Iba.State.get().tag_list[tagname]

  def node_from_tagname(tagname) when is_binary(tagname) do
    try do
      nid = tagname |> tag_from_name! |> node_from_tag!
      {:ok, nid}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################

defmodule OpcSx.Iba.State do
  use Task

  @pid :opc_sx_iba_io_config_pid

  def start_link(_init_arg) do
    try do
      {:ok, pid} = Task.start_link(fn -> loop nil end)
      Process.register pid, @pid
      {:ok, ioc} = OpcSx.Iba.IoConfig.read
      OpcSx.Iba.State.set ioc
      {:ok, pid}
    catch _, reason -> {:error, reason}
    end
  end

  defp loop(state) do
    receive do
      {:set, value} -> loop value
      {:get, caller} ->
        send caller, {@pid, state}
        loop state
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

##########################################################################################################################
