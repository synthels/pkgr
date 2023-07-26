import os
import subprocess
import urllib.request
import tarfile

from . import log


def from_git(package, clone_at):
    """Grab source from git repository"""
    if "tag" in package:
        repo = ("--depth", "1", "--branch", f"{package['tag']}",
                f"{package['git']}")
    else:
        repo = ("--depth", "1", package["git"])
    p = subprocess.run(
        ["git", "clone", *repo, f"{clone_at}/{package['name']}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    # Did we actually clone anything?
    if p.returncode != 0:
        log.error(
            f"Couldn't clone {package['git']}! (exit code: {p.returncode})")
        exit(1)


def from_ftp(package, clone_at):
    """Grab package from random url"""
    # urlretrieve complains if the directory we give
    # it doesn't exist...
    cloned_at = f"{clone_at}/{package['name']}"
    if not os.path.isdir(clone_at):
        os.makedirs(clone_at)
    urllib.request.urlretrieve(package["ftp"], f"{cloned_at}.tar.gz")

    # We assume (WLOG) that the file is a tarball!
    tar = tarfile.open(f"{cloned_at}.tar.gz", "r:gz")
    tar.extractall(path=clone_at)
    extracted = os.path.commonprefix(tar.getnames())
    tar.close()

    # Remove tar file and rename extracted archive to package name!
    os.remove(f"{cloned_at}.tar.gz")
    os.rename(f"{clone_at}/{extracted}", f"{clone_at}/{package['name']}")


def get_source(package, opt):
    """Get package source"""
    # Where do we clone the source?
    clone_at = opt['working-dir']
    if "clone-at" in package:
        clone_at = f"{clone_at}/{package['clone-at']}"

    # Git or ftp??
    if "git" in package:
        from_git(package, clone_at)
    elif "ftp" in package:
        from_ftp(package, clone_at)
