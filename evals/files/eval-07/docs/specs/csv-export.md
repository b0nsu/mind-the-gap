# Spec: CSV export for reports

Status: **Approved** (2026-09-30)

## Endpoint
`GET /reports/export?reportId=<id>&from=<YYYY-MM-DD>&to=<YYYY-MM-DD>`

- Auth: same as the other report endpoints.
- `from` and `to` are optional; when omitted, export the whole report.

## Response
- `Content-Type: text/csv; charset=utf-8`
- Body is UTF-8 **with BOM** (Excel compatibility).
- `Content-Disposition: attachment; filename="report-{reportId}-{YYYYMMDD}.csv"`, where the date is the export date in UTC.
- Columns, in order: `date`, `metric`, `value`.
- One header row.

## Errors
- Unknown `reportId`: 404 with the same JSON error shape as other report endpoints.
