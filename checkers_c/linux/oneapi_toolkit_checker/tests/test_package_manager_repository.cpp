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
#include <sqlite3.h>

#include "Mocks.h"
#include "PackageManagerRepository.h"

using ::std::string;
using ::testing::_;
using ::testing::DoAll;
using ::testing::IsEmpty;
using ::testing::IsNull;
using ::testing::Return;
using ::testing::SetArgPointee;
using ::testing::SizeIs;
using ::testing::StrCaseEq;
using ::testing::StrEq;
using ::testing::StrictMock;

TEST(TestPackageManagerRepository, WhenFailedToOpenThenReturnFalse) {
  // given
  string dbPath = "/var/intel/installercache/packagemanager.db";
  string message;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(sqliteLibWrapper,
              Open(StrEq(dbPath), _, SQLITE_OPEN_READONLY, IsNull()))
      .WillOnce(Return(SQLITE_ERROR));
  EXPECT_CALL(sqliteLibWrapper, ErrorMsg(_))
      .WillOnce(Return("<Sqlite error message>"));
  // EXPECT_CALL(sqliteLibWrapper, Close(_))
  //     .Times(1);

  // when
  bool result = sut.Open(dbPath, message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Cannot open Binary Installer "
            "database./var/intel/installercache/packagemanager.db: "
            "<Sqlite error message>\n");
}

TEST(TestPackageManagerRepository, WhenSucceededToOpenThenReturnTrue) {
  // given
  string dbPath = "/var/intel/installercache/packagemanager.db";
  string message;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(sqliteLibWrapper,
              Open(StrEq(dbPath), _, SQLITE_OPEN_READONLY, IsNull()))
      .WillOnce(
          DoAll(SetArgPointee<1>((sqlite3 *)0x0000001), Return(SQLITE_OK)));
  EXPECT_CALL(sqliteLibWrapper, Close(_)).Times(1);

  // when
  bool result = sut.Open(dbPath, message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, "");
}

TEST(TestPackageManagerRepository,
     GetPackageInstallationPathWhenFailedToPrepareStatement) {
  // given
  string message;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(
      sqliteLibWrapper,
      Prepare(_, StrCaseEq("SELECT PATH FROM INSTALL_DIR;"), -1, _, IsNull()))
      .WillOnce(Return(SQLITE_ERROR));
  EXPECT_CALL(sqliteLibWrapper, ErrorMsg(_))
      .WillOnce(Return("<Sqlite error message>"));
  EXPECT_CALL(sqliteLibWrapper, Finalize(_));

  // when
  bool result = sut.GetPackageInstallationPath(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Error while compiling SQL statement \"SELECT PATH FROM "
            "INSTALL_DIR;\": <Sqlite error message>\n");
}

TEST(TestPackageManagerRepository, GetPackageInstallationPathWhenNoPathInDb) {
  // given
  string message;
  string packagePath;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(
      sqliteLibWrapper,
      Prepare(_, StrCaseEq("SELECT PATH FROM INSTALL_DIR;"), -1, _, IsNull()))
      .WillOnce(Return(SQLITE_OK));
  EXPECT_CALL(sqliteLibWrapper, Step(_)).WillOnce(Return(SQLITE_DONE));
  EXPECT_CALL(sqliteLibWrapper, Finalize(_));

  // when
  bool result = sut.GetPackageInstallationPath(message);

  // then
  ASSERT_FALSE(result);
  ASSERT_EQ(message,
            "Unable to find oneAPI package. Your database format is "
            "not supported by the current version of this check.\n");
}

