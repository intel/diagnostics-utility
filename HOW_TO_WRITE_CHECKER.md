# Diagnostic Utility Concepts

The Diagnostics Utility for oneAPI uses two basic concepts:

| Concept  | Description |
|:---------|:------------|
| *check*  | Information or a requirement that is extracted from the system to avoid potential problems with a oneAPI installation. |
| *checker* | A script or program that implements a check. |

Checks are used for:

* Requirement verification.
* Information reports.

## Content Recommendations

* Determine the general requirements for the solution, as well as
  specific requirements for individual components.
* Information checks should only show data that will be useful to the user.
* Before implementing new checks, review checks that already exist
  in the Diagnostics Utility for oneAPI.

The Diagnostic Utility has the ability to run checks that depend on the
result of other checks. There are some basic system checks that can be useful
for writing custom checks. To find a detailed description of dependency
mechanisms, see the [`README`](README.md).

### Checks for oneAPI Products

Product system checks are a set of tests that ensure that the system is
suitable and ready to use the product. At the same time, these checks can
help identify problems that do not affect the launch of the product, but
affect its operation and the obtained results.

Below is a list of various objectives that can be formulated as checks.

This list suggests options for checks that may be possible in
a variety of practical scenarios; Add only those that are relevant for your
specific case, a specific operating system (Linux, Windows) or the type of
system for its intended purpose (host, target):

* System requirements for product installation.
* Infrastructure to confirm that the product is installed correctly.
* Configuration requirements for product launch and correct product functionality.
* Basic product launch succeeds with expected result.
* Useful information about the main characteristics of the product.
* System settings that affect product performance.

### Result Format

* The check should generate the result in JSON format. This format will be
  used to display the check results in a tree.
* Any check can have a hierarchical structure with nested checks of any depth.
* Each level of the check hierarchy should consist of some fields; Required fields are marked with an asterisk (`*`):

| Field           | Description |
|:----------------|:------------|
| `CheckStatus`\* | Status of performed check (`PASS`, `FAIL`, `INFO`, `WARNING`, or `ERROR`).|
| `CheckResult`\* | Information obtained as a result of the check. Nested checks are listed in this field.|
| `Message`       | Important information for a user. In general, this is information about an error or failure.|
| `Command`       | Command line or a description of how the information was obtained for verification or display.|
| `HowToFix`      | Suggestion on how to fix the problem. Use when the check has completed with a problem that has a distinct prescription to fix.|
| `AutomationFix` | Command line that can fix the problem. Use when the check has completed with a problem addressed by this command.|
| `Verbosity`     | The level of verbosity required to reveal this branch of the check tree;  Nested checks may have a higher verbosity number, so they stay hidden depending on the verbosity level. |

Consult the [`README`](README.md) documentation for more information on:

* Descriptions on the status of a check.
* Nested checks and verbosity.

Example:
  
A check tree with one level of hierarchy (created by the `CheckResult` field) could
look like this:

```json
{
  "CheckResult": {
    "name_of_check": {
      "CheckStatus": "PASS",
      "Verbosity": 0,
      "Message": "Some message",
      "CheckResult": {
        "name_of_sub_check": {
          "CheckStatus": "PASS",
          "Verbosity": 0,
          "Message": "Some message",
          "CheckResult": "Received value"
        }
      }
    }
  }
}
```

### Script Checker Requirements

A shell script-based checker should implement three command line options:

* `--get_metadata` option: this should return the check metadata with the following fields:

    ```json
    {
      "name": "name_of_check_without_spaces",
      "type": "",
      "groups": "group1,group2,group3",
      "descr": "Description of check",
      "dataReq": "{}",
      "merit": 0,
      "timeout": 5,
      "version": 1,
      "run": "how_to_run"
    }
    ```

* `--get_summary` option: this option runs the check, and returns the result summary as follows:

    ```json
    {
      "result": {}
    }
    ```

* `--get_api_version` option: this options simply returns the version of the
implemented API:

    ```txt
    0.2
    ```

| /!\ Warning |
|:------------|
| Currently, the only supported type is `.sh` and `.bat`. |

For an example, see [`Shell script checker example`](checkers_exe/linux/example_exe_checker.sh).

### C++ Checker Requirements

Checker should have:

* `get_api_version` function that returns a pointer to null terminated char
  string with version.
* `get_check_list` function that returns a null-terminated
  pointer array of pointers to the `Check` structure. The `Check` structure and
  related structures, defined as:

```cpp
struct Check
{
  struct CheckMetadata metadata;
  struct CheckResult (*run)(char *);
};

struct CheckMetadata
{
  char name[MAX_STRING_LEN];
  char type[MAX_STRING_LEN];
  char groups[MAX_STRING_LEN];
  char descr[MAX_STRING_LEN];
  char dataReq[MAX_STRING_LEN];
  int merit;
  int timeout;
  int version;
};

struct CheckResult
{
  char * result;
};
```

For an example, see [`C++ checker example`](checkers_c/example_c_checker).

### Python Checker Requirements

The checker should have:

* `get_api_version` function that returns string value with version.
* `get_check_list` function that returns list of `CheckMetadataPy` objects where
  `run` field consists the name of function that returns `CheckSummary` object.

The `CheckMetadataPy` and `CheckSummary` classes, defined as:

```python
class CheckMetadataPy:
    name: str
    type: str
    groups: str
    descr: str
    dataReq: str
    merit: int
    timeout: int
    version: int
    run: str

class CheckSummary:
    error_code: int
    result: str
```

For examples, see [`Python checker example 1`](checkers_py/example_py_checker_1.py)
and [`Python checker example 2`](checkers_py/example_py_checker_2.py).

## Custom Checker Options

You can to run checks from the custom checker in two different ways:

* Pass the path to the configuration file with the checker path and check name
  using the `--config` option.

| [i] Note |
|:---------|
| In this case, the utility will load and run the checks with the names and paths from the config contained in the list of `name` and `path` config fields. |

* Add the checker path or the checkers folder path to the `DIAGUTIL_PATH`
  environment variable manually or pass the necessary paths using the `--path` option.

| [i] Note |
|:---------|
|In this case, the utility will load all the checks from the given paths in addition to the checks loaded by default. The set of checks to run will be determined by the value passed to the `--select` option. For more information about selecting checks, see [`README`](README.md). |

## Run Example Checks

From root folder:

```bash
# Create `build` directory
$ mkdir build
$ cd build
# Create the build files
$ cmake -DDEV_PACKAGE ..
# Compile C checkers and install tool
$ make install
# The install directory should be in the build directory
$ cd install
```

Run example checks:

* Run checks for all examples:

    ```bash
    ./diagnostics.py --select example
    ```

* Run check by check name:

    ```bash
    ./diagnostics.py --select example_c_check
    ```
