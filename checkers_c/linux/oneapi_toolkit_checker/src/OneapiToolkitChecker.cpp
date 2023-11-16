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
#include "OneapiToolkitChecker.h"

#include "AptChecker.h"
#include "BInstallerChecker.h"
#include "CheckerHelper.h"
#include "JsonNode.h"
#include "RpmChecker.h"

OneapiChecker::OneapiChecker(AptChecker *aptChecker,
                             BInstallerChecker *bInstallerChecker,
                             RpmChecker *rpmChecker)
    : aptChecker(aptChecker),
      bInstallerChecker(bInstallerChecker),
      rpmChecker(rpmChecker) {}

int OneapiChecker::PerformCheck(string &message) {
  json_object *root = json_object_new_object();
  json_object *top = json_object_new_object();
  json_object *apps = json_object_new_object();

  JsonNode::AddJsonTopNode(root, top);
  JsonNode::AddJsonNode(top, "APP", STATUS_INFO, apps);

  string message1, message2, message3;
  bool binary_installer_is_found = false,
       package_manager_installer_is_found = false,
       rpm_package_manager_installer_is_found = false;
  int result = CHECK_STATUS_SUCCESS;
  if (!bInstallerChecker->Initialize(message1)) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_ERROR, message1, "",
                          0, "");
    result = CHECK_STATUS_ERROR;
  } else {
    message1.clear();
    binary_installer_is_found = bInstallerChecker->GetAppInfo(message1);
  }

  if (!aptChecker->Initialize(message2)) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_ERROR, message2, "",
                          0, "");
    result = CHECK_STATUS_ERROR;
  } else {
    message2.clear();
    package_manager_installer_is_found = aptChecker->GetAppInfo(message2);
  }

  if (!rpmChecker->Initialize(message3)) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_ERROR, message3, "",
                          0, "");
    result = CHECK_STATUS_ERROR;
  } else {
    message3.clear();
    rpm_package_manager_installer_is_found = rpmChecker->GetAppInfo(message3);
  }

  if (binary_installer_is_found && package_manager_installer_is_found) {
    // Glue 2 output from dpkg and binary installer into a single JSON node
    JsonNode::AddJsonNode(
        apps, "oneAPI products", STATUS_INFO, "",
        "Parse installed oneAPI caches and installed dpkg packages.", 0,
        json_tokener_parse(
            (message1.erase(message1.size() - 1) + "," + message2.erase(0, 1))
                .c_str()));
  } else if (binary_installer_is_found &&
             rpm_package_manager_installer_is_found) {
    // Glue 2 output from rpm and binary installer into a single JSON node
    JsonNode::AddJsonNode(
        apps, "oneAPI products", STATUS_INFO, "",
        "Parse installed oneAPI caches and installed rpm packages.", 0,
        json_tokener_parse(
            (message1.erase(message1.size() - 1) + "," + message3.erase(0, 1))
                .c_str()));
  } else if (binary_installer_is_found) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_INFO, "",
                          "Parse installed oneAPI caches.", 0,
                          json_tokener_parse(message1.c_str()));
  } else if (package_manager_installer_is_found) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_INFO, "",
                          "Parse installed dpkg packages.", 0,
                          json_tokener_parse(message2.c_str()));
  } else if (rpm_package_manager_installer_is_found) {
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_INFO, "",
                          "Parse installed rpm packages.", 0,
                          json_tokener_parse(message3.c_str()));
  } else {
    // No products installed by Binary Installer or dpkg manager were found.
    // ToDo: log all error messages. Currently they are dropped.
    stringstream ss;
    ss << "Cannot locate installed oneAPI products. Additional information: "
       << endl;
    if (!message1.empty()) ss << message1 << endl;
    if (!message2.empty()) ss << message2;
    JsonNode::AddJsonNode(apps, "oneAPI products", STATUS_INFO, ss.str());
    // Skip check of dependencies
    message =
        string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));
    return result;
  }

  message =
      string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));

  if (message.find("WARNING") != std::string::npos) {
    result = CHECK_STATUS_SUCCESS;
  }
  if (message.find("FAIL") != std::string::npos) {
    result = CHECK_STATUS_FAIL;
  }
  if (message.find("ERROR") != std::string::npos) {
    result = CHECK_STATUS_ERROR;
  }

  return result;
}
