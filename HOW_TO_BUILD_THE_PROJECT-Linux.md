# How to build the project

## Install dependencies

### Project dependencies

1. Install system development packages:

    ```bash
    $ sudo apt update
    # Build tools
    $ sudo apt install cmake
    # Database
    $ sudo apt install libsqlite3-dev
    # Documentation
    $ sudo apt install doxygen graphviz sphinx-common
    ```

Please note that the required package is named "libsqlite3-dev" on Ubuntu,
but it may have a different name if you are using another OS: on
SLES/SuSE system the package name is sqlite3-devel, on RHEL the package
name is sqlite-libs.x86_64, and on RedHat the package name is
libsqlite3x-devel.

2. Install GPGPU level-zero API (instructions derived from [Installation Guide](https://dgpu-docs.intel.com/installation-guides/index.html)):

    ```bash
    # Convenience variables
    $ key=/usr/share/keyrings/intel-graphics.gpg
    $ rep_key=https://repositories.intel.com/graphics/intel-graphics.key
    $ rep_url=https://repositories.intel.com/graphics/ubuntu
    $ rep_options="arch=amd64 signed-by=$key"
    $ rep_list=/etc/apt/sources.list.d/intel.list
    # Download and install ascii-armored key
    $ curl $rep_key | sudo gpg --dearmor --yes --output $key
    # Add Intel repository to the apt source list
    $ echo "deb [$rep_options] $rep_url focal main" | sudo tee -a $rep_list
    $ sudo apt update
    # Download and install the developer packages
    $ sudo apt install \
      level-zero-dev
    ```

3. Install OpenCL API headers:

    ```bash
    sudo apt install opencl-headers 
    ```

### Documentation dependencies

* Install Python documentation utilities

    ```bash
    # Go to root directory of git repository
    $ cd .../diagnostics-utility
    # Installing with Python package manager
    $ python3 -m pip install -r docs/requirements.txt
    ```

## Build options

Cmake build options:

| Option             |Default| Description                                    |
|:-------------------|:------|:-----------------------------------------------|
| `‑DBUILD_TESTS=ON` |`OFF`  | Install unit and integration tests in package. |
| `‑DCOVERAGE=ON`    |`OFF`  | Add --coverage flag to C/CPP compilers.        |
| `‑DBUILD_DOCS=ON`  |`OFF`  | Install HTML documentation package.            |

## Build procudure

```bash
# Go to root directory of git repository
$ cd .../diagnostics-utility
# Create a build directory
$ mkdir build
$ cd build
# Create the build files
$ cmake -DOS=LINUX ..
# Compile C checks and install tool
$ make install
```

👉 # The `install` folder should be packed in the  `build` directory.

👉 The application should be available to test in the root directory:

```bash
$ cd .../diagnostics-utility
$ ./diagnostics.py --help
usage: diagnostics.py [--filter FILTER [FILTER ...]] [-l] [-c PATH_TO_CONFIG] [-o PATH_TO_OUTPUT | -t] [-s | -u] [-p PATH [PATH ...]] [--force] [-v] [-V] [-h]

Diagnostics Utility for Intel® oneAPI Toolkits is a tool designed to diagnose the system status for using Intel® software.
...
```
