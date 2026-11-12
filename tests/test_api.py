from app.main import app


def client():
    return app.test_client()


def test_health():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_fetch_order():
    c = client()
    created = c.post("/orders", json={"items": [{"unit_price": 20.0, "qty": 10}]})
    assert created.status_code == 201
    body = created.get_json()
    assert body["total"] == 180.0
    fetched = c.get(f"/orders/{body['id']}")
    assert fetched.status_code == 200


def test_order_requires_items():
    response = client().post("/orders", json={})
    assert response.status_code == 400


def test_unknown_order_is_404():
    assert client().get("/orders/9999").status_code == 404
