# pkgr

Automatically build, patch and install packages.

## Installation

```bash
# clone the repo
$ git clone https://github.com/synthels/pkgr.git

# change your working directory
$ cd pkgr

# install globally
$ python3 -m pip install .

# You can then invoke pkgr anywhere!
$ python3 -m pkgr
```

## Basic usage

`pkgr` works by parsing a simple YAML file (named `packages.yml`), where you describe your packages and their dependencies. The skeleton of this file consists of:

```yaml
build:
    sysroot: "sysroot" # System root
    working-dir: "working_dir" # Build working directory
    prefix: "prefix" # Binary prefix
    patches: "patches_dir" # Directory where patches can be found

packages:
    # Packages go here
```

Under `packages`, you may list any number of packages you want to install, like this:

```yaml
- name: name # Package name
    clone-at: directory # Where the package will be cloned (relative to build/working-dir)
    git: 'git://sourceware.org/git/binutils-gdb.git' # Git repository (if the source is hosted on git)
    ftp: 'https://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz' # ftp url (if the source is hosted on some random server on the internet)
    tag: 'binutils-2_32' # Git tag (applies only if source is hosted on git)
    dependencies: # Packages which need to be built before this package
        - package1
        - package2
    build:
        # Build options (see USAGE.md)
```

The subcommands are as follows:

```sh
$ python3 pkgr.py --help

Usage:
  pkgr build    Build packages
  pkgr list     List packages

Options:
  -h --help     Show this message
```

For more details, see [`USAGE.md`](https://github.com/synthels/pkgr/blob/master/USAGE.md).
