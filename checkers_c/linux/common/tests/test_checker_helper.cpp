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

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <string>

#include "CheckerHelper.h"

using ::std::string;

TEST(SplitString, ShouldReturnListOfStrings) {
  string before = "part1 part2";
  string separatorRegex = "\\s+";

  vector<string> result = CheckerHelper::SplitString(before, separatorRegex);

  vector<string> expected = {"part1", "part2"};
  ASSERT_EQ(result, expected);
}
