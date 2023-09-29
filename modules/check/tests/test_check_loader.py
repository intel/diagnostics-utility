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

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402
from pathlib import Path  # noqa: E402

from modules.check import check_loader  # noqa: E402


class TestLoadChecksFromChecker(unittest.TestCase):

    def setUp(self):
        # Create two mocked object for each check

        # Mocks for CheckC
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_metadata = MagicMock()
        self.mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = self.mock_check_c_1_metadata

        self.mock_check_c_2_name = "mocked_check_c_2"
        self.mock_check_c_2_metadata = MagicMock()
        self.mock_check_c_2_metadata.name = self.mock_check_c_2_name
        self.mock_check_c_2 = MagicMock()
        self.mock_check_c_2.get_metadata.return_value = self.mock_check_c_2_metadata

        # Mocks for CheckExe
        self.mock_check_exe_1_name = "mocked_check_exe_1"
        self.mock_check_exe_1_metadata = MagicMock()
        self.mock_check_exe_1_metadata.name = self.mock_check_exe_1_name
        self.mock_check_exe_1 = MagicMock()
        self.mock_check_exe_1.get_metadata.return_value = self.mock_check_exe_1_metadata

        self.mock_check_exe_2_name = "mocked_check_exe_2"
        self.mock_check_exe_2_metadata = MagicMock()
        self.mock_check_exe_2_metadata.name = self.mock_check_exe_2_name
        self.mock_check_exe_2 = MagicMock()
        self.mock_check_exe_2.get_metadata.return_value = self.mock_check_exe_2_metadata

        # Mocks for CheckPy
        self.mock_check_py_1_name = "mocked_check_py_1"
        self.mock_check_py_1_metadata = MagicMock()
        self.mock_check_py_1_metadata.name = self.mock_check_py_1_name
        self.mock_check_py_1 = MagicMock()
        self.mock_check_py_1.get_metadata.return_value = self.mock_check_py_1_metadata

        self.mock_check_py_2_name = "mocked_check_py_2"
        self.mock_check_py_2_metadata = MagicMock()
        self.mock_check_py_2_metadata.name = self.mock_check_py_2_name
        self.mock_check_py_2 = MagicMock()
        self.mock_check_py_2.get_metadata.return_value = self.mock_check_py_2_metadata

    @patch("logging.warning")
    def test_checker_path_does_not_exist(self, mocked_log):
        expected = []

        checker_path = MagicMock()
        checker_path.__str__.return_value = "wrong path"
        checker_path.exists.return_value = False

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()
        mocked_log.assert_called_once()

    @patch("logging.warning")
    def test_checker_path_does_not_match_to_pattern(self, mocked_log):
        expected = []

        checker_path = MagicMock()
        checker_path.__str__.return_value = "checker.txt"
        checker_path.exists.return_value = True

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()

    @patch("os.access", return_value=False)
    @patch("logging.warning")
    def test_checker_does_not_have_ececute_perm(self, mocked_log, mocked_access):
        expected = []

        checker_path = MagicMock()
        checker_path.__str__.return_value = "checker.sh"
        checker_path.exists.return_value = True

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()

    @patch("modules.check.check_loader.getChecksC")
    def test_checker_path_load_all_check_c(self, mocked_get_checks):
        expected = [self.mock_check_c_1, self.mock_check_c_2]

        checker_path = MagicMock()
        checker_path.__str__.return_value = "checker.so"
        checker_path.exists.return_value = True
        checker_path.name = "checker.so"
        checker_path.suffix = ".so"

        mocked_get_checks.return_value = [self.mock_check_c_1, self.mock_check_c_2]

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()
        mocked_get_checks.assert_called()

    @patch("modules.check.check_loader.getChecksPy")
    def test_checker_path_load_all_check_py(self, mocked_get_checks):
        expected = [self.mock_check_py_1, self.mock_check_py_2]

        checker_path = MagicMock()
        checker_path.__str__.return_value = "checker.py"
        checker_path.exists.return_value = True
        checker_path.name = "checker.py"
        checker_path.suffix = ".py"

        mocked_get_checks.return_value = [self.mock_check_py_1, self.mock_check_py_2]

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()
        mocked_get_checks.assert_called()

    @patch("modules.check.check_loader.getChecksPy")
    @patch("logging.warning")
    def test_checker_path___init___does_not_match(self, mocked_log, mocked_get_checks):
        expected = []

        checker_path = MagicMock()
        checker_path.__str__.return_value = "__init__.py"
        checker_path.exists.return_value = True
        checker_path.name = "__init__.py"
        checker_path.suffix = ".py"

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()
        mocked_get_checks.assert_not_called()

    @patch("os.access", side_effect=[True, True])
    @patch("modules.check.check_loader.getChecksExe")
    def test_checker_path_load_all_check_exe(self, mocked_get_checks, mocked_access):
        expected = [self.mock_check_exe_1, self.mock_check_exe_2]

        checker_path = MagicMock()
        checker_path.__str__.return_value = "exe_check.sh"
        checker_path.exists.return_value = True
        checker_path.name = "exe_check.sh"
        checker_path.suffix = ".sh"

        mocked_get_checks.return_value = [self.mock_check_exe_1, self.mock_check_exe_2]

        actual = check_loader.load_checks_from_checker(checker_path, "0.2", {})

        self.assertEqual(expected, actual)
        checker_path.exists.assert_called_once()
        mocked_get_checks.assert_called()


