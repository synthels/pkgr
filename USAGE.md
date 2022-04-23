# Usage

A typical use case for `xpkg` is installing a bunch of packages and building them from source, all with one command. The packages are described in a file named `packages.yml`, which must always exist in the root directory where you're calling `xpkg` from.

The header of the file is where you specify basic build options

```yaml
build:
    sysroot: "sysroot"
    working-dir: "working_dir"
    prefix: "prefix"
    patches: "patches_dir"
```

- The `sysroot` field specifies the system root of the build. If you're not cross compiling, you probably wont ever need this.
- The `working-dir` field specifies the directory where all of the built packages and their sources will go.
- The `prefix` field specifies the directory relative to `working-dir`, where the built binaries will be installed.
- The `patches` field specifies the directory relative to `working-dir`, where patches for each package can be found. Patches are expected to be laid out under `<patches>/package_name`.

The default values for these fields are as follows:
```py
{
    "sysroot": "sysroot", 
    "working-dir": ".xpkg", 
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
- `clone-at`: Where the source will be cloned (applies both on `git` and `ftp`).

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
        - ['make']
    install:
        - ['make', 'install']
```

In every command that is ran, you can expect that the current directory will be set to wherever the current package's source was installed. In these commands, you can also use a set of special variables prefixed with `%`, which will be replaced with their values before being ran.

### Special variables
- `%CORES`: The number of cores that `xpkg` recommends be used with the `-j` option when running `make`.
- `%PREFIX`: The prefix specified on the header.
- `%SYSROOT`: The system root specified on the header.
