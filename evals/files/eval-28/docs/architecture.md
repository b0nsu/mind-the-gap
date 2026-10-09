# Architecture

- Stateless HTTP handlers on each app server.
- Every server writes orders as they arrive; there is no single writer.
- Storage layer: TBD.
