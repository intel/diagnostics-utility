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

#ifndef MOCKS_H_
#define MOCKS_H_

#include <gmock/gmock.h>

#include "AptChecker.h"
#include "BInstallerChecker.h"
#include "OsUtils.h"
#include "RpmChecker.h"
#include "Sqlite3Wrapper.h"

class AptCheckerMock : public AptChecker {
 public:
  MOCK_METHOD(bool, Initialize, (string & message), (override));
  MOCK_METHOD(bool, GetAppInfo, (string & message), (override));
};

class BInstallerCheckerMock : public BInstallerChecker {
 public:
  MOCK_METHOD(bool, Initialize, (string & message), (override));
  MOCK_METHOD(bool, GetAppInfo, (string & message), (override));
};

class RpmCheckerMock : public RpmChecker {
 public:
  MOCK_METHOD(bool, Initialize, (string & message), (override));
  MOCK_METHOD(bool, GetAppInfo, (string & message), (override));
};

class Sqlite3WrapperMock : public Sqlite3Wrapper {
 public:
  MOCK_METHOD(int, Open,
              (const char *filename, sqlite3 **ppDb, int flags,
               const char *zVfs),
              (override));
  MOCK_METHOD(int, Prepare,
              (sqlite3 * db, const char *zSql, int nByte, sqlite3_stmt **ppStmt,
               const char **pzTail),
              (override));
  MOCK_METHOD(int, Finalize, (sqlite3_stmt * pStmt), (override));
  MOCK_METHOD(int, Close, (sqlite3 * db), (override));
  MOCK_METHOD(int, Step, (sqlite3_stmt * pStmt), (override));
  MOCK_METHOD(const unsigned char *, ColumnText,
              (sqlite3_stmt * pStmt, int iCol), (override));
  MOCK_METHOD(const char *, ErrorMsg, (sqlite3 * db), (override));
};

class PackageManagerRepositoryFactoryMock
    : public PackageManagerRepositoryFactory {
 public:
  MOCK_METHOD(shared_ptr<PackageManagerRepository>, GetPackageManagerRepository,
              (), (override));
};

class PackageManagerRepositoryMock : public PackageManagerRepository {
 public:
  MOCK_METHOD(bool, Open, (string dbPath, string &error), (override));
  MOCK_METHOD(void, Close, (), (override));
  MOCK_METHOD(bool, GetPackageInstallationPath, (string & message), (override));
  MOCK_METHOD(bool, GetComponents,
              (std::function<Component *()> & productIterator, string &message),
              (override));
};

#endif
