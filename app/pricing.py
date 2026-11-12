"""Pricing rules for order-service."""

BULK_THRESHOLD = 10
BULK_DISCOUNT_PERCENT = 10


def line_total(unit_price: float, qty: int) -> float:
    """Price of one order line, rounded to 2 decimals."""
    if qty <= 0:
        raise ValueError("qty must be positive")
    if unit_price < 0:
        raise ValueError("unit_price must not be negative")
    return round(unit_price * qty, 2)


def order_total(items: list[dict]) -> float:
    """Total for an order. Lines with qty >= BULK_THRESHOLD get a discount."""
    total = 0.0
    for item in items:
        subtotal = line_total(item["unit_price"], item["qty"])
        if item["qty"] >= BULK_THRESHOLD:
            subtotal = round(subtotal * (1 - BULK_DISCOUNT_PERCENT / 100), 2)
        total += subtotal
    return round(total, 2)
