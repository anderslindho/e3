"""
Utility functions.
"""


def print_modules(module_list: dict) -> None:
    """Prints a module_list as valid yaml."""
    for name, versions in module_list.items():
        print(f"{name}:")
        for version in versions:
            print(f"- {version}")
