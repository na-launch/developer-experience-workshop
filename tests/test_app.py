import pytest
import json
from app import app, get_translation
from flask import Flask
from unittest.mock import patch
from flask import Response

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_missing_translation_key(client, monkeypatch):
    monkeypatch.setenv("COUNTRY_CODE", "xx")  # assume not in JSON
    response = client.get("/")
    assert response.status_code in [200, 404]
    assert isinstance(response.data.decode(), str)

def test_index_success(client):
    with patch("routes.main.get_translation") as mock_get_translation, \
         patch("routes.main.get_current_datetime") as mock_get_current_datetime:
        
        mock_get_translation.return_value = "Hello"
        mock_get_current_datetime.return_value = "2025-04-03 12:00:00"

        response = client.get("/")
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "hello @ 2025-04-03 12:00:00"
        assert response.mimetype == "text/plain"

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
    path = tmp_path / "translations.json"
    path.write_text(json.dumps(translations_data), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    from routes.main import get_translation

    # Valid case
    assert get_translation("en") == "hello world"
    assert get_translation("FR") == "bonjour monde!"

    # Invalid key
    with pytest.raises(Exception, match="Translation not found"):
        get_translation("JP")
