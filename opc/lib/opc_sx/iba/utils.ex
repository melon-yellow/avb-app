
##########################################################################################################################

defmodule OpcSx.Iba.NodeId do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}

  @unsafe [from_tag: 1, from_tagname: 1]

  @node_prefix %{ns: 3, s: "V:0.3"}
  @tag_regex ~r/([0-9]+)((.|:){1})([0-9]+)/

  defp throw_tag!(valid) when valid, do: true
  defp throw_tag!(_), do: throw "invalid tag"

  defp check_tag!(text), do:
    text |> String.match?(@tag_regex) |> throw_tag!

  defp split!(tag), do: if String.contains?(tag, ":"),
    do:   [0 | String.split(tag, ":")],
    else: [1 | String.split(tag, ".")]

  defp node!([dig, mod, i]), do: OpcSx.NodeId.new!(
    s: @node_prefix.s <> ".#{mod}.#{dig}.#{i}",
    ns: @node_prefix.ns
  )

  def from_tag(tag) when is_binary(tag) do
    try do
      check_tag! tag
      nid = tag |> split! |> node!
      {:ok, nid}
    catch _, reason -> {:error, reason}
    end
  end

  defp named_tag!(tagname) do
    config = Agent.get IbaIoConfig, & &1
    config.names[tagname]
  end

  def from_tagname(tagname) when is_binary(tagname) do
    try do
      nid = tagname |> named_tag! |> from_tag!
      {:ok, nid}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
