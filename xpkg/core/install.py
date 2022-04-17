#!/usr/bin/env python3

"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

import io
import os
import subprocess
import urllib.request

from . import grab, log
from .dependency_graph import DependencyGraph


def ordinal(n):
    """Utility to convert number to ordinal"""
    return "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def check_package(p):
    """Check package format"""
    return (("name" in p) and (("git" in p) ^ ("ftp" in p)))


def install_packages(packages, args, opt):
    """Install packages"""
    order = []
    packages_dict = {}

    # Convert list of packages to dictionary
    for i, package in enumerate(packages):
        if not check_package(package):
            log.error(
                f"Invalid package format! (while parsing {ordinal(i + 1)} package)")
            return
        packages_dict[package["name"]] = package

    # Get correct installation order
    deps = DependencyGraph(packages_dict)
    order = deps.resolve_dependencies()
    if args["list"]:
        log.info("Packages will be installed in the following order:")
        for package in order:
            print(f" - {package['name']}")
        return

    # Clone/retrieve source code for each package
    if args["build"]:
        with open(f"{opt['working-dir']}/.xpkgcache", 'a+') as cache:
            cache.seek(0)
            already_installed = cache.read().split("\n")
            cache.seek(0, io.SEEK_END)
            for package in order:
                if package["name"] not in already_installed:
                    log.installing(package['name'])
                    grab.get_source(package, opt)
                    # Add package to cache
                    cache.write(f"{package['name']}\n")
                else:
                    log.skipping(package['name'])
        return
