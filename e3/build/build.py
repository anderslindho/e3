#!/usr/bin/env python3
"""
Python utility to build and to generate configuration files from a specification.
"""

import sys
from pathlib import Path

import yaml

from e3.gitlab.core import get_module_url  # noqa: F401

# todo: replace print with logging


def clone_modules(root_path: Path, modules: dict) -> None:
    """
    Clone modules to defined location.

    :param root_path: Path to clone to
    :param modules: Modules to clone
    """
    print("Cloning repositories")
    for module in modules:
        try:
            git_url = module["git_url"]
        except KeyError:
            git_url = "Fake"
        module_clone_path = root_path / module["name"]
        if not module_clone_path.exists():
            print(f"Fake cloning {git_url} to folder {module_clone_path}")
        else:
            print(f"Module {module['name']} already exists")


def create_local_files(
    root_path: Path, build_dir: Path, base_ver: str, require_ver: str
) -> None:
    """
    Create a RELEASE.local file

    :param root_path: Path (directory) to create file in
    :param build_dir: Target build directory
    :param base_ver: Version of EPICS base
    :param require_ver: Version of *require*
    """
    print("Setting up configuration files")
    # todo: define files elsewhere ?
    release_local = f"""
EPICS_BASE:={build_dir.as_posix()}/base-{base_ver}
E3_REQUIRE_VERSION:={require_ver}
"""
    with open(root_path / "RELEASE.local", "w") as f:
        f.write(release_local)
    # todo: create also CONFIG_BASE.local


def create_tree(
    root_path: Path, base_ver: str, require_ver: str, modules: list
) -> None:
    """
    Build all versions of modules.

    :param root_path: Target build directory
    :param base_ver: Version of EPICS base
    :param require_ver: Version of *require*
    :param modules: Modules to build
    """
    print("Building...")
    base_path = root_path / f"base-{base_ver}" / "require" / require_ver
    for module in modules:
        if not module["versions"]:
            print(
                f"{module['name']} has no defined versions. Skipping.", file=sys.stderr
            )
            continue
        for version in module["versions"]:
            print(base_path / module["name"] / version)


def build(
    specification_file,
    build_dirs: list = None,
    clone_dir: Path = None,
    clone: bool = True,
    create_local: bool = True,
) -> None:
    """Build modules from specification."""
    package_path = Path(__file__).parent.absolute()
    if clone and clone_dir is None:
        clone_dir = package_path / "modules"
    if build_dirs is None:
        build_dirs = [package_path / "build"]

    with open(specification_file, "r") as f:
        specification = yaml.safe_load(f)

    base_version: str = specification["config"]["base"]
    require_version: str = specification["config"]["require"]
    modules: list = specification["modules"]
    if not base_version or not require_version or not modules:
        print(
            "You need to have EPICS base and require versions defined, and you need to have at least one module in the list.",
            file=sys.stderr,
        )
        sys.exit(-1)

    def exit_because_not_ordered():
        print(
            "This specification is not ordered and thus cannot be built.",
            file=sys.stderr,
        )
        sys.exit(-1)

    try:
        ordered = specification["meta"]["ordered"]
    except KeyError:
        exit_because_not_ordered()
    if not ordered:
        exit_because_not_ordered()

    print("You will build")
    print(f"EPICS base version: {base_version}")
    print(f"require version: {require_version}")
    try:
        print(f"Cross-compiler toolchain version: {specification['config']['cct']}")
    except KeyError:
        pass
    print("\nFor locations:")
    for build_dir in build_dirs:
        print(f"- {Path(build_dir)}")

    if input("\nConfirm (y/n): ").lower() in ("y", "yes"):
        if clone or create_local:
            try:
                clone_dir.mkdir(parents=True)
            except FileExistsError:
                pass
            else:
                print(f"Directory {clone_dir} created.")

        for build_dir in build_dirs:
            if clone:
                clone_modules(root_path=clone_dir, modules=modules)
            if create_local:
                create_local_files(
                    root_path=clone_dir,
                    build_dir=build_dir,
                    base_ver=base_version,
                    require_ver=require_version,
                )
            create_tree(
                root_path=Path(build_dir),
                base_ver=base_version,
                require_ver=require_version,
                modules=modules,
            )
