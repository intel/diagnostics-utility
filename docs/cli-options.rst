.. _cli-options:

===========
Get Started
===========


To run the Diagnostics Utility for oneAPI:

1. Open a terminal. Put the location of the diagnostic utility in the PATH.
   If you installed your Intel® oneAPI Toolkit in the default directory, then the
   utility will be located in:
   Linux (Component Directory Layout): `/opt/intel/oneapi/diagnostics/`
   Linux (Unified Directory Layout):
   `/opt/intel/oneapi/<toolkit-version>/opt/diagnostics`
   Windows: `C:\Program Files (x86)\Intel\oneAPI\diagnostics`


2. Run the Diagnostics Utility for oneAPI using this syntax:

Linux: ``python3 diagnostics.py --select <ARGUMENT_NAME>``

Windows: ``diagnostics.bat <ARGUMENT NAME>`` or
``diagnostics.ps1 <ARGUMENT NAME>``

To simplify usage of Diagnostics Utility on Windows systems, wrappers for
Windows command prompt and PowerShell have been added. Wrappers are located
in `C:\Program Files (x86)\Intel\oneAPI\diagnostics\<version>\bin`. Usually,
Diagnostics Utility runs using ``python3 diagnostics.py <list of arguments>``.
With wrappers, the utility can be run by calling
``diagnostics.bat <list of arguments>`` or
``diagnostics.ps1 <list of arguments>``. For example:
``diagnostics.bat --select gpu -vvvv`` will run GPU-specific checkers on
Windows, and ``diagnostics.ps1 --list`` will show the full list of
available checks.

The  **select** modifier specifies how many checks to run at one time.
With a select, you can run a :ref:`group of checks<check-table-by-group>`
or a :ref:`single check<check-table>`. In this
example, you will run all available checks, using the ``all`` argument:

::

  python3 diagnostics.py --select all


The output will display in the active console and in:

* a text file (.txt)
* a JSON file (.json)

Checks listed at the top of the list have higher priority and may have
dependent checks further down the list. When diagnosing problems, start by
troubleshooting the checks at the top of the list.

The default directory of the output files is
$HOME/intel/diagnostics/logs for Linux.

.. and C:\\Users\\<username>\\intel\\diagnostics\\logs for Windows.

To customize the default directory, see :ref:`customization`.


To increase the amount of detail, add the -v argument:

::

  python3 diagnostics.py --select all -v


The Diagnostics Utility for oneAPI can be customized to output
only the data you need. Use these methods to customize the command for your
needs:

- :ref:`Run a group of related checks <group-checks>`
- :ref:`Run a single check <single-check>`
- :ref:`Increase the output detail using Verbose Mode <verbosity>`


.. _check-table:


List of Checks by Check Name
----------------------------

Note: the checks below are all supported on Linux. On Windows,
the ``diagnostics.ps1 --list`` command can be used to view the full
list of  available checks.



.. list-table::

   * - **Check Name**
     - the name of the diagnostic check that can be run in the command line.
   * - **Group**
     -  Checks are grouped together so that you can run multiple checks using
        one command. For example, you can run all checks associated with
        GPUs by using the GPU argument.
   * - **Rights**
     - the permissions needed to run this check.
   * - **Description**
     - a short description of the check.


The table below shows the list of  **checks** and which  **groups** can
also be used to run that check.



