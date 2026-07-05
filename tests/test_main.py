import os
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import main


def config(**overrides):
    values = {
        "url": "https://keycloak.example/realms/test/protocol/openid-connect/token",
        "client_id": "monitor",
        "client_secret": "not-a-real-secret",
        "instance": "test",
        "namespace": "test",
        "pod": "test-1",
        "verify_tls": True,
        "interval": 60,
        "timeout": 10,
        "listen_port": 8000,
    }
    values.update(overrides)
    return main.Config(**values)


def test_tls_verification_is_enabled_by_default(monkeypatch):
    for name in ("KEYCLOAK_URL", "CLIENT_ID", "CLIENT_SECRET", "VERIFY_TLS"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("KEYCLOAK_URL", "https://keycloak.example/token")
    monkeypatch.setenv("CLIENT_ID", "monitor")
    monkeypatch.setenv("CLIENT_SECRET", "secret")
    assert main.Config.from_env().verify_tls is True


def test_missing_required_environment(monkeypatch):
    monkeypatch.delenv("KEYCLOAK_URL", raising=False)
    monkeypatch.delenv("CLIENT_ID", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)
    with pytest.raises(ValueError):
        main.Config.from_env()


def test_successful_measurement_uses_tls_verification():
    response = Mock(status_code=200)
    response.raise_for_status.return_value = None
    session = Mock()
    session.post.return_value = response

    assert main.measure_once(config(), session) is True
    assert session.post.call_args.kwargs["verify"] is True
    assert "client_secret" in session.post.call_args.kwargs["data"]


def test_request_failure_is_reported():
    session = Mock()
    session.post.side_effect = requests.Timeout("timeout")
    assert main.measure_once(config(), session) is False
