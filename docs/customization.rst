.. _customization:

================================
Diagnostic Utility Check Options
================================


The arguments below describe options for running your check. Multiple
arguments may be added or they can be used one at a time. To use an argument,
follow this syntax:

::

  python3 diagnostics.py ARGUMENT1 ARGUMENT2

For example, to run the GPU detector check with verbosity and only output
to the terminal:

::

  python3 diagnostics.py --select intel_gpu_detector_check -t -v

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Argument
     - Description
     - Example

   * - ``--select``
     - Select checks to run by group or check name.
       Each check can be marked with one or more
       groups. For a full list of available checks and groups, see :ref:`check-table`.
     -  ``python3 diagnostics.py --select oneapi_toolkit_check``

   * - ``--list``
     - Show list of available checks in the terminal window. You can also
       see a list of available checks and groups in :ref:`check-table`.
     -  ``python3 diagnostics.py --list``

   * - ``-c PATH_TO_CONFIG``
     - Path to the JSON config file to run a group of checks or particular check from checkers.
     -  ``python3 diagnostics.py -c configs/sample_config.json``

   * - ``-o PATH_TO_OUTPUT``
     - Path to the folder for saving the console output file and
       the JSON file with the results of the performed checks.
     -  ``python3 diagnostics.py -o $HOME/intel/diagnostics/logs``

   * - ``-t``
     -  Allow output only to the terminal window without saving additional output files.
     -  ``python3 diagnostics.py -t``

   * - ``-u``
     - Download new databases if they are available.
     -  ``python3 diagnostics.py -u``

   * - ``-p``
     - Add paths to environment variable DIAGUTIL_PATH to additionally
       load checks.
     -  ``python3 diagnostics.py -p checkers_py/base_system_checker.py``

   * - ``--force``
     - Force the program to run on any operating system.
     -  ``python3 diagnostics.py --force``

   * - ``-v``
     - Increase the amount of verbosity in the output. This will give more details in the output.
     -  ``python3 diagnostics.py -v``

   * - ``--version``
     - Show program's version.
     -  ``python3 diagnostics.py --version``

   * - ``-h``
     - Show help message.
     -  ``python3 diagnostics.py -h``

For more information about increasing the details in the output,
see :ref:`Verbose Mode Options <verbosity>`.