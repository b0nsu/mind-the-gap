const crypto = require("crypto");
const db = require("./db");

// TODO: hashing. Passwords are currently compared in plain text.
async function register(email, password) {
  await db.query("INSERT INTO users (email, password) VALUES ($1, $2)", [email, password]);
}

async function login(email, password) {
  const { rows } = await db.query("SELECT password FROM users WHERE email = $1", [email]);
  return rows.length === 1 && rows[0].password === password;
}

module.exports = { register, login };
