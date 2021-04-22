#!/usr/bin/env python3
"""
Functions to compare specifications.
"""

from pathlib import Path

import yaml


def get_module_difference(source_file, target_file) -> dict:
    """Return module set difference (one way) of two specification files."""
    with open(source_file, "r") as f:
        source = yaml.safe_load(source_file)
    with open(target_file, "r") as f:
        target = yaml.safe_load(target_file)

    source_modules: dict = {
        module["name"]: module["versions"] for module in source["modules"]
    }
    target_modules: dict = {
        module["name"]: module["versions"] for module in target["modules"]
    }
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

