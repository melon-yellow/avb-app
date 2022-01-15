import Config

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :opc_sx, OpcSxWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "7U/Jba5uLX2Na0/PHz+LJIXKSZUPIfBQj4sFWAttUvLZJFlqK+WnK9QUlXDqGv7X",
  server: false

# Print only warnings and errors during test
config :logger, level: :warn

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime
