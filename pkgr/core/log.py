from colored import fg, attr


def installing(name):
    """Print installation message"""
    print(f"Installing {fg('green')}{name}{attr('reset')}...")


def skipping(name):
    """Print skipping message"""
    print(
        f"Skipping {fg('orange_1')}{name}{attr('reset')}, as it is already built."
    )


def patching(name):
    """Print patching message"""
    print(f"Patching {fg('green')}{name}{attr('reset')}...")


def bold(msg):
    """Print bold message"""
    print(f"{attr('bold')}{msg}{attr('reset')}")


def println(msg):
    """Normal print equivalent"""
    print(msg)


def error(msg):
    """Log a fatal error"""
    print(f"{fg('red')}Error: {msg}{attr('reset')}")


def info(msg):
    """Print in one level of indentation"""
    print(f"{fg('light_blue')}{attr('bold')}info{attr('reset')} {msg}")
