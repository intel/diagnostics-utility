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

#ifndef SRC_CHECKERHELPER_H_
#define SRC_CHECKERHELPER_H_

#ifdef __linux__
#include <dlfcn.h>
#define ZE_LOADER_LIB "libze_loader.so.1"
#define OPENCL_LIB "libOpenCL.so.1"
#define DLOPEN(libname) dlopen((libname), RTLD_LAZY)
#define DLSYM(lib, fn) dlsym((lib), (fn))
#define SETENV(name, value) setenv((name), (value), 0)
#else
#include <Windows.h>
#define ZE_LOADER_LIB L"ze_loader.dll"
#define OPENCL_LIB L"OpenCL.dll"
#define DLOPEN(libname) \
  LoadLibraryExW(libname, NULL, LOAD_LIBRARY_SEARCH_SYSTEM32)
#define DLSYM(lib, fn) GetProcAddress((lib), (fn))
#define SETENV(name, value) _putenv_s((name), (value))
#endif

#include <map>
#include <regex>
#include <vector>

using ::std::string;
using ::std::vector;

enum CHECK_STATUS : int {
  CHECK_STATUS_SUCCESS = 0,
  CHECK_STATUS_WARNING = 1,
  CHECK_STATUS_FAIL = 2,
  CHECK_STATUS_ERROR = 3
};

namespace CheckerHelper {
vector<string> SplitString(const string str, const string regex_str);
};

std::string GetLastErrorString();

#endif /* SRC_CHECKERHELPER_H_ */
