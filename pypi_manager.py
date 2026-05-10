"""PyPI Token and Release Management."""

import os
import json
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".vscode-ark" / "internal"
CONFIG_FILE = CONFIG_DIR / "pypi-config.json"


class PyPIManager:
    """Manage PyPI tokens and publishing."""

    def __init__(self):
        self.token = self._load_token()

    def _load_token(self) -> str:
        """Load token from env or config file."""
        if token := os.getenv("PYPI_TOKEN"):
            return token
        if CONFIG_FILE.exists():
            try:
                config = json.loads(CONFIG_FILE.read_text())
                return config.get("token", "")
            except (json.JSONDecodeError, IOError):
                pass
        return ""

    def save_token(self, token: str) -> None:
        """Save token securely."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps({"token": token}, indent=2))
        CONFIG_FILE.chmod(0o600)
        self.token = token

    def is_configured(self) -> bool:
        """Check if token is set."""
        return bool(self.token)

    def publish(self, project_dir: str, dist_dir: str = "dist") -> bool:
        """Publish project to PyPI."""
        if not self.is_configured():
            raise RuntimeError("PyPI token not configured")

        dist_path = Path(project_dir) / dist_dir
        if not dist_path.exists():
            raise FileNotFoundError(f"Distribution directory not found: {dist_path}")

        env = os.environ.copy()
        env["TWINE_USERNAME"] = "__token__"
        env["TWINE_PASSWORD"] = self.token

        try:
            subprocess.run(
                ["python", "-m", "twine", "upload", f"{dist_path}/*"],
                cwd=project_dir,
                check=True,
                env=env,
            )
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PyPI publish failed: {e}")
