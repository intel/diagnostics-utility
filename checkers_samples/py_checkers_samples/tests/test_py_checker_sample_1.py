#!/usr/bin/env python3
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

# NOTE: workaround to import modules
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402

from py_checkers_samples import py_checker_sample_1  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestExamplePyChecker1(unittest.TestCase):

    def test_run_checker1_positive(self):
        expected = CheckSummary

        actual = py_checker_sample_1.run_checker1({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = py_checker_sample_1.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = py_checker_sample_1.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


if __name__ == '__main__':
    unittest.main()
