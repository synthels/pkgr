import io
import os
import json
import subprocess
import urllib.request

from . import grab, log, build, patch, util
from .dependencies import DependencyGraph

# List of known options
known_options = [
    "name",
    "git",
    "ftp",
    "tag",
    "build",
    "clone-at",
    "separate",
    "dependencies"
]


def ordinal(n):
    """Utility to convert number to ordinal"""
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) *
                                   (n % 10 < 4) * n % 10::4])


def check_package(p):
    """Check package format"""
    for opt in p.keys():
        # Complain if option is unknown
        if opt not in known_options:
            return False
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
            try:
                log.error(
                    f'Couldn\'t parse package "{package["name"]}"!'
                )
            # Hack to catch unnamed packages early
            except KeyError:
                log.error(
                    f'{ordinal(i+1)} package has no name!'
                )
            return
        # While we're at it, we save the package's source directory
        package["source_dir"] = util.get_package_directory(package, opt)
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
        with open(f"{opt['working-dir']}/.cache", 'a+') as cache:
            cache.seek(0)
            try:
                already_installed = json.load(cache)
            except json.decoder.JSONDecodeError:
                # Cache is empty
                pass

        # Try to install packages
        # Note: we open the file again, since opening it as 'r+' at the beginning
        # would mess things up
        with open(f"{opt['working-dir']}/.cache", 'r+') as cache:
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

                # Write new packages to cache
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
