# How to build the project

## Install dependencies

### Project dependencies

For linux:

1. Install system development packages

   ```bash
      # Make sure that these packages are installed
      # Build tools
      $ sudo apt install cmake
      # Database
      $ sudo apt install libsqlite3-dev
      # Documentation
      $ sudo apt install doxygen graphviz sphinx-common
   ```

For windows:

1. Install Visual Studio with Spectre-mitigated libs
2. Install CMake

### Documentation dependencies

  1. Go to the root directory of the git repository
  2. Run the following command:

     ```bash
     # Installing with Python package manager
     $ pip install -r docs/requirements.txt
     ```

## Build options

Cmake build options:

| Option             |Default| Description                                    |
|:-------------------|:------|:-----------------------------------------------|
| `‑DBUILD_TESTS=ON` |`OFF`  | Install unit and integration tests in package. |
| `‑DCOVERAGE=ON`    |`OFF`  | Add --coverage flag to C/CPP compilers.        |
| `‑DBUILD_DOCS=ON`  |`OFF`  | Install HTML documentation package.            |

## Build procudure

### Linux

```bash
# Go to root directory of git repository
$ cd .../applications.validation.one-diagnostics.source

# Create a build directory
$ mkdir build
$ cd build

# Create the build files
$ cmake -DOS=LINUX ..

# Compile C checks and install tool
$ make install
# The `install` folder should be packed in the  `build` directory
```

### Windows

```powershell
# Go to root directory of git repository
PS> cd ...\applications.validation.one-diagnostics.source

# Create a build directory
PS> md build
PS> cd build

# Create the build files
PS> cmake -DOS=WINDOWS ..

# Compile C checks and install tool
PS> cmake --build . --target INSTALL --config Release
# The `install` folder should be packed in the  `build` directory
```

👉 The application should be available to test in the root directory:

Linux:

```bash
$ cd .../applications.validation.one-diagnostics.source
$ ./diagnostics.py --help
usage: diagnostics.py [--filter FILTER [FILTER ...]] [-l] [-c PATH_TO_CONFIG] [-o PATH_TO_OUTPUT | -t] [-s | -u] [-p PATH [PATH ...]] [--force] [-v] [-V] [-h]

Diagnostics Utility for Intel® oneAPI Toolkits is a tool designed to diagnose the system status for using Intel® software.
...
```

Windows:

```powershell
PS> cd .../applications.validation.one-diagnostics.source
PS> python diagnostics.py --help
usage: diagnostics.py [--filter FILTER [FILTER ...]] [-l] [-c PATH_TO_CONFIG] [-o PATH_TO_OUTPUT | -t] [-s | -u] [-p PATH [PATH ...]] [--force] [-v] [-V] [-h]

Diagnostics Utility for Intel® oneAPI Toolkits is a tool designed to diagnose the system status for using Intel® software.
...
```
