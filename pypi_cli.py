#!/usr/bin/env python3
"""
PyPI Publishing CLI

Standalone internal tool for secure package publishing.
"""

import sys
import click
from pathlib import Path
from pypi_manager import PyPIManager


def bold(text):
    return f"\033[1m{text}\033[0m"


def green(text):
    return f"\033[92m{text}\033[0m"


def yellow(text):
    return f"\033[93m{text}\033[0m"


def red(text):
    return f"\033[91m{text}\033[0m"


@click.group()
def cli():
    """PyPI Release Management."""
    pass


@cli.command("setup")
def setup():
    """Configure PyPI token interactively."""
    import getpass

    print("\n=== PyPI Token Setup ===")
    print("Get token from: https://pypi.org/manage/account/token/\n")

    token = getpass.getpass("Enter PyPI API token: ").strip()
    if not token:
        print("Setup cancelled.")
        return

    manager = PyPIManager()
    manager.save_token(token)
    print(green("✓ Token saved securely"))


@cli.command("check")
def check():
    """Check if token is configured."""
    manager = PyPIManager()
    if manager.is_configured():
        print(green("✓ PyPI token configured"))
    else:
        print(yellow("⚠ PyPI token not configured"))
        print("  Run: python publish.py setup")


@cli.command("publish")
@click.argument("project_dir", type=click.Path(exists=True))
@click.option("--dist", default="dist", show_default=True, help="Distribution directory")
def publish(project_dir, dist):
    """Publish a project to PyPI."""
    manager = PyPIManager()

    if not manager.is_configured():
        click.echo(red("✗ PyPI token not configured"))
        click.echo("  Run: python publish.py setup")
        return

    try:
        click.echo(yellow(f"Publishing {project_dir}..."))
        manager.publish(project_dir, dist)
        click.echo(green(f"✓ Published successfully"))
    except Exception as exc:
        click.echo(red(f"✗ Publish failed: {exc}"))
        sys.exit(1)


@cli.command("build-publish")
@click.argument("project_dir", type=click.Path(exists=True))
@click.option("--dist", default="dist", show_default=True, help="Distribution directory")
def build_publish(project_dir, dist):
    """Build and publish a project to PyPI."""
    manager = PyPIManager()

    if not manager.is_configured():
        click.echo(red("✗ PyPI token not configured"))
        click.echo("  Run: python publish.py setup")
        return

    try:
        click.echo(yellow(f"Building {project_dir}..."))
        import subprocess

        subprocess.run(
            ["python", "-m", "build", "--sdist", "--wheel"],
            cwd=project_dir,
            check=True,
        )
        click.echo(yellow(f"Publishing..."))
        manager.publish(project_dir, dist)
        click.echo(green(f"✓ Built and published successfully"))
    except Exception as exc:
        click.echo(red(f"✗ Build/publish failed: {exc}"))
        sys.exit(1)


if __name__ == "__main__":
    cli()
