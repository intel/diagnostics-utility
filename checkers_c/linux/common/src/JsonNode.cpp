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

#include "JsonNode.h"

JsonNode::JsonNode() {
  // TODO Auto-generated constructor stub
}

JsonNode::~JsonNode() {
  // TODO Auto-generated destructor stub
}

void JsonNode::AddJsonTopNode(json_object *parent, json_object *check_result) {
  json_object_object_add(parent, "CheckResult", check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, json_object *check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", 0, check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, unsigned int verbosity,
                           json_object *check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", verbosity,
                        check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, string message, string command,
                           unsigned int verbosity, json_object *check_result) {
  json_object *json_value = json_object_new_object();
  json_object_object_add(parent, name.c_str(), json_value);
  if (!message.empty())
    json_object_object_add(json_value, "Message",
                           json_object_new_string(message.c_str()));
  if (!command.empty())
    json_object_object_add(json_value, "Command",
                           json_object_new_string(command.c_str()));
  if (verbosity)
    json_object_object_add(json_value, "Verbosity",
                           json_object_new_int(verbosity));
  json_object_object_add(json_value, "CheckStatus",
                         json_object_new_string(check_status.c_str()));
  json_object_object_add(json_value, "CheckResult", check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, string check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", 0, check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, unsigned int verbosity,
                           string check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", verbosity,
                        check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, string message, string command,
                           unsigned int verbosity, string check_result) {
  json_object *json_value = json_object_new_object();
  json_object_object_add(parent, name.c_str(), json_value);
  if (!message.empty())
    json_object_object_add(json_value, "Message",
                           json_object_new_string(message.c_str()));
  if (!command.empty())
    json_object_object_add(json_value, "Command",
                           json_object_new_string(command.c_str()));
  if (verbosity)
    json_object_object_add(json_value, "Verbosity",
                           json_object_new_int(verbosity));
  json_object_object_add(json_value, "CheckStatus",
                         json_object_new_string(check_status.c_str()));
  json_object_object_add(json_value, "CheckResult",
                         json_object_new_string(check_result.c_str()));
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, unsigned int check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", 0, check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, unsigned int verbosity,
                           unsigned int check_result) {
  JsonNode::AddJsonNode(parent, name, check_status, "", "", verbosity,
                        check_result);
}

void JsonNode::AddJsonNode(json_object *parent, string name,
                           string check_status, string message, string command,
                           unsigned int verbosity, unsigned int check_result) {
  json_object *json_value = json_object_new_object();
  json_object_object_add(parent, name.c_str(), json_value);
  if (!message.empty())
    json_object_object_add(json_value, "Message",
                           json_object_new_string(message.c_str()));
  if (!command.empty())
    json_object_object_add(json_value, "Command",
                           json_object_new_string(command.c_str()));
  if (verbosity)
    json_object_object_add(json_value, "Verbosity",
                           json_object_new_int(verbosity));
  json_object_object_add(json_value, "CheckStatus",
                         json_object_new_string(check_status.c_str()));
  json_object_object_add(
      json_value, "CheckResult",
      json_object_new_int64(
          check_result));  // use int64 to prevent overflow because it accepts
                           // signed integer
}

json_object *JsonNode::GetObject(json_object *root, const string path) {
  json_object *obj = root;
  vector<string> keys = SplitString(path, "/");

  for (auto k : keys) {
    if (!json_object_object_get_ex(obj, k.c_str(), &obj)) {
      return nullptr;
    }
  }

  return obj;
}

vector<string> JsonNode::SplitString(const string str, const string regex_str) {
  std::regex regexz(regex_str);
  std::vector<std::string> list(
      std::sregex_token_iterator(str.begin(), str.end(), regexz, -1),
      std::sregex_token_iterator());
  return list;
}
