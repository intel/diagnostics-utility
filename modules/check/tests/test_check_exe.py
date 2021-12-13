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

import json  # noqa: E402
import importlib  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from modules.check.check import CheckMetadataPy, CheckSummary  # noqa: E402
from modules.check import check_exe  # noqa: E402


test_filename = "test.sh"


exe_metadata_output = json.dumps({
    "name": "exe_example",
    "type": "Data",
    "tags": "cpu",
    "descr": "This is example of exe module",
    "dataReq": "{}",
    "rights": "user",
    "timeout": 1,
    "version": "0.5",
    "run": ""
})

exe_api_version_output = "0.1"

exe_check_result_output = json.dumps({
    "error_code": 0,
    "result": """{"Value": {"Exe example check": {"Value": "Exe example value", "RetVal": "PASS"}}}"""
})


class TestClassCheckExe(unittest.TestCase):

    @patch("subprocess.Popen")
    def setUp(self, mock_popen):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch = patch("modules.check.check.timeout_exit", lambda func: func)
        self.timeout_exit_patch.start()
        importlib.reload(check_exe)

        mock_popen.return_value.communicate.return_value = (exe_metadata_output, "")
        mock_popen.return_value.returncode = 0
        self.check_exe = check_exe.CheckExe("path")

    def tearDown(self):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch.stop()
        importlib.reload(check_exe)

    def test_class_init_correct(self):
        expected = CheckMetadataPy(
            name='exe_example',
            type='Data',
            tags='cpu',
            descr='This is example of exe module',
            dataReq='{}',
            rights='user',
            timeout=1,
            version='0.5',
            run=''
        )

        value = self.check_exe.get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("subprocess.Popen")
    def test_get_api_version_correct(self, mock_popen):
        expected = "0.1"
        mock_popen.return_value.communicate.return_value = (exe_api_version_output, "")
        mock_popen.return_value.returncode = 0

        value = self.check_exe.get_api_version()

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_summury_correct(self, mock_popen):
        expected = CheckSummary(
            result="""{"Value": {"Exe example check": {"Value": "Exe example value", "RetVal": "PASS"}}}"""
        )
        mock_popen.return_value.communicate.return_value = (exe_check_result_output, "")
        mock_popen.return_value.returncode = 0

        value = self.check_exe.run({})

        self.assertEqual(expected.__dict__, value.__dict__)


class TestGetCheckExe(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_get_checks_exe_correct_with_correct_argument(self, mock_popen):
        expected = CheckMetadataPy(
            name='exe_example',
            type='Data',
            tags='cpu',
            descr='This is example of exe module',
            dataReq='{}',
            rights='user',
            timeout=1,
            version='0.5',
            run=''
        )
        mock_popen.return_value.communicate.return_value = (exe_metadata_output, "")
        mock_popen.return_value.returncode = 0

        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = True

        value = check_exe.getChecksExe(mock_file)[0].get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("logging.error")
    @patch("subprocess.Popen")
    def test_get_checks_exe_raise_error_if_check_has_non_zero_return_code(self, mock_popen, mock_log):
        mock_popen.return_value.communicate.return_value = (exe_metadata_output, "")
        mock_popen.return_value.returncode = 1

        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = True

        self.assertRaises(Exception, check_exe.getChecksExe, mock_file)
        mock_log.assert_called()

    @patch("logging.error")
    def test_get_checks_exe_raise_error_if_file_not_exist(self, mock_log):
        mock_file = MagicMock()
        mock_file.__str__.return_value = test_filename
        mock_file.exists.return_value = False

        self.assertRaises(OSError, check_exe.getChecksExe, mock_file)
        mock_log.assert_called()


if __name__ == '__main__':
    unittest.main()
