..
   _output:

============
Output files
============

After a check is run, the Diagnostics Utility for Intel® oneAPI Toolkits
generates two files:

* a console output
* a JSON file with the results of the checks

You can specify the output folder to store these files by using the
`--output` option. For example:

  ``python3 diagnostics.py --output PATH_TO_DESIRED_OUTPUT_DIRECTORY``

..

  -----------------------
  Interpreting the Output
  -----------------------

  If a check Fails, that means the system was unable to retrieve the information
  needed. For example, if you run

  - unable to retrieve information
  - Some checks may report that cannot get some information only,
    some checks provide diagnostics what wrong.

  Output may have different format in case of using verbose mode (with -v or without the parameter). Both variants may be presented.

  There are two messages with potential issue may be shown. It is ERROR,
  if issue is in check itself and we cannot get some information for achieve check's aim. For example (without and with -v):

  Result status: ERROR
  [Errno 13] Permission denied: '/sys/module/i915/parameters/enable_hangcheck'

  |  GPU hangcheck is disabled-------------------------------------------------------------------------------------------------------------------------------------------------------ERROR  |
  |  Message:[Errno 13] Permission denied: '/sys/module/i915/parameters/enable_hangcheck'                                                                                                   |


  It can be some access issue (administrative privileges are required) or internal errors in check. We recommend to start analysis from FAILs. FAIL means that check find that configuration is incorrect. For example (without and with -v):

  Result status: FAIL
  Current user is not part of the video group, to add a user: sudo usermod -a -G video test.

  |  Current user is in the video group----------------------------------------------------------------------------------------------------------------------------------------------FAIL   |
  |  Message:Current user is not part of the video group, to add a user: sudo usermod -a -G video test.                                                                                     |


  You may have multiple failures simultaneously. For example:

  Result status: FAIL
  Install Metrics Library for Metrics Discovery API.
  Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0.
  Rebuild the i915 driver or kernel.

  Result status: FAIL
  Current user is not part of the video group, to add a user: sudo usermod -a -G video test.

  Result status: FAIL
  Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0.

  In this case try to analyze you problem and guest what is the root cause of your issue (most probably) and try to fix it. Of fix failures one by one.

  If all FAILs were fixed and you still have issue, try to fix ERRORs. First, try to run Diag tool with administrative privileges and check that you have setup setenv script from oneAPI.

  If all checks passed, please collect all logs: run  “python3 diagnostics.py --filter all”, find full log into $HOME/intel/diagnostics/logs for Linux and C:\Users\<username>\intel\diagnostics\logs for Windows (by default) and report issue to forum <link> .

  How to interpret Diagnostics tool output
  ----------------------------------------

  Each category of checks contains multiple checks with different level of details. Please go throw all checks and analyze all failures before make decision what is wrong. Some checks may report that cannot get some information only, some checks provide diagnostics what wrong. There is no order or dependencies for these checks yet. Please, read all failures\infos and combine it in one bird eye view

  Output may have different format in case of using verbose mode (with -v or without the parameter). Both variants may be presented.

  There are 2 messages with potential issue may be shown. It is ERROR, if issue is in check itself and we cannot get some information for achieve check's aim. For example (without and with -v):

  Result status: ERROR
  [Errno 13] Permission denied: '/sys/module/i915/parameters/enable_hangcheck'

  |  GPU hangcheck is disabled-------------------------------------------------------------------------------------------------------------------------------------------------------ERROR  |
  |  Message:[Errno 13] Permission denied: '/sys/module/i915/parameters/enable_hangcheck'                                                                                                   |


  It can be some access issue (administrative privileges are required) or internal errors in check. We recommend to start analysis from FAILs. FAIL means that check find that configuration is incorrect. For example (without and with -v):

  Result status: FAIL
  Current user is not part of the video group, to add a user: sudo usermod -a -G video test.

  |  Current user is in the video group----------------------------------------------------------------------------------------------------------------------------------------------FAIL   |
  |  Message:Current user is not part of the video group, to add a user: sudo usermod -a -G video test.                                                                                     |


  You may have multiple failures simultaneously. For example:

  Result status: FAIL
  Install Metrics Library for Metrics Discovery API.
  Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0.
  Rebuild the i915 driver or kernel.

  Result status: FAIL
  Current user is not part of the video group, to add a user: sudo usermod -a -G video test.

  Result status: FAIL
  Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0.

  In this case try to analyze you problem and guest what is the root cause of your issue (most probably) and try to fix it. Of fix failures one by one.

  If all FAILs were fixed and you still have issue, try to fix ERRORs. First, try to run Diag tool with administrative privileges and check that you have setup setenv script from oneAPI.

  If all checks passed, please collect all logs: run  “python3 diagnostics.py --filter all”, find full log into $HOME/intel/diagnostics/logs for Linux and C:\Users\<username>\intel\diagnostics\logs for Windows (by default) and report issue to forum <link> .

