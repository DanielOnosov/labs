import app as shop


def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "ok\n"


def test_ready_reports_file_store(client):
    r = client.get("/ready")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ready"] is True
    assert body["store"].startswith("file:")


def test_visits_counts_up(client):
    first = client.get("/visits").get_json()
    second = client.get("/visits").get_json()
    assert first == {"visits": 1, "store": "file"}
    assert second["visits"] == 2


def test_visits_persists_to_counter_file(client):
    client.get("/visits")
    client.get("/visits")
    assert shop.COUNTER_FILE.read_text() == "2"


def test_visits_answers_503_when_store_is_broken(client, monkeypatch, tmp_path):
    broken = tmp_path / "is-a-dir"
    broken.mkdir()
    monkeypatch.setattr(shop, "COUNTER_FILE", broken)
    r = client.get("/visits")
    assert r.status_code == 503
    assert r.get_json()["store"] == "file"