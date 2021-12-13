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

from pathlib import Path  # noqa: E402

from unittest.mock import MagicMock, patch  # noqa: E402

from modules.check.check import CheckMetadataPy, CheckSummary  # noqa: E402
from modules.check import sys_check  # noqa: E402


TEST_COMPONENT = "test_component"
SYS_CHECK_TEST_PATH = f"/opt/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"


class TestClassCheckPy(unittest.TestCase):

    def setUp(self):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch = patch("modules.check.check.timeout_exit", lambda func: func)
        self.timeout_exit_patch.start()
        importlib.reload(sys_check)

        self.check = sys_check.SysCheck(Path(SYS_CHECK_TEST_PATH))

    def tearDown(self):
        # NOTE: workaround to patching timeout exit
        self.timeout_exit_patch.stop()
        importlib.reload(sys_check)

    def test_class_init_correct(self):
        expected = CheckMetadataPy(
            name=f"{TEST_COMPONENT}_sys_check",
            type="",
            tags="syscheck",
            descr=f"System check for {TEST_COMPONENT} found in {SYS_CHECK_TEST_PATH}",
            dataReq="{}",
            rights="user",
            timeout=10,
            version="",
            run=SYS_CHECK_TEST_PATH)

        value = self.check.get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    def test_get_api_version_positive_correct(self):
        expected = "0.1"

        value = self.check.get_api_version()

        self.assertEqual(expected, value)

    @patch("logging.error")
    @patch("modules.check.check.timeout_exit", side_effect=lambda func: func)
    def test_get_summury_provide_data_to_syscheck(self, mock_timeout_exit, mock_log):
        self.assertRaises(NotImplementedError, self.check.run, {"NOT_EMPTY_DICT": "NOT_EMPTY_DICT"})
        mock_log.assert_called()

    @patch("os.getuid", return_value=0)
    def test_get_summury_run_syscheck_with_root(self, mock_getuid):
        expected = CheckSummary(
            result=json.dumps({
                "Value": {
                    f"{TEST_COMPONENT}_sys_check": {
                        "RetVal": "ERROR",
                        "Value": "Undefined",
                        "Message": "Sys_checks cannot be run with root privileges"
                    }
                }
            })
        )

        value = self.check.run({})

        mock_getuid.assert_called_once()
        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("subprocess.Popen")
    @patch("os.getuid", return_value=1000)
    def test_get_summury_syscheck_pass(self, mock_getuid, mock_popen):
        expected = CheckSummary(
            result=json.dumps({
                "Value": {
                    f"{TEST_COMPONENT}_sys_check": {
                        "RetVal": "PASS",
                        "Value": {
                            "Stdout": {
                                "Value": "",
                                "RetVal": "PASS"
                            },
                            "Stderr": {
                                "Value": "",
                                "RetVal": "PASS"
                            }
                        }
                    }
                }
            })
        )
        mock_popen.return_value.communicate.return_value = ("", "")
        mock_popen.return_value.returncode = 0

        value = self.check.run({})

        mock_getuid.assert_called_once()
        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("subprocess.Popen")
    @patch("os.getuid", return_value=1000)
    def test_get_summury_syscheck_fail(self, mock_getuid, mock_popen):
        expected = CheckSummary(
            result=json.dumps({
                "Value": {
                    f"{TEST_COMPONENT}_sys_check": {
                        "RetVal": "FAIL",
                        "Value": {
                            "Stdout": {
                                "Value": "",
                                "RetVal": "FAIL"
                            },
                            "Stderr": {
                                "Value": "",
                                "RetVal": "FAIL"
                            }
                        }
                    }
                }
            })
        )
        mock_popen.return_value.communicate.return_value = ("", "")
        mock_popen.return_value.returncode = 1

        value = self.check.run({})

        mock_getuid.assert_called_once()
        self.assertEqual(expected.__dict__, value.__dict__)


