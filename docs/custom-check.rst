.. _custom-check:

======================================
Personalizing Your Own Group of Checks
======================================

To create your own personal set of checks for diagnosing your system,
use the ``--config`` option. Create the configuration JSON file and specify name of each check file.

- Optional: You can specify the absolute or relative path to check file if this check won't be loaded by default.

An example of a configuration file is in ``configs/sample_config.json``.
It looks similar to this:

::

  [
      {
          "name": "compiler_check"
      },
      {
          "name": "gpu_backend_check"
      }
  ]

Note: A checker file can contain more than one check. You can choose only one by specifying the name.

Find the name and path of each of the checks you wish to run from
the :ref:`check-table` and add each of the checks to the JSON file.

Then run the Diagnostics Utility for oneAPI using the config argument:

::

  python3 diagnostics.py --config configs/sample_config.json

If your config file has a different name or path, change the
`configs/sample_config.json` to the name and path of your config file.

**Example output**

::

  Checks results:

  =============================================================================================
  Check name: compiler_check
  Description: This check shows information about the compiler.
  Result status: PASS
  =============================================================================================

  =============================================================================================
  Check name: gpu_backend_check
  Description: This check shows information from OpenCL™ and Intel® oneAPI Level Zero drivers.
  Result status: ERROR
  Intel® oneAPI Level Zero driver is not initialized
  =============================================================================================

  2 CHECKS, 1 PASS, 0 FAIL, 0 WARNINGS, 1 ERROR

  Console output file: /home/test/intel/diagnostics/logs/diagnostics_config_example_config_hostname_20211123_103737097543.txt
  JSON output file: /home/test/intel/diagnostics/logs/diagnostics_config_example_config_hostname_20211123_103737097593.json

  The report was generated for the machine: hostname
  by the Diagnostics Utility for oneAPI 2024.2.0

