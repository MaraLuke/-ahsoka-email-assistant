from fastapi.testclient import TestClient
import pytest
from email_assistant.api import app

client = TestClient(app)

def test_list_emails(monkeypatch):
    monkeypatch.setattr("email_assistant.client.EmailClient.fetch", lambda self, days: [])
    response = client.get("/emails")
    assert response.status_code == 200
    assert response.json() == []

def test_star_email(monkeypatch):
    monkeypatch.setattr("email_assistant.client.EmailClient.star", lambda self, uid: {"status": "starred", "uid": uid})
    response = client.post("/emails/123/star")
    assert response.status_code == 200
    assert response.json() == {"status": "starred", "uid": "123"}
