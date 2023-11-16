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

#ifndef OS_UTILS_H_
#define OS_UTILS_H_

#include <pwd.h>
#include <unistd.h>

#include <string>

using std::string;

enum OsType { UnknownOS, DebianBased, RpmBased, Windows, MacOS, FreeBSD };

class OsUtils {
 public:
  virtual int RunCommand(const string cmd, string& out);
  virtual OsType GetOsType();
  virtual passwd* GetPwUid(uid_t uid);
  virtual uid_t GetUid();
  virtual uid_t GetEUid();
  virtual bool LoadFile(string path, string& message);
  virtual int SetEnv(const char* name, const char* value, int replace);
  virtual char* GetEnv(const char* name);
};

#endif
