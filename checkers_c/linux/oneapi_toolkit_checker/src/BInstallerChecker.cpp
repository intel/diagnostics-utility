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

#include "BInstallerChecker.h"

#include <sqlite3.h>

const char *ROOT_IC_PATH =
    "/var/intel";  // Path to search root installer cache folder
const char *USER_IC_PATH =
    "/intel";  // Path to search user installer cache folder
const char *DB_NAME = "packagemanager.db";

BInstallerChecker::BInstallerChecker() {
  os = nullptr;
  CachePaths = nullptr;
}

BInstallerChecker::BInstallerChecker(
    OsUtils *osUtils,
    PackageManagerRepositoryFactory *packageManagerRepositoryFactory,
    vector<string> *cache)
    : os(osUtils),
      packageManagerRepositoryFactory(packageManagerRepositoryFactory),
      CachePaths(cache) {}

bool BInstallerChecker::Initialize(string &message) {
  bool status = false;
  uid_t myprivs = os->GetEUid();

  // Always try to read root database
  status = FindCaches(ROOT_IC_PATH, message);

  if (myprivs != 0) {
    // Run as not privileged user
    passwd *pw = os->GetPwUid(os->GetEUid());
    if ((!pw) || (!pw->pw_dir)) {
      message = "Cannot get user name. Try running as a different user.";
      return false;
    }

    stringstream ss;
    ss << pw->pw_dir << USER_IC_PATH;
    if (FindCaches(ss.str(), message)) status = true;
  }

  return status;
}

bool BInstallerChecker::GetAppInfo(string &message) {
  string info;
  string errorMessage;
  for (string path : *CachePaths) {
    if (GetAppInfo(path + DB_NAME, path, info)) {
      message = info;
    } else {
      errorMessage += info;
    }
  }

  if (message.size() == 0) {
    // No product information was found. Return error message.
    message = errorMessage;
    return false;
  }

  if (message == "{ }") {
    // No visible products were found.
    message = {};
    return false;
  }

  if (errorMessage.size() != 0) {
    message += errorMessage;
    return false;
  }

  return true;
}

bool BInstallerChecker::GetAppInfo(string dbPath, string icPath,
                                   string &message) {
  json_object *node = json_object_new_object();

  auto packageManager =
      packageManagerRepositoryFactory->GetPackageManagerRepository();

  if (!packageManager->Open(dbPath, message)) return false;

  if (!packageManager->GetPackageInstallationPath(message)) return false;
  string package_path = message;

  std::function<Component *()> nextProduct;
  if (!packageManager->GetComponents(nextProduct, message)) return false;

  Component *productRecord;
  while ((productRecord = nextProduct()) != nullptr) {
    stringstream ss;
    ss << icPath << "packagescache/" << productRecord->id
       << ",v=" << productRecord->fullVersion << +"/manifest.json";
    if (!os->LoadFile(ss.str(), message)) {
      stringstream ss;
      ss << "Cannot obtain human readable product names: " << message;
      message = ss.str();
      return false;
    }
    json_object *root = json_tokener_parse(message.c_str());
    if (json_object_get_boolean(json_object_object_get(root, "visible")) != 0) {
      json_object *localizedDisplay = json_object_object_get(
          json_object_object_get(root, "display"), "localized");

      const char *description = nullptr, *title = nullptr, *version = nullptr;
      // Loop through array of localizations and fill the fields with "en-us"
      // localization or with the first one if it is not exist.
      for (size_t i = 0; i < json_object_array_length(localizedDisplay); i++) {
        json_object *localize = json_object_array_get_idx(localizedDisplay, i);

        const char *language = json_object_get_string(
            json_object_object_get(localize, "language"));
        if (description == nullptr || strcmp(language, "en-us") == 0)
          description = json_object_get_string(
              json_object_object_get(localize, "description"));
        if (title == nullptr || strcmp(language, "en-us") == 0)
          title =
              json_object_get_string(json_object_object_get(localize, "title"));
        if (version == nullptr || strcmp(language, "en-us") == 0)
          version = json_object_get_string(
              json_object_object_get(localize, "version"));
      }

      json_object *product = json_object_new_object();
      JsonNode::AddJsonNode(node, title, STATUS_INFO, product);
      JsonNode::AddJsonNode(product, "Product ID", STATUS_INFO, 1,
                            productRecord->id);
      JsonNode::AddJsonNode(product, "Version", STATUS_INFO, version);
      JsonNode::AddJsonNode(product, "Full Version", STATUS_INFO, 1,
                            productRecord->fullVersion);
      JsonNode::AddJsonNode(product, "Description", STATUS_INFO, 1,
                            description);
      JsonNode::AddJsonNode(product, "Path", STATUS_INFO, 1, package_path);
    }
  }

  const char *json_string = json_object_to_json_string(node);
  if (json_string == NULL) {
    message = "Cannot convert json object to string.";
  } else {
    message = string(json_string);
  }

  return true;
}

// Finds installer cache directories within specified path.
// The directories may have different names, so, search for package manager DB
// file in this directory. Expect that the DB file name is constant.
bool BInstallerChecker::FindCaches(string path, string &message) {
  stringstream ss;
  string out;
  // Find paths to package manager DB files within the specified path.
  ss << "find " << path << " -name '" << DB_NAME << "' -type f 2>/dev/null";
  int exit_status = os->RunCommand(ss.str().c_str(), out);
  if (exit_status != 0 || out.size() == 0) {
    message = "Cannot obtain paths to package manager databases.";
    return false;
  }

  vector<string> lines = CheckerHelper::SplitString(out, "\n");
  for (string s : lines) {
    CachePaths->push_back(s.substr(0, s.length() - strlen(DB_NAME)));
  }
  return true;
}
