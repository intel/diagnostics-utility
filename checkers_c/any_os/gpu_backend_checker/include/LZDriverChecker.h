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

#ifndef SRC_LZDRIVERCHECKER_H_
#define SRC_LZDRIVERCHECKER_H_

#include <loader/ze_loader.h>
#include <ze_api.h>
#include <zes_api.h>

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "CheckerHelper.h"
#include "JsonNode.h"

using namespace std;

class LZ_DriverChecker {
 private:
  bool GetLoaderVersion(string& message);
  void GetDeviceInfo(ze_driver_handle_t driver, string& message);
  string GetAPIVersionString(_ze_api_version_t version);
  string GetDriverVersionString(unsigned int version);
  string GetUUIDString(ze_driver_uuid_t uuid);
  string GetUUIDString(ze_device_uuid_t uuid);
  string GetDeviceTypeString(ze_device_type_t type);

 public:
  LZ_DriverChecker();
  virtual ~LZ_DriverChecker();
  virtual bool Load(string& message);
  virtual bool Initialize(string& message);
  virtual void GetDriverInfo(string& message);
};

#endif /* SRC_LZDRIVERCHECKER_H_ */
