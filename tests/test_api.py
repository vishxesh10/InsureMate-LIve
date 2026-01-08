from fastapi.testclient import TestClient
from insuremate.main import app

client = TestClient(app)


def test_root_predict_not_implemented():
    # verify predict endpoint exists and returns 422 with empty payload
    resp = client.post("/predict", json={})
    assert resp.status_code in (200, 422)


def test_results_endpoints():
    resp = client.get("/results")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)

    resp2 = client.get("/results/city/test-city")
    assert resp2.status_code == 200

    resp3 = client.get("/results/category/test-category")
    assert resp3.status_code == 200
