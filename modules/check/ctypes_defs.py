# /*******************************************************************************
# Copyright Intel Corporation.
# This software and the related documents are Intel copyrighted materials, and your use of them
# is governed by the express license under which they were provided to you (License).
# Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
# or transmit this software or the related documents without Intel's prior written permission.
# This software and the related documents are provided as is, with no express or implied warranties,
# other than those that are expressly stated in the License.
#
# *******************************************************************************/
import ctypes
import ctypes.util

MAX_STRING_LEN = 500
MAX_LIB_NAME = 256


class CheckMetadata(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * MAX_STRING_LEN),
        ("type", ctypes.c_char * MAX_STRING_LEN),
        ("tags", ctypes.c_char * MAX_STRING_LEN),
        ("descr", ctypes.c_char * MAX_STRING_LEN),
        ("dataReq", ctypes.c_char * MAX_STRING_LEN),
        ("rights", ctypes.c_char * MAX_STRING_LEN),
        ("timeout", ctypes.c_int),
        ("version", ctypes.c_char * MAX_STRING_LEN)
    ]


class CheckResult(ctypes.Structure):
    _fields_ = [
        ("result", ctypes.c_char_p)
    ]


class Check(ctypes.Structure):
    _fields_ = [
        ("check_metadata", CheckMetadata),
        ("run", ctypes.CFUNCTYPE(CheckResult, ctypes.c_char_p)),
        ("api_version", ctypes.c_char * MAX_STRING_LEN)
    ]
