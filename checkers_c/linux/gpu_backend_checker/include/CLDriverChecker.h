/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef CLDRIVERCHECKER_H_
#define CLDRIVERCHECKER_H_

#define CL_TARGET_OPENCL_VERSION 210

#include <dlfcn.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif
#include <json-c/json.h>

#include "JsonNode.h"

using namespace std;


class CL_DriverChecker {
public:
	CL_DriverChecker();
	virtual ~CL_DriverChecker();

	static bool Load(string &message);
	static void GetDriverInfo(string& message);
	static void GetDeviceInfo(cl_device_id deviceId, string& message);

	static string GetErrorMessage(cl_int error);
	static string GetDeviceTypeString(cl_device_type type);
	// Represent array as a comma separated string
	static string GetArrayString(size_t* array, size_t array_size);
	static string GetCacheTypeString(cl_device_mem_cache_type type);
	static string GetLocalMemTypeString(cl_device_local_mem_type type);
};

#endif /* CLDRIVERCHECKER_H_ */
