#!/usr/bin/env python3
"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

import os
from . import log, util


def patch_package(package, opt):
    """Patch single package"""
    patches = f"{opt['patches']}/{package['name']}"
    if os.path.isdir(patches):
        log.patching(package["name"])
        # Apply patches
        for patch in os.listdir(patches):
            cwd = os.getcwd()
            os.chdir(f"{util.get_package_directory(package, opt)}/..")
            util.execute_command(package, ["patch", "-p0", "<", f"{patches}/{patch}"], opt)
            os.chdir(cwd)
