#!/usr/bin/env python3
"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

import os
import pathlib
import subprocess

from . import log, util


def install_package(package, opt):
    """Compile, configure and install package"""
    clone_at = util.get_package_directory(package, opt)
    name = package["name"]
    if "build" in package:
        build = package["build"]
        try:
            stages = {
                "configure": "configuring",
                "compile": "compiling",
                "install": "installing"
            }

            # We change our directory to the directory
            # where the installed package resides
            cwd = os.getcwd()
            os.chdir(clone_at)
            for stage in stages:
                if stage in build:
                    log.info(f"{stages[stage]} {name}...")
                    for args in build[stage]:
                        if util.execute_command(package, args, opt) != 0:
                            raise ValueError(f"Couldn't run {' '.join(util.parse(args, package, opt))}")
            # Go back to root
            os.chdir(cwd)

        # Maybe a bit too generic for this, but it gets the job done
        except Exception as e:
            log.error(f"Couldn't build {name}! ({e})")
            exit(1)
