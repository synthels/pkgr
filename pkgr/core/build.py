import os
import pathlib
import subprocess

from . import log, util


def create_build_directory(package, opt):
    """Create build directory for package"""
    clone_at = ""
    if "clone-at" in package:
        clone_at = package["clone-at"]
    path = os.path.join(opt["working-dir"], clone_at, "build", package["name"])
    util.mkdir(path)
    return str(pathlib.Path(path).absolute())


def install_package(package, opt):
    """Compile, configure and install package"""
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
            build_dir = util.get_package_directory(package, opt)
            package["build_dir"] = build_dir
            if "separate" in package:
                if package["separate"]:
                    dirloc = create_build_directory(package, opt)
                    build_dir, package["build_dir"] = [dirloc] * 2

            os.chdir(build_dir)
            for stage in stages:
                if stage in build:
                    log.info(f"{stages[stage]} {name}...")
                    for args in build[stage]:
                        util.execute_command(package, args, opt)
            # Go back to root
            os.chdir(cwd)

        # Maybe a bit too generic for this, but it gets the job done
        except Exception as e:
            log.error(f"Couldn't build {name}! ({e})")
            exit(1)

    return ("build" in package)
