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

#include "Mocks.h"
#include "OneapiToolkitChecker.h"

using ::testing::_;
using ::testing::DoAll;
using ::testing::Ref;
using ::testing::Return;
using ::testing::SetArgReferee;

TEST(OneapiChecker, FailedToInitialize) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize AptChecker"),
                      Return(false)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("Failed to initialize BInstallerChecker"),
                Return(false)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize RpmChecker"),
                      Return(false)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"oneAPI "
      "products\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":\"Cannot locate installed oneAPI products. Additional "
      "information: \\nFailed to initialize BInstallerChecker\\nFailed to "
      "initialize AptChecker\"\n        }\n      }\n    }\n  }\n}");
}

TEST(OneapiChecker, IBinaryInstallerAndAptCheckerInitialized) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("AptChecker initialized"), Return(true)));
  EXPECT_CALL(aptChecker, GetAppInfo(_))
      .WillOnce(DoAll(SetArgReferee<0>("{ \"AptChecker\":\"App info\" }"),
                      Return(true)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("BInstallerChecker initialized"),
                      Return(true)));
  EXPECT_CALL(bInstallerChecker, GetAppInfo(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("{ \"BInstallerChecker\":\"App info\" }"),
                Return(true)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize RpmChecker"),
                      Return(false)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"oneAPI "
      "products\":{\n          \"Command\":\"Parse installed oneAPI caches and "
      "installed dpkg packages.\",\n          \"CheckStatus\":\"INFO\",\n      "
      "    \"CheckResult\":{\n            \"BInstallerChecker\":\"App "
      "info\",\n            \"AptChecker\":\"App info\"\n          }\n        "
      "}\n      }\n    }\n  }\n}");
}

TEST(OneapiChecker, IBinaryInstallerAndRpmCheckerInitialized) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize AptChecker"),
                      Return(false)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("BInstallerChecker initialized"),
                      Return(true)));
  EXPECT_CALL(bInstallerChecker, GetAppInfo(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("{ \"BInstallerChecker\":\"App info\" }"),
                Return(true)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("RpmChecker initialized"), Return(true)));
  EXPECT_CALL(rpmChecker, GetAppInfo(_))
      .WillOnce(DoAll(SetArgReferee<0>("{ \"RpmChecker\":\"App info\" }"),
                      Return(true)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"oneAPI "
      "products\":{\n          \"Command\":\"Parse installed oneAPI caches and "
      "installed rpm packages.\",\n          \"CheckStatus\":\"INFO\",\n       "
      "   \"CheckResult\":{\n            \"BInstallerChecker\":\"App info\",\n "
      "           \"RpmChecker\":\"App info\"\n          }\n        }\n      "
      "}\n    }\n  }\n}");
}

TEST(OneapiChecker, OnlyIBinaryInstallerInitialized) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize AptChecker"),
                      Return(false)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("BInstallerChecker initialized"),
                      Return(true)));
  EXPECT_CALL(bInstallerChecker, GetAppInfo(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("{ \"BInstallerChecker\":\"App info\" }"),
                Return(true)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize RpmChecker"),
                      Return(false)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(message,
            "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
            "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
            "\"oneAPI products\":{\n          \"Command\":\"Parse installed "
            "oneAPI caches.\",\n          \"CheckStatus\":\"INFO\",\n          "
            "\"CheckResult\":{\n            \"BInstallerChecker\":\"App "
            "info\"\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(OneapiChecker, OnlyAptCheckerInitialized) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("AptChecker initialized"), Return(true)));
  EXPECT_CALL(aptChecker, GetAppInfo(_))
      .WillOnce(DoAll(SetArgReferee<0>("{ \"AptChecker\":\"App info\" }"),
                      Return(true)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("Failed to initialize BInstallerChecker"),
                Return(false)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize RpmChecker"),
                      Return(false)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(message,
            "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
            "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
            "\"oneAPI products\":{\n          \"Command\":\"Parse installed "
            "dpkg packages.\",\n          \"CheckStatus\":\"INFO\",\n          "
            "\"CheckResult\":{\n            \"AptChecker\":\"App info\"\n      "
            "    }\n        }\n      }\n    }\n  }\n}");
}

TEST(OneapiChecker, OnlyRpmCheckerInitialized) {
  string message;
  AptCheckerMock aptChecker;
  BInstallerCheckerMock bInstallerChecker;
  RpmCheckerMock rpmChecker;

  OneapiChecker sut(&aptChecker, &bInstallerChecker, &rpmChecker);

  // given
  EXPECT_CALL(aptChecker, Initialize(_))
      .WillOnce(DoAll(SetArgReferee<0>("Failed to initialize AptChecker"),
                      Return(false)));
  EXPECT_CALL(bInstallerChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("Failed to initialize BInstallerChecker"),
                Return(false)));
  EXPECT_CALL(rpmChecker, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>("RpmChecker initialized"), Return(true)));
  EXPECT_CALL(rpmChecker, GetAppInfo(_))
      .WillOnce(DoAll(SetArgReferee<0>("{ \"RpmChecker\":\"App info\" }"),
                      Return(true)));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(message,
            "{\n  \"CheckResult\":{\n    \"APP\":{\n      "
            "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
            "\"oneAPI products\":{\n          \"Command\":\"Parse installed "
            "rpm packages.\",\n          \"CheckStatus\":\"INFO\",\n          "
            "\"CheckResult\":{\n            \"RpmChecker\":\"App info\"\n      "
            "    }\n        }\n      }\n    }\n  }\n}");
}