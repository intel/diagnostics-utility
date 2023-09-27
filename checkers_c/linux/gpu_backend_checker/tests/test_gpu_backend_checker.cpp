#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "checker_list_interface.h"
#include "checker_interface.h"
#include "gpu_backend_checker.h"

#include <string>

using ::testing::_;
using ::testing::DoAll;
using ::testing::Return;
using ::testing::Ref;
using ::testing::SetArgReferee;

class LZ_DriverCheckerMock : public LZ_DriverChecker {
public:
	MOCK_METHOD(bool, Load, (string& message), (override));
	MOCK_METHOD(bool, Initialize, (string& message), (override));
	MOCK_METHOD(bool, GetLoaderVersion, (string& message), (override));
	MOCK_METHOD(void, GetDriverInfo, (string& message), (override));
	MOCK_METHOD(void, GetDeviceInfo, (ze_driver_handle_t driver, string& message), (override));
	MOCK_METHOD(string, GetErrorMessage, (ze_result_t error), (override));
	MOCK_METHOD(string, GetAPIVersionString, (_ze_api_version_t version), (override));
	MOCK_METHOD(string, GetDriverVersionString, (uint32_t version), (override));
	MOCK_METHOD(string, GetUUIDString, (ze_driver_uuid_t uuid), (override));
	MOCK_METHOD(string, GetUUIDString, (ze_device_uuid_t uuid), (override));
	MOCK_METHOD(string, GetDeviceTypeString, (ze_device_type_t type), (override));
};

class CL_DriverCheckerMock : public CL_DriverChecker {
public:
	MOCK_METHOD(bool, Load, (string &message), (override));
	MOCK_METHOD(void, GetDriverInfo, (string& message), (override));
	MOCK_METHOD(void, GetDeviceInfo, (cl_device_id deviceId, string& message), (override));
	MOCK_METHOD(string, GetErrorMessage, (cl_int error), (override));
	MOCK_METHOD(string, GetDeviceTypeString, (cl_device_type type), (override));
	MOCK_METHOD(string, GetArrayString, (size_t* array, size_t array_size), (override));
	MOCK_METHOD(string, GetCacheTypeString, (cl_device_mem_cache_type type), (override));
	MOCK_METHOD(string, GetLocalMemTypeString, (cl_device_local_mem_type type), (override));
};

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
    EXPECT_CALL(lzMock, Load(Ref(message)))
        .WillOnce(Return(false));
    EXPECT_CALL(clMock, Load(Ref(message)))
        .WillOnce(Return(false));
    
    // when
    int retVal = sut.PerformCheck(message);

    // then
    ASSERT_EQ(retVal, 3);
	ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"Message\":\"ERROR\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"Message\":\"ERROR\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, LevelZeroNotInitialized) {
	string message;
    string lzMessage;
    string clMessage;
    LZ_DriverCheckerMock lzMock;
    CL_DriverCheckerMock clMock;
    
    GpuBackendChecker sut(&lzMock, &clMock);

    // given
    EXPECT_CALL(lzMock, Load(_))
        .WillOnce(Return(true));
	EXPECT_CALL(lzMock, Initialize(_))
		.WillOnce(DoAll(SetArgReferee<0>("Intel® oneAPI Level Zero driver is not initialized."),
                        Return(false)));

    EXPECT_CALL(clMock, Load(_))
        .WillOnce(Return(false));
    
    // when
    int check_status = sut.PerformCheck(message);

    // then
    ASSERT_EQ(check_status, 3);
	ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"Message\":\"Intel\xC2\xAE oneAPI Level Zero driver is not initialized.\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"Message\":\"ERROR\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        }\n      }\n    }\n  }\n}");
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
    EXPECT_CALL(lzMock, Load(_))
        .WillOnce(Return(true));
	EXPECT_CALL(lzMock, Initialize(_))
		.WillOnce(Return(true));
    EXPECT_CALL(lzMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(invalidJson));

    EXPECT_CALL(clMock, Load(_))
        .WillOnce(Return(true));
    EXPECT_CALL(clMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(invalidJson));
    
    // when
    int retVal = sut.PerformCheck(message);

    // then
    ASSERT_EQ(retVal, 3);
    ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"Message\":\"Unable to get driver information.\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"Message\":\"Unable to get driver information.\",\n              \"CheckStatus\":\"ERROR\",\n              \"CheckResult\":\"\"\n            }\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnFail) {
    const string validJson = "{\"CheckResult\": \"This is valid string\", \"CheckStatus\":\"FAIL\"}";
    string message;
    string lzMessage;
    string clMessage;
    LZ_DriverCheckerMock lzMock;
    CL_DriverCheckerMock clMock;
    
    GpuBackendChecker sut(&lzMock, &clMock);

    // given
    EXPECT_CALL(lzMock, Load(_))
        .WillOnce(Return(true));
	EXPECT_CALL(lzMock, Initialize(_))
		.WillOnce(Return(true));
    EXPECT_CALL(lzMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));

    EXPECT_CALL(clMock, Load(_))
        .WillOnce(Return(true));
    EXPECT_CALL(clMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));
    
    // when
    int retVal = sut.PerformCheck(message);

    // then
    ASSERT_EQ(retVal, 2);
    ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"FAIL\"\n              }\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"FAIL\"\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnWarning) {
    const string validJson = "{\"CheckResult\": \"This is valid string\", \"CheckStatus\":\"WARNING\"}";
    string message;
    string lzMessage;
    string clMessage;
    LZ_DriverCheckerMock lzMock;
    CL_DriverCheckerMock clMock;
    
    GpuBackendChecker sut(&lzMock, &clMock);

    // given
    EXPECT_CALL(lzMock, Load(_))
        .WillOnce(Return(true));
	EXPECT_CALL(lzMock, Initialize(_))
		.WillOnce(Return(true));
    EXPECT_CALL(lzMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));

    EXPECT_CALL(clMock, Load(_))
        .WillOnce(Return(true));
    EXPECT_CALL(clMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));
    
    // when
    int retVal = sut.PerformCheck(message);

    // then
    ASSERT_EQ(retVal, 1);
    ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"WARNING\"\n              }\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"WARNING\"\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}");
}

