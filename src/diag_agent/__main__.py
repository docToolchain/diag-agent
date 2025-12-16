"""Entry point for diag-agent CLI when run as module (python -m diag_agent)."""

from diag_agent.cli.commands import cli


def main():
    """Main entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