class TestGetSysCheck(unittest.TestCase):

    def test_get_sys_check_correct_with_correct_argument(self):
        expected = CheckMetadataPy(
            name=f"{TEST_COMPONENT}_sys_check",
            type="",
            tags="syscheck",
            descr=f"System check for {TEST_COMPONENT} found in {SYS_CHECK_TEST_PATH}",
            dataReq="{}",
            rights="user",
            timeout=10,
            version="",
            run=SYS_CHECK_TEST_PATH)

        file = MagicMock()
        file.__str__.return_value = SYS_CHECK_TEST_PATH
        file.is_file.return_value = True

        value = sys_check.getSysChecks(file)[0].get_metadata()

        self.assertEqual(expected.__dict__, value.__dict__)

    @patch("logging.error")
    def test_get_sys_check_raise_error_if_file_not_exist(self, mock_log):
        file = MagicMock()
        file.__str__.return_value = SYS_CHECK_TEST_PATH
        file.is_file.return_value = False

        self.assertRaises(OSError, sys_check.getSysChecks, file)
        mock_log.assert_called()


class TestSearchSysCheck(unittest.TestCase):

    def setUp(self):
        # NOTE: workaround to patching search pathes
        self.mocked_path_to_oneapi_user = MagicMock()
        self.mocked_path_to_oneapi_user.__str__.return_value = "/home/user/intel/oneapi"

        self.mocked_path_to_oneapi_opt = MagicMock()
        self.mocked_path_to_oneapi_opt.__str__.return_value = "/opt/intel/oneapi"

    def tearDown(self):
        # NOTE: workaround to patching search pathes
        importlib.reload(sys_check)

    def test_search_sys_check_return_empty_list(self):
        expected = []

        user_does_not_contain_oneapi = self.mocked_path_to_oneapi_user
        user_does_not_contain_oneapi.rglob.return_value = []
        sys_check.PATH_TO_ONEAPI_USER = user_does_not_contain_oneapi

        opt_does_not_contain_oneapi = self.mocked_path_to_oneapi_opt
        opt_does_not_contain_oneapi.rglob.return_value = []
        sys_check.PATH_TO_ONEAPI_OPT = opt_does_not_contain_oneapi

        value = sys_check.search_sys_checks()

        self.assertEqual(expected, value)

    def test_search_sys_check_user_contains_oneapi(self):
        expected = [
            f"/home/user/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]

        user_contains_oneapi = self.mocked_path_to_oneapi_user
        user_contains_oneapi.rglob.return_value = [
            f"/home/user/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]
        sys_check.PATH_TO_ONEAPI_USER = user_contains_oneapi

        opt_does_not_contain_oneapi = self.mocked_path_to_oneapi_opt
        opt_does_not_contain_oneapi.rglob.return_value = []
        sys_check.PATH_TO_ONEAPI_OPT = opt_does_not_contain_oneapi

        value = sys_check.search_sys_checks()

        self.assertEqual(expected, value)

    def test_search_sys_check_opt_contains_oneapi(self):
        expected = [
            f"/opt/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]

        user_does_not_contain_oneapi = self.mocked_path_to_oneapi_user
        user_does_not_contain_oneapi.rglob.return_value = []
        sys_check.PATH_TO_ONEAPI_USER = user_does_not_contain_oneapi

        opt_contains_oneapi = self.mocked_path_to_oneapi_opt
        opt_contains_oneapi.rglob.return_value = [
            f"/opt/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]
        sys_check.PATH_TO_ONEAPI_OPT = opt_contains_oneapi

        value = sys_check.search_sys_checks()

        self.assertEqual(expected, value)

    def test_search_sys_check_both_contain_oneapi(self):
        expected = [
            f"/opt/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh",
            f"/home/user/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]

        user_contains_oneapi = self.mocked_path_to_oneapi_user
        user_contains_oneapi.rglob.return_value = [
            f"/home/user/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]
        sys_check.PATH_TO_ONEAPI_USER = user_contains_oneapi

        opt_contains_oneapi = self.mocked_path_to_oneapi_opt
        opt_contains_oneapi.rglob.return_value = [
            f"/opt/intel/oneapi/{TEST_COMPONENT}/latest/sys_check/sys_check.sh"
        ]
        sys_check.PATH_TO_ONEAPI_OPT = opt_contains_oneapi

        value = sys_check.search_sys_checks()

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