TEST(GpuBackendChecker, ReturnSuccess) {
    const string validJson = "{\"CheckResult\": \"This is valid string\", \"CheckStatus\":\"PASS\"}";
    string message;
    string lzMessage;
    string clMessage;
    LZ_DriverCheckerMock lzMock;
    CL_DriverCheckerMock clMock;
    
    GpuBackendChecker sut(&lzMock, &clMock);

    // given
    EXPECT_CALL(lzMock, Load(_))
        .WillOnce(Return(true));
	EXPECT_CALL(lzMock, Initialize(_))
		.WillOnce(Return(true));
    EXPECT_CALL(lzMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));

    EXPECT_CALL(clMock, Load(_))
        .WillOnce(Return(true));
    EXPECT_CALL(clMock, GetDriverInfo(_))
        .WillOnce(SetArgReferee<0>(validJson));
    
    // when
    int retVal = sut.PerformCheck(message);

    // then
    ASSERT_EQ(retVal, 0);
    ASSERT_EQ(message, "{\n  \"CheckResult\":{\n    \"GPU\":{\n      \"CheckStatus\":\"INFO\",\n      \"CheckResult\":{\n        \"Intel\xC2\xAE oneAPI Level Zero Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded.\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"PASS\"\n              }\n            }\n          }\n        },\n        \"OpenCL\xE2\x84\xA2 Driver\":{\n          \"CheckStatus\":\"INFO\",\n          \"CheckResult\":{\n            \"Driver is loaded\":{\n              \"CheckStatus\":\"PASS\",\n              \"CheckResult\":\"\"\n            },\n            \"Driver information\":{\n              \"CheckStatus\":\"INFO\",\n              \"CheckResult\":{\n                \"CheckResult\":\"This is valid string\",\n                \"CheckStatus\":\"PASS\"\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}");
}


