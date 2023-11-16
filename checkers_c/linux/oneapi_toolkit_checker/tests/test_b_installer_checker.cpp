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
#include <pwd.h>

#include <memory>
#include <string>

#include "BInstallerChecker.h"
#include "CommonMocks.h"
#include "Mocks.h"

using ::std::make_shared;
using ::std::shared_ptr;
using ::std::string;
using ::testing::_;
using ::testing::Address;
using ::testing::Contains;
using ::testing::DoAll;
using ::testing::IsEmpty;
using ::testing::Return;
using ::testing::SetArgReferee;
using ::testing::SizeIs;
using ::testing::StrictMock;

TEST(TestBInstallerChecker,
     InitializeAsPrivilegedUserWhenFailToFindCachesShouldReturnFalse) {
  // given
  string message;
  vector<string> cache;
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(osUtils, GetEUid()).WillOnce(Return(0));
  EXPECT_CALL(
      osUtils,
      RunCommand(
          "find /var/intel -name 'packagemanager.db' -type f 2>/dev/null", _))
      .WillOnce(DoAll(SetArgReferee<1>(""), Return(-1)));

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Cannot obtain paths to package manager databases.");
  ASSERT_THAT(cache, IsEmpty());
}

TEST(TestBInstallerChecker,
     InitializeAsPrivilagedUserWhenSuccedToFindCachesShouldReturnTrue) {
  // given
  string message;
  vector<string> cache;
  string dbPaths = "/var/intel/installercache/packagemanager.db\n";
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(osUtils, GetEUid()).WillOnce(Return(0));
  EXPECT_CALL(
      osUtils,
      RunCommand(
          "find /var/intel -name 'packagemanager.db' -type f 2>/dev/null", _))
      .WillOnce(DoAll(SetArgReferee<1>(dbPaths), Return(0)));

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, "");
  ASSERT_THAT(cache, SizeIs(1));
  ASSERT_THAT(cache, Contains("/var/intel/installercache/"));
}

TEST(TestBInstallerChecker,
     InitializeAsUnprivilegedUserWhenCannotFindUserShouldReturnFalse) {
  // given
  string message;
  vector<string> cache;
  const uid_t uid = 1000;
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(osUtils, GetEUid()).WillRepeatedly(Return(uid));
  EXPECT_CALL(osUtils, GetPwUid(uid)).WillRepeatedly(Return(nullptr));
  EXPECT_CALL(
      osUtils,
      RunCommand(
          "find /var/intel -name 'packagemanager.db' -type f 2>/dev/null", _))
      .WillOnce(DoAll(SetArgReferee<1>(""), Return(0)));

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Cannot get user name. Try running as a different user.");
  ASSERT_THAT(cache, IsEmpty());
}

TEST(
    TestBInstallerChecker,
    InitializeAsUnprivilegedUserWhenSuccedToFindUserAndFindCachesShouldReturnTrue) {
  // given
  string message;
  vector<string> cache;
  uid_t uid = 1000;
  string rootDbPaths = "/var/intel/installercache/packagemanager.db\n";
  string dbPaths = "/home/user/intel/diagnostics/databases/packagemanager.db\n";
  char username[] = "user";
  char password[] = "password";
  char gecos[] = "user info";
  char dir[] = "/home/user";
  char shell[] = "/bin/bash";
  passwd pwd = {username, password, uid, 1000, gecos, dir, shell};

  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(osUtils, GetEUid()).WillRepeatedly(Return(uid));
  EXPECT_CALL(osUtils, GetPwUid(uid)).WillRepeatedly(Return(&pwd));
  EXPECT_CALL(
      osUtils,
      RunCommand(
          "find /var/intel -name 'packagemanager.db' -type f 2>/dev/null", _))
      .WillOnce(DoAll(SetArgReferee<1>(rootDbPaths), Return(0)));
  EXPECT_CALL(
      osUtils,
      RunCommand(
          "find /home/user/intel -name 'packagemanager.db' -type f 2>/dev/null",
          _))
      .WillOnce(DoAll(SetArgReferee<1>(dbPaths), Return(0)));

  // when
  bool result = sut.Initialize(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, "");
  ASSERT_THAT(cache, SizeIs(2));
  ASSERT_THAT(cache, Contains("/var/intel/installercache/"));
  ASSERT_THAT(cache, Contains("/home/user/intel/diagnostics/databases/"));
}

