import pytest
from email_assistant.client import EmailClient
from email_assistant.settings import Settings

def test_settings_env(monkeypatch):
    monkeypatch.setenv("EMAIL_USER", "user")
    monkeypatch.setenv("EMAIL_PASS", "pass")
    cfg = Settings()
    assert cfg.email_user == "user"
    assert cfg.email_pass == "pass"

def test_client_init():
    cfg = Settings(email_user="u", email_pass="p")
    client = EmailClient(cfg)
    assert client.cfg.email_user == "u"
