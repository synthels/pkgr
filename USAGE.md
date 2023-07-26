# Usage

A typical use case for `pkgr` is installing a bunch of packages and building them from source, all with one command. The packages are described in a file named `packages.yml`, which must always exist in the root directory where you're calling `pkgr` from.

The header of the file is where you specify basic build options

```yaml
build:
    sysroot: "sysroot"
    working-dir: "working_dir"
    prefix: "prefix"
    patches: "patches_dir"
```

## Sysroot

You can specify a sysroot in two ways. One, you can just specify a directory path like this:

```yaml
sysroot: "path/to/sysroot"
```

This will work just fine and the sysroot will be created if it doesn't already exist. But, if you want to specify multiple nested subdirectories within the sysroot, you can also pass a list of paths.

```yaml
sysroot:
    - "path/to/sysroot"
    - "subdir1/nested-subdir1"
    - "subdir2/nested-subdir2/nested-subdir3"
```

In this case, the first path in the list will be treated as the sysroot (what will be returned by `%SYSROOT`, see [Special variables](#Special-variables)) and every other path will be created relative to this one.

## The other header options

- The `working-dir` field specifies the directory where all of the built packages and their sources will go.
- The `prefix` field specifies the directory relative to `working-dir`, where the built binaries will be installed.
- The `patches` field specifies the directory relative to `working-dir`, where patches for each package can be found. Patches are expected to be laid out under `<patches>/package_name`.

The default values for these fields are as follows:
```py
{
    "sysroot": "sysroot", 
    "working-dir": ".pkgr", 
    "prefix": "bin",
    "patches": None
}
```

## Packages

Under the `build` header is where you specify the packages you would like to be installed, like this:

```yaml
packages:
    - name: name # Package name
      # Options...
```

The options for each package are as follows:

- `git`: If the source is hosted on a git repository, this field specifies the URL to that repository.
- `ftp`: If the source is hosted on an FTP server, this field specifies the URL to the source.
- `tag`: If the `git` field was specified, this field specifies the tag which will be cloned.
- `clone-at`: Where the source will be cloned (applies both to `git` and `ftp`).
- `separate`: If set to `true`, the package's source and build directories will be separate.

## Dependencies

You can also specify a set of dependencies for each package, guaranteeing that the specified dependencies will be built before this package.

```yaml
dependencies:
    - package1
    - package2
    # ...
```

## Building packages

The build process happens in three steps. `configure`, `compile` and `install`. The arguments for each step can be configured under the `build` option for each package.

```yaml
build:
    configure:
        - ['some-command', 'and-arguments', 'more-arguments']
        - ['another-command', 'MORE-ARGUMENTS']
    compile:
        - ['make', '-j%CORES']
    install:
        - ['make', 'install']
```

In every command that is ran, you can expect that the current directory will be set to wherever the current package's source was installed (unless the `separate` option was set, in which case the current directory will be set to the package's build directory). In these commands, you can also use a set of special variables prefixed with `%`.

### Special variables
- `%CORES`: Number of cores available.
- `%PREFIX`: The prefix specified in the header.
- `%SYSROOT`: The sysroot specified in the header.
- `%PROJECT_SOURCE_DIR`: The directory where `pkgr` was called from.
- `%THIS_DIR`: Points to the current package's source directory
- `%BUILD_DIR`: Points to the current package's build directory. (if it exists, otherwise points to the same value as `%THIS_DIR`)
