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
from pathlib import Path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import Mock, MagicMock, call, patch, mock_open  # noqa: E402

from modules import files_helper  # noqa: E402


class TestIsFileExist(unittest.TestCase):

    def test_path_exist_and_it_is_file(self):
        file = Mock()
        file.exists.return_value = True
        file.is_file.return_value = True

        files_helper.is_file_exist(file)

    def test_path_exits_but_is_not_file(self):
        file = Mock()
        file.exists.return_value = True
        file.is_file.return_value = False

        self.assertRaises(ValueError, files_helper.is_file_exist, file)

    def test_path_does_not_exits(self):
        file = Mock()
        file.exists.return_value = False
        file.is_file.return_value = False

        self.assertRaises(ValueError, files_helper.is_file_exist, file)


class TestGetJsonContentFromFile(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="""{"Test": "Content"}"""))
    def test_content_is_json(self):
        expected = {"Test": "Content"}
        file = Mock()
        file.exists.return_value = True

        value = files_helper.get_json_content_from_file(file)

        file.exists.assert_called_once()
        self.assertEqual(expected, value)

    @patch("builtins.open", mock_open(read_data="Wrong content"))
    def test_content_is_not_json(self):
        file = Mock()
        file.exists.return_value = True

        self.assertRaises(ValueError, files_helper.get_json_content_from_file, file)
        file.exists.assert_called_once()


class TestReadConfigData(unittest.TestCase):

    @patch("modules.files_helper.get_json_content_from_file", return_value=[{"path": "check.so"}])
    def test_return_valid_config(self, mock_get_json_content_from_file):
        expected = [{"path": "check.so"}]

        value = files_helper.read_config_data("config.json")

        mock_get_json_content_from_file.assert_called_once()
        self.assertEqual(expected, value)

    @patch("modules.files_helper.get_json_content_from_file",
           return_value=[{"path": "check.so"}, {"not_path_filed": "test"}])
    def test_handle_invalid_config_without_path_field(self, mock_get_json_content_from_file):
        self.assertRaises(ValueError, files_helper.read_config_data, "config.json")
        mock_get_json_content_from_file.assert_called_once()

    @patch("modules.files_helper.get_json_content_from_file",
           return_value={"not_path_filed": "test"})
    def test_handle_invalid_config_is_not_list(self, mock_get_json_content_from_file):
        self.assertRaises(ValueError, files_helper.read_config_data, "config.json")
        mock_get_json_content_from_file.assert_called_once()


class TestGetFilesListFromFolder(unittest.TestCase):

    def test_get_files_list_from_folder_positive(self):
        expected = ["file"]

        path = MagicMock()
        path.exists.return_value = True
        path.iterdir.return_value = ["file"]

        value = files_helper.get_files_list_from_folder(path)

        self.assertEqual(expected, value)

    def test_get_files_list_from_folder_path_does_not_exist(self):
        expected = []

        path = MagicMock()
        path.exists.return_value = False

        value = files_helper.get_files_list_from_folder(path)

        self.assertEqual(expected, value)


class TestGetExamineData(unittest.TestCase):

    @patch("modules.files_helper.get_json_content_from_file", return_value={})
    def test_get_examine_data_positive(self, mocked_get_json_content_from_file):
        expected = {}

        value = files_helper.get_examine_data(MagicMock())

        self.assertEqual(expected, value)

    @patch("logging.warning")
    @patch("modules.files_helper.get_json_content_from_file", side_effect=ValueError())
    def test_get_files_list_from_folder_path_does_not_exist(
            self, mocked_get_json_content_from_file, mocked_log):
        expected = None

        value = files_helper.get_examine_data(MagicMock())

        self.assertEqual(expected, value)
        mocked_log.assert_called()


