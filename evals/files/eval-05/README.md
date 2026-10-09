# notes-api

Multi-tenant notes API. One deployment serves three tenants (acme, globex, initech); the tenant is resolved from `X-Tenant-Id`.
Sessions are stored in Redis.
