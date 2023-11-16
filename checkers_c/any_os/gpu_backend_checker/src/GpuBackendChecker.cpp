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

#include "GpuBackendChecker.h"

GpuBackendChecker::GpuBackendChecker(LZ_DriverChecker *lzDriverChecker,
                                     CL_DriverChecker *clDriverChecker)
    : lzDriverChecker(lzDriverChecker), clDriverChecker(clDriverChecker) {}

int GpuBackendChecker::PerformCheck(string &message) {
  json_object *root = json_object_new_object();
  json_object *top = json_object_new_object();
  json_object *drivers = json_object_new_object();
  json_object *opencl = json_object_new_object();
  json_object *level_zero = json_object_new_object();

  JsonNode::AddJsonTopNode(root, top);
  JsonNode::AddJsonNode(top, "GPU", STATUS_INFO, drivers);
  JsonNode::AddJsonNode(drivers, "Intel® oneAPI Level Zero Driver", STATUS_INFO,
                        level_zero);
  JsonNode::AddJsonNode(drivers, "OpenCL™ Driver", STATUS_INFO, opencl);

  int result = 0;

  if (!lzDriverChecker->Load(message)) {
    JsonNode::AddJsonNode(level_zero, "Driver is loaded.", STATUS_ERROR,
                          message, "", 0, "");
  } else {
    JsonNode::AddJsonNode(level_zero, "Driver is loaded.", STATUS_PASS, 0, "");
    if (!lzDriverChecker->Initialize(message)) {
      JsonNode::AddJsonNode(level_zero, "Driver information", STATUS_ERROR,
                            message, "", 0, "");
    } else {
      lzDriverChecker->GetDriverInfo(message);
      json_object *driver_info = json_tokener_parse(message.c_str());
      if (driver_info == NULL) {
        JsonNode::AddJsonNode(level_zero, "Driver information", STATUS_ERROR,
                              "Unable to get driver information.", "", 0, "");
      } else {
        JsonNode::AddJsonNode(level_zero, "Driver information", STATUS_INFO,
                              driver_info);
      }
    }
  }

  if (!clDriverChecker->Load(message)) {
    JsonNode::AddJsonNode(opencl, "Driver is loaded", STATUS_ERROR, message, "",
                          0, "");
  } else {
    JsonNode::AddJsonNode(opencl, "Driver is loaded", STATUS_PASS, 0, "");
    clDriverChecker->GetDriverInfo(message);
    json_object *driver_info = json_tokener_parse(message.c_str());
    if (driver_info == NULL) {
      JsonNode::AddJsonNode(opencl, "Driver information", STATUS_ERROR,
                            "Unable to get driver information.", "", 0, "");
    } else {
      JsonNode::AddJsonNode(opencl, "Driver information", STATUS_INFO,
                            driver_info);
    }
  }

  message =
      string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));

  if (message.find("WARNING") != std::string::npos) {
    result = 1;
  }
  if (message.find("FAIL") != std::string::npos) {
    result = 2;
  }
  if (message.find("ERROR") != std::string::npos) {
    result = 3;
  }

  return result;
}
