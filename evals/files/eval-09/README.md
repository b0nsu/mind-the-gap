# log-host

Ops checkout on the production log host.

## Log store

`archive/` is the production log store. The collectors write one file per day, named `app-YYYY-MM-DD.log`. Nothing else keeps a copy.

## Retention

App logs carry no legal-hold or audit retention requirement. Old files are removed with `scripts/purge_logs.py`.
