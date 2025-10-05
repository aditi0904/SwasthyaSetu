from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_search_basic():
    payload = {"query": "fever", "top_k": 5, "min_similarity": 0.5}
    r = client.post("/search", json=payload)
    assert r.status_code == 200
    assert "results" in r.json()
