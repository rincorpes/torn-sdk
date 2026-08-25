from __future__ import annotations

import argparse
import importlib
from importlib.metadata import PackageNotFoundError, version

from limen.app import BaseCLIApp
from limen.config import CLIConfig
from limen.runner import run_cli


class TornSDKCLI(BaseCLIApp):
    """Limen-powered Torn SDK developer CLI."""

    def __init__(self, config: CLIConfig) -> None:
        super().__init__(config)
        self.build_commands()


def load_commands() -> None:
    importlib.import_module("torn_sdk.cli.commands.generate")


def create_config(
    global_parser: argparse.ArgumentParser,
) -> CLIConfig:
    return CLIConfig(
        app_name="torn-sdk",
        description=(
            "Developer tooling for generating Torn SDK code, "
            "network-free mocks, and pytest contract tests."
        ),
        usage="%(prog)s [options] generate <sdk|mock|tests> [<args>]",
        formatter_class=global_parser.formatter_class,
        parents=[global_parser],
    )


def package_version() -> str:
    try:
        return version("torn-sdk")
    except PackageNotFoundError:
        return "0.0.0"


def main(argv: list[str] | None = None) -> int:
    return run_cli(
        version=package_version(),
        app_factory=TornSDKCLI,
        config_factory=create_config,
        command_loaders=(load_commands,),
        argv=argv,
    )
