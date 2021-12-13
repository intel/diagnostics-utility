/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "gpu_backend_checker.h"
#include "checker_list_interface.h"
#include "checker_interface.h"

#include <stdio.h>
#include <json-c/json.h>

#define API_VERSION "0.1"
char api_version[MAX_STRING_LEN];


int test(string &message)
{
	json_object *root = json_object_new_object();
	json_object *top = json_object_new_object();
	json_object *drivers = json_object_new_object();
	json_object *opencl = json_object_new_object();
	json_object *level_zero = json_object_new_object();


	JsonNode::AddJsonTopNode(root, top);
	JsonNode::AddJsonNode(top, "GPU", INFO, drivers);
	JsonNode::AddJsonNode(drivers, "Intel® oneAPI Level Zero Driver", INFO, level_zero);
	JsonNode::AddJsonNode(drivers, "OpenCL™ Driver", INFO, opencl);

	int result = 0;

	if (!LZ_DriverChecker::Load(message)) {
		JsonNode::AddJsonNode(level_zero, "Driver is loaded", ERROR, message, "", 0, "");
	}
	else {
		JsonNode::AddJsonNode(level_zero, "Driver is loaded", PASS, 0, "");
		if (!LZ_DriverChecker::Initialize(message)) {
			JsonNode::AddJsonNode(level_zero, "Driver information", ERROR, message, "", 0, "");
		}
		else {
			LZ_DriverChecker::GetDriverInfo(message);
			json_object* driver_info = json_tokener_parse(message.c_str());
			if (driver_info == NULL) {
				JsonNode::AddJsonNode(level_zero, "Driver information", ERROR, "Can't get information from driver", "", 0, "");
			}
			else {
				JsonNode::AddJsonNode(level_zero, "Driver information", INFO, driver_info);
			}
		}
	}


	if (!CL_DriverChecker::Load(message))
	{
		JsonNode::AddJsonNode(opencl, "Driver is loaded", ERROR, message, "", 0, "");
	}
	else {
		JsonNode::AddJsonNode(opencl, "Driver is loaded", PASS, 0, "");
		CL_DriverChecker::GetDriverInfo(message);
		json_object* driver_info = json_tokener_parse(message.c_str());
		if (driver_info == NULL) {
			JsonNode::AddJsonNode(opencl, "Driver information", ERROR, "Can't get information from driver", "", 0, "");
		}
		else {
			JsonNode::AddJsonNode(opencl, "Driver information", INFO, driver_info);
		}
	}

	message = string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));

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

int main()
{
	// we cannot call main function directly from python due to
	// Fatal Python error: pymain_init_cmdline_argv: memory allocation failed
	string message;
	int retVal = test(message);
	cout << message << endl;
	return retVal;
}

//-------------------------------------------------------------------------
//------------------------Library part there ------------------------------
//-------------------------------------------------------------------------

extern "C" struct CheckResult gpu_backend_check(char *data)
{
	string message;
	test(message);
	char *buffer = new char[message.size() + 1];
	std::copy(message.begin(), message.end(), buffer);
	buffer[message.size()] = '\0';

	struct CheckResult ret = {buffer};

	return ret;
}

REGISTER_CHECKER(gpu_backend_check_struct,
				 "gpu_backend_check",
				 "GetData",
				 "default,gpu,sysinfo,compile,runtime,host,target",
				 "This check shows information from OpenCL™ and Intel® oneAPI Level Zero drivers.",
				 "{}",
				 "user",
				 10,
				 "2.0",
				 gpu_backend_check)

static struct Check *checkers[] =
	{&gpu_backend_check_struct, NULL};

extern "C" char *get_api_version(void)
{
	snprintf(api_version, sizeof(api_version), "%s", API_VERSION);
	return api_version;
}

extern "C" __attribute__((const)) struct Check **get_check_list(void)
{
	return checkers;
}
