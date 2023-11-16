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

#ifndef PACKAGE_MANAGER_REPOSITORY_H_
#define PACKAGE_MANAGER_REPOSITORY_H_

#include <sqlite3.h>

#include <functional>
#include <memory>
#include <sstream>
#include <string>

#include "Sqlite3Wrapper.h"

using std::endl;
using std::make_shared;
using std::shared_ptr;
using std::string;
using std::stringstream;

struct Component {
  string id;
  string fullVersion;
};

class PackageManagerRepository {
 protected:
  Sqlite3Wrapper *sqliteWrapper;
  sqlite3 *db = nullptr;

 public:
  PackageManagerRepository();
  PackageManagerRepository(Sqlite3Wrapper *sqlite3Wrapper);
  virtual ~PackageManagerRepository();

  virtual bool Open(string dbPath, string &error);
  virtual void Close();
  virtual bool GetPackageInstallationPath(string &message);
  virtual bool GetComponents(std::function<Component *()> &components,
                             string &message);
};

class PackageManagerRepositoryFactory {
 protected:
  Sqlite3Wrapper *sqlite3Wrapper;

 public:
  PackageManagerRepositoryFactory() = default;
  PackageManagerRepositoryFactory(Sqlite3Wrapper *sqlite3Wrapper);
  virtual shared_ptr<PackageManagerRepository> GetPackageManagerRepository();
};

#endif
