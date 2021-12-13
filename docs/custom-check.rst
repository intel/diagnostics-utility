.. _custom-check:

======================================
Personalizing Your Own Group of Checks
======================================

To create your own personal set of checks for diagnosing your system,
use the --config option. Create the configuration JSON file and specify
the absolute or relative path to each check file.

- Optional: You can specify the name of the check to launch.

An example of a configuration file is in ``configs/example_config.json``.
It looks similar to this:

::

  [
      {
          "name": "gcc_version_check",
          "path": "./checkers_py/gcc_checker.py"
      },
      {
          "name": "gpu_backend_check",
          "path": "./checkers_c/libgpu_backend_checker.so"
      }
  ]

Note: A checker file can contain more than one check. You can choose only one by specifying the name.

Find the name and path of each of the checks you wish to run from
the :ref:`check-table` and add each of the checks to the JSON file.

Then run the Diagnostics Utility for Intel® oneAPI Toolkits using the config argument:

::

  python3 diagnostics.py --config configs/example_config.json

If your config file has a different name or path, change the
`configs/example_config.json` to the name and path of your config file.

**Example output**

::

  Checks results:

  =========================================================================================================================================================================
  Check name: gcc_version_check
  Description : Contains information about GCC compiler version.
  Result status: PASS
  =========================================================================================================================================================================

  =========================================================================================================================================================================
  Check name: gpu_backend_check
  Description : This is a module for getting GPU information.
  Result status: ERROR
  Intel® oneAPI Level Zero driver is not initialized
  =========================================================================================================================================================================

  2 CHECKS, 1 PASSED, 0 FAILED, 0 WARNING, 1 ERROR

  Console output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-132421.txt
  JSON output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-132421.json
