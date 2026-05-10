# PyPI CLI - Internal Tool

Standalone PyPI publishing tool for Ernie's projects.

## Setup

```bash
python publish.py setup
```

## Usage

### Publish existing build
```bash
python publish.py publish /path/to/project
```

### Build and publish
```bash
python publish.py build-publish /path/to/project
```

### Check configuration
```bash
python publish.py check
```

## Token Management

- **Environment Variable**: `export PYPI_TOKEN=...`
- **Local Config**: Stored in `~/.vscode-ark/internal/pypi-config.json` (chmod 0600)

Priority: env var > local config
