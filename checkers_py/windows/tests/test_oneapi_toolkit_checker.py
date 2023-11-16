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

import os
import platform
import unittest
from unittest.mock import patch
from checkers_py.windows import oneapi_toolkit_checker

from modules.check.check import CheckMetadataPy, CheckSummary


@unittest.skipIf(platform.system() == "Linux", "run on windows only")
class TestOneapiToolkitCheckerApiTest(unittest.TestCase):
    @patch("checkers_py.windows.oneapi_toolkit_checker.installer_cache_check")
    def test_run_positive(self, mock):
        expected = CheckSummary
        actual = oneapi_toolkit_checker.run_oneapi_toolkit_checker({})
        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str
        actual = oneapi_toolkit_checker.get_api_version()
        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy
        check_list = oneapi_toolkit_checker.get_check_list()
        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


@unittest.skipIf(platform.system() == "Linux", "run on windows only")
class TestInstallerCacheCheck(unittest.TestCase):

    @patch("checkers_py.windows.oneapi_toolkit_checker.OneApiCacheChecker")
    def test_run_positive(self, mock_OneApiCacheChecker):
        mock_OneApiCacheChecker.return_value.get_information_as_json.return_value = {
            "CheckResult": {}, "CheckStatus": "INFO"}
        expected = {"OneAPI Installed products": {"CheckResult": {}, "CheckStatus": "INFO"}}
        actual = oneapi_toolkit_checker.installer_cache_check()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.oneapi_toolkit_checker.OneApiCacheChecker")
    def test_get_information_as_json_raise(self, mock_OneApiCacheChecker):
        mock_OneApiCacheChecker.return_value.get_information_as_json.side_effect = PermissionError(
            "Permission denied.")
        expected = {
            "OneAPI Installed products": {
                "CheckResult": {},
                "CheckStatus": "ERROR",
                "Message": "Permission denied.",
                "HowToFix": "Try run as administrator"}
        }
        actual = oneapi_toolkit_checker.installer_cache_check()
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system() == "Linux", "run on windows only")
class TestOneApiCacheChecker(unittest.TestCase):

    @patch("sqlite3.connect")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path", return_value='/path/')  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    def test_get_information_as_json(self, mock_get_toolkits_db, mock2, mock3, mock_db_connect):
        toolkit = oneapi_toolkit_checker.OneApiToolkit(1, "baseKit", "21.22")
        component = oneapi_toolkit_checker.OneApiComponent(
            "Compiler", "21.20", "/path_to_compiler/", 2)
        component.description = "compiler for oneAPI"
        toolkit.components = [component]
        mock_get_toolkits_db.return_value = [toolkit]
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()

        expected = {
            "CheckResult": {
                "oneAPI baseKit 21.22": {
                    "CheckResult": {
                        "Compiler": {
                            "CheckResult": {
                                "Version": {"CheckResult": "21.20", "CheckStatus": "INFO"},
                                "Description":  {"CheckResult": "compiler for oneAPI", "CheckStatus": "INFO"},
                                "Path":  {"CheckResult": "/path_to_compiler/", "CheckStatus": "INFO"}
                            },
                            "CheckStatus": "INFO"
                        },
                    },
                    "CheckStatus": "INFO"
                }
            },
            "CheckStatus": "INFO"}
        actual = cache_checker.get_information_as_json()
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch("os.getenv")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_installer_cache_path_positive(self, mock_db, mock_get_tk, mock_getenv, mock_fill_tk):
        mock_getenv.return_value = "ProgramData_path"
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        expected = os.path.join("ProgramData_path", "Intel", "InstallerCache")
        actual = cache_checker._OneApiCacheChecker__get_installer_cache_path()
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch("os.getenv")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_installer_cache_path_no_ALLUSERSPROFILE_env_var(self, mock_db, mock_get_tk, mock_getenv,
                                                                   mock_fill_tk):
        mock_getenv.side_effect = [None, 'ProgramData_path']
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        expected = os.path.join("ProgramData_path", "Intel", "InstallerCache")
        actual = cache_checker.installer_cache_path
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch("os.getenv")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_installer_cache_path_no_PROGRAMDATA_env_var(self, mock_db, mock_get_tk, mock_getenv,
                                                               mock_fill_tk):
        mock_getenv.side_effect = [None, None, "SystemDrive"]
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        expected = os.path.join("SystemDrive", "ProgramData", "Intel", "InstallerCache")
        actual = cache_checker.installer_cache_path
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch("os.getenv")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_installer_cache_path_no_SYSTEMDRIVE_env_var(self, mock_db, mock_get_tk, mock_getenv,
                                                               mock_fill_tk):
        mock_getenv.side_effect = [None, None, None]
        self.assertRaises(Exception,  oneapi_toolkit_checker.OneApiCacheChecker)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_toolkits_from_db(self, mock_db, mock_get_ic_path, mock_fill_tk):
        mock_db.return_value.cursor.return_value.fetchall.return_value = [
            (1, 'intel.oneapi.win.BaseKit.package', '2023.2.0-00001')]
        expected = oneapi_toolkit_checker.OneApiToolkit(
            1, 'BaseKit', '2023.2.0-00001')
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        cache_checker._OneApiCacheChecker__installed_toolkits
        actual = cache_checker._OneApiCacheChecker__installed_toolkits[0]
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__update_components_information_from_manifest_json")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_components_from_db")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___fill_toolkits_with_components(self,
                                             mock_db,
                                             mock_get_tk,
                                             mock_get_ic_path,
                                             mock_get_components,
                                             mock_upd_from_manifest):
        mock_upd_from_manifest.return_value = [oneapi_toolkit_checker.OneApiComponent(
            "Compiler", "21.20", "/path_to_compiler/", 1)]
        mock_get_tk.return_value = [oneapi_toolkit_checker.OneApiToolkit(
            1, 'intel.oneapi.win.BaseKit.package', '2023.2.0-00001')]
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        expected = cache_checker._OneApiCacheChecker__installed_toolkits[0].components[0]
        self.assertEqual(expected.name, "Compiler")

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__update_components_information_from_manifest_json")  # noqa: E501
    @patch("sqlite3.connect")
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker,
                  "_OneApiCacheChecker__get_installation_paths_dict_from_db",
                  return_value={1: "/path_to_compiler/"})
    def test___get_components_from_db(self,
                                      mock_inst_path_dict_db,
                                      mock_db,
                                      mock_update_from_manifest,
                                      mock_get_tk,
                                      mock_get_ic_path,
                                      mock_fill_tk):
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        mock_db.return_value.cursor.return_value.fetchall.return_value = [
            ('intel.oneapi.win.compiler', '21.20', 1, 1)]

        expected = oneapi_toolkit_checker.OneApiComponent(
            "intel.oneapi.win.compiler", "21.20", "/path_to_compiler/", 1)
        actual = cache_checker._OneApiCacheChecker__get_components_from_db()[0]
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_installation_paths_dict_from_db(self, mock_db,
                                                   mock_get_tk, mock_get_ic_path,
                                                   mock_fill_tk):
        mock_db.return_value.cursor.return_value.fetchall.return_value = [(1, '/path/')]
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        expected = {1: "/path/"}
        actual = cache_checker._OneApiCacheChecker__get_installation_paths_dict_from_db()
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    @patch("builtins.open")
    @patch("json.load")
    def test___update_components_information_from_manifest_json(self, mock_json_load,
                                                                mock_open, mock_db,
                                                                mock_get_tk, mock_get_ic_path,
                                                                mock_fill_tk):
        components = [oneapi_toolkit_checker.OneApiComponent(
            "Compiler", "21.20", "/path_to_compiler/", 2)]
        mock_json_load.return_value = {
            "display": {
                "localized": [
                    {
                        "description": "Compiler for Intel OneAPI",
                        "language": "en-us",
                        "title": "Intel Compiler",
                        "version": "21.20"
                    }
                ]
            },
            "type": "msi",
            "version": "2023.2.0-49390",
            "visible": True
        }
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        actual = cache_checker._OneApiCacheChecker__update_components_information_from_manifest_json(
            components)
        self.assertEqual(actual[0].description, "Compiler for Intel OneAPI")
        self.assertEqual(actual[0].name, "Intel Compiler")

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___is_component_visible_positive(self, mock_db, mock_get_tk, mock_get_ic_path, mock_fill_tk):
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        manifest = {
            "display": {
                "localized": [
                    {
                        "description": "Some definition",
                        "language": "en-us",
                        "title": "Some name",
                        "version": "2023.2.0"
                    }
                ]
            },
            "type": "msi",
            "version": "2023.2.0-49390",
            "visible": True
        }
        expected = True
        actual = cache_checker._OneApiCacheChecker__is_component_visible(manifest)
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___is_component_visible_negative(self, mock_db, mock_get_tk, mock_get_ic_path, mock_fill_tk):
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        manifest = {
            "display": {
                "localized": [
                    {
                        "description": "Some definition",
                        "language": "en-us",
                        "title": "Some name",
                        "version": "2023.2.0"
                    }
                ]
            },
            "type": "msi",
            "version": "2023.2.0-49390",
        }
        expected = False
        actual = cache_checker._OneApiCacheChecker__is_component_visible(manifest)
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_name_from_manifest_json_positive(self,
                                                    mock_db,
                                                    mock_get_tk,
                                                    mock_get_ic_path,
                                                    mock_fill_tk):
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        manifest = {
            "display": {
                "localized": [
                    {
                        "description": "Some definition",
                        "language": "en-us",
                        "title": "Some name",
                        "version": "2023.2.0"
                    }
                ]
            },
            "type": "msi",
            "version": "2023.2.0-49390",
            "visible": True
        }
        expected = "Some name"
        actual = cache_checker._OneApiCacheChecker__get_name_from_manifest_json(manifest)
        self.assertEqual(actual, expected)

    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__fill_toolkits_with_components")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_installer_cache_path")  # noqa: E501
    @patch.object(oneapi_toolkit_checker.OneApiCacheChecker, "_OneApiCacheChecker__get_toolkits_from_db")  # noqa: E501
    @patch("sqlite3.connect")
    def test___get_name_from_manifest_json_negative(self, mock_db,
                                                    mock_get_tk,
                                                    mock_get_ic_path,
                                                    mock_fill_tk):
        cache_checker = oneapi_toolkit_checker.OneApiCacheChecker()
        manifest = {
            "display": {
                "localized": [
                    {
                        "description": "Some definition",
                        "language": "en",
                        "title": "Some name",
                        "version": "2023.2.0"
                    }
                ]
            },
            "type": "msi",
            "version": "2023.2.0-49390",
            "visible": True
        }
        expected = "Undefined"
        actual = cache_checker._OneApiCacheChecker__get_name_from_manifest_json(manifest)
        self.assertEqual(actual, expected)
