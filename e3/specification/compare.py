#!/usr/bin/env python3
"""
Functions to compare specifications.
"""

from pathlib import Path

import yaml


def module_loader(specification_file: Path) -> dict:
    """Load specification file."""
    with open(specification_file, "r") as f:
        specification = yaml.safe_load(f)
    modules: dict = {
        module["name"]: module["versions"] for module in specification["modules"]
    }
    return modules


def get_module_difference(source_file: Path, target_file: Path) -> dict:
    """Return module set difference (one way) of two specification files."""
    source_modules: dict = module_loader(source_file)
    target_modules: dict = module_loader(target_file)

    diff_modules = dict()
    for module, versions in target_modules.items():
        if module not in source_modules.keys():
            diff_modules[module] = versions
        else:
            new_versions = set(versions)
            old_versions = set(source_modules[module])
            diff_versions = list(new_versions - old_versions)
            if diff_versions:
                diff_modules[module] = diff_versions

    return diff_modules
