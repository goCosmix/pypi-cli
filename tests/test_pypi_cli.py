import os
from pypi_manager import PyPIManager


def test_token_loading_from_env(monkeypatch):
    monkeypatch.setenv("PYPI_TOKEN", "test-token")
    manager = PyPIManager()
    assert manager.is_configured()
    assert manager.token == "test-token"


def test_token_not_configured(tmp_path, monkeypatch):
    monkeypatch.delenv("PYPI_TOKEN", raising=False)
    config_dir = tmp_path / ".vscode-ark" / "internal"
    monkeypatch.setenv("HOME", str(tmp_path))
    manager = PyPIManager()
    assert not manager.is_configured()