TEST(TestBInstallerChecker,
     GivenNoCachedPathsWhenGetAppInfoThenShouldRetunFalse) {
  // given
  string message;
  vector<string> cache;
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "");
}

TEST(TestBInstallerChecker,
     GivenFailsToOpenDbWhenGetAppInfoThenShouldReturnFalse) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(DoAll(SetArgReferee<1>("Error message"), Return(false)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Error message");
}

TEST(TestBInstallerChecker,
     GivenFailsToGetPackageInstallPathWhenGetAppInfoThenShouldReturnFalse) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetPackageInstallationPath(_))
      .WillOnce(DoAll(SetArgReferee<0>("Error message"), Return(false)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Error message");
}

TEST(TestBInstallerChecker,
     WhenErrorWhileQueryingProductNamesThenShouldReturnFalse) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetPackageInstallationPath(_))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetComponents(_, _))
      .WillOnce(DoAll(SetArgReferee<1>("Error message"), Return(false)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "Error message");
}

TEST(TestBInstallerChecker, GetAppInfoWhenNoProducts) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetPackageInstallationPath(_))
      .WillOnce(DoAll(SetArgReferee<0>("/opt/intel/oneapi"), Return(true)));
  EXPECT_CALL(*packageManagerRepository, GetComponents(_, _))
      .WillOnce(DoAll(SetArgReferee<0>([]() -> Component* { return nullptr; }),
                      Return(true)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message, "");
}

