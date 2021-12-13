/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/


#ifndef SRC_CHECKERHELPER_H_
#define SRC_CHECKERHELPER_H_

#include <array>
#include <vector>
#include <map>
#include <regex>


using namespace std;


enum Retval: int {
	Retval_Success = 0,
	Retval_Warning = 1,
	Retval_Fail = 2,
	Retval_Error = 3
};


enum OsType {
	UnknownOS,
	DebianBased,
	RpmBased,
	Windows,
	MacOS,
	FreeBSD
};


class CheckerHelper {
public:
	CheckerHelper();
	~CheckerHelper();

	static int RunCommand(const string cmd, string& out);
	static vector<string> SplitString(const string str, const string regex_str);
	static OsType GetOsType();
};


struct Product {
	string Title;
	string Version;
	string Architecture;
	string Packages; // List of packages separated by comma
};

#endif /* SRC_CHECKERHELPER_H_ */
