defmodule Unsafe.Handler do

  def bang!({:ok, return}), do: return
  def bang!({:error, reason}), do: throw reason
  def bang!(_), do: throw "invalid return"

end
