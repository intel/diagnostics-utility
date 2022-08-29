.. _cli-options:

===========
Get Started
===========


To run the Diagnostics Utility for Intel® oneAPI Toolkits:

1. Open a terminal and navigate to the directory where oneAPI products is installed.

   If you installed to the default directory,
   the utility will be located at ``/opt/intel/oneapi/``.


2. Change to the diagnostics directory:

::

  cd diagnostics/latest/


3. Run the Diagnostics Utility for Intel® oneAPI Toolkits using this syntax:

``python3 diagnostics.py --filter <ARGUMENT_NAME>``

The  **filter** modifier specifies how many checks to run at one time.
With a filter, you can run a :ref:`group of checks<check-table-by-group>`
or a :ref:`single check<check-table>`. In this
example, you will run all available checks, using the ``all`` argument:

::

  python3 diagnostics.py --filter all


The output will display in two places:

* the active console
* a JSON file

The default directory of the output files is
$HOME/intel/diagnostics/logs for Linux and
C:\Users\<username>\intel\diagnostics\logs for Windows.
To customize the default directory, see :ref:`customization`.


To increase the amount of detail, add the -v argument:

::

  python3 diagnostics.py --filter all -v


The Diagnostics Utility for Intel® oneAPI Toolkits can be customized to output only the data you need.
Use these methods to customize the command for your needs:

- :ref:`Run a group of related checks <group-checks>`
- :ref:`Run a single check <single-check>`
- :ref:`Increase the output detail using Verbose Mode <verbosity>`


.. _check-table:


List of Checks by Check Name
----------------------------

  Note: the checks below are all supported on Linux. For Windows, only the
  `base_system_check`` is supported.


The table below shows the list of  **checks** and which  **groups** can
also be used to run that check.

**Check Name**: the name of the diagnostic check that can be run in the command line.

**Group**:  Checks are grouped together
so that you can run multiple checks using
one command. For example, you can run all checks associated with
GPUs by using the GPU argument.

**Rights**: the permissions needed to run this check.

**Description**: a short description of the check.



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
   * -  ``oneapi_app_check``
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
   * -  ``gcc_version_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``sysinfo``
     - This check shows information about GCC compiler version.
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
     - user
     - This check shows limits of each resource.


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
       |  ``oneapi_app_check``
       |  ``oneapi_env_check``
       |  ``gcc_version_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``default``
     - |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_backend_check``
       |  ``oneapi_app_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``gcc_version_check``
   * -  ``host``
     - |  ``driver_compatibility_check``
       |  ``gpu_backend_check``
       |  ``oneapi_app_check``
       |  ``oneapi_env_check``
       |  ``gcc_version_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``runtime``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_metrics_check``
       |  ``gpu_backend_check``
       |  ``oneapi_app_check``
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
       |  ``oneapi_app_check``
       |  ``intel_gpu_detector_check``
       |  ``oneapi_env_check``
       |  ``gcc_version_check``
       |  ``base_system_check``
       |  ``kernel_options_check``
       |  ``user_resources_limits_check``
   * -  ``target``
     - |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``driver_compatibility_check``
       |  ``gpu_metrics_check``
       |  ``gpu_backend_check``
       |  ``oneapi_app_check``
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

