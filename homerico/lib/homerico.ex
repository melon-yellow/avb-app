defmodule HomericoApp do
  @moduledoc """
  HomericoApp keeps the contexts that define your domain
  and business logic.

  Contexts are also responsible for managing your data, regardless
  if it comes from the database, an external API or others.
  """

  @keys keys!
  @config config!

  defp config! do
    System.get_env("HOMERICO_GATEWAY")
      |> Homerico.Connect.gateway!
      |> Homerico.Connect.login!(
        System.get_env("HOMERICO_USER"),
        System.get_env("HOMERICO_PASSWORD")
      )
  end

  defp keys! do
    Homerico.Reports.__info__(:functions)
      |> Enum.map(&Atom.to_string elem(&1, 0))
      |> Enum.filter(&!String.contains?(&1, "!"))
      |> Enum.map(&String.to_atom &1)
  end

end
