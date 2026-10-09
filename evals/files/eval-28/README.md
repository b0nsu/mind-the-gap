# orders-service

Small internal service for order intake.

## Deployment

Runs on three app servers behind a load balancer (`app-1`, `app-2`, `app-3`). All three accept writes. Storage must be reachable from every server.
