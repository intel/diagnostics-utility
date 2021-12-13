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

from typing import List, Sequence
import ctypes
import logging

from modules.check.ctypes_defs import Check


class CheckList(Sequence[Check]):

    def __init__(self, lib_name: str):
        # load checker lib
        self.lib_name = lib_name
        self.checker_lib = self._load_c_checker_lib(lib_name)

        # get version api
        api_version = self.checker_lib.get_api_version()
        self.api_version = api_version.decode("utf-8")

        # load checkers
        checker_pointers = self.checker_lib.get_check_list()

        # get checkers list
        self.checkers = self._get_check_list_from_pointers(checker_pointers)

    @staticmethod
    def _load_c_checker_lib(lib_name: str) -> ctypes.CDLL:
        try:
            lib = ctypes.CDLL(lib_name)
        except Exception as ex:
            logging.error("Failed to load %s: %s", lib_name, str(ex))
            raise

        # get_check_list
        lib.get_check_list.restype = ctypes.POINTER(ctypes.POINTER(Check))
        lib.get_check_list.argtypes = None

        # get_api_version
        lib.get_api_version.restype = ctypes.c_char_p
        lib.get_api_version.argtypes = None

        return lib

    @staticmethod
    def _get_check_list_from_pointers(
            checker_pointers: ctypes.POINTER(ctypes.POINTER(Check))) -> List[Check]:
        result: List[Check] = []
        i = 0
        while(checker_pointers[i]):
            result.append(checker_pointers[i].contents)
            i += 1
        return result

    def __getitem__(self, key: int) -> Check:
        if isinstance(key, slice):
            raise Exception("Subclass disallows slicing")
        return self.checkers[key]

    def __len__(self) -> int:
        return len(self.checkers)

    def __str__(self) -> str:
        return f"CheckList({self.lib_name})"
