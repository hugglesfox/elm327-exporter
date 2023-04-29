def test_metrics_endpoint(emulator, client):
    resp = client.get('/metrics')
    assert resp.status_code == 200