class TestLoadChecks(unittest.TestCase):

    def setUp(self):
        # Checks examples
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_metadata = MagicMock()
        self.mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = self.mock_check_c_1_metadata

    @patch("modules.check.check_loader.load_checks_from_checker")
    def test_load_checks_return_correct_checks(self, mocked_load_checks_from_checker):
        expected = [self.mock_check_c_1]

        checker_path = MagicMock()
        checker_path.is_symlink.return_value = False

        mocked_load_checks_from_checker.return_value = [self.mock_check_c_1]

        actual = check_loader.load_checks([checker_path], "0.2", {})

        self.assertEqual(expected, actual)
        mocked_load_checks_from_checker.assert_called()


class TestLoadDefaultChecks(unittest.TestCase):

    def setUp(self):
        # Create two mocked object for each check

        # Mocks for CheckC
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_metadata = MagicMock()
        self.mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = self.mock_check_c_1_metadata

        self.mock_check_c_2_name = "mocked_check_c_2"
        self.mock_check_c_2_metadata = MagicMock()
        self.mock_check_c_2_metadata.name = self.mock_check_c_2_name
        self.mock_check_c_2 = MagicMock()
        self.mock_check_c_2.get_metadata.return_value = self.mock_check_c_2_metadata

        # Mocks for CheckExe
        self.mock_check_exe_1_name = "mocked_check_exe_1"
        self.mock_check_exe_1_metadata = MagicMock()
        self.mock_check_exe_1_metadata.name = self.mock_check_exe_1_name
        self.mock_check_exe_1 = MagicMock()
        self.mock_check_exe_1.get_metadata.return_value = self.mock_check_exe_1_metadata

        self.mock_check_exe_2_name = "mocked_check_exe_2"
        self.mock_check_exe_2_metadata = MagicMock()
        self.mock_check_exe_2_metadata.name = self.mock_check_exe_2_name
        self.mock_check_exe_2 = MagicMock()
        self.mock_check_exe_2.get_metadata.return_value = self.mock_check_exe_2_metadata

        # Mocks for CheckPy
        self.mock_check_py_1_name = "mocked_check_py_1"
        self.mock_check_py_1_metadata = MagicMock()
        self.mock_check_py_1_metadata.name = self.mock_check_py_1_name
        self.mock_check_py_1 = MagicMock()
        self.mock_check_py_1.get_metadata.return_value = self.mock_check_py_1_metadata

        self.mock_check_py_2_name = "mocked_check_py_2"
        self.mock_check_py_2_metadata = MagicMock()
        self.mock_check_py_2_metadata.name = self.mock_check_py_2_name
        self.mock_check_py_2 = MagicMock()
        self.mock_check_py_2.get_metadata.return_value = self.mock_check_py_2_metadata

        # Mocks for SysCheck
        self.mock_sys_check_1_name = "mocked_sys_check_1"
        self.mock_sys_check_1_metadata = MagicMock()
        self.mock_sys_check_1_metadata.name = self.mock_sys_check_1_name
        self.mock_sys_check_1 = MagicMock()
        self.mock_sys_check_1.get_metadata.return_value = self.mock_sys_check_1_metadata

        self.mock_sys_check_2_name = "mocked_sys_check_2"
        self.mock_sys_check_2_metadata = MagicMock()
        self.mock_sys_check_2_metadata.name = self.mock_sys_check_2_name
        self.mock_sys_check_2 = MagicMock()
        self.mock_sys_check_2.get_metadata.return_value = self.mock_sys_check_2_metadata

    @patch("modules.check.check_loader.load_checks")
    def test_load_all_default_checks(self, mocked_load_checks):
        expected = [
            self.mock_check_c_1,
            self.mock_check_c_2,
            self.mock_check_py_1,
            self.mock_check_py_2,
            self.mock_check_exe_1,
            self.mock_check_exe_2
        ]

        mocked_load_checks.side_effect = [
            [self.mock_check_c_1,
             self.mock_check_c_2],
            [self.mock_check_py_1,
             self.mock_check_py_2],
            [self.mock_check_exe_1,
             self.mock_check_exe_2],
            [],
            [],
            []
        ]

        actual = check_loader.load_default_checks("0.2", {})

        self.assertEqual(expected, actual)

    @patch("modules.check.check_loader.load_checks")
    def test_load_sys_checks_only(self, mocked_load_checks):
        expected = [
            self.mock_sys_check_1,
            self.mock_sys_check_2
        ]

        mocked_load_checks.side_effect = [
            [self.mock_sys_check_1,
             self.mock_sys_check_2],
            [],
            [],
            [],
            [],
            [],
            []
        ]

        actual = check_loader.load_default_checks("0.2", {})

        self.assertEqual(expected, actual)

    @patch("modules.check.check_loader.load_checks")
    def test_load_checks_c_only(self, mocked_load_checks):
        expected = [
            self.mock_check_c_1,
            self.mock_check_c_2
        ]

        mocked_load_checks.side_effect = [
            [],
            [self.mock_check_c_1,
             self.mock_check_c_2],
            [],
            [],
            [],
            [],
            []
        ]

        actual = check_loader.load_default_checks("0.2", {})

        self.assertEqual(expected, actual)

    @patch("modules.check.check_loader.load_checks")
    def test_load_checks_py_only(self, mocked_load_checks):
        expected = [
            self.mock_check_py_1,
            self.mock_check_py_2
        ]

        mocked_load_checks.side_effect = [
            [],
            [],
            [self.mock_check_py_1,
             self.mock_check_py_2],
            [],
            [],
            [],
            []
        ]

        actual = check_loader.load_default_checks("0.2", {})

        self.assertEqual(expected, actual)

    @patch("modules.check.check_loader.load_checks")
    def test_load_checks_exe_only(self, mocked_load_checks):
        expected = [
            self.mock_check_exe_1,
            self.mock_check_exe_2
        ]

        mocked_load_checks.side_effect = [
            [],
            [],
            [self.mock_check_exe_1,
             self.mock_check_exe_2],
            [],
            [],
            []
        ]

        actual = check_loader.load_default_checks("0.2", {})

        self.assertEqual(expected, actual)

    @patch("builtins.exit")
    @patch("builtins.print")
    @patch("modules.check.check_loader.load_checks", side_effect=Exception())
    def test_load_checks_raise_error(self, mocked_load_checks, mocked_print, mocked_exit):
        expected_exit_code = 1

        check_loader.load_default_checks("0.2", {})

        mocked_load_checks.assert_called()
        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)