.. list-table::
   :header-rows: 1

   * - Check Name
     - Groups where check is included
     - Description
   * -  ``hangcheck_check``
     - |  ``gpu``
       |  ``profiling``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check verifies that the GPU hangcheck option is disabled to
       allow long-running jobs.
   * -  ``user_group_check``
     - |  ``default``
       |  ``profiling``
       |  ``gpu``
       |  ``runtime``
       |  ``target``
     - This check verifies that the current user is in the same group
       as the GPU(s).
   * - ``driver_compatibility_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check verifies compatibility of oneAPI products versions and
       GPU drivers versions.
   * -  ``oneapi_gpu_check``
     - |  ``gpu``
       |  ``sysinfo``
     - This check runs GPU workloads and verifies readiness to run
       applications on GPU(s).
   * -  ``gpu_metrics_check``
     - |  ``gpu``
       |  ``runtime``
       |  ``target``
     - This check verifies that GPU metrics are good.
   * -  ``gpu_backend_check``
     - |  ``compile``
       |  ``default``
       |  ``gpu``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows information from OpenCL™ and Intel® oneAPI Level
       Zero drivers.
   * -  ``oneapi_toolkit_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows version information of installed oneAPI products.
   * -  ``intel_gpu_detector_check``
     - |  ``profiling``
       |  ``default``
       |  ``gpu``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows which Intel GPU(s) is on the system based on lspci
       information and internal table.
   * - ``oneapi_env_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows the version information of the oneAPI products
       installed in the environment.
   * -  ``compiler_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``sysinfo``
     - This check shows information about the compiler.
   * -  ``base_system_check``
     - |  ``compile``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows information about hostname, CPU, BIOS and
       operating system.
   * - ``kernel_options_check``
     - |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows kernel options.
   * -  ``user_resources_limits_check``
     - |  ``compile``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - This check shows limits of each resource.
   * -  ``sys_check``
     - |  ``not included in any groups``
     - Some oneAPI components may have checks specific to that component.
       These checks will be available after setting environment variables using
       the `setvars <https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2024-1/use-the-setvars-and-oneapi-vars-scripts-with-linux.html>`_ script. Run the script and then run the Diagnostics
       Utility with the  `sys_check` name to see checks that are specific
       to installed components.


Information about product-specific sys_check's can be found in the table below:

.. list-table::
   :header-rows: 1

   * - Check Name
     - Product
     - What check is doing?
     - Toolkit
   * -  ``debugger_sys_check``
     - Intel® Distribution for GDB*
     - This check verifies platform readiness for `GPU workloads debugging <https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-gdb.html>`_.
       It checks presence of libipt and libiga, version of Linux* kernel,
       correctness of required environment variables and i915 debug
       support in kernel
     - | Intel® oneAPI Base Toolkit
       |
       | Intel® HPC Toolkit
   * -  ``advisor_sys_check``
     - Intel® Advisor
     - This check verifies version of Linux kernel and state of dev.i915.perf_stream_paranoid option
     - | Intel® oneAPI Base Toolkit
   * -  ``vtune_sys_check``
     - Intel® VTune™ Profiler
     - This check verifies platform readiness for `GPU analysis <https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html>`_.
     - | Intel® oneAPI Base Toolkit
   * -  ``dpcpp_ct_sys_check``
     - Intel® DPC++ Compatibility Tool
     - This check verifies presence of installed Python 3 on machine.
     - | Intel® oneAPI Base Toolkit
   * -  ``dpcpp_compiler_sys_check``
     - Intel® oneAPI DPC++/C++ Compiler
     - During this check Diagnostics Utility verifies presence of gcc compiler, its version and platform configuration for FPGA bitstream generation
     - | Intel® oneAPI Base Toolkit
       |
       | Intel® HPC Toolkit

To learn more about the output, see :ref:`diagnose`.



.. _check-table-by-group:


List of Checks by Group Name
----------------------------


**Check Name**: the name of the diagnostic check that can be run in the
command line.

**Group**:  Checks are grouped together so that you
can run multiple checks using one command.
For example, you can run all checks associated with GPUs by using
the  ``gpu``  argument.

For a description of what each **check** does and what permissions are needed
to run the **check**, see :ref:`check-table`.


.. list-table::
   :header-rows: 1

   * - Group of Checks
     - Checks included
   * -  ``compile``
     - |  ``driver_compatibility_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``oneapi_env_check``
       |  ``compiler_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``default``
     - |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``compiler_check``
   * -  ``host``
     - |  ``driver_compatibility_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``oneapi_env_check``
       |  ``compiler_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``runtime``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_metrics_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``base_system_check``
       |  ``kernel_options_check``
       |  ``user_resources_limits_check``
   * -  ``sysinfo``
     - |  ``hangcheck_check``
       |  ``driver_compatibility_check``
       |  ``oneapi_gpu_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``compiler_check``
       |  ``base_system_check``
       |  ``kernel_options_check``
       |  ``user_resources_limits_check``
   * -  ``target``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_metrics_check``
       |  ``gpu_backend_check``
       |  ``oneapi_toolkit_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``base_system_check``
       |  ``kernel_options_check``
       |  ``user_resources_limits_check``
   * -  ``gpu``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``oneapi_gpu_check``
       |  ``gpu_metrics_check``
       |  ``gpu_backend_check``
       |  ``intel_gpu_detector_check``
   * -  ``profiling``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``intel_gpu_detector_check``
