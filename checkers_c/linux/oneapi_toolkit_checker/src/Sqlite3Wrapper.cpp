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

#include "Sqlite3Wrapper.h"

#include <sqlite3.h>

#include <iostream>
#include <sstream>

using std::endl;
using std::make_shared;
using std::stringstream;

int Sqlite3Wrapper::Open(const char *filename, sqlite3 **ppDb, int flags,
                         const char *zVfs) {
  return sqlite3_open_v2(filename, ppDb, flags, zVfs);
}

int Sqlite3Wrapper::Prepare(sqlite3 *db, const char *zSql, int nByte,
                            sqlite3_stmt **ppStmt, const char **pzTail) {
  return sqlite3_prepare_v2(db, zSql, nByte, ppStmt, pzTail);
}

int Sqlite3Wrapper::Finalize(sqlite3_stmt *pStmt) {
  return sqlite3_finalize(pStmt);
}

int Sqlite3Wrapper::Close(sqlite3 *db) { return sqlite3_close_v2(db); }

int Sqlite3Wrapper::Step(sqlite3_stmt *pStmt) { return sqlite3_step(pStmt); }

const unsigned char *Sqlite3Wrapper::ColumnText(sqlite3_stmt *pStmt, int iCol) {
  return sqlite3_column_text(pStmt, iCol);
}

const char *Sqlite3Wrapper::ErrorMsg(sqlite3 *db) { return sqlite3_errmsg(db); }
