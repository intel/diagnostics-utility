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
c_metadata.groups = "cpu".encode()
c_metadata.descr = "This is example of c module".encode()
c_metadata.dataReq = '''{}'''.encode()
c_metadata.merit = 0
c_metadata.timeout = 1
c_metadata.version = 2

c_api_version = "0.2"

c_run_output = Mock()
c_run_output.error_code = 0
result_str = """{"CheckResult": {"C example check": {"CheckResult": "C example value", "CheckStatus": "PASS"}}}"""   # noqa: E501
c_run_output.result = result_str.encode()


c_run = Mock()
c_run.return_value = c_run_output

c_check = Mock()
c_check.check_metadata = c_metadata
c_check.run = c_run

c_check_list = MagicMock()
c_check_list.__getitem__.return_value = c_check
c_check_list.__len__.return_value = 1
c_check_list.__iter__.return_value = [c_check]
c_check_list.api_version = c_api_version


class TestClassCheckC(unittest.TestCase):

    def setUp(self):
        importlib.reload(check_c)
        self.check = check_c.CheckC(0, c_check_list)

    def tearDown(self):
        importlib.reload(check_c)

    def test_class_init_correct(self):
        expected = CheckMetadataPy(
            name='c_example',
            type='Data',
            groups='cpu',
            descr='This is example of c module',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

        actual = self.check.get_metadata()

        self.assertEqual(expected.__dict__, actual.__dict__)

    def test_get_api_version_positive_correct(self):
        expected = c_api_version

        actual = self.check.get_api_version()

        self.assertEqual(expected, actual)

    def test_get_summury_positive_correct(self):
        expected = CheckSummary(
            result="""{"CheckResult": {"C example check": {"CheckResult": "C example value", "CheckStatus": "PASS"}}}"""  # noqa: E501
        )
        actual = self.check.run({})

        self.assertEqual(expected.__dict__, actual.__dict__)


class TestGetCheckC(unittest.TestCase):

    @patch("modules.check.check_c.CheckListC", return_value=c_check_list)
    def test_get_checks_c_correct_with_correct_argument(self, mock_check_list):
        expected = CheckMetadataPy(
            name='c_example',
            type='Data',
            groups='cpu',
            descr='This is example of c module',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = True

        actual = check_c.getChecksC(mock_file, "0.2")[0].get_metadata()

        self.assertEqual(expected.__dict__, actual.__dict__)

    @patch("logging.error")
    def test_get_checks_c_raise_error_if_file_not_exist(self, mock_log):
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = False

        self.assertRaises(OSError, check_c.getChecksC, mock_file, "0.2")
        mock_log.assert_called()

    @patch("modules.check.check_c.CheckListC", return_value=c_check_list)
    @patch("logging.error")
    def test_get_checks_py_raise_error_if_version_not_compatible(self, mock_log, mock_check_list):
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = True

        self.assertRaises(ValueError, check_c.getChecksC, mock_file, "0.3")
        mock_log.assert_called()


if __name__ == '__main__':
    unittest.main()
