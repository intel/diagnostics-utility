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

#ifndef SRC_CHECKERHELPER_H_
#define SRC_CHECKERHELPER_H_

#include <map>
#include <regex>
#include <vector>

using ::std::string;
using ::std::vector;

enum CHECK_STATUS : int {
  CHECK_STATUS_SUCCESS = 0,
  CHECK_STATUS_WARNING = 1,
  CHECK_STATUS_FAIL = 2,
  CHECK_STATUS_ERROR = 3
};

namespace CheckerHelper {
vector<string> SplitString(const string str, const string regex_str);
};

#endif /* SRC_CHECKERHELPER_H_ */
