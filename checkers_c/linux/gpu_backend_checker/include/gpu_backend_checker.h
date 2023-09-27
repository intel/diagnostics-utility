/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef GPU_BACKEND_CHECK_H_
#define GPU_BACKEND_CHECK_H_

#include <iostream>
#include "JsonNode.h"
#include "CLDriverChecker.h"
#include "LZDriverChecker.h"

using namespace std;

class GpuBackendChecker {
    private:
        LZ_DriverChecker* lzDriverChecker;
        CL_DriverChecker* clDriverChecker;

    public:
        GpuBackendChecker(LZ_DriverChecker* lzDriverChecker, CL_DriverChecker* clDriverChecker);
        ~GpuBackendChecker() = default;

        int PerformCheck(string &message);
};


#endif /* GPU_BACKEND_CHECK_H_ */
