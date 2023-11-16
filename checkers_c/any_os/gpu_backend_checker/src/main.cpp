/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and
your use of them is governed by the express license under which they were
provided to you (License). Unless the License provides otherwise, you may not
use, modify, copy, publish, distribute, disclose or transmit this software or
the related documents without Intel's prior written permission. This software
and the related documents are provided as is, with no express or implied
warranties, other than those that are expressly stated in the License.

*******************************************************************************/

#include "GpuBackendChecker.h"
#include "checker_interface.h"
#include "checker_list_interface.h"

#define API_VERSION "0.2"
char api_version[MAX_STRING_LEN];

int main() {
  // we cannot call main function directly from python due to
  // Fatal Python error: pymain_init_cmdline_argv: memory allocation failed
  LZ_DriverChecker lzDriverChecker = LZ_DriverChecker();
  CL_DriverChecker clDriverChecker = CL_DriverChecker();
  GpuBackendChecker gpuBackendChecker =
      GpuBackendChecker(&lzDriverChecker, &clDriverChecker);
  string message;
  int check_status = gpuBackendChecker.PerformCheck(message);
  cout << message << endl;
  return check_status;
}

//-------------------------------------------------------------------------
//------------------------Library part there ------------------------------
//-------------------------------------------------------------------------

extern "C" struct CheckResult gpu_backend_check(char *data) {
  LZ_DriverChecker lzDriverChecker = LZ_DriverChecker();
  CL_DriverChecker clDriverChecker = CL_DriverChecker();
  GpuBackendChecker gpuBackendChecker =
      GpuBackendChecker(&lzDriverChecker, &clDriverChecker);
  string message;
  gpuBackendChecker.PerformCheck(message);
  char *buffer = new char[message.size() + 1];
  std::copy(message.begin(), message.end(), buffer);
  buffer[message.size()] = '\0';

  struct CheckResult ret = {buffer};

  return ret;
}

REGISTER_CHECKER(gpu_backend_check_struct, "gpu_backend_check", "GetData",
                 "default,gpu,sysinfo,compile,runtime,host,target",
                 "This check shows information from OpenCL™ and Intel® oneAPI "
                 "Level Zero drivers.",
                 "{}", 20, 10, 2, gpu_backend_check)

static struct Check *checkers[] = {&gpu_backend_check_struct, NULL};

extern "C" EXPORT_API char *get_api_version(void) {
  snprintf(api_version, sizeof(api_version), "%s", API_VERSION);
  return api_version;
}

extern "C" EXPORT_API struct Check **get_check_list(void) { return checkers; }
