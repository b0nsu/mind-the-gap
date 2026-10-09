import express from "express";
import session from "express-session";
import RedisStore from "connect-redis";
import { redis } from "./redis.js";
import { resolveTenant } from "./middleware/tenant.js";
import { notesRouter } from "./routes/notes.js";

const app = express();
app.use(express.json());
app.use(session({ store: new RedisStore({ client: redis }), secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: false }));
app.use(resolveTenant);
app.use("/notes", notesRouter);

app.listen(process.env.PORT ?? 3000);
