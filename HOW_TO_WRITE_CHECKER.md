# How to write the checkers

The Diagnostics Utility for Intel® oneAPI Toolkits has the ability to run and output the results of your own checks.
To ensure the correct interaction of the tool with checkers - files of checks, you must adhere to a unified interface.

## Interface requirements

### The check result format

The check should generate the result of launching in JSON format that will be used for displaying as a check result tree. Any check can have a hierarchical structure with nested checks of any depth. Each level of the result should consist of some fields:
* Required: RetVaL is the status of the performed check. It can be *PASS*, *WARNING*,  *FAIL* or *ERROR*. To find a detailed description of each one, see [`README`](README.md).
* Required: Value is the value or information obtained as a result of the check. If there are nested checks on this level value contains them.
* Optional: Message is an important information for a user. In general, message contains an information about the error or failure.
* Optional: Verbosity is a level of verbosity of output tree. Some nested checks may have a higher verbosity level. To find an information about verbosity levels, see [`README`](README.md).
The first level should only contain a *Value* like this:

```json
{
    "Value": {
        "name_of_check": {
            "RetVal": "PASS",
            "Verbosity": 0,
            "Message": "Some message",
            "Value": {
                "name_of_sub_check": {
                    "Value": "Received value",
                    "Verbosity": 0,
                    "Message": "Some message",
                    "RetVal": "PASS"
                }
            }
        }
    }
}
```
### C++ checker requirements

Checker should have:

* get_api_version function that returns a pointer to null terminated char string with version.
* get_check_list function that returns a null-terminated pointer array of pointers to the *Check* structure. The *Check* structure and related structures, defined as:

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
    char tags[MAX_STRING_LEN];
    char descr[MAX_STRING_LEN];
    char dataReq[MAX_STRING_LEN];
    char rights[MAX_STRING_LEN];
    int timeout;
    char version[MAX_STRING_LEN];
};

struct CheckResult
{
    char * result;
};
```


For an example, see [`C checker example`](checkers_c/example_c_checker).

### Python checker requirements

Checker should have:

* get_api_version function that returns string value with version.
* get_check_list function that returns list of *CheckMetadataPy* objects where *run* field consists the name of function that returns *CheckSummary* object. The *CheckMetadataPy* and *CheckSummary* classes, defined as:

```python
class CheckMetadataPy:
    name: str
    type: str
    tags: str
    descr: str
    dataReq: str
    rights: str
    timeout: int
    version: str
    run: str

class CheckSummary:
    error_code: int
    result: str
```

For examples, see [`Python checker example 1`](checkers_py/example_py_checker_1.py) and [`Python checker example 2`](checkers_py/example_py_checker_2.py).

### Executable checker requirements

Checker should have:

* *--get_metadata* option that outputs the check metadata in format:

      ```json
      {
          "name": "name_of_check_without_spaces",
          "type": "",
          "tags": "tag1,tag2,tag3",
          "descr": "Description of check",
          "dataReq": "{}",
          "rights": "admin_or_user",
          "timeout": 5,
          "version": "1",
          "run": "how_to_run"
      }
      ```
* *--get_summary* that runs the check and outputs the result summary in format:

      ```json
      {
          "error_code": 0,
          "result": "{}"
      }
      ```

* *--get_api_version* that outputs version.

**Note:** Limitations:
* Currently, the only supported type is .sh.
* 


For an example, see [`Exe checker example`](checkers_exe/example_exe_checker.sh).

## Options to run the checks from the custom checker

You are able to run the checks from the custom checker in two different ways:

* Pass the path to the checker by *--single_checker* option.
* Pass the path to the configuration file with the checker path by *--config* option.

## Run examples checkers

From root folder:

1. Create `build` directory:

    ```bash
    mkdir build
    ```

1. Go to `build` directory:

    ```bash
    cd build
    ```

1. Create the build files:

    ```bash
    cmake -DDEV_PACKAGE ..
    ```

1. Compile C checkers and install tool:

    ```bash
    make install
    ```

    **Note:** `install` folder should be in the `build` directory.

1. Go to `install` directory:

    ```bash
    cd install
    ```

1. Run example checks:

    Run checks for all examples:

      ```bash
      ./diagnostics.py --filter example
      ```

    Run checks from the checker by the single checker option:

      ```bash
      ./diagnostics.py --single_checker ./checkers_c/libexample_c_checker.so
      ```

    Run check by check name:

      ```bash
      ./diagnostics.py --filter example_c_check
      ```
