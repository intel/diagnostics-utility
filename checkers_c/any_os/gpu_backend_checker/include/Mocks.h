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

#ifndef GPU_BACKEND_CHECKER_MOCKS_H
#define GPU_BACKEND_CHECKER_MOCKS_H

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <string>

#include "CLDriverChecker.h"
#include "LZDriverChecker.h"

using std::string;

class LZ_DriverCheckerMock : public LZ_DriverChecker {
 public:
  MOCK_METHOD(bool, Load, (string & message), (override));
  MOCK_METHOD(bool, Initialize, (string & message), (override));
  MOCK_METHOD(void, GetDriverInfo, (string & message), (override));
};

class CL_DriverCheckerMock : public CL_DriverChecker {
 public:
  MOCK_METHOD(bool, Load, (string & message), (override));
  MOCK_METHOD(void, GetDriverInfo, (string & message), (override));
  MOCK_METHOD(void, GetDeviceInfo, (cl_device_id deviceId, string& message),
              (override));
  MOCK_METHOD(string, GetErrorMessage, (cl_int error), (override));
  MOCK_METHOD(string, GetDeviceTypeString, (cl_device_type type), (override));
  MOCK_METHOD(string, GetArrayString, (size_t * array, size_t array_size),
              (override));
  MOCK_METHOD(string, GetCacheTypeString, (cl_device_mem_cache_type type),
              (override));
  MOCK_METHOD(string, GetLocalMemTypeString, (cl_device_local_mem_type type),
              (override));
};

#endif
