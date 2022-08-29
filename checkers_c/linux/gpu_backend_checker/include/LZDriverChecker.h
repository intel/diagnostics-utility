/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef SRC_LZDRIVERCHECKER_H_
#define SRC_LZDRIVERCHECKER_H_

#include <dlfcn.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <level_zero/ze_api.h>
#include <level_zero/zes_api.h>
#include <json-c/json.h>
#include "JsonNode.h"
#include "CheckerHelper.h"

using namespace std;


class LZ_DriverChecker {
public:
	LZ_DriverChecker();
	virtual ~LZ_DriverChecker();

	static bool Load(string& message);
	static bool Initialize(string& message);
	static bool GetLoaderVersion(string& message);
	static void GetDriverInfo(string& message);
	static void GetDeviceInfo(ze_driver_handle_t driver, string& message);

	static string GetErrorMessage(ze_result_t error);
	static string GetAPIVersionString(_ze_api_version_t version);
	static string GetDriverVersionString(uint32_t version);
	static string GetUUIDString(ze_driver_uuid_t uuid);
	static string GetUUIDString(ze_device_uuid_t uuid);
	static string GetDeviceTypeString(ze_device_type_t type);
};

#endif /* SRC_LZDRIVERCHECKER_H_ */
