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

#include "CheckerHelper.h"

vector<string> CheckerHelper::SplitString(const string str,
                                          const string regex_str) {
  std::regex regexz(regex_str);
  std::vector<std::string> list(
      std::sregex_token_iterator(str.begin(), str.end(), regexz, -1),
      std::sregex_token_iterator());
  return list;
}
