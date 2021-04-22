#!/usr/bin/env python3
"""
Python utility to generate specification from existing specification file and environment.

The existing specification file is required because build order is defined there.
The targeted environment must either be loaded, else you can just set the environment variables:

.. codeblock:: sh

    $EPICS_BASE
    $E3_REQUIRE_NAME
    $E3_REQUIRE_VERSION

"""

import datetime
import re
import sys
from argparse import ArgumentParser
from os import environ
from pathlib import Path

import yaml

REQUIRED_ENV_VARS = [
    "EPICS_BASE",
    "E3_REQUIRE_NAME",
    "E3_REQUIRE_VERSION",
]


def generate_specification(args) -> None:
    """Generate specification file from existing specification."""
    if not all(environ.get(var) for var in REQUIRED_ENV_VARS):
        print(
            f"You need to first source an e3 environment, or set the environment variables {REQUIRED_ENV_VARS}.",
            file=sys.stderr,
        )
        sys.exit(-1)
    base_version: str = environ.get("EPICS_BASE").split("-")[-1]
    require_version: str = environ.get("E3_REQUIRE_VERSION")
    sitemods_path = (
        Path(environ.get("EPICS_BASE")) / "require" / require_version / "siteMods"
    )
    if not sitemods_path.exists():
        print("The defined environment does not exist.", file=sys.stderr)
        sys.exit(-1)

    if args.infile:
        try:
            with open(args.infile, "r") as f:
                specification: dict = yaml.safe_load(f)
        except FileNotFoundError:
            print("You need a valid (existing) specification file.", file=sys.stderr)
            sys.exit(-1)
        specification["config"]["base"] = None
        specification["config"]["require"] = None
        specification["config"]["cct"] = None
        try:
            ordered: bool = specification["meta"]["ordered"]
        except KeyError:
            ordered: bool = False
        infile: Path = args.infile
        for module in specification["modules"]:
            module_path = sitemods_path / module["name"]
            if module_path.exists():
                module["versions"] = [
                    re.sub(r"\+\d+", r"", version.name)
                    for version in module_path.iterdir()
                ]
            else:
                module["versions"] = [None]

        specification["removed_modules"]: list = []
        module_names = [module["name"] for module in specification["modules"]]
        for module in sitemods_path.iterdir():
            if module.stem not in module_names:
                specification["removed_modules"].append({"name": module.stem})
            # todo: add version, and order items according to name
    else:
        specification = dict()
        ordered: bool = False
        infile: Path = None
        specification["config"]: dict = {
            "base": base_version,
            "require": require_version,
            "cct": None,
        }
        specification["modules"]: list = []
        modules = dict()
        for module in sitemods_path.iterdir():
            modules[module.stem]: list = [
                re.sub(r"\+\d+", r"", version.name) for version in module.iterdir()
            ]
        for module, versions in modules.items():
            specification["modules"].append({"name": module, "versions": versions})

    specification["meta"] = {
        "environment": sitemods_path.parent.as_posix(),
        "datestamp": datetime.datetime.now().isoformat(),
        "ordered": ordered,
        "infile": infile,
    }
    # todo: add info also about version of this package?

    with open(args.outfile, "w") as f:
        yaml.dump(specification, f, default_flow_style=False)


def main():
    parser = ArgumentParser(
        description="Support utility to create specification. Requires sourcing an e3 environment."
    )
    parser.add_argument("-i", "--infile", help="specification file")
    parser.add_argument("-o", "--outfile", required=True, help="specification file")

    args = parser.parse_args()
    generate_specification(args)


if __name__ == "__main__":
    main()

