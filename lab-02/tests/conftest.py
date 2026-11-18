import sys
from pathlib import Path

import pytest

# lab-02/ is one level up: make `import app` work from any working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as shop  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    # file store in a temp dir, never Postgres, never /data
    monkeypatch.setattr(shop, "DATABASE_URL", None)
    monkeypatch.setattr(shop, "COUNTER_FILE", tmp_path / "visits.txt")
    shop.app.config["TESTING"] = True
    with shop.app.test_client() as c:
        yield c