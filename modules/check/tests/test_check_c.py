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
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

import importlib  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import Mock, MagicMock, patch  # noqa: E402

from modules.check.check import CheckMetadataPy, CheckSummary  # noqa: E402
from modules.check import check_c  # noqa: E402


test_filename = "test.so"

c_metadata = Mock()
c_metadata.name = "c_example".encode()
c_metadata.type = "Data".encode()
c_metadata.tags = "cpu".encode()
c_metadata.descr = "This is example of c module".encode()
c_metadata.dataReq = "{}".encode()
c_metadata.rights = "user".encode()
c_metadata.timeout = 1
c_metadata.version = "0.5".encode()

c_api_version = "0.1".encode()

c_run_output = Mock()
c_run_output.error_code = 0
result_str = """{"Value": {"C example check": {"Value": "C example value", "RetVal": "PASS"}}}"""
c_run_output.result = result_str.encode()


c_run = Mock()
c_run.return_value = c_run_output

c_check = Mock()
c_check.check_metadata = c_metadata
c_check.run = c_run

c_check_list = MagicMock()
c_check_list.__iter__.return_value = [c_check]
c_check_list.api_version = c_api_version


class TestClassCheckC(unittest.TestCase):

    def setUp(self):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch = patch("modules.check.check.timeout_exit", lambda func: func)
        self.timeout_exit_patch.start()
        importlib.reload(check_c)

        self.check = check_c.CheckC(c_check, c_check_list)

    def tearDown(self):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch.stop()
        importlib.reload(check_c)

    def test_class_init_correct(self):
        expected = CheckMetadataPy(
            name='c_example',
            type='Data',
            tags='cpu',
            descr='This is example of c module',
            dataReq='{}',
            rights='user',
            timeout=1,
            version='0.5',
            run='run'
        )

        value = self.check.get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    def test_get_api_version_positive_correct(self):
        expected = c_api_version

        value = self.check.get_api_version()

        self.assertEqual(expected, value)

    def test_get_summury_positive_correct(self):
        expected = CheckSummary(
            result="""{"Value": {"C example check": {"Value": "C example value", "RetVal": "PASS"}}}"""
        )

        value = self.check.run({})

        self.assertEqual(expected.__dict__, value.__dict__)


class TestGetCheckC(unittest.TestCase):

    @patch("modules.check.check_c.CheckList", return_value=c_check_list)
    def test_get_checks_c_correct_with_correct_argument(self, mock_check_list):
        expected = CheckMetadataPy(
            name='c_example',
            type='Data',
            tags='cpu',
            descr='This is example of c module',
            dataReq='{}',
            rights='user',
            timeout=1,
            version='0.5',
            run='run'
        )
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = True

        value = check_c.getChecksC(mock_file)[0].get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("logging.error")
    def test_get_checks_c_raise_error_if_file_not_exist(self, mock_log):
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = False

        self.assertRaises(OSError, check_c.getChecksC, mock_file)
        mock_log.assert_called()


if __name__ == '__main__':
    unittest.main()
