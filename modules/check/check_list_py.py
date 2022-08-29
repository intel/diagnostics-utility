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

from typing import Sequence
from pathlib import Path

from modules.check.check import CheckMetadataPy


class CheckListPy(Sequence[CheckMetadataPy]):

    def __init__(self, module_name: Path):
        # load checker module
        self.module_name = module_name
        self.checker_module = __import__(self.module_name.stem)

        # get version api
        self.api_version = self.checker_module.get_api_version()

        # get checkers list
        self.checkers = self.checker_module.get_check_list()

    def __reduce__(self):
        return(self.__class__, (self.module_name,))

    def __getitem__(self, key: int) -> CheckMetadataPy:
        if isinstance(key, slice):
            raise Exception("Subclass disallows slicing")
        return self.checkers[key]

    def __len__(self) -> int:
        return len(self.checkers)

    def __str__(self) -> str:
        return f"CheckListPy({self.module_name})"
