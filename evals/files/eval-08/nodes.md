# Pipeline nodes to review

1. `fetch_orders` — pulls orders from the shop API every 15 minutes; retries 3 times, then drops the batch.
2. `dedupe` — removes orders with the same `order_id`; keeps the first seen.
3. `currency_normalize` — converts amounts to EUR using yesterday's rate.
4. `fraud_flag` — flags orders over 2,000 EUR from accounts younger than 7 days.
5. `write_warehouse` — upserts into `orders_fact`; on conflict overwrites all columns.
6. `notify_finance` — emails finance a daily summary at 06:00 UTC.
