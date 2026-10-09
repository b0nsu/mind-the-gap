import { prisma } from "../db.js";

// Called from DELETE /account. Soft vs hard delete not decided yet.
export async function deleteUser(userId) {
  throw new Error("not implemented");
}
