import { Router } from "express";

export const notesRouter = Router();
notesRouter.get("/", async (req, res) => res.json([]));
notesRouter.post("/", async (req, res) => res.status(201).json({ id: "n_1", ...req.body }));
