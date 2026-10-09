const REPORTS = {
  r1: [
    { date: "2026-09-01", metric: "signups", value: 42 },
    { date: "2026-09-02", metric: "signups", value: 37 },
  ],
};

export async function getReport(id) {
  return REPORTS[id] ?? null;
}
