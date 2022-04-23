#!/usr/bin/env python3
"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

import os
import subprocess


def get_cores():
    """Get a good approximation on available cores"""
    try:
        cpus = os.sched_getaffinity(0)
    except AttributeError:
        return os.cpu_count()
    return len(cpus)


def parse(commands, package, opt):
    """Parse commands and replace variables with their values"""
    variables = {
        "%CORES": str(get_cores()),
        "%PREFIX": opt["prefix"],
        "%SYSROOT": opt["sysroot"]
    }

    for i, c in enumerate(commands):
        for s in variables:
            commands[i] = commands[i].replace(s, variables[s])
    return commands


def execute_command(package, args, opt):
    """Execute command after parsing it"""
    parsed = parse(args, package, opt)
    subprocess.call(" ".join(parsed), shell=True)


def get_package_directory(package, opt):
    """Get package's directory"""
    directory = opt['working-dir']
    if "clone-at" in package:
        directory = f"{directory}/{package['clone-at']}"
    return f"{directory}/{package['name']}"
