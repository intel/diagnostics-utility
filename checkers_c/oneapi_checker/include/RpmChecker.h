/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/


#ifndef SRC_RPMCHECKER_H_
#define SRC_RPMCHECKER_H_

#include <json-c/json.h>

#include "JsonNode.h"
#include "CheckerHelper.h"

using namespace std;


class RpmChecker {
public:
	RpmChecker();
	~RpmChecker();

	static bool Initialize(string& message);
	static bool GetAppInfo(string& message);

};

#endif /* SRC_RPMCHECKER_H_ */
