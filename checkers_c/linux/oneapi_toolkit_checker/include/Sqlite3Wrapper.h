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

#ifndef SQLITE_3_WRAPPER_H_
#define SQLITE_3_WRAPPER_H_

#include <sqlite3.h>

#include <functional>
#include <memory>
#include <string>

using std::string;

class Sqlite3Wrapper {
 public:
  virtual int Open(const char *filename, sqlite3 **ppDb, int flags,
                   const char *zVfs);
  virtual int Prepare(sqlite3 *db, const char *zSql, int nByte,
                      sqlite3_stmt **ppStmt, const char **pzTail);
  virtual int Finalize(sqlite3_stmt *pStmt);
  virtual int Close(sqlite3 *db);
  virtual int Step(sqlite3_stmt *pStmt);
  virtual const unsigned char *ColumnText(sqlite3_stmt *pStmt, int iCol);
  virtual const char *ErrorMsg(sqlite3 *db);
};

#endif