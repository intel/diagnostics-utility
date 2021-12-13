/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include <fstream>
#include <stdio.h>
#include <sstream>
#include <iostream>
#include <json-c/json.h>

#include "checker_interface.h"
#include "checker_list_interface.h"

#include "AptChecker.h"
#include "BInstallerChecker.h"
#include "CheckerHelper.h"
#include "JsonNode.h"
#include "RpmChecker.h"


#define API_VERSION "0.1"
char api_version[MAX_STRING_LEN];

using namespace std;


int test(string &message) {

	json_object *root = json_object_new_object();
	json_object *top = json_object_new_object();
	json_object *apps = json_object_new_object();

	JsonNode::AddJsonTopNode(root, top);
	JsonNode::AddJsonNode(top, "APP", INFO, apps);

	string message1, message2, message3;
	bool binary_installer_is_found = false, package_manager_installer_is_found = false, rpm_package_manager_installer_is_found = false;
	int result = Retval_Success;
	if(!BInstallerChecker::Initialize(message1)){
		JsonNode::AddJsonNode(apps, "oneAPI products", ERROR, message1, "", 0, "");
		result = Retval_Error;
	}
	else {
		message1.clear();
		binary_installer_is_found = BInstallerChecker::GetAppInfo(message1);
	}

	if(!AptChecker::Initialize(message2)){
		JsonNode::AddJsonNode(apps, "oneAPI products", ERROR, message2, "", 0, "");
		result = Retval_Error;
	}
	else {
		message2.clear();
		package_manager_installer_is_found = AptChecker::GetAppInfo(message2);
	}


	if(!RpmChecker::Initialize(message3)){
		JsonNode::AddJsonNode(apps, "oneAPI products", ERROR, message3, "", 0, "");
		result = Retval_Error;
	}
	else {
		message3.clear();
		rpm_package_manager_installer_is_found = RpmChecker::GetAppInfo(message3);
	}

	if (binary_installer_is_found && package_manager_installer_is_found) {
		// Glue 2 output from dpkg and binary installer into a single JSON node
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, "", "Parse installed oneapi caches and installed dpkg packages", 0, json_tokener_parse((message1.erase(message1.size() - 1) + "," + message2.erase(0, 1)).c_str()));
	}
	else if (binary_installer_is_found && rpm_package_manager_installer_is_found) {
		// Glue 2 output from rpm and binary installer into a single JSON node
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, "", "Parse installed oneapi caches and installed rpm packages", 0, json_tokener_parse((message1.erase(message1.size() - 1) + "," + message3.erase(0, 1)).c_str()));
	}
	else if (binary_installer_is_found) {
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, "", "Parse installed oneapi caches", 0, json_tokener_parse(message1.c_str()));
	}
	else if (package_manager_installer_is_found){
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, "", "Parse installed dpkg packages", 0, json_tokener_parse(message2.c_str()));
	}
	else if (rpm_package_manager_installer_is_found){
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, "", "Parse installed rpm packages", 0, json_tokener_parse(message3.c_str()));
	}
	else {
		// No products installed by Binary Installer or dpkg manager were found.
		// ToDo: log all error messages. Currently they are dropped.
		stringstream ss;
		ss << "No installed oneAPI products are discovered. Additional information: " << endl;
		if (!message1.empty()) ss << message1 << endl;
		if (!message2.empty()) ss << message2;
		JsonNode::AddJsonNode(apps, "oneAPI products", INFO, ss.str());
		// Skip check of dependencies
		message = string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));
		return result;
	}

	message = string(json_object_to_json_string_ext(root, JSON_C_TO_STRING_PRETTY));

	if (message.find("WARNING") != std::string::npos) {
		result = Retval_Success;
	}
	if (message.find("FAIL") != std::string::npos) {
		result = Retval_Fail;
	}
	if (message.find("ERROR") != std::string::npos) {
		result = Retval_Error;
	}

	return result;
}


int main() {

	// Run tests
	string message;
	int retVal = test(message);
	cout << message << endl;
	return retVal;
}

//-------------------------------------------------------------------------
//------------------------Library part there ------------------------------
//-------------------------------------------------------------------------

extern "C" struct CheckResult app_check(char *data)
{
	string message;
	test(message);
	char* buffer = new char[message.size() + 1];
	std::copy(message.begin(), message.end(), buffer);
	buffer[message.size()] = '\0';

	struct CheckResult ret = {buffer};

	return ret;
}


// "{\"Value\":{\"GPU\":{}},\"Value\":{\"App\":{}}}" "{\"Value\":{\"GPU\":{}}}"
REGISTER_CHECKER(app_check_struct,
				 "oneapi_app_check",
				 "GetData",
				 "default,sysinfo,compile,runtime,host,target",
				 "This check shows version information of installed oneAPI products.",
				 "{}",
				 "user",
				 10,
				 "1.0",
				 app_check)


static struct Check* checkers[] =
	{&app_check_struct, NULL};

extern "C" char* get_api_version(void)
{
	snprintf(api_version, sizeof(api_version), "%s", API_VERSION);
	return api_version;
}

extern "C" __attribute__((const)) struct Check **get_check_list(void)
{
	return checkers;
}
