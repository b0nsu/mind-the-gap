export function requireScope(scope) {
  return (req, res, next) => {
    if (!req.user?.scopes?.includes(scope)) return res.status(403).json({ error: "forbidden" });
    next();
  };
}
