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

#ifndef ONEAPI_TOOLKIT_CHECKER_H
#define ONEAPI_TOOLKIT_CHECKER_H

#include <string>

#include "AptChecker.h"
#include "BInstallerChecker.h"
#include "CheckerHelper.h"
#include "JsonNode.h"
#include "RpmChecker.h"

using std::string;

class OneapiChecker {
 private:
  AptChecker *aptChecker;
  BInstallerChecker *bInstallerChecker;
  RpmChecker *rpmChecker;

 public:
  OneapiChecker(AptChecker *aptChecker, BInstallerChecker *bInstallerChecker,
                RpmChecker *rpmChecker);

  int PerformCheck(string &message);
};

#endif
