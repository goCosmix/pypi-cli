# PyPI CLI - Internal Tool

Standalone PyPI publishing tool for Ernie's projects.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
pypi --help
```

### Publish existing build
```bash
pypi publish /path/to/project
```

### Build and publish
```bash
pypi build-publish /path/to/project
```

### Check configuration
```bash
pypi check
```

## Token Management

- **Environment Variable**: `export PYPI_TOKEN=...`
- **Local Config**: Stored in `~/.vscode-ark/internal/pypi-config.json` (chmod 0600)

Priority: env var &gt; local config

## GitHub and PyPI Deployment

This repository is ready for GitHub hosting and public PyPI release.

- `pyproject.toml` is configured for packaging.
- `.github/workflows/ci.yml` runs tests on push/PR.
- `.github/workflows/publish.yml` publishes tagged releases to PyPI.

### Publish on GitHub

Create a public repository for this package and push the code.

### Publish on PyPI

Add `PYPI_API_TOKEN` as a GitHub secret, then create a version tag like `v1.0.0` and push it.

You can also publish locally with:

```bash
pypi setup
pypi build-publish .
```
