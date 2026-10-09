const TENANTS = new Set(["acme", "globex", "initech"]);

// Every request carries X-Tenant-Id; set by the edge proxy.
export function resolveTenant(req, res, next) {
  const id = req.get("X-Tenant-Id");
  if (!TENANTS.has(id)) return res.status(400).json({ error: "unknown tenant" });
  req.tenantId = id;
  next();
}
