/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef SRC_JSONNODE_H_
#define SRC_JSONNODE_H_

// Return values
#define PASS 	"PASS"		// if everything is ok
#define WARNING "WARNING"	// if we have potential issue like driver exists, but we do not have it in our knowledge base
#define FAIL 	"FAIL"		// if check found some issues on system
#define ERROR 	"ERROR" 	// in case of internal test's  error
#define INFO	"INFO"		// if check get some info about the system

#include <iostream>
#include <sstream>
#include <string>
#include <json-c/json.h>
#include <fcntl.h>
#include <regex>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>


using namespace std;


class JsonNode {
public:
	JsonNode();
	virtual ~JsonNode();

	static void AddJsonTopNode(json_object* parent, json_object * value);
	static void AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, json_object * value);
	static void AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, string value);
	static void AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, uint32_t value);
	static void AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, json_object * value);
	static void AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, string value);
	static void AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, uint32_t value);
	static void AddJsonNode(json_object* parent, string name, string retVal, json_object * value);
	static void AddJsonNode(json_object* parent, string name, string retVal, string value);
	static void AddJsonNode(json_object* parent, string name, string retVal, uint32_t value);

	static bool ParseFile(string name, json_object** root, string message);
	static json_object* GetObject(json_object* root, const string path);

	static vector<string> SplitString(const string str, const string regex_str);
};

#endif /* SRC_JSONNODE_H_ */
