import Unsafe.Handler

defmodule OpcSx.Utils do
  use Unsafe.Generator, handler: :bang!

  @unsafe [
    node_from: 1
  ]

  def node_from(opts \\ []) when is_list(opts) do
    try do
      node_id = OpcUA.NodeId.new(
        ns_index: Keyword.fetch!(opts, :ns),
        identifier_type: "string",
        identifier: Keyword.fetch!(opts, :s)
      )
      {:ok, node_id}
    catch _, reason -> {:error, reason}
    end
  end

end
