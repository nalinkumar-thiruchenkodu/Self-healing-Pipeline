"""order-service: a small orders API used for the self-healing pipeline demo."""

from itertools import count

from flask import Flask, jsonify, request

from app.pricing import order_total

app = Flask(__name__)

_orders: dict[int, dict] = {}
_next_id = count(1)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])
    if not items:
        return jsonify(error="items are required"), 400
    try:
        total = order_total(items)
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify(error=f"invalid item: {exc}"), 400
    order_id = next(_next_id)
    _orders[order_id] = {"id": order_id, "items": items, "total": total}
    return jsonify(_orders[order_id]), 201


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    order = _orders.get(order_id)
    if order is None:
        return jsonify(error="order not found"), 404
    return jsonify(order)
