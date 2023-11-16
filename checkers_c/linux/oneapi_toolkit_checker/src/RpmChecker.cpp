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

#include "RpmChecker.h"

#include "Product.h"

RpmChecker::RpmChecker() {}

RpmChecker::RpmChecker(OsUtils *osUtils) : os(osUtils) {}

bool RpmChecker::Initialize(string &message) { return true; }

bool RpmChecker::GetAppInfo(string &message) {
  string out;
  int exit_status;

  if (os->GetOsType() != RpmBased) {
    message =
        "Application information is not available for products installed "
        "by RPM.";
    return false;
  }

  // Extract information about installed packages
  exit_status = os->RunCommand(
      "rpm -q -a --qf '%{Name}\t%{Version}\t%{Arch}\t%{Summary}\t:%{Vendor}\n' "
      "| grep :Intel",
      out);
  if (exit_status != 0) {
    message = "Cannot obtain installed package.";
    return false;
  }

  // Parse output and translate it into JSON structure
  json_object *node = json_object_new_object();
  stringstream ss;
  vector<string> lines = CheckerHelper::SplitString(out, "\n");
  map<string, Product> products;
  // Each product can have multiple packages, so, go through the package list
  // and create a unique product list
  string package, version, arch, title;
  for (auto it = begin(lines); it != end(lines); ++it) {
    vector<string> fields = CheckerHelper::SplitString(*it, "\t");
    title.clear();
    if (fields.size() > 3) {
      package = fields[0];
      version = fields[1];
      arch = fields[2];
      title = fields[3] + " ";
    } else {
      package = "";
      version = "";
      arch = "";
    }
    auto product = products.find(title);
    if (product != products.end()) {
      product->second.Packages = product->second.Packages + ", " + package;
    } else {
      Product prod;
      prod.Packages = package;
      prod.Version = version;
      prod.Architecture = arch;
      prod.Title = title;
      products.insert({title, prod});
    }
  }

  // Encode products in JSON structure
  for (auto it = products.begin(); it != products.end(); it++) {
    json_object *product = json_object_new_object();
    JsonNode::AddJsonNode(node, it->second.Title, STATUS_INFO, product);
    JsonNode::AddJsonNode(product, "Packages", STATUS_INFO, 1,
                          it->second.Packages);
    JsonNode::AddJsonNode(
        product, "Version", STATUS_INFO,
        it->second.Version.substr(0, it->second.Version.find("-")));
    JsonNode::AddJsonNode(product, "Full Version", STATUS_INFO, 1,
                          it->second.Version);
    JsonNode::AddJsonNode(product, "Architecture", STATUS_INFO, 1,
                          it->second.Architecture);
    JsonNode::AddJsonNode(
        product, "Path", STATUS_INFO, 1,
        "/opt/intel/oneapi");  // Hardcode the path for the time being
  }

  const char *json_string = json_object_to_json_string(node);
  if (json_string == NULL) {
    message = "Cannot convert json object to string.";
  } else {
    message = string(json_string);
  }

  return true;
}