class TestSaveJsonOutputFile(unittest.TestCase):

    def setUp(self):
        # Example checks
        self.mock_check_c_1_name = "mocked_check_c_1"
        self.mock_check_c_1_result = {
            "Value": {
                "Check 1": {
                    "RetVal": "PASS",
                    "Value": "Check 1 Value"
                }
            }
        }
        mock_check_c_1_metadata = MagicMock()
        mock_check_c_1_metadata.name = self.mock_check_c_1_name
        self.mock_check_c_1 = MagicMock()
        self.mock_check_c_1.get_metadata.return_value = mock_check_c_1_metadata

        self.mock_check_c_2_name = "mocked_check_c_2"
        self.mock_check_c_2_result = {
            "Value": {
                "Check 2": {
                    "RetVal": "PASS",
                    "Value": "Check 2 Value"
                }
            }
        }
        mock_check_c_2_metadata = MagicMock()
        mock_check_c_2_metadata.name = self.mock_check_c_2_name
        self.mock_check_c_2 = MagicMock()
        self.mock_check_c_2.get_metadata.return_value = mock_check_c_2_metadata

    @patch("builtins.open", create=True)
    @patch("json.loads")
    @patch("json.dump")
    def test_save_json_output_file_positive(self, mocked_dump, mocked_loads, mocked_open):
        expected_output = {
            self.mock_check_c_1_name: self.mock_check_c_1_result,
            self.mock_check_c_2_name: self.mock_check_c_2_result
        }

        expected_file = MagicMock()

        mocked_loads.side_effect = [self.mock_check_c_1_result, self.mock_check_c_2_result]
        mocked_open.return_value.__enter__.return_value = expected_file

        files_helper.save_json_output_file([self.mock_check_c_1, self.mock_check_c_2], MagicMock())

        mocked_dump.assert_called_once_with(expected_output, expected_file, indent=4)

    @patch("builtins.print")
    @patch("builtins.open", create=True)
    @patch("json.loads")
    @patch("json.dump")
    def test_save_json_output_file_loads_raise_exception(
            self, mocked_dump, mocked_loads, mocked_open, mocked_print):
        expected_output = {
            self.mock_check_c_1_name: self.mock_check_c_1_result
        }

        expected_file = MagicMock()

        mocked_loads.side_effect = [self.mock_check_c_1_result, ValueError()]
        mocked_open.return_value.__enter__.return_value = expected_file

        files_helper.save_json_output_file([self.mock_check_c_1, self.mock_check_c_2], MagicMock())

        mocked_dump.assert_called_once_with(expected_output, expected_file, indent=4)
        mocked_print.assert_called_once()


class TestConfigureOutputFiles(unittest.TestCase):

    @patch("modules.files_helper.logging")
    def test_configure_output_files_permission_create(self, mocked_logging):
        args = MagicMock()
        args.output.mkdir.side_effect = PermissionError

        expected_value = (None, None)

        real_value = files_helper.configure_output_files(args)

        self.assertTrue(mocked_logging.warning.called)
        self.assertEqual(real_value, expected_value)

    @patch("os.access", return_value=False)
    @patch("modules.files_helper.logging")
    def test_configure_output_files_permission_exist(
            self,
            mocked_logging,
            mocked_access):
        args = MagicMock()
        args.output.exists.return_value = True

        expected_value = (None, None)

        real_value = files_helper.configure_output_files(args)

        self.assertTrue(mocked_logging.warning.called)
        self.assertEqual(real_value, expected_value)

    @patch("os.access", return_value=True)
    @patch("modules.files_helper._args_string", return_value="arg1_value_arg2")
    @patch("platform.node", return_value="node")
    @patch("modules.files_helper.datetime")
    def test_configure_output_files_positive(
            self,
            mocked_datetime,
            mocked_node,
            mocked__args_string,
            mocked_access):
        args = MagicMock()
        args.output.exists.return_value = True
        mocked_datetime.now.return_value.strftime.return_value = "time"

        expected_value = (
            call("diagnostics_arg1_value_arg2_node_time.txt"),
            call("diagnostics_arg1_value_arg2_node_time.json")
        )

        files_helper.configure_output_files(args)

        args.output.__truediv__.assert_has_calls(expected_value)


class TestArgsString(unittest.TestCase):

    def test_args_string_all_positive(self):
        args = MagicMock()
        args.filter = ["fil"]
        args.list = True
        args.config = Path("/home/test/config.json")
        args.single_checker = Path("/home/test/check.py")
        args.force = True
        args.verbosity = 5

        expected_value = "filter_fil_list_config_config_single_checker_check_force_verbosity_5"

        real_value = files_helper._args_string(args)

        self.assertEqual(real_value, expected_value)

    def test_args_string_empty_positive(self):
        args = MagicMock()
        args.filter = ["not_initialized"]
        args.list = False
        args.config = None
        args.single_checker = None
        args.examine = None
        args.force = False
        args.verbosity = -1

        expected_value = ""

        real_value = files_helper._args_string(args)

        self.assertEqual(real_value, expected_value)


if __name__ == '__main__':
    unittest.main()
