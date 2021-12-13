.. _filter-checks:

=========================
Basic Check Customization
=========================

You can adjust the set of launched checks by using the --filter option. Pass the required Tag to run a group of
checks or the name of the desired check to run a single check. Use the "all" keyword to run all checks.


Run all checks
--------------

The command below will run all checks and output the minimum details.

::

  python3 diagnostics.py --filter all


**Example output**

::

  Checks results:

  =============================================================================================================================================================================================================
  Check name: debugger_sys_check
  Description : System check for debugger found in /opt/intel/oneapi/debugger/latest/sys_check/sys_check.sh
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================

  Check name: oneapi_app_check
  Description : This is a module for getting oneAPI product information.
  Result status: PASS
  =============================================================================================================================================================================================================

  ...


  21 CHECKS, 21 PASSED, 0 FAILED, 0 WARNING, 0 ERROR

  Console output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141425.txt
  JSON output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141425.json


To run all checks and see more detail in the output, add the ``-v`` argument:

::

  python3 diagnostics.py --filter all -v

For more information about Verbose options, see :ref:`verbosity`.

**Example output**

  NOTE: The example below only shows a portion of the output.

::

  ======================================================================================================================================================================================================
  Check name: oneapi_app_check
  Description : This check shows version information of installed oneAPI   products.
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

To run a group of checks, use the Tag from :ref:`check-table` for the type of check you want to run. For example, to run all checks with the ``gpu`` Tag:

::

  python3 diagnostics.py --filter gpu

**Example output**

::

  Checks results:

  =============================================================================================================================================================================================================
  Check name: gpu_backend_check
  Description : This is a module for getting GPU information.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: vtune_check
  Description : Check system set up for GPU analysis.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: intel_gpu_detector_check
  Description : Detect which Intel GPU is on the system.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: hangcheck_check
  Description : Check that GPU hangcheck is disabled to allow long-running jobs.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: user_group_check
  Description : Check that the current user is in the same group as the GPU(s).
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: gpu_metrics_check
  Description : Check that GPU metrics are good.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: oneapi_gpu_check
  Description : Contains information about the readiness to run GPU workloads.
  Result status: PASS
  =============================================================================================================================================================================================================

  =============================================================================================================================================================================================================
  Check name: advisor_check
  Description : Check is setting up an environment to analyze GPU kernels.
  Result status: PASS
  =============================================================================================================================================================================================================

  8 CHECKS, 8 PASSED, 0 FAILED, 0 WARNING, 0 ERROR

  Console output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141635.txt
  JSON output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141635.json


Run a Specific Check
--------------------

To run a specific check, use the check name from the :ref:`check-table` table. For example, to run the gcc version check:

::

  python3 diagnostics.py --filter gcc_version_check


**Example output**

::

  Checks results:

  =============================================================================================================================================================================================================
  Check name: gcc_version_check
  Description : Contains information about GCC compiler version.
  Result status: PASS
  =============================================================================================================================================================================================================

  1 CHECKS, 1 PASSED, 0 FAILED, 0 WARNING, 0 ERROR

  Console output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141832.txt
  JSON output file: /home/test/intel/diagnostics/diagnostics_nnladtldev-01_20210831-141832.json

To view more information about the check, use the verbosity argument (-v): ::


  python3 diagnostics.py --filter gcc_version_check -v

There are six levels of verbosity. To learn more, see :ref:`verbosity`.

To run a customized list of checks, see :ref:`custom-check`.

