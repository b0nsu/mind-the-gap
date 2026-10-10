# shop

Single-host deployment with docker compose. The `cron` container runs whatever is in `cron.d/` (alpine periodic layout).

Requirements agreed with finance: a restorable copy of the database every night, kept for at least 30 days. Where the copies live has not been decided; the host has 200 GB free and the company has an S3 account used by other teams.
