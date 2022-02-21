
##########################################################################################################################

defmodule OpcSx.NodeId do
  use Unsafe.Generator, handler: {Unsafe.Handler, :bang!}

  @unsafe [node_from: 1]

  def new(opts) when is_list(opts) do
    try do
      nid = OpcUA.NodeId.new(
        ns_index: Keyword.fetch!(opts, :ns),
        identifier: Keyword.fetch!(opts, :s),
        identifier_type: "string"
      )
      {:ok, nid}
    catch _, reason -> {:error, reason}
    end
  end

end

##########################################################################################################################
