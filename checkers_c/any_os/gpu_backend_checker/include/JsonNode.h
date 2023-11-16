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

#ifndef SRC_JSONNODE_H_
#define SRC_JSONNODE_H_

#include <fcntl.h>
#include <json-c/json_object.h>
#include <json-c/json_tokener.h>
#include <sys/stat.h>

#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#ifdef __linux__
#include <sys/mman.h>
#include <unistd.h>
#endif

// Return values
#define STATUS_PASS "PASS"  // if everything is ok
#define STATUS_WARNING \
  "WARNING"  // if we have potential issue like driver exists, but we do not
             // have it in our knowledge base
#define STATUS_FAIL "FAIL"    // if check found some issues on system
#define STATUS_ERROR "ERROR"  // in case of internal test's  error
#define STATUS_INFO "INFO"    // if check get some info about the system

using namespace std;

class JsonNode {
 public:
  JsonNode();
  virtual ~JsonNode();

  static void AddJsonTopNode(json_object *parent, json_object *check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          string message, string command,
                          unsigned int verbosity, json_object *check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          string message, string command,
                          unsigned int verbosity, string check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          string message, string command,
                          unsigned int verbosity, unsigned int check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          unsigned int verbosity, json_object *check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          unsigned int verbosity, string check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          unsigned int verbosity, unsigned int check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          json_object *check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          string check_result);
  static void AddJsonNode(json_object *parent, string name, string check_status,
                          unsigned int check_result);

  static json_object *GetObject(json_object *root, const string path);

  static vector<string> SplitString(const string str, const string regex_str);
};

#endif /* SRC_JSONNODE_H_ */