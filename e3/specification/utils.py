"""
Utility functions.
"""
from pathlib import Path

import yaml


def load_specification(specification_file: Path) -> dict:
    """Load specification file."""
    with open(specification_file, "r") as f:
        specification = yaml.safe_load(f)
    return specification


def get_modules(specification: dict) -> dict:
    modules: dict = {
        module["name"]: module["versions"] for module in specification["modules"]
    }
    return modules


def print_modules_as_yaml(module_list: dict) -> None:
    """Prints a module_list as valid yaml."""
    for name, versions in module_list.items():
        print(f"{name}:")
        for version in versions:
            print(f"- {version}")
