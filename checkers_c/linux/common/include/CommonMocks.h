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

#ifndef COMMON_MOCKS_H
#define COMMON_MOCKS_H

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <string>

#include "OsUtils.h"

using ::std::string;

class OsUtilsMock : public OsUtils {
 public:
  MOCK_METHOD(int, RunCommand, (const string cmd, string& out), (override));
  MOCK_METHOD(OsType, GetOsType, (), (override));
  MOCK_METHOD(passwd*, GetPwUid, (uid_t uid), (override));
  MOCK_METHOD(uid_t, GetUid, (), (override));
  MOCK_METHOD(uid_t, GetEUid, (), (override));
  MOCK_METHOD(bool, LoadFile, (string path, string& message), (override));
  MOCK_METHOD(int, SetEnv, (const char* name, const char* value, int replace),
              (override));
  MOCK_METHOD(char*, GetEnv, (const char* name), (override));
};

#endif
