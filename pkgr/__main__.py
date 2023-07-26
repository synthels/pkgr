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

from pkgr.core import install, log, util

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


def parse_sysroot(opt):
    """Parse sysroot options"""
    if opt is None:
        log.error("No directories declared under sysroot!")
        exit(1)

    # Hack alert!
    # We handle this separately, in order to support both the
    # sysroot: 'str' syntax and the tree-like syntax
    if isinstance(opt, str):
        util.mkdir(opt)
        return str(pathlib.Path(opt).absolute())

    # Create subdirectories
    base = str(pathlib.Path(opt[0]).absolute())
    try:
        util.mkdir(base)
        for i in opt[1:]:
            util.mkdir(os.path.join(base, i))
        return base
    except OSError as e:
        log.error(f"Couldn't create sysroot! ({e})")
        exit(1)

    return base


def get_build_options(yml):
    """Get build options from config"""
    build_options = {
        "sysroot": "sysroot", 
        "working-dir": ".pkgr", "prefix": "bin",
        "patches": None, 
        "project_dir": str(pathlib.Path(os.getcwd()).absolute())
    }

    for key, val in yml.items():
        if key == "build":
            for opt, v in val.items():
                try:
                    if opt in ["prefix", "patches"]:
                        v = str(pathlib.Path(v).absolute())
                    # Parse sysroot options
                    elif opt == "sysroot":
                        v = parse_sysroot(v)
                    build_options[opt] = v
                except TypeError:
                    # Hacky, but gets the job done,
                    # what can i say
                    log.error(f"Couldn't parse {opt}!")
                    exit(1) # Return prints a stacktrace. Why am I
                            # still allowed to write python?
    return build_options


def configure_working_directory(opt):
    """Configure working directory"""
    util.mkdir(opt["working-dir"])


def main():
    args = docopt(__doc__)
    log.bold(f"pkgr version {__version__}")
    try:
        with open("packages.yml", "r") as f:
            # Get build options from YAML
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
