/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef BINSTALLERCHECKER_H_
#define BINSTALLERCHECKER_H_

#define MAX_USERID_LENGTH 32


#include <map>
#include <regex>
#include <string.h>
#include <string>
#include <sstream>
#include <sqlite3.h>
#include <pwd.h>
#include <unistd.h>
#include <vector>
#include <json-c/json.h>

#include "JsonNode.h"
#include "CheckerHelper.h"


using namespace std;


class BInstallerChecker {
public:
	BInstallerChecker();
	virtual ~BInstallerChecker();

	static bool Initialize(string& message);
	// Returns false in case of any infrastructure issues which don't allow obtain information.
	static bool GetAppInfo(string& message);
	static bool GetAppInfo(string dbPath, string icPath, string& message);
	static bool FindCaches(string path, vector<string>& cachePaths, string& message);

private:
	static vector<string> CachePaths; // Paths to found installer caches
};

#endif /* BINSTALLERCHECKER_H_ */
