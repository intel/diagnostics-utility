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

#include "CommonMocks.h"
#include "Mocks.h"
#include "RpmChecker.h"

using ::std::string;
using ::testing::_;
using ::testing::DoAll;
using ::testing::Return;
using ::testing::SetArgReferee;

TEST(RpmChecker, InitializeShouldAlwaysReturnTrue) {
  // given
  string message;
  OsUtilsMock osUtils;
  RpmChecker sut(&osUtils);

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_TRUE(result);
}

TEST(RpmChecker, GetAppInfoShouldReturnFalseOnNonRpmBasedOs) {
  // given
  string message;
  OsUtilsMock osUtils;

  RpmChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(Windows));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Application information is not available for products "
            "installed by RPM.");
}

TEST(RpmChecker, GetAppInfoShouldReturnFalseWhenFailsToRunRpmCommand) {
  // given
  string message;
  OsUtilsMock osUtils;

  RpmChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(RpmBased));
  EXPECT_CALL(osUtils, RunCommand("rpm -q -a --qf "
                                  "'%{Name}\t%{Version}\t%{Arch}\t%{Summary}\t:"
                                  "%{Vendor}\n' | grep :Intel",
                                  _))
      .WillOnce(Return(-1));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Cannot obtain installed package.");
}

TEST(RpmChecker, GetAppInfoShouldSuccedAndReturnListOfPackagesIfAnyInstalled) {
  // given
  string message;
  const string rpmOutput =
      "intel-oneapi-runtime-ccl\t2021.9.0-43543\tx86_64\tIntel® oneAPI "
      "Collective Communications Library runtime\t:Intel\n"
      "intel-oneapi-runtime-compilers\t2023.1.0-46305\tx86_64\tIntel® oneAPI "
      "DPC++/C++ Compiler & Intel® C++ Compiler Classic runtime common "
      "files\t:Intel\n"
      "intel-oneapi-runtime-compilers-common\t2023.1.0-46305\tx86_64\tIntel® "
      "oneAPI DPC++/C++ Compiler & Intel® C++ Compiler Classic runtime common "
      "files\t:Intel\n";
  OsUtilsMock osUtils;

  RpmChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(RpmBased));
  EXPECT_CALL(osUtils, RunCommand("rpm -q -a --qf "
                                  "'%{Name}\t%{Version}\t%{Arch}\t%{Summary}\t:"
                                  "%{Vendor}\n' | grep :Intel",
                                  _))
      .WillOnce(DoAll(SetArgReferee<1>(rpmOutput), Return(0)));

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
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"x86_64\" }, \"Path\": { "
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
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"x86_64\" }, \"Path\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"\\/opt\\/intel\\/oneapi\" } } } }");
}

TEST(RpmChecker,
     GetAppInfoShouldSuccedAndReturnEmptyListOfPackagesIfNoneAreInstalled) {
  // given
  string message;
  const string rpmOutput = "";
  OsUtilsMock osUtils;

  RpmChecker sut(&osUtils);

  EXPECT_CALL(osUtils, GetOsType()).WillOnce(Return(RpmBased));
  EXPECT_CALL(osUtils, RunCommand("rpm -q -a --qf "
                                  "'%{Name}\t%{Version}\t%{Arch}\t%{Summary}\t:"
                                  "%{Vendor}\n' | grep :Intel",
                                  _))
      .WillOnce(DoAll(SetArgReferee<1>(rpmOutput), Return(0)));

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
}