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

#include "PackageManagerRepository.h"

PackageManagerRepository::PackageManagerRepository() {
  sqliteWrapper = nullptr;
  db = nullptr;
}

PackageManagerRepository::PackageManagerRepository(
    Sqlite3Wrapper *sqliteWrapper)
    : sqliteWrapper(sqliteWrapper) {}

PackageManagerRepository::~PackageManagerRepository() { Close(); }

bool PackageManagerRepository::Open(string dbPath, string &error) {
  if (sqliteWrapper->Open(dbPath.c_str(), &db, SQLITE_OPEN_READONLY, nullptr) !=
      SQLITE_OK) {
    stringstream ss;
    ss << "Cannot open Binary Installer database." << dbPath << ": "
       << sqliteWrapper->ErrorMsg(db) << endl;
    error = ss.str();
    return false;
  }
  return true;
}

void PackageManagerRepository::Close() {
  if (db != nullptr) sqliteWrapper->Close(db);
}

bool PackageManagerRepository::GetPackageInstallationPath(string &message) {
  const char *select_dir = "SELECT PATH FROM INSTALL_DIR;";
  sqlite3_stmt *statement = nullptr;
  if (sqliteWrapper->Prepare(db, select_dir, -1, &statement, NULL) !=
      SQLITE_OK) {
    stringstream ss;
    ss << "Error while compiling SQL statement \"" << select_dir
       << "\": " << sqliteWrapper->ErrorMsg(db) << endl;
    message = ss.str();
    sqliteWrapper->Finalize(statement);
    return false;
  }
  if (sqliteWrapper->Step(statement) != SQLITE_ROW) {
    stringstream ss;
    ss << "Unable to find oneAPI package. Your database format is not "
          "supported by the current version of this check."
       << endl;
    message = ss.str();
    sqliteWrapper->Finalize(statement);
    return false;
  }
  // The table has just one record now.
  message = (char *)sqliteWrapper->ColumnText(statement, 0);
  sqliteWrapper->Finalize(statement);
  return true;
}

bool PackageManagerRepository::GetComponents(
    std::function<Component *()> &components, string &message) {
  const char *select_components =
      "SELECT ID, VERSION FROM COMPONENT ORDER BY ID, VERSION;";
  sqlite3_stmt *statement = nullptr;
  if (sqliteWrapper->Prepare(db, select_components, -1, &statement, NULL) !=
      SQLITE_OK) {
    stringstream ss;
    ss << "Error while compiling SQL statement \"" << select_components
       << "\": " << sqliteWrapper->ErrorMsg(db) << endl;
    message = ss.str();
    sqliteWrapper->Finalize(statement);
    return false;
  }

  components = [=]() -> Component * {
    if (sqliteWrapper->Step(statement) == SQLITE_ROW) {
      string id = (char *)sqliteWrapper->ColumnText(statement, 0);
      string fullVersion = (char *)sqliteWrapper->ColumnText(statement, 1);
      return new Component{id, fullVersion};
    }
    sqliteWrapper->Finalize(statement);
    return nullptr;
  };

  return true;
}

PackageManagerRepositoryFactory::PackageManagerRepositoryFactory(
    Sqlite3Wrapper *sqlite3Wrapper)
    : sqlite3Wrapper(sqlite3Wrapper) {}

shared_ptr<PackageManagerRepository>
PackageManagerRepositoryFactory::GetPackageManagerRepository() {
  return make_shared<PackageManagerRepository>(sqlite3Wrapper);
}
