import pytest

from app.pricing import line_total, order_total


def test_line_total_basic():
    assert line_total(20.0, 3) == 60.0


def test_line_total_rejects_bad_qty():
    with pytest.raises(ValueError):
        line_total(20.0, 0)


def test_no_discount_below_threshold():
    assert order_total([{"unit_price": 20.0, "qty": 5}]) == 100.0


def test_bulk_discount_applies_at_threshold():
    # 10 x 20.00 = 200.00, minus 10% bulk discount = 180.00
    assert order_total([{"unit_price": 20.0, "qty": 10}]) == 180.0


def test_mixed_order():
    items = [
        {"unit_price": 20.0, "qty": 10},
        {"unit_price": 5.0, "qty": 2},
    ]
    assert order_total(items) == 190.0
