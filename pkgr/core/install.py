#!/usr/bin/env python3
"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

import io
import os
import json
import subprocess
import urllib.request

from . import grab, log, build, patch
from .dependencies import DependencyGraph


def ordinal(n):
    """Utility to convert number to ordinal"""
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) *
                                   (n % 10 < 4) * n % 10::4])


def check_package(p):
    """Check package format"""
    return (("name" in p) and (("git" in p) ^ ("ftp" in p)))


def dump_to_cache(d, cache):
    """Dump data to cache"""
    cache.seek(0)
    json.dump(d, cache)
    cache.truncate()


def install_packages(packages, args, opt):
    """Install packages"""
    order = []
    packages_dict = {}

    # Convert list of packages to dictionary
    for i, package in enumerate(packages):
        if not check_package(package):
            log.error(
                f"Invalid package format! (while parsing {ordinal(i + 1)} package)"
            )
            return
        packages_dict[package["name"]] = package

    # Get correct installation order
    deps = DependencyGraph(packages_dict)
    order = deps.resolve_dependencies()
    if args["list"]:
        log.println("Packages will be installed in the following order:")
        for package in order:
            log.println(f" - {package['name']}")
        return

    # Clone/retrieve source code for each package
    if args["build"]:
        # Attempt to read cache
        already_installed = {}
        with open(f"{opt['working-dir']}/cache.json", 'a+') as cache:
            cache.seek(0)
            try:
                already_installed = json.load(cache)
            except json.decoder.JSONDecodeError:
                # Cache is empty
                pass

        # Try to install packages
        # Note: we open the file again, since opening it as 'r+' at the beginning
        # would mess things up
        with open(f"{opt['working-dir']}/cache.json", 'r+') as cache:
            for package in order:
                name = package["name"]
                if name not in already_installed:
                    log.installing(name)
                    grab.get_source(package, opt)
                    # Patch package
                    if opt["patches"] != None:
                        patch.patch_package(package, opt)
                else:
                    continue

                # Sync cache
                already_installed[name] = "installed"
                dump_to_cache(already_installed, cache)

            # Build packages
            for package in order:
                name = package["name"]
                if name in already_installed:
                    if already_installed[name] != "built":
                        if build.install_package(package, opt):
                            already_installed[name] = "built"
                            dump_to_cache(already_installed, cache)
                    else:
                        log.skipping(name)
