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

from modules.select import process_select, get_selected_checks  # noqa: E402


class TestProcessSelect(unittest.TestCase):

    def test_process_select_one_select_initialized(self):
        expected = {"select"}

        actual = process_select(["select"])

        self.assertEqual(expected, actual)

    def test_process_select_two_select_initialized(self):
        expected = {"select_1", "select_2"}

        actual = process_select(["select_1", "select_2"])

        self.assertEqual(expected, actual)

    def test_process_select_not_initialized(self):
        expected = {"default"}

        actual = process_select(["not_initialized"])

        self.assertEqual(expected, actual)


class TestGetSelectedChecks(unittest.TestCase):

    def setUp(self):
        self.check_1 = MagicMock()
        self.check_1.get_metadata.return_value.name = "check_1"
        self.check_1.get_metadata.return_value.groups = "select_1"

        self.check_2 = MagicMock()
        self.check_2.get_metadata.return_value.name = "check_2"
        self.check_2.get_metadata.return_value.groups = "select_2"

    def test_get_selected_checks_all_select_only(self):
        expected = [self.check_1, self.check_2]

        actual = get_selected_checks([self.check_1, self.check_2], ["all"])

        self.assertEqual(expected, actual)

    def test_get_selected_checks_all_select_not_only(self):
        expected = [self.check_1, self.check_2]

        actual = get_selected_checks([self.check_1, self.check_2], ["select_1", "all"])

        self.assertEqual(expected, actual)

    def test_get_selected_checks_select_by_group(self):
        expected = [self.check_2]

        actual = get_selected_checks([self.check_1, self.check_2], ["select_2"])

        self.assertEqual(expected, actual)

    def test_get_selected_checks_select_by_two_groups(self):
        expected = [self.check_1, self.check_2]

        actual = get_selected_checks([self.check_1, self.check_2], ["select_1", "select_2"])

        self.assertEqual(expected, actual)

    def test_get_selected_checks_select_by_name(self):
        expected = [self.check_1]

        actual = get_selected_checks([self.check_1, self.check_2], ["check_1"])

        self.assertEqual(expected, actual)

    def test_get_selected_checks_select_by_name_and_group(self):
        expected = [self.check_1, self.check_2]

        actual = get_selected_checks([self.check_1, self.check_2], ["check_1", "select_2"])

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
