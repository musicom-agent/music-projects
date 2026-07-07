# KiloGateway Provider Alias Note

## Finding
Hermes accepts `kilo-gateway` as the provider name. It resolves to the `kilocode` provider plugin.

## Verification
- `hermes config set model.provider kilo-gateway` succeeds.
- `hermes config path` shows the updated config.
- `model.provider: kilo-gateway` is stored in `/opt/data/config.yaml`.

## Practical Use
- Use `kilo-gateway` in Hermes config and cron job provider fields.
- Backing credential is `KILOCODE_API_KEY`.

## Pitfall
Do not write bare `kilo`, `kilo code`, or `kilogateway` in config. Use the canonical alias `kilo-gateway`.
