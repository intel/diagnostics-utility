.. _select-checks:

=========================
Basic Check Customization
=========================

You can adjust the set of launched checks by using the --select option. Pass
the required Group to run a group of checks or the name of the desired check to
run a single check. Use the "all" keyword to run all checks.

  Note: the checks below are all supported on Linux. For Windows, only the
  `base_system_check`` is supported.


Run all checks
--------------

The command below will run all checks and output the minimum details.

::

  python3 diagnostics.py --select all


**Example output**

::

  Checks results:

  ==========================================================================================================
  Check name: debugger_sys_check
  Description: System check for debugger found in /opt/intel/oneapi/debugger/latest/sys_check/sys_check.sh
  Result status: PASS
  ==========================================================================================================

  ==========================================================================================================

  Check name: oneapi_app_check
  Description: This is a module for getting oneAPI product information.
  Result status: PASS
  ==========================================================================================================

  ...


  21 CHECKS, 21 PASS, 0 FAIL, 0 WARNINGS, 0 ERRORS

  Console output file: /home/test/intel/diagnostics/logs/diagnostics_select_all_hostname_20211123_130044508587.txt
  JSON output file: /home/test/intel/diagnostics/logs/diagnostics_select_all_hostname_20211123_130044508628.json

  The report was generated for the machine: hostname
  by the Diagnostics Utility for Intel® oneAPI Toolkits 2022.1.0


To run all checks and see more detail in the output, add the ``-v`` argument:

::

  python3 diagnostics.py --select all -v

For more information about Verbose options, see :ref:`verbosity`.

**Example output**

  NOTE: The example below only shows a portion of the output.

::

  ======================================================================================================================================================================================================
  Check name: oneapi_app_check
  Description: This check shows version information of installed oneAPI   products.
  ======================================================================================================================================================================================================

  |    APP
  |  ├─oneAPI   Products
  |  │ ├─Intel®   Advisor
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® oneAPI Collective   Communications
  |  │ │   Library
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® Cluster   Checker
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® oneAPI Data Analytics   Library
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® oneAPI Deep Neural Network   Library
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® oneAPI DPC++/C++   Compiler
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® oneAPI DPC++/C++ Compiler &   Intel®
  |  │ │ C++ Compiler   Classic
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® DPC++ Compatibility   Tool
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel® Distribution for   GDB*
  |  │ │ └─Version-----------------------------------10.2.4------------------------INFO
  |  │ ├─Intel® oneAPI DPC++   Library
  |  │ │ └─Version-----------------------------------2021.5.0----------------------INFO
  |  │ ├─IoT Plugins for   Eclipse
  |  │ │ └─Version-----------------------------------2021.4.0----------------------INFO
  |  │ ├─Intel®   Embree
  |  │ │ └─Version-----------------------------------3.13.1------------------------INFO


Run a Group of Checks Using the Type of Check
---------------------------------------------

To run a group of checks, use the Group from :ref:`check-table` for the type of check you want to run. For example, to run all checks with the ``gpu`` Group:

::

  python3 diagnostics.py --select gpu

**Example output**

::

  Checks results:

  =================================================================================================================
  Check name: gpu_backend_check
  Description: This check shows information from OpenCL™ and Intel® oneAPI Level Zero drivers.
  Result status: PASS
  =================================================================================================================

  =================================================================================================================
  Check name: intel_gpu_detector_check
  Description: This check shows which Intel GPU(s) is on the system based on lspci information and internal table.
  Result status: PASS
  =================================================================================================================

  =================================================================================================================
  Check name: hangcheck_check
  Description: This check verifies that the GPU hangcheck option is disabled to allow long-running jobs.
  Result status: PASS
  =================================================================================================================

  =================================================================================================================
  Check name: user_group_check
  Description: This check verifies that the current user is in the same group as the GPU(s).
  Result status: PASS
  =================================================================================================================

  =================================================================================================================
  Check name: gpu_metrics_check
  Description: This check verifies that GPU metrics are good.
  Result status: PASS
  =================================================================================================================

  =================================================================================================================
  Check name: oneapi_gpu_check
  Description: This check runs GPU workloads and verifies readiness to run applications on GPU(s).
  Result status: PASS
  =================================================================================================================

  6 CHECKS, 6 PASS, 0 FAIL, 0 WARNINGS, 0 ERRORS

  Console output file: /home/test/intel/diagnostics/logs/diagnostics_select_gpu_hostname_20211123_130221787054.txt
  JSON output file: /home/test/intel/diagnostics/logs/diagnostics_select_gpu_hostname_20211123_130221787096.json

  The report was generated for the machine: hostname
  by the Diagnostics Utility for Intel® oneAPI Toolkits 2022.1.0


Run a Specific Check
--------------------

To run a specific check, use the check name from the :ref:`check-table` table. For example, to run the gcc version check:

::

  python3 diagnostics.py --select gcc_compiler_check


**Example output**

::

  Checks results:

  ===========================================================================
  Check name: gcc_compiler_check
  Description: This check shows information about the GCC compiler..
  Result status: PASS
  ===========================================================================

  1 CHECK, 1 PASS, 0 FAIL, 0 WARNINGS, 0 ERRORS

  Console output file: /home/test/intel/diagnostics/logs/diagnostics_select_gcc_compiler_check_hostname_20211123_130559427725.txt
  JSON output file: /home/test/intel/diagnostics/logs/diagnostics_select_gcc_compiler_check_hostname_20211123_130559427767.json

  The report was generated for the machine: hostname
  by the Diagnostics Utility for Intel® oneAPI Toolkits 2022.1.0

To view more information about the check, use the verbosity argument (-v): ::


  python3 diagnostics.py --select gcc_compiler_check -v

There are six levels of verbosity. To learn more, see :ref:`verbosity`.

To run a customized list of checks, see :ref:`custom-check`.

