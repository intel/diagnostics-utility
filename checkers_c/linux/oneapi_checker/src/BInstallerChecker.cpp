/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "BInstallerChecker.h"


const char* ROOT_IC_PATH = "/var/intel";  // Path to search root installer cache folder
const char* USER_IC_PATH = "/intel";	  // Path to search user installer cache folder
const char* DB_NAME = "packagemanager.db";

vector<string> BInstallerChecker::CachePaths;



BInstallerChecker::BInstallerChecker() {
	// TODO Auto-generated constructor stub

}

BInstallerChecker::~BInstallerChecker() {
	// TODO Auto-generated destructor stub
}


bool BInstallerChecker::Initialize(string& message) {
	bool status = false;
    uid_t me = getuid();
    uid_t myprivs = geteuid();

    // Always try to read root database
    if (FindCaches(ROOT_IC_PATH, CachePaths, message))
    	status = true;

    if (me == myprivs){
    	// Running as self
    	if (me == 0) {
    		// Run as privileged user
    	}
    	else {
			// Run as not privileged user
    	    passwd *pw = getpwuid(geteuid());
    	    if ((!pw) || (!pw->pw_dir))
    		{
				message = "Cannot get user name. Try running as a different user.";
    		}

    	 	stringstream ss;
    		ss << pw->pw_dir << USER_IC_PATH;
    	    if (FindCaches(ss.str(), CachePaths, message))
    	    	status = true;
    	}
    }
    else {
        // Running as somebody else
    	if (myprivs == 0) {
    		// Run as privileged user
    	}
    	else {
    		// Run as not privileged user
    	    passwd *pw = getpwuid(geteuid());
    	    if ((!pw) || (!pw->pw_dir)) {
    	    	  message = "Cannot get user name. Try running as a different user.";
    		}

    	 	stringstream ss;
    		ss << pw->pw_dir << USER_IC_PATH;
    	    if (FindCaches(ss.str(), CachePaths, message))
    	    	status = true;
    	}
    }

	return status;
}


bool BInstallerChecker::GetAppInfo(string& message) {
	string info;
	string errorMessage;
	for (string path: CachePaths) {
		if(GetAppInfo(path + DB_NAME, path, info)) {
			if (message.size() == 0)
				message = info;
			else
				// Glue 2 JSON strings into a single one
				message = message.erase(message.size() - 1) + "," + info.erase(0, 1);
		}
		else {
			errorMessage += info;
		}
	}

	if (message.size() == 0) {
		// No product information was found. Return error message.
		message = errorMessage;
		return false;
	}

	if (message == "{ }") {
		// No visible products were found.
		message = {};
		return false;
	}

	if (errorMessage.size() != 0) {
		message += errorMessage;
		return false;
	}

	return true;
}


