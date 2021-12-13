.. _cli-options:

===========
Get Started
===========


To run the diagnostics utility:

1. Open a terminal and navigate to the directory where oneAPI is installed.

   If you installed to the default directory,
   the utility will be located at ``/opt/intel/oneapi/``.


2. Change to the diagnostics directory:

::

  cd diagnostics/latest/


3. Run the utility using this syntax:

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

The default directory of the JSON file is Home/intel/diagnostics. To customize
the default directory, see :ref:`customization`.


To increase the amount of detail, add the -v argument:

::

  python3 diagnostics.py --filter all -v


The diagnostics utility can be customized to output only the data you need.
Use these methods to customize the command for your needs:

- :ref:`Run a group of related checks <group-checks>`
- :ref:`Run a single check <single-check>`
- :ref:`Increase the output detail using Verbose Mode <verbosity>`


.. _check-table:


List of Checks by Check Name
----------------------------

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
     - Rights
     - Description
   * -  ``oneapi_app_check``
     - | ``compile``
       |  ``default``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - user
     - The check shows version information of installed oneAPI products.
   * -  ``gpu_backend_check``
     - |  ``compile``
       |  ``default``
       |  ``gpu``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - user
     - The check shows information from OpenCL and LevelZero drivers.
   * - ``oneapi_env_check``
     - | ``compile``
       | ``default``
       | ``host``
       | ``runtime``
       | ``sysinfo``
       | ``target``
     - user
     - This check shows the version information of the oneAPI products installed in the environment.
   * - ``dependencies_check``
     - | ``compile``
       | ``default``
       | ``host``
       | ``runtime``
       | ``sysinfo``
       | ``target``
     - user
     - This check verifies compatibility of oneAPI products versions and GPU drivers versions.
   * -  ``vtune_check``
     - |  ``gpu``
       |  ``runtime``
       |  ``target``
       |  ``vtune``
     - user
     - The check verifies if the system is ready to do VTune analysis on GPU(s).
   * - ``debugger_check``
     - | ``debugger``
       | ``gdb``
     - user
     - This check verifies if the environment is ready to use Intel(R) Distribution for GDB*.
   * -  ``gcc_version_check``
     - |  ``compile``
       |  ``default``
       |  ``host``
       |  ``sysinfo``
     - user
     - The check shows information about GCC compiler version.
   * -  ``intel_gpu_detector_check``
     - |  ``advisor``
       |  ``default``
       |  ``gpu``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
       |  ``vtune``
     - user
     - The check shows which Intel GPU(s) is on the system, based on lspci information and internal table.
   * -  ``base_system_check``
     - |  ``compile``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - user
     - The check shows information about hostname, CPU, BIOS, and operating system.
   * -  ``hangcheck_check``
     - |  ``advisor``
       |  ``gpu``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
       |  ``vtune``
     - user
     - The check verifies that the GPU hangcheck option is disabled to allow long-running jobs.
   * -  ``user_group_check``
     - |  ``advisor``
       |  ``gpu``
       |  ``runtime``
       |  ``target``
       |  ``vtune``
     - user
     - The check verifies that the current user is in the same group as the GPU(s).
   * -  ``kernel_boot_options_check``
     - |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - user
     - The check shows kernel boot options.
   * -  ``gpu_metrics_check``
     - |  ``gpu``
       |  ``runtime``
       |  ``target``
     - user
     - The check verifies that GPU metrics are good.
   * -  ``oneapi_gpu_check``
     - |  ``gpu``
       |  ``sysinfo``
     - user
     - The check runs GPU workloads and verifies readiness to run applications on GPU(s).
   * -  ``advisor_check``
     - |  ``advisor``
       |  ``gpu``
       |  ``kernel``
       |  ``runtime``
       |  ``target``
     - user
     - The check verifies if environment is ready to analyze GPU kernels.
   * -  ``user_resources_limits_check``
     - |  ``compile``
       |  ``host``
       |  ``runtime``
       |  ``sysinfo``
       |  ``target``
     - user
     - The check shows resources limits.

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
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``gcc_version_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``default``
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``gcc_version_check``
       |  ``intel_gpu_detector_check``
   * -  ``host``
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``gcc_version_check``
       |  ``base_system_check``
       |  ``user_resources_limits_check``
   * -  ``runtime``
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``vtune_check``
       |  ``intel_gpu_detector_check``
       |  ``base_system_check``
       |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``kernel_boot_options_check``
       |  ``gpu_metrics_check``
       |  ``advisor_check``
       |  ``user_resources_limits_check``
   * -  ``sysinfo``
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``gcc_version_check``
       |  ``intel_gpu_detector_check``
       |  ``base_system_check``
       |  ``hangcheck_check``
       |  ``kernel_boot_options_check``
       |  ``oneapi_gpu_check``
       |  ``user_resources_limits_check``
   * -  ``target``
     - |  ``oneapi_app_check``
       |  ``gpu_backend_check``
       |  ``oneapi_env_check``
       |  ``dependencies_check``
       |  ``vtune_check``
       |  ``intel_gpu_detector_check``
       |  ``base_system_check``
       |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``kernel_boot_options_check``
       |  ``gpu_metrics_check``
       |  ``advisor_check``
       |  ``user_resources_limits_check``
   * -  ``gpu``
     - | ``gpu_backend_check``
       |  ``vtune_check``
       |  ``intel_gpu_detector_check``
       |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``gpu_metrics_check``
       |  ``advisor_check``
   * -  ``vtune``
     - |  ``vtune_check``
       |  ``intel_gpu_detector_check``
       |  ``hangcheck_check``
       |  ``user_group_check``
   * -  ``advisor``
     - |  ``intel_gpu_detector_check``
       |  ``hangcheck_check``
       |  ``user_group_check``
       |  ``advisor_check``
   * -  ``kernel``
     - |  ``kernel_boot_options_check``
       |  ``advisor_check``