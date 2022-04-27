#!/usr/bin/env python3
"""
Usage:
  pkgr build
  pkgr list

Options:
  -h --help     Show this message
"""

import os
import shutil

import yaml
import pathlib

from docopt import docopt

from pkgr.core import install, log

__version__ = "1.0.0"

# Required binaries for pkgr to function
requirements = ["git", "make", "patch"]


def require(req):
    """Require that binary exists before continuing"""
    for r in req:
        if shutil.which(r) == None:
            log.error(
                f"{r}, which is required for distro to work, was not found in the PATH."
            )


def get_build_options(yml):
    """Get build options from config"""
    build_options = {"sysroot": "sysroot", "working-dir": ".pkgr", "prefix": "bin", "patches": None}
    for key, val in yml.items():
        if key == "build":
            for opt, v in val.items():
                if opt == "prefix" or opt == "patches":
                    v = str(pathlib.Path(v).absolute())
                build_options[opt] = v
    return build_options


def configure_working_directory(opt):
    """Configure working directory"""
    working_dir = opt["working-dir"]
    # Create working directory
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)

    # Create sysroot (if specified)
    if "sysroot" in opt:
        sysroot = opt["sysroot"]
        if not os.path.isdir(sysroot):
            os.mkdir(sysroot)

def main():
    args = docopt(__doc__)
    log.bold(f"pkgr version {__version__}")
    try:
        with open("packages.yml", "r") as f:
            try:
                y = yaml.safe_load(f)
                require(requirements)
                build_options = get_build_options(y)
                configure_working_directory(build_options)
                if "packages" not in y:
                    log.error("No packages specified in packages.yml!")
                for key, val in y.items():
                    # Install packages!
                    if key == "packages":
                        install.install_packages(val, args, build_options)
            except yaml.YAMLError as exc:
                log.error(exc)
                return
    except FileNotFoundError:
        log.error("packages.yml not found in current directory!")
        pass


if __name__ == "__main__":
    main()
