import pytest
import json
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_failure(client):
    with patch("routes.main.get_translation", side_effect=Exception("Something went wrong")):
        response = client.get("/")
        assert response.status_code == 500
        assert b"Something went wrong" in response.data

def test_get_translation_direct(tmp_path, monkeypatch):
    translations_data = {
        "translations": {
            "EN": "hello world",
            "FR": "bonjour monde!"
        }
    }
    # Write the translations JSON file to the temporary directory.
    path = tmp_path / "translations.json"
    path.write_text(json.dumps(translations_data), encoding="utf-8")
    # Change the working directory so that get_translation can find translations.json.
    monkeypatch.chdir(tmp_path)

    # Import the function after changing the directory.
    from routes.main import get_translation

    # Valid cases.
    assert get_translation("EN") == "hello world"
    assert get_translation("FR") == "bonjour monde!"

    # Invalid key should raise an Exception.
    with pytest.raises(Exception, match="Translation not found"):
        get_translation("JP")