TEST(TestBInstallerChecker,
     WhenErrorWhileReadingManifestJsonThenShouldReturnFalse) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetPackageInstallationPath(_))
      .WillOnce(DoAll(SetArgReferee<0>("/opt/intel/oneapi"), Return(true)));
  EXPECT_CALL(*packageManagerRepository, GetComponents(_, _))
      .WillOnce(DoAll(SetArgReferee<0>([]() {
                        int i = 0;
                        return [=]() mutable -> Component* {
                          switch (i++) {
                            case 0:
                              return new Component{
                                  "intel.oneapi.lin.basekit.getting_started",
                                  "2023.0.0-25537"};
                            case 1:
                              return new Component{"intel.oneapi.lin.dpcpp-ct",
                                                   "2023.0.0-25483"};
                            case 2:
                              return new Component{"intel.oneapi.lin.dnnl",
                                                   "2023.0.0-25399"};
                            default:
                              return nullptr;
                          }
                        };
                      }()),
                      Return(true)));
  EXPECT_CALL(osUtils, LoadFile(_, _))
      .WillOnce(DoAll(SetArgReferee<1>("<Loading file error>"), Return(false)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Cannot obtain human readable product names: <Loading file error>");
}

string jsonA =
    "{"
    "    \"display\": {"
    "        \"localized\": ["
    "            {"
    "                \"description\": \"Develop accelerated C++ and DPC++ "
    "applications for CPUs, and GPUs. Toolkit includes compilers, "
    "pre-optimized libraries, and analysis tools for optimizing workloads "
    "including AI, HPC, and media.\",\"language\": \"en-us\","
    "                \"title\": \"Intel® oneAPI Base Toolkit\","
    "                \"version\": \"2023.0.0\""
    "            }"
    "        ]"
    "    }"
    "}";
string jsonB =
    "{"
    "    \"display\": {"
    "        \"localized\": ["
    "            {"
    "                \"description\": \"Not american english description\","
    "                \"language\": \"not-en-us\","
    "                \"title\": \"Not american english title\","
    "                \"version\": \"2023.0.0\""
    "            }"
    "        ]"
    "    },"
    "    \"visible\": true"
    "}";
string jsonC =
    "{"
    "    \"display\": {"
    "        \"localized\": ["
    "            {"
    "                \"description\": \"Not en-us description\","
    "                \"language\": \"not-en-us\","
    "                \"title\": \"Not en-us title\","
    "                \"version\": \"Not en-us version\""
    "            },"
    "            {"
    "                \"description\": \"Develop fast neural networks on Intel "
    "CPUs and GPUs with performance-optimized building blocks.\","
    "                \"language\": \"en-us\","
    "                \"title\": \"Intel® oneAPI Deep Neural Network Library\","
    "                \"version\": \"2023.0.0\""
    "            }"
    "        ]"
    "    },"
    "    \"visible\": true"
    "}";

TEST(TestBInstallerChecker, GetAppInfoWhenMultipleComponents) {
  // given
  string message;
  string dbDir = "/var/intel/installercache/";
  string dbPath = dbDir + "packagemanager.db";
  vector<string> cache = {dbDir};
  StrictMock<OsUtilsMock> osUtils;
  StrictMock<PackageManagerRepositoryFactoryMock>
      packageManagerRepositoryFactory;
  auto packageManagerRepository =
      make_shared<StrictMock<PackageManagerRepositoryMock>>();

  BInstallerChecker sut(&osUtils, &packageManagerRepositoryFactory, &cache);

  EXPECT_CALL(packageManagerRepositoryFactory, GetPackageManagerRepository())
      .WillOnce(Return(packageManagerRepository));
  EXPECT_CALL(*packageManagerRepository, Open(dbPath, _))
      .WillOnce(Return(true));
  EXPECT_CALL(*packageManagerRepository, GetPackageInstallationPath(_))
      .WillOnce(DoAll(SetArgReferee<0>("/opt/intel/oneapi"), Return(true)));
  EXPECT_CALL(*packageManagerRepository, GetComponents(_, _))
      .WillOnce(DoAll(SetArgReferee<0>([]() {
                        int i = 0;
                        return [=]() mutable -> Component* {
                          switch (i++) {
                            case 0:
                              return new Component{
                                  "intel.oneapi.lin.basekit.getting_started",
                                  "2023.0.0-25537"};
                            case 1:
                              return new Component{"intel.oneapi.lin.dpcpp-ct",
                                                   "2023.0.0-25483"};
                            case 2:
                              return new Component{"intel.oneapi.lin.dnnl",
                                                   "2023.0.0-25399"};
                            default:
                              return nullptr;
                          }
                        };
                      }()),
                      Return(true)));
  string manifestPath =
      "/var/intel/installercache/packagescache/"
      "intel.oneapi.lin.basekit.getting_started,v=2023.0.0-25537/manifest.json";
  EXPECT_CALL(osUtils, LoadFile(manifestPath, _))
      .WillOnce(DoAll(SetArgReferee<1>(jsonA), Return(true)));
  manifestPath =
      "/var/intel/installercache/packagescache/"
      "intel.oneapi.lin.dpcpp-ct,v=2023.0.0-25483/manifest.json";
  EXPECT_CALL(osUtils, LoadFile(manifestPath, _))
      .WillOnce(DoAll(SetArgReferee<1>(jsonB), Return(true)));
  manifestPath =
      "/var/intel/installercache/packagescache/"
      "intel.oneapi.lin.dnnl,v=2023.0.0-25399/manifest.json";
  EXPECT_CALL(osUtils, LoadFile(manifestPath, _))
      .WillOnce(DoAll(SetArgReferee<1>(jsonC), Return(true)));

  // when
  bool result = sut.GetAppInfo(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(
      message,
      "{ \"Not american english title\": { \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": { \"Product ID\": { \"Verbosity\": 1, \"CheckStatus\": "
      "\"INFO\", \"CheckResult\": \"intel.oneapi.lin.dpcpp-ct\" }, "
      "\"Version\": { \"CheckStatus\": \"INFO\", \"CheckResult\": \"2023.0.0\" "
      "}, \"Full Version\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"2023.0.0-25483\" }, \"Description\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": \"Not "
      "american english description\" }, \"Path\": { \"Verbosity\": 1, "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"\\/opt\\/intel\\/oneapi\" "
      "} } }, \"Intel\xC2\xAE oneAPI Deep Neural Network Library\": { "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": { \"Product ID\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"intel.oneapi.lin.dnnl\" }, \"Version\": { \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"2023.0.0\" }, \"Full Version\": { \"Verbosity\": 1, "
      "\"CheckStatus\": \"INFO\", \"CheckResult\": \"2023.0.0-25399\" }, "
      "\"Description\": { \"Verbosity\": 1, \"CheckStatus\": \"INFO\", "
      "\"CheckResult\": \"Develop fast neural networks on Intel CPUs and GPUs "
      "with performance-optimized building blocks.\" }, \"Path\": { "
      "\"Verbosity\": 1, \"CheckStatus\": \"INFO\", \"CheckResult\": "
      "\"\\/opt\\/intel\\/oneapi\" } } } }");
}