TEST(TestPackageManagerRepository, GetPackageInstallationPathWhenPathInDb) {
  // given
  string message;
  string packagePath;
  string expectedPath = "/package/installation/path";
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(
      sqliteLibWrapper,
      Prepare(_, StrCaseEq("SELECT PATH FROM INSTALL_DIR;"), -1, _, IsNull()))
      .WillOnce(Return(SQLITE_OK));
  EXPECT_CALL(sqliteLibWrapper, Step(_)).WillOnce(Return(SQLITE_ROW));
  EXPECT_CALL(sqliteLibWrapper, ColumnText(_, 0))
      .WillOnce(Return((unsigned char *)expectedPath.c_str()));
  EXPECT_CALL(sqliteLibWrapper, Finalize(_));

  // when
  bool result = sut.GetPackageInstallationPath(message);

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, expectedPath);
}

TEST(TestPackageManagerRepository,
     GetInstalledProductNamesWhenMultipleRecords) {
  // given
  string message;
  vector<Component *> products;
  std::function<Component *()> productIterator;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(
      sqliteLibWrapper,
      Prepare(
          _,
          StrCaseEq("SELECT ID, VERSION FROM COMPONENT ORDER BY ID, VERSION;"),
          -1, _, IsNull()))
      .WillOnce(Return(SQLITE_OK));
  EXPECT_CALL(sqliteLibWrapper, Step(_))
      .WillOnce(Return(SQLITE_ROW))
      .WillOnce(Return(SQLITE_ROW))
      .WillOnce(Return(SQLITE_ROW))
      .WillRepeatedly(Return(SQLITE_DONE));
  EXPECT_CALL(sqliteLibWrapper, ColumnText(_, 0))
      .WillOnce(Return((unsigned char *)"intel.oneapi.lin.advisor"))
      .WillOnce(Return((unsigned char *)"intel.oneapi.lin.basekit.product"))
      .WillOnce(Return((unsigned char *)"intel.oneapi.lin.ccl.runtime"));
  EXPECT_CALL(sqliteLibWrapper, ColumnText(_, 1))
      .WillOnce(Return((unsigned char *)"2023.0.0-25338"))
      .WillOnce(Return((unsigned char *)"2023.0.0-25537"))
      .WillOnce(Return((unsigned char *)"2021.8.0-25371"));
  EXPECT_CALL(sqliteLibWrapper, Finalize(_));

  // when
  bool result = sut.GetComponents(productIterator, message);
  Component *product;
  while ((product = productIterator()) != nullptr) {
    products.push_back(product);
  }

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, "");
  ASSERT_THAT(products, SizeIs(3));
  ASSERT_EQ(products[0]->id, "intel.oneapi.lin.advisor");
  ASSERT_EQ(products[0]->fullVersion, "2023.0.0-25338");
  ASSERT_EQ(products[1]->id, "intel.oneapi.lin.basekit.product");
  ASSERT_EQ(products[1]->fullVersion, "2023.0.0-25537");
  ASSERT_EQ(products[2]->id, "intel.oneapi.lin.ccl.runtime");
  ASSERT_EQ(products[2]->fullVersion, "2021.8.0-25371");
}

TEST(TestPackageManagerRepository, GetInstalledProductNamesWhenNoRecords) {
  // given
  string message;
  vector<Component *> products;
  std::function<Component *()> productIterator;
  StrictMock<Sqlite3WrapperMock> sqliteLibWrapper;

  PackageManagerRepository sut(&sqliteLibWrapper);

  EXPECT_CALL(
      sqliteLibWrapper,
      Prepare(
          _,
          StrCaseEq("SELECT ID, VERSION FROM COMPONENT ORDER BY ID, VERSION;"),
          -1, _, IsNull()))
      .WillOnce(Return(SQLITE_OK));
  EXPECT_CALL(sqliteLibWrapper, Step(_)).WillRepeatedly(Return(SQLITE_DONE));
  EXPECT_CALL(sqliteLibWrapper, Finalize(_));

  // when
  bool result = sut.GetComponents(productIterator, message);
  Component *product;
  while ((product = productIterator()) != nullptr) {
    products.push_back(product);
  }

  // then
  ASSERT_TRUE(result);
  ASSERT_EQ(message, "");
  ASSERT_THAT(products, IsEmpty());
}