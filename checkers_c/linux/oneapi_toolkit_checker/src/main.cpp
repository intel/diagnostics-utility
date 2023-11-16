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

#include <stdio.h>

#include <fstream>
#include <iostream>
#include <sstream>

#include "AptChecker.h"
#include "BInstallerChecker.h"
#include "OneapiToolkitChecker.h"
#include "OsUtils.h"
#include "PackageManagerRepository.h"
#include "RpmChecker.h"
#include "Sqlite3Wrapper.h"
#include "checker_interface.h"
#include "checker_list_interface.h"

#define API_VERSION "0.2"
char api_version[MAX_STRING_LEN];

using namespace std;

int main() {
  vector<string> cache;
  OsUtils osUtils;
  Sqlite3Wrapper sqlite3Wrapper;
  PackageManagerRepositoryFactory packageManagerRepositoryFactory(
      &sqlite3Wrapper);
  AptChecker aptChecker(&osUtils);
  BInstallerChecker bInstallerChecker(&osUtils,
                                      &packageManagerRepositoryFactory, &cache);
  RpmChecker rpmChecker(&osUtils);
  OneapiChecker oneapiChecker(&aptChecker, &bInstallerChecker, &rpmChecker);

  // Run tests
  string message;
  int retVal = oneapiChecker.PerformCheck(message);
  cout << message << endl;
  return retVal;
}

//-------------------------------------------------------------------------
//------------------------Library part there ------------------------------
//-------------------------------------------------------------------------

extern "C" struct CheckResult app_check(char *data) {
  vector<string> cache;
  OsUtils osUtils;
  Sqlite3Wrapper sqlite3Wrapper;
  PackageManagerRepositoryFactory packageManagerRepositoryFactory(
      &sqlite3Wrapper);
  AptChecker aptChecker(&osUtils);
  BInstallerChecker bInstallerChecker(&osUtils,
                                      &packageManagerRepositoryFactory, &cache);
  RpmChecker rpmChecker(&osUtils);
  OneapiChecker oneapiChecker(&aptChecker, &bInstallerChecker, &rpmChecker);

  string message;
  oneapiChecker.PerformCheck(message);
  char *buffer = new char[message.size() + 1];
  std::copy(message.begin(), message.end(), buffer);
  buffer[message.size()] = '\0';

  struct CheckResult ret = {buffer};

  return ret;
}

REGISTER_CHECKER(
    app_check_struct, "oneapi_toolkit_check", "GetData",
    "default,sysinfo,compile,runtime,host,target",
    "This check shows information about installed oneAPI toolkits.", "{}", 20,
    10, 2, app_check)

static struct Check *checkers[] = {&app_check_struct, NULL};

extern "C" EXPORT_API char *get_api_version(void) {
  snprintf(api_version, sizeof(api_version), "%s", API_VERSION);
  return api_version;
}

extern "C" EXPORT_API struct Check **get_check_list(void) { return checkers; }
