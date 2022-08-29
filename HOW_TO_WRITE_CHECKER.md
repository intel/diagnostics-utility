# How to write Checkers

The Diagnostics Utility for Intel® oneAPI Toolkits uses *checks* to obtain
system information and configuration information to give you a report of
possible problems with your oneAPI installation. You can customize which checks
are run with the use of a *Checker* file.

## Recommendations for the checker content

There is a huge variety of system requirements that are critical for the
installation, launch, and performance of various programs and applications. In
order to get started with creating your own check, you need to:

* determine the area of verification (requirements for a specific program,
general system requirements for working with programs on different layers of
the system etc)
* view checks that already exist in the Diagnostics Utility for
Intel® oneAPI Toolkits.

**Note:** The utility has the ability to run checks
depending on the result of other checks. There are some basic system checks in
the Diagnostics Utility that can be useful for writing custom checks. To find a
detailed description of dependency mechanism, see [`README`](README.md).

### System checks for oneAPI products

Product system checks are a sufficient set of tests, the successful completion
of which allows you to make sure that the system is suitable and ready to use
the product. At the same time, these checks can help identify problems that do
not affect the launch of the product, but affect its operation and the result
obtained.

Below are the various objectives that can be verified in system checks.

**Note:** It describes all the possible options for checks that may be
necessary in various cases. Add only those that are suitable for a specific
case, a specific operating system (Linux, Windows) or the type of system for
its intended purpose (host, target).

* System requirements for product installation.

* The product is installed correctly.

* System requirements for product launch and correct work.

* Basic product launch succeeds with expected result.

* Information about the main characteristics of the product.

  **Note:** Checks can be both verification and informational. Information
  checks only show data that may be useful to the end user.

* System settings that affect product performance.

## Interface requirements

### The check result format

The check should generate the result of launching in JSON format that will be
used for displaying as a check result tree. Any check can have a hierarchical
structure with nested checks of any depth. Each level of the result should
consist of some fields:

* Required: RetVaL is a status of the performed check.
It can be *PASS*, *WARNING*, *FAIL* or *ERROR*. To find a detailed description
of each one, see [`README`](README.md).
* Required: Value is a value or an
information obtained as a result of the check. If there are nested checks on
this level value contains them.
* Optional: Message is an important information
for a user. In general, message contains an information about the error or
failure.
* Optional: Command is a command line or a description of how the
information was obtained for verification or display.
* Optional: HowToFix is a
description of how to fix the problem. It makes sense to fill in this field
when the check has completed with a specific problem that can be fixed quite
specifically.
* Optional: AutomationFix is a command line to fix the problem.
It makes sense to fill in this field when the check has completed with a
specific problem that can be fixed quite specifically.
* Optional: Verbosity is
a level of verbosity of output tree. Some nested checks may have a higher
verbosity level. To find an information about verbosity levels, see
[`README`](README.md). The first level should only contain a *Value* like this:

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

* get_api_version function that returns a pointer to null terminated char
string with version.
* get_check_list function that returns a null-terminated
pointer array of pointers to the *Check* structure. The *Check* structure and
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
    char tags[MAX_STRING_LEN];
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

For an example, see [`C/C++ checker sample`](checkers_samples/c_checker_sample).

### Python checker requirements

Checker should have:

* get_api_version function that returns string value with version.
* get_check_list function that returns list of *CheckMetadataPy* objects where
*run* field consists the name of function that returns *CheckSummary* object.
The *CheckMetadataPy* and *CheckSummary* classes, defined as:

```python
class CheckMetadataPy:
    name: str
    type: str
    tags: str
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

For examples, see [`Python checker sample 1`](checkers_samples/py_checkers_samples/py_checker_sample_1.py)
and [`Python checker sample 2`](checkers_samples/py_checkers_samples/py_checker_sample_2.py).

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
        "merit": 0,
        "timeout": 5,
        "version": 1,
        "run": "how_to_run"
    }
    ```

* *--get_summary* that runs the check and outputs the result summary in format:

    ```json
    {
        "result": "{}"
    }
    ```

* *--get_api_version* that outputs version.

**Note:** Limitations:

* Currently, the only supported type is .sh and .bat.

For an example, see [`Exe checker sample`](checkers_samples/exe_checkers_samples/linux/exe_checker_sample.sh).

## Options to run the checks from the custom checker

You are able to run the checks from the custom checker in two different ways:

* Pass the path to the configuration file with the checker path and check name
by *--config* option.

**Note:** In this case, the utility will load and run the checks with the names
and paths from the config contained in the list of *name* and *path* config
fields.

* Add the checker path or the checkers folder path to the DIAGUTIL_PATH
environment variable manually or pass nessesary paths by *--path* option.

**Note:** In this case, the utility will load all the checks from the given
paths in addition to the checks loaded by default. The set of checks to run
will be determined by the value passed to the *--filter* option. To find an
information about filtering checks, see [`README`](README.md).

## Run samples checkers

Build Diagnostics Utility for Intel® oneAPI Toolkits project, see [HOW_TO_BUILD_THE_PROJECT.md](HOW_TO_BUILD_THE_PROJECT.md)

Linux:

```bash
# Go to `install` directory
$ cd .../applications.validation.one-diagnostics.source
$ cd build/install

# Run sample checks:

$ ./diagnostics.py --config ./configs/sample_config.json

```

Windows:

```powershell
# Go to `install` directory
PS> cd ...\applications.validation.one-diagnostics.source
PS> cd build\install

# Run sample checks:

PS> python diagnostics.py --config ./configs/sample_config.json

```
