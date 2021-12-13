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
from unittest.mock import MagicMock  # noqa: E402

from modules.filter import process_filter, get_filtered_checks  # noqa: E402


class TestProcessFilter(unittest.TestCase):

    def test_process_filter_one_filter_initialized(self):
        expected = ["filter"]

        value = process_filter(["filter"])

        self.assertEqual(expected, value)

    def test_process_filter_two_filter_initialized(self):
        expected = ["filter_1", "filter_2"]

        value = process_filter(["filter_1", "filter_2"])

        self.assertEqual(expected, value)

    def test_process_filter_not_initialized(self):
        expected = ["default"]

        value = process_filter(["not_initialized"])

        self.assertEqual(expected, value)


class TestGetFilteredChecks(unittest.TestCase):

    def setUp(self):
        self.check_1 = MagicMock()
        self.check_1.get_metadata.return_value.name = "check_1"
        self.check_1.get_metadata.return_value.tags = "filter_1"

        self.check_2 = MagicMock()
        self.check_2.get_metadata.return_value.name = "check_2"
        self.check_2.get_metadata.return_value.tags = "filter_2"

    def test_get_filtered_checks_all_filter_only(self):
        expected = [self.check_1, self.check_2]

        value = get_filtered_checks([self.check_1, self.check_2], ["all"])

        self.assertEqual(expected, value)

    def test_get_filtered_checks_all_filter_not_only(self):
        expected = [self.check_1, self.check_2]

        value = get_filtered_checks([self.check_1, self.check_2], ["filter_1", "all"])

        self.assertEqual(expected, value)

    def test_get_filtered_checks_filter_by_tag(self):
        expected = [self.check_2]

        value = get_filtered_checks([self.check_1, self.check_2], ["filter_2"])

        self.assertEqual(expected, value)

    def test_get_filtered_checks_filter_by_two_tags(self):
        expected = [self.check_1, self.check_2]

        value = get_filtered_checks([self.check_1, self.check_2], ["filter_1", "filter_2"])

        self.assertEqual(expected, value)

    def test_get_filtered_checks_filter_by_name(self):
        expected = [self.check_1]

        value = get_filtered_checks([self.check_1, self.check_2], ["check_1"])

        self.assertEqual(expected, value)

    def test_get_filtered_checks_filter_by_name_and_tag(self):
        expected = [self.check_1, self.check_2]

        value = get_filtered_checks([self.check_1, self.check_2], ["check_1", "filter_2"])

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
