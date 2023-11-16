# How to build the project

## Install dependencies

### Project dependencies

1. Install Visual Studio with Spectre-mitigated libraries
2. Install CMake

### Documentation dependencies

  1. Go to the root directory of the git repository
  2. Run the following command:

     ```bash
     # Installing with Python package manager
     $ python3 -M pip install -r docs/requirements.txt
     ```

## Build options

Cmake build options:

| Option             |Default| Description                                    |
|:-------------------|:------|:-----------------------------------------------|
| `‑DBUILD_TESTS=ON` |`OFF`  | Install unit and integration tests in package. |
| `‑DCOVERAGE=ON`    |`OFF`  | Add --coverage flag to C/CPP compilers.        |
| `‑DBUILD_DOCS=ON`  |`OFF`  | Install HTML documentation package.            |

## Build procudure

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

```powershell
PS> cd .../applications.validation.one-diagnostics.source
PS> python diagnostics.py --help
usage: diagnostics.py [--select SELECTION [SELECTION ...]] [-l] [-c PATH_TO_CONFIG] [-o PATH_TO_OUTPUT | -t] [-u] [-p PATH [PATH ...]] [--force] [-v] [-V] [-h]

Diagnostics Utility for Intel® oneAPI Toolkits is a tool designed to diagnose the system status for using Intel® software.
...
```