bool BInstallerChecker::GetAppInfo(string dbPath, string icPath, string& message) {
	sqlite3* db;

	if( sqlite3_open_v2(dbPath.c_str(), &db, SQLITE_OPEN_READONLY, nullptr) != SQLITE_OK ) {
		stringstream ss;
		ss << "Cannot open Binary Installer database." << dbPath <<": " << sqlite3_errmsg(db) << endl;
		message = ss.str();
		return false;
	}

	// Get package installation path
	string package_path;
	const char* select_dir = "SELECT PATH FROM INSTALL_DIR;";
	sqlite3_stmt* statement = nullptr;
	if (sqlite3_prepare_v2(db, select_dir, -1, &statement, NULL) != SQLITE_OK) {
		stringstream ss;
		ss << "Error while compiling SQL statement \"" << select_dir << "\": " << sqlite3_errmsg(db) << endl;
		message = ss.str();
		sqlite3_finalize(statement);
		sqlite3_close_v2(db);
		return false;
	}
	else {	// The table has just one record now.
		if (sqlite3_step(statement) == SQLITE_ROW) {
			package_path = (char*)sqlite3_column_text(statement, 0);

			sqlite3_finalize(statement);
		}
		else
		{
			stringstream ss;
			ss << "Unable to find oneAPI package. Your database format is not supported by the current version of this check." << endl;
			message = ss.str();
			sqlite3_finalize(statement);
			sqlite3_close_v2(db);
			return false;
		}
	}

	// Obtain installed product names
	const char* select_components = "SELECT ID, VERSION FROM COMPONENT ORDER BY ID, VERSION;";
	statement = nullptr;
	if (sqlite3_prepare_v2(db, select_components, -1, &statement, NULL) != SQLITE_OK) {
		stringstream ss;
		ss << "Error while compiling SQL statement \"" << select_components << "\": " << sqlite3_errmsg(db) << endl;
		message = ss.str();
		sqlite3_finalize(statement);
		sqlite3_close_v2(db);
		return false;
	}

	json_object* node = json_object_new_object();
	stringstream ss;
	while (sqlite3_step(statement) == SQLITE_ROW) {
		string id = (char*)sqlite3_column_text(statement, 0);
		string fullVersion = (char*)sqlite3_column_text(statement, 1);

		// Obtain human readable name for the each product
		stringstream ss;
		ss << icPath << "packagescache/" << id << ",v=" << fullVersion <<  + "/manifest.json";
		json_object* root;
		if (!JsonNode::ParseFile(ss.str().c_str(), &root, message)) {
			stringstream ss;
			ss << "Cannot obtain human readable product names: " << message;
			message = ss.str();
			sqlite3_finalize(statement);
			sqlite3_close_v2(db);
			return false;
		}

		// Display the products only which have visible = true
		if (json_object_get_boolean(json_object_object_get(root, "visible")) != 0) {
			json_object* localizedDisplay = json_object_object_get(json_object_object_get(root, "display"), "localized");

			const char *description = nullptr, *title = nullptr, *version = nullptr;
			// Loop through array of localizations and fill the fields with "en-us" localization or with the first one if it is not exist.
		    for ( size_t i = 0; i < json_object_array_length( localizedDisplay ); i++ )
		    {
		        json_object* localize = json_object_array_get_idx( localizedDisplay, i );

		        const char* language = json_object_get_string(json_object_object_get(localize, "language"));
		        if (description == nullptr || strcmp(language, "en-us") == 0)
		        	description = json_object_get_string(json_object_object_get(localize, "description"));
		        if (title == nullptr || strcmp(language, "en-us") == 0)
		        	title = json_object_get_string(json_object_object_get(localize, "title"));
		        if (version == nullptr || strcmp(language, "en-us") == 0)
		        	version = json_object_get_string(json_object_object_get(localize, "version"));
		    }

	    	json_object* product = json_object_new_object();
	    	JsonNode::AddJsonNode(node, title, INFO, product);
	    	JsonNode::AddJsonNode(product, "Product ID", INFO, 1, id);
	    	JsonNode::AddJsonNode(product, "Version", INFO, version);
	    	JsonNode::AddJsonNode(product, "Full Version", INFO, 1, fullVersion);
	    	JsonNode::AddJsonNode(product, "Description", INFO, 1, description);
	    	JsonNode::AddJsonNode(product, "Path", INFO, 1, package_path);

		}
	}


	sqlite3_finalize(statement);
	sqlite3_close_v2(db);

	const char *json_string = json_object_to_json_string(node);
	if (json_string == NULL) {
		message = "Cannot convert json object to string.";
	} else {
		message = string(json_string);
	}

	return true;
}


// Finds installer cache directories within specified path.
// The directories may have different names, so, search for package manager DB file in this directory.
// Expect that the DB file name is constant.
bool BInstallerChecker::FindCaches(string path, vector<string>& cashPaths, string& message) {
	stringstream ss;
	string out;
	// Find paths to package manager DB files within the specified path.
	ss << "find " << path << " -name '" << DB_NAME << "' -type f 2>/dev/null";
	int exit_status = CheckerHelper::RunCommand(ss.str().c_str(), out);
	if (exit_status != 0 || out.size() == 0)	{
		message = "Cannot obtain paths to package manager databases.";
		return false;
	}

	vector<string> lines = CheckerHelper::SplitString(out, "\n");
	for (string s: lines) {
		cashPaths.push_back(s.substr(0, s.length()- strlen(DB_NAME)));
	}
	return true;
}