class TestLoadChecksFromConfig(unittest.TestCase):

    def setUp(self):
        # Checks examples
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_metadata = MagicMock()
        self.mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = self.mock_check_c_1_metadata

    @patch("modules.check.check_loader.read_config_data")
    @patch("modules.check.check_loader.load_checks_from_checker")
    def test_load_checks_from_config_positive(self, mocked_load_checks_from_checker, mocked_read_config_data):
        expected = [self.mock_check_c_1]

        mocked_read_config_data.return_value = [{"name": self.mock_check_c_1_name, "path": "path"}]
        mocked_load_checks_from_checker.return_value = [self.mock_check_c_1]

        actual = check_loader.load_checks_from_config(MagicMock(), "0.2", {})

        self.assertEqual(expected, actual)

    @patch("builtins.exit")
    @patch("builtins.print")
    @patch("modules.check.check_loader.read_config_data")
    @patch("modules.check.check_loader.load_checks_from_checker")
    def test_load_checks_from_config_no_checks_were_found(
            self, mocked_load_checks_from_checker, mocked_read_config_data, mocked_print, mocked_exit):
        expected_exit_code = 1

        mocked_read_config_data.return_value = [{"name": self.mock_check_c_1_name, "path": "path"}]
        mocked_load_checks_from_checker.return_value = []

        check_loader.load_checks_from_config(MagicMock(), "0.2", {})

        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)


