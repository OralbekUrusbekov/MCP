import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_query_endpoint():
    r = client.post(
        "/api/v1/agent/query",
        json={"query": "покажи продукты"}
    )

    assert r.status_code == 200
    data = r.json()
    assert "response" in data


def test_products_endpoint():
    r = client.get("/api/v1/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_invalid_json():
    r = client.post(
        "/api/v1/agent/query",
        content="not json",
        headers={"Content-Type": "application/json"}
    )

    assert r.status_code == 422
