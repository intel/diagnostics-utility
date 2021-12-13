/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/


#include "CheckerHelper.h"


CheckerHelper::CheckerHelper() {
	// TODO Auto-generated constructor stub

}

CheckerHelper::~CheckerHelper() {
	// TODO Auto-generated destructor stub
}


int CheckerHelper::RunCommand(const string cmd, string& out)
{
    int exitStatus = 0;
    auto pPipe = popen(cmd.c_str(), "r");
    if(!pPipe) {
        return 1;
    }

    std::array<char, 256> buffer;
    while(fgets(buffer.data(), buffer.size(), pPipe) != nullptr) {
        out += buffer.data();
    }

    auto rc = pclose(pPipe);
    if(WIFEXITED(rc)) {
        exitStatus = WEXITSTATUS(rc);
    }

    return exitStatus;
}



vector<string> CheckerHelper::SplitString(const string str, const string regex_str)
{
    std::regex regexz(regex_str);
    std::vector<std::string> list(std::sregex_token_iterator(str.begin(), str.end(), regexz, -1),
                                  std::sregex_token_iterator());
    return list;
}

OsType CheckerHelper::GetOsType()
{
#if defined(WIN64) || defined(WIN32) || defined(WINIA64)
	return Windows;

#elif defined(MACI386) || defined(MACX86_64)
	return MacOs;

#elif defined(FREEBSD64)
	return FreeBSD;

#endif

//#elif defined(LINX86) || defined(LINX64)
	string out;
	int retval;
	// Check that dpkg is installed
	retval = CheckerHelper::RunCommand("which dpkg 2>/dev/null", out);
	if (retval == 0)	{
		return DebianBased;
	}

	// Check that rpm is installed
	retval = CheckerHelper::RunCommand("which rpm 2>/dev/null", out);
	if (retval == 0)	{
		return RpmBased;
	}


	return UnknownOS;
}
