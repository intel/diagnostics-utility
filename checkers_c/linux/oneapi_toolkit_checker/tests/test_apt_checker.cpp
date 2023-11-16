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

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <string>

#include "AptChecker.h"
#include "CommonMocks.h"
#include "Mocks.h"

using ::std::string;
using ::testing::_;
using ::testing::DoAll;
using ::testing::Return;
using ::testing::SetArgReferee;

TEST(AptChecker, InitializeShouldAlwaysReturnTrue) {
  // given
  string message;
  OsUtilsMock osUtils;
  AptChecker sut(&osUtils);

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_TRUE(result);
}

TEST(AptChecker, GetAppInfoShouldReturnFalseOnNonDebianOs) {
  // given
  string message;
  OsUtilsMock osUtils;

  AptChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(Windows));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Application information is not available for products "
            "installed by dpkg.");
}

TEST(AptChecker, GetAppInfoShouldReturnFalseWhenFailsToRunDpkgCommand) {
  // given
  string message;
  OsUtilsMock osUtils;

  AptChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(DebianBased));
  EXPECT_CALL(
      osUtils,
      RunCommand("dpkg --no-pager -l '*intel-oneapi*' 2>/dev/null | grep ii",
                 _))
      .WillOnce(Return(-1));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Unable to find installed package. Verify package is installed and "
            "that current user has permissions to access the package.");
}

TEST(AptChecker, GetAppInfoShouldSuccedAndReturnListOfPackagesIfAnyInstalled) {
  // given
  string message;
  const string dpkgOutput =
      "ii  intel-oneapi-runtime-ccl               2021.9.0-43543 amd64        "
      "Intel® oneAPI Collective Communications Library runtime\n"
      "ii  intel-oneapi-runtime-compilers         2023.1.0-46305 amd64        "
      "Intel® oneAPI DPC++/C++ Compiler & Intel® C++ Compiler Classic runtime "
      "common files\n"
      "ii  intel-oneapi-runtime-compilers-common  2023.1.0-46305 all          "
      "Intel® oneAPI DPC++/C++ Compiler & Intel® C++ Compiler Classic runtime "
      "common files\n";
  OsUtilsMock osUtils;

  AptChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(DebianBased));
  EXPECT_CALL(
      osUtils,
      RunCommand("dpkg --no-pager -l '*intel-oneapi*' 2>/dev/null | grep ii",
                 _))
      .WillOnce(DoAll(SetArgReferee<1>(dpkgOutput), Return(0)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(
      message,
      "{ \"Intel\xC2\xAE oneAPI Collective Communications Library runtime \": "
      "{ \"CheckStatus\": \"INFO\", \"CheckResult\": { \"Packages\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"intel-oneapi-runtime-ccl\" }, \"Version\": { \"CheckStatus\": "
      "\"INFO\", \"CheckResult\": \"2021.9.0\" }, \"Full Version\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"2021.9.0-43543\" }, \"Architecture\": { \"Verbosity\": 1, "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"amd64\" }, \"Path\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"\\/opt\\/intel\\/oneapi\" } } }, \"Intel\xC2\xAE oneAPI DPC++\\/C++ "
      "Compiler & Intel\xC2\xAE C++ Compiler Classic runtime common files \": "
      "{ \"CheckStatus\": \"INFO\", \"CheckResult\": { \"Packages\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"intel-oneapi-runtime-compilers, "
      "intel-oneapi-runtime-compilers-common\" }, \"Version\": { "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"2023.1.0\" }, \"Full "
      "Version\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"2023.1.0-46305\" }, \"Architecture\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": \"amd64\" "
      "}, \"Path\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"\\/opt\\/intel\\/oneapi\" } } } }");
}

TEST(AptChecker,
     GetAppInfoShouldSuccedAndReturnEmptyListOfPackagesIfNoneAreInstalled) {
  // given
  string message;
  const string dpkgOutput = "\n";
  OsUtilsMock osUtils;

  AptChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(DebianBased));
  EXPECT_CALL(
      osUtils,
      RunCommand("dpkg --no-pager -l '*intel-oneapi*' 2>/dev/null | grep ii",
                 _))
      .WillOnce(DoAll(SetArgReferee<1>(dpkgOutput), Return(0)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(
      message,
      "{ \"\": { \"CheckStatus\": \"INFO\", \"CheckResult\": { \"Packages\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": \"\" }, "
      "\"Version\": { \"CheckStatus\": \"INFO\", \"CheckResult\": \"\" }, "
      "\"Full Version\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"\" }, \"Architecture\": { \"Verbosity\": 1, "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"\" }, \"Path\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"\\/opt\\/intel\\/oneapi\" } } } }");
  // ASSERT_TRUE(false);
}