#!/usr/bin/env python3
"""
Functions to compare specifications.
"""


def get_module_difference(source_modules: dict, target_modules: dict) -> dict:
    """Return module set difference (one way) of two specifications."""
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
