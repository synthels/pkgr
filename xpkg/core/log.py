#!/usr/bin/env python3

"""
Copyright (c) 2022 synthels
See the file 'LICENSE' for copying permission
"""

from colored import fg, attr


def installing(name):
    """Print installation message"""
    print(
        f"{fg('dark_gray')}[{fg('green')}+{fg('dark_gray')}]{attr('reset')} Grabbing {fg('green')}{name}{attr('reset')}...")


def skipping(name):
    """Print skipping message"""
    print(
        f"{fg('dark_gray')}[{fg('orange_3')}-{fg('dark_gray')}]{attr('reset')} Skipping {fg('orange_3')}{name}{attr('reset')}, as it is already installed.")


def info(msg):
    """Normal print equivalent"""
    print(f"{fg('light_blue')}{msg}{attr('reset')}")


def error(msg):
    """Log an error"""
    print(f"{fg('red')}Error: {msg}{attr('reset')}")
