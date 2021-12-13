/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "JsonNode.h"

JsonNode::JsonNode() {
	// TODO Auto-generated constructor stub

}

JsonNode::~JsonNode() {
	// TODO Auto-generated destructor stub
}

void JsonNode::AddJsonTopNode(json_object* parent, json_object * value ) {
	json_object_object_add(parent, "Value", value);
}


void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, json_object * value ) {
	JsonNode::AddJsonNode(parent, name, retVal, "", "", 0, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, json_object * value ) {
	JsonNode::AddJsonNode(parent, name, retVal, "", "", verbosity, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, json_object * value ) {
	json_object *json_value = json_object_new_object();
	json_object_object_add(parent, name.c_str(), json_value);
	if (!message.empty())
		json_object_object_add(json_value, "Message", json_object_new_string(message.c_str()));
	if (!command.empty())
		json_object_object_add(json_value, "Command", json_object_new_string(command.c_str()));
	if (verbosity)
		json_object_object_add(json_value, "Verbosity", json_object_new_int(verbosity));
	json_object_object_add(json_value, "RetVal", json_object_new_string(retVal.c_str()));
	json_object_object_add(json_value, "Value", value);
}


void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, string value ) {
	JsonNode::AddJsonNode (parent, name, retVal, "", "", 0, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, string value ) {
	JsonNode::AddJsonNode (parent, name, retVal, "", "", verbosity, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, string value ) {
	json_object *json_value = json_object_new_object();
	json_object_object_add(parent, name.c_str(), json_value);
	if (!message.empty())
		json_object_object_add(json_value, "Message", json_object_new_string(message.c_str()));
	if (!command.empty())
		json_object_object_add(json_value, "Command", json_object_new_string(command.c_str()));
	if (verbosity)
		json_object_object_add(json_value, "Verbosity", json_object_new_int(verbosity));
	json_object_object_add(json_value, "RetVal", json_object_new_string(retVal.c_str()));
	json_object_object_add(json_value, "Value", json_object_new_string(value.c_str()));
}


void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, uint32_t value ) {
	JsonNode::AddJsonNode(parent, name, retVal, "", "", 0, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, uint32_t verbosity, uint32_t value ) {
	JsonNode::AddJsonNode(parent, name, retVal, "", "", verbosity, value);
}

void JsonNode::AddJsonNode(json_object* parent, string name, string retVal, string message, string command, uint32_t verbosity, uint32_t value ) {
	json_object *json_value = json_object_new_object();
	json_object_object_add(parent, name.c_str(), json_value);
	if (!message.empty())
		json_object_object_add(json_value, "Message", json_object_new_string(message.c_str()));
	if (!command.empty())
		json_object_object_add(json_value, "Command", json_object_new_string(command.c_str()));
	if (verbosity)
		json_object_object_add(json_value, "Verbosity", json_object_new_int(verbosity));
	json_object_object_add(json_value, "RetVal", json_object_new_string(retVal.c_str()));
	json_object_object_add(json_value, "Value", json_object_new_int64(value));		// use int64 to prevent overflow because it accepts signed integer

}


bool JsonNode::ParseFile(string name, json_object** root, string message) {
	struct stat sb;
	int fd = open(name.c_str(), O_RDONLY);
    if (fstat(fd, &sb) == -1) {          /* To obtain file size */
		stringstream ss;
		ss << "Cannot obtain length of file \"" << name << "\" "<< endl;
		message = ss.str();
		return false;
    }
    const char* json = (const char*)mmap(nullptr, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (json == MAP_FAILED) {
		stringstream ss;
		ss << "Cannot read file \"" << name << "\" "<< endl;
		message = ss.str();
		return false;
    }

    *root = json_tokener_parse(json);

    munmap((void*)json, sb.st_size);
    close(fd);

    return true;
}


json_object* JsonNode::GetObject(json_object* root, const string path) {
	json_object* obj = root;
	vector<string> keys = SplitString(path, "/");

	for (auto k : keys) {
        if( !json_object_object_get_ex(obj, k.c_str(), &obj) ) {
            return nullptr;
        }
	}

	return obj;
}


vector<string> JsonNode::SplitString(const string str, const string regex_str)
{
    std::regex regexz(regex_str);
    std::vector<std::string> list(std::sregex_token_iterator(str.begin(), str.end(), regexz, -1),
                                  std::sregex_token_iterator());
    return list;
}
