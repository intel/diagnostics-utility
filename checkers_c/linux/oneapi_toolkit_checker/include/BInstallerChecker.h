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

#ifndef BINSTALLERCHECKER_H_
#define BINSTALLERCHECKER_H_

#define MAX_USERID_LENGTH 32

#include <string.h>

#include <map>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include "CheckerHelper.h"
#include "JsonNode.h"
#include "OsUtils.h"
#include "PackageManagerRepository.h"

using ::std::string;
using ::std::vector;

class BInstallerChecker {
 private:
  OsUtils *os;
  PackageManagerRepositoryFactory *packageManagerRepositoryFactory;
  vector<string> *CachePaths;  // Paths to found installer caches

  bool GetAppInfo(string dbPath, string icPath, string &message);
  bool FindCaches(string path, string &message);

 public:
  BInstallerChecker();
  BInstallerChecker(
      OsUtils *osUtils,
      PackageManagerRepositoryFactory *packageManagerRepositoryFactory,
      vector<string> *cache);
  virtual ~BInstallerChecker() = default;

  virtual bool Initialize(string &message);
  // Returns false in case of any infrastructure issues which don't allow obtain
  // information.
  virtual bool GetAppInfo(string &message);
};

#endif /* BINSTALLERCHECKER_H_ */
