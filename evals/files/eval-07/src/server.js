import express from "express";
import { reportsRouter } from "./routes/reports.js";

const app = express();
// Auth gateway populates req.user before requests reach this service.
app.use("/reports", reportsRouter);

app.listen(process.env.PORT ?? 3000);
