/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "AptChecker.h"


AptChecker::AptChecker() {
	// TODO Auto-generated constructor stub

}


AptChecker::~AptChecker() {
	// TODO Auto-generated destructor stub
}


bool AptChecker::Initialize(string& message) {
	return true;
}


bool AptChecker::GetAppInfo(string& message) {
	string out;
	int retval;

	if (CheckerHelper::GetOsType() != DebianBased) {
		message = "Obtaining information about products installed by dpkg is skipped.";
		return false;
	}

	// Extract information about installed packages
	retval = CheckerHelper::RunCommand("dpkg --no-pager -l '*intel-oneapi*' 2>/dev/null | grep ii", out);
	if (retval != 0)	{
		message = "Cannot obtain installed package.";
		return false;
	}

	// Parse output and translate it into JSON structure
	json_object* node = json_object_new_object();
	stringstream ss;
	vector<string> lines = CheckerHelper::SplitString(out, "\n");
	map<string, Product> products;
    // Each product can have multiple packages, so, go through the package list and create a unique product list
	string package, version, arch;
	stringstream title;
	for (auto it = begin(lines); it != end(lines); ++it) {
	    vector <string> fields = CheckerHelper::SplitString(*it, "(\\s+)");
	    title.str("");
	    for (size_t iter = 0; iter < fields.size(); iter ++) {
	    	switch(iter) {
	    	case 0:
	    		break; // skip the first field
	    	case 1:
	    		package = fields[iter];
	    		break;
	    	case 2:
	    		version = fields[iter];
	    		break;
	    	case 3:
	    		arch = fields[iter];
	    		break;
	    	default:
	    		title << fields[iter] << " ";
	    	}
	    }
	    auto product = products.find(title.str());
	    if (product != products.end()) {
	    	product->second.Packages = product->second.Packages + ", " + package;
	    }
	    else {
	    	Product prod;
	    	prod.Packages = package;
	    	prod.Version = version;
	    	prod.Architecture = arch;
	    	prod.Title = title.str();
	    	products.insert({title.str(), prod});
	    }
	}

	// Encode products in JSON structure
	for (auto it = products.begin(); it != products.end(); it ++) {
	    json_object* product = json_object_new_object();
	    JsonNode::AddJsonNode(node, it->second.Title, INFO, product);
	    JsonNode::AddJsonNode(product, "Packages", INFO, 1, it->second.Packages);
	    JsonNode::AddJsonNode(product, "Version", INFO, it->second.Version.substr(0, it->second.Version.find("-")));
	    JsonNode::AddJsonNode(product, "Full Version", INFO, 1, it->second.Version);
	    JsonNode::AddJsonNode(product, "Architecture", INFO, 1, it->second.Architecture);
	    JsonNode::AddJsonNode(product, "Path", INFO, 1, "/opt/intel/oneapi");		// Hardcode the path for the time being
	}

	const char *json_string = json_object_to_json_string(node);
	if (json_string == NULL) {
		message = "Can't convert json object to string";
	} else {
		message = string(json_string);
	}

	return true;
}

