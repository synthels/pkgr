import os
from . import log, util


def patch_package(package, opt):
    """Patch single package"""
    patches = f"{opt['patches']}/{package['name']}"

    # Just so that execute_command doesn't die,
    # define the build_dir key temporarily
    package["build_dir"] = None
    if os.path.isdir(patches):
        log.patching(package["name"])
        # Apply patches
        for patch in os.listdir(patches):
            cwd = os.getcwd()
            os.chdir(f"{util.get_package_directory(package, opt)}/..")
            util.execute_command(
                package, ["patch", "-p0", "<", f"{patches}/{patch}"], opt)
            os.chdir(cwd)
