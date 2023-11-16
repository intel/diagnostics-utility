#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <string>

#include "GpuBackendChecker.h"
#include "Mocks.h"
#include "checker_interface.h"
#include "checker_list_interface.h"

using ::testing::_;
using ::testing::DoAll;
using ::testing::Ref;
using ::testing::Return;
using ::testing::SetArgReferee;

TEST(GpuBackendChecker, GetApiVersionReturnsRightVersion) {
  std::string version;

  version = std::string(get_api_version());

  EXPECT_EQ(version, "0.2");
}

TEST(GpuBackendChecker, DriversNotLoaded) {
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(Ref(message))).WillOnce(Return(false));
  EXPECT_CALL(clMock, Load(Ref(message))).WillOnce(Return(false));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              "
      "\"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n   "
      "         }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 "
      "Driver\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":{\n            \"Driver is loaded\":{"
      "\n              \"CheckStatus\":\"ERROR\",\n      "
      "        \"CheckResult\":\"\"\n            }\n          }\n        }\n   "
      "   }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, LevelZeroNotInitialized) {
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, Initialize(_))
      .WillOnce(
          DoAll(SetArgReferee<0>(
                    "Intel® oneAPI Level Zero driver is not initialized."),
                Return(false)));

  EXPECT_CALL(clMock, Load(_))
      .WillOnce(DoAll(SetArgReferee<0>(""), Return(false)));

  // when
  int check_status = sut.PerformCheck(message);

  // then
  ASSERT_EQ(check_status, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n      "
      "        \"CheckResult\":\"\"\n            },\n            \"Driver "
      "information\":{\n              \"Message\":\"Intel\xC2\xAE oneAPI Level "
      "Zero driver is not initialized.\",\n              "
      "\"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n        "
      "    }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 "
      "Driver\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":{\n            \"Driver is loaded\":{\n              "
      "\"CheckStatus\":\"ERROR\",\n      "
      "        \"CheckResult\":\"\"\n            }\n          }\n        }\n   "
      "   }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, NoDriverInfo) {
  const string invalidJson = "This is not valid JSON";
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, Initialize(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(invalidJson));

  EXPECT_CALL(clMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(clMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(invalidJson));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 3);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n      "
      "        \"CheckResult\":\"\"\n            },\n            \"Driver "
      "information\":{\n              \"Message\":\"Unable to get driver "
      "information.\",\n              \"CheckStatus\":\"ERROR\",\n             "
      " \"CheckResult\":\"\"\n            }\n          }\n        },\n        "
      "\"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n  "
      "        \"CheckResult\":{\n            \"Driver is loaded\":{\n         "
      "     \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n    "
      "        },\n            \"Driver information\":{\n              "
      "\"Message\":\"Unable to get driver information.\",\n              "
      "\"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n        "
      "    }\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnFail) {
  const string validJson =
      "{\"CheckResult\": \"This is valid string\", \"CheckStatus\":\"FAIL\"}";
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, Initialize(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  EXPECT_CALL(clMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(clMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 2);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n      "
      "        \"CheckResult\":\"\"\n            },\n            \"Driver "
      "information\":{\n              \"CheckStatus\":\"INFO\",\n              "
      "\"CheckResult\":{\n                \"CheckResult\":\"This is valid "
      "string\",\n                \"CheckStatus\":\"FAIL\"\n              }\n  "
      "          }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 "
      "Driver\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":{\n            \"Driver is loaded\":{\n              "
      "\"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n         "
      "   },\n            \"Driver information\":{\n              "
      "\"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n            "
      "    \"CheckResult\":\"This is valid string\",\n                "
      "\"CheckStatus\":\"FAIL\"\n              }\n            }\n          }\n "
      "       }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnWarning) {
  const string validJson =
      "{\"CheckResult\": \"This is valid string\", "
      "\"CheckStatus\":\"WARNING\"}";
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, Initialize(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  EXPECT_CALL(clMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(clMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 1);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n      "
      "        \"CheckResult\":\"\"\n            },\n            \"Driver "
      "information\":{\n              \"CheckStatus\":\"INFO\",\n              "
      "\"CheckResult\":{\n                \"CheckResult\":\"This is valid "
      "string\",\n                \"CheckStatus\":\"WARNING\"\n              "
      "}\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 "
      "Driver\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":{\n            \"Driver is loaded\":{\n              "
      "\"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n         "
      "   },\n            \"Driver information\":{\n              "
      "\"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n            "
      "    \"CheckResult\":\"This is valid string\",\n                "
      "\"CheckStatus\":\"WARNING\"\n              }\n            }\n          "
      "}\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnSuccess) {
  const string validJson =
      "{\"CheckResult\": \"This is valid string\", \"CheckStatus\":\"PASS\"}";
  string message;
  string lzMessage;
  string clMessage;
  LZ_DriverCheckerMock lzMock;
  CL_DriverCheckerMock clMock;

  GpuBackendChecker sut(&lzMock, &clMock);

  // given
  EXPECT_CALL(lzMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, Initialize(_)).WillOnce(Return(true));
  EXPECT_CALL(lzMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  EXPECT_CALL(clMock, Load(_)).WillOnce(Return(true));
  EXPECT_CALL(clMock, GetDriverInfo(_)).WillOnce(SetArgReferee<0>(validJson));

  // when
  int retVal = sut.PerformCheck(message);

  // then
  ASSERT_EQ(retVal, 0);
  ASSERT_EQ(
      message,
      "{\n  \"CheckResult\":{\n    \"GPU\":{\n      "
      "\"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        "
      "\"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          "
      "\"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            "
      "\"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n      "
      "        \"CheckResult\":\"\"\n            },\n            \"Driver "
      "information\":{\n              \"CheckStatus\":\"INFO\",\n              "
      "\"CheckResult\":{\n                \"CheckResult\":\"This is valid "
      "string\",\n                \"CheckStatus\":\"PASS\"\n              }\n  "
      "          }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 "
      "Driver\":{\n          \"CheckStatus\":\"INFO\",\n          "
      "\"CheckResult\":{\n            \"Driver is loaded\":{\n              "
      "\"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n         "
      "   },\n            \"Driver information\":{\n              "
      "\"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n            "
      "    \"CheckResult\":\"This is valid string\",\n                "
      "\"CheckStatus\":\"PASS\"\n              }\n            }\n          }\n "
      "       }\n      }\n    }\n  }\n}");
}
