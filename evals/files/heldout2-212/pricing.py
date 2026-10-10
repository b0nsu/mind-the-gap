BULK_THRESHOLD = 100
BULK_DISCOUNT = 0.15


def order_total(subtotal):
    """Return the amount to charge for an order subtotal (in dollars)."""
    if subtotal >= BULK_THRESHOLD:
        return round(subtotal * (1 - BULK_DISCOUNT), 2)
    return round(subtotal, 2)