class TestLoadChecksFromEnv(unittest.TestCase):

    def setUp(self):
        # Create two mocked object for each check

        # Mocks for CheckC
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_metadata = MagicMock()
        self.mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = self.mock_check_c_1_metadata

        # Mocks for CheckExe
        self.mock_check_exe_1_name = "mocked_check_exe_1"
        self.mock_check_exe_1_metadata = MagicMock()
        self.mock_check_exe_1_metadata.name = self.mock_check_exe_1_name
        self.mock_check_exe_1 = MagicMock()
        self.mock_check_exe_1.get_metadata.return_value = self.mock_check_exe_1_metadata

        # Mocks for CheckPy
        self.mock_check_py_1_name = "mocked_check_py_1"
        self.mock_check_py_1_metadata = MagicMock()
        self.mock_check_py_1_metadata.name = self.mock_check_py_1_name
        self.mock_check_py_1 = MagicMock()
        self.mock_check_py_1.get_metadata.return_value = self.mock_check_py_1_metadata

        self.mock_check_py_2_name = "mocked_check_py_2"
        self.mock_check_py_2_metadata = MagicMock()
        self.mock_check_py_2_metadata.name = self.mock_check_py_2_name
        self.mock_check_py_2 = MagicMock()
        self.mock_check_py_2.get_metadata.return_value = self.mock_check_py_2_metadata

    @patch("os.getenv", return_value=None)
    def test_load_checks_from_env_env_not_found(self, mocked_getenv):
        expected = []

        actual = check_loader.load_checks_from_env("0.2", {})

        self.assertEqual(expected, actual)

    @patch("builtins.exit")
    @patch("builtins.print")
    @patch("os.getenv", return_value="file_doesnt_exist")
    def test_load_checks_from_env_path_doesnt_exist(self, mocked_getenv, mocked_print, mocked_exit):
        expected_exit_code = 1
        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = False
            check_loader.load_checks_from_env("0.2", {})

        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)

    @patch("builtins.exit")
    @patch("builtins.print")
    @patch("os.getenv", return_value="file_doesnt_exist")
    def test_load_checks_from_env_path_is_not_file_or_dir(self, mocked_getenv, mocked_print, mocked_exit):
        expected_exit_code = 1
        with patch.object(Path, 'exists'):
            check_loader.load_checks_from_env("0.2", {})

        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)

    @patch("os.getenv", return_value="dir")
    @patch.object(Path, "exists", return_value=True)
    @patch.object(Path, "is_dir", return_value=True)
    @patch.object(Path, "is_file", return_value=False)
    @patch("modules.check.check_loader.load_checks")
    @patch("modules.check.check_loader.get_files_list_from_folder", return_value=[MagicMock(), MagicMock(), MagicMock()])  # noqa: E501
    def test_load_checks_from_env_is_dir(
            self,
            mocked_get_files_list_from_folder,
            mocked_load_checks,
            mocked_is_file,
            mocked_is_dir,
            mocked_exists,
            mocked_getenv):

        mocked_load_checks.return_value = [
            self.mock_check_c_1,
            self.mock_check_exe_1,
            self.mock_check_py_1
        ]
        expected = [
            self.mock_check_c_1,
            self.mock_check_exe_1,
            self.mock_check_py_1
        ]

        actual = check_loader.load_checks_from_env("0.2", {})

        self.assertEqual(expected, actual)

    @patch("os.getenv", return_value="file")
    @patch.object(Path, "exists", return_value=True)
    @patch.object(Path, "is_dir", return_value=False)
    @patch.object(Path, "is_file", return_value=True)
    @patch("modules.check.check_loader.load_checks_from_checker")
    def test_load_checks_from_env_is_file(
            self,
            mocked_load_checks_from_checker,
            mocked_is_file,
            mocked_is_dir,
            mocked_exists,
            mocked_getenv):

        mocked_load_checks_from_checker.return_value = [self.mock_check_py_1]
        expected = [self.mock_check_py_1]

        actual = check_loader.load_checks_from_env("0.2", {})

        self.assertEqual(expected, actual)

    @patch("os.getenv", return_value="file1;file2")
    @patch("platform.system", return_value="Windows")
    @patch.object(Path, "exists", side_effect=[True, True])
    @patch.object(Path, "is_dir", side_effect=[False, False])
    @patch.object(Path, "is_file", side_effect=[True, True])
    @patch("modules.check.check_loader.load_checks_from_checker")
    def test_load_checks_from_env_several_file(
            self,
            mocked_load_checks_from_checker,
            mocked_is_file,
            mocked_is_dir,
            mocked_exists,
            mocked_system,
            mocked_getenv):

        mocked_load_checks_from_checker.side_effect = [
            [self.mock_check_py_1],
            [self.mock_check_py_2]
        ]
        expected = [self.mock_check_py_1, self.mock_check_py_2]

        actual = check_loader.load_checks_from_env("0.2", {})

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
