import { Router } from "express";
import { requireScope } from "../middleware/auth.js";
import { getReport } from "../services/reports.js";

export const reportsRouter = Router();

reportsRouter.get("/:id", requireScope("reports:read"), async (req, res) => {
  const rows = await getReport(req.params.id);
  if (!rows) return res.status(404).json({ error: "report not found" });
  res.json(rows);
});

reportsRouter.get("/:id/summary", requireScope("reports:read"), async (req, res) => {
  const rows = await getReport(req.params.id);
  if (!rows) return res.status(404).json({ error: "report not found" });
  res.json({ count: rows.length });
});
