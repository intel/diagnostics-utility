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
from unittest.mock import MagicMock, patch, mock_open  # noqa: E402

from checkers_py.linux import driver_compatibility_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestDriverCompatibilityCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.driver_compatibility_checker.check_compatibilities")
    def test_run_positive(self, mocked_check_compatibilities):
        expected = CheckSummary

        mocked_check_compatibilities.side_effect = lambda node, data: node.update({
            "Check": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = driver_compatibility_checker.run_driver_compatibility_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = driver_compatibility_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = driver_compatibility_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestCheckCompatibilities(unittest.TestCase):

    def setUp(self):
        self.data = {
            "oneapi_app_check": {
                "Value": {
                    "APP": {
                        "RetVal": "INFO",
                        "Value": {
                            "oneAPI products": {
                                "Command": "Parse installed oneapi caches",
                                "RetVal": "INFO",
                                "Value": {
                                    "Intel® Advisor": {
                                        "RetVal": "INFO",
                                        "Value": {
                                            "Version": {
                                                "RetVal": "INFO",
                                                "Value": "2021.4.0"
                                            }
                                        }
                                    },
                                    "Intel® Cluster Checker": {
                                        "RetVal": "INFO",
                                        "Value": {
                                            "Version": {
                                                "RetVal": "INFO",
                                                "Value": "2021.3.0"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "gpu_backend_check": {
                "Value": {
                    "GPU": {
                        "RetVal": "INFO",
                        "Value": {
                            "Intel® oneAPI Level Zero Driver": {
                                "Value": {
                                    "Driver information": {
                                        "RetVal": "INFO",
                                        "Value": {
                                            "Driver # 0": {
                                                "Command": "",
                                                "RetVal": "INFO",
                                                "Value": {
                                                    "Driver version": {
                                                        "Command": "",
                                                        "Verbosity": 1,
                                                        "RetVal": "INFO",
                                                        "Value": "1.0.19310"
                                                    },
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "OpenCL™ Driver": {
                                "Value": {
                                    "Driver information": {
                                        "RetVal": "INFO",
                                        "Value": {
                                            "Platform # 0": {
                                                "Value": {
                                                    "Devices": {
                                                        "RetVal": "INFO",
                                                        "Value": {
                                                            "Device # 0": {
                                                                "Command": "",
                                                                "RetVal": "INFO",
                                                                "Value": {
                                                                    "Driver version": {
                                                                        "Verbosity": 2,
                                                                        "RetVal": "INFO",
                                                                        "Value": "21.11.19310"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "oneapi_env_check": {
                "Value": {
                    "oneAPI products installed in the environment": {
                        "Value": {
                            "Intel® oneAPI Compiler": {
                                "Value": {
                                    "Version": {
                                        "Value": "2021.4.0",
                                        "RetVal": "INFO"
                                    }
                                },
                                "RetVal": "INFO"
                            }
                        },
                        "RetVal": "INFO"
                    }
                }
            }
        }

    def test__get_compatibilities_for_product_positive(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [("Intel® oneAPI Level Zero", "1.0.19310"), ("OpenCL™", "21.11.19310")]
        expected_value = {"Intel® oneAPI Level Zero": "1.0.19310", "OpenCL™": "21.11.19310"}

        real_value = driver_compatibility_checker._get_compatibilities_for_product("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__get_compatibilities_for_product_empty_positive(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = []
        expected_value = {}

        real_value = driver_compatibility_checker._get_compatibilities_for_product("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__get_compatibilities_for_product_negative(self):
        cursor = MagicMock()
        cursor.execute.side_effect = ValueError()

        with self.assertRaises(ValueError):
            driver_compatibility_checker._get_compatibilities_for_product("name", "version", cursor)

    def test__is_regression_yes_positive(self):
        cursor = MagicMock()
        cursor.fetchone.return_value = "1.0.19310"
        expected_value = True

        real_value = driver_compatibility_checker._is_regression("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__is_regression_no_positive(self):
        cursor = MagicMock()
        cursor.fetchone.return_value = None
        expected_value = False

        real_value = driver_compatibility_checker._is_regression("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__is_regression_negative(self):
        cursor = MagicMock()
        cursor.execute.side_effect = ValueError()

        with self.assertRaises(ValueError):
            driver_compatibility_checker._is_regression("name", "version", cursor)

    def test__is_latest_version_yes_positive(self):
        cursor = MagicMock()
        cursor.fetchone.return_value = "version"
        expected_value = True

        real_value = driver_compatibility_checker._is_latest_version("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__is_latest_version_no_positive(self):
        cursor = MagicMock()
        cursor.fetchone.return_value = "version2"
        expected_value = False

        real_value = driver_compatibility_checker._is_latest_version("name", "version", cursor)

        self.assertEqual(real_value, expected_value)

    def test__is_latest_version_negative(self):
        cursor = MagicMock()
        cursor.execute.side_effect = ValueError()

        with self.assertRaises(ValueError):
            driver_compatibility_checker._is_latest_version("name", "version", cursor)

    def test_get_gpu_driver_version_positive(self):
        expected_value = {"Intel® oneAPI Level Zero": "1.0.19310", "OpenCL™": "21.11.19310"}

        real_value = driver_compatibility_checker.get_gpu_driver_version(self.data)

        self.assertEqual(real_value, expected_value)

    def test_get_gpu_driver_version_empty_positive(self):
        expected_value = {}

        real_value = driver_compatibility_checker.get_gpu_driver_version({})

        self.assertEqual(real_value, expected_value)

    def test_get_product_versions_install_positive(self):
        expected_value = {"Intel® Advisor": "2021.4.0", "Intel® Cluster Checker": "2021.3.0"}

        real_value = driver_compatibility_checker.get_product_versions_install(self.data)

        self.assertEqual(real_value, expected_value)

    def test_get_product_versions_install_empty_positive(self):
        expected_value = {}

        real_value = driver_compatibility_checker.get_product_versions_install({})

        self.assertEqual(real_value, expected_value)

    def test_get_product_versions_env_positive(self):
        expected_value = {"Intel® oneAPI Compiler": "2021.4.0"}

        real_value = driver_compatibility_checker.get_product_versions_env(self.data)

        self.assertEqual(real_value, expected_value)

    def test_get_product_versions_env_empty_positive(self):
        expected_value = {}

        real_value = driver_compatibility_checker.get_product_versions_env({})

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._is_regression", return_value=True)
    def test__check_regression_yes_positive(self, mocked__is_regression):
        expected_value = {
            "Regression": {
                "Message": "Installed version of name is regression.",
                "RetVal": "FAIL",
                "Value": "Yes"
            }
        }

        real_value = {}
        driver_compatibility_checker._check_regression(real_value, "name", "version", "cursor")

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._is_regression", return_value=False)
    def test__check_regression_no_positive(self, mocked__is_regression):
        expected_value = {
            "Regression": {
                "RetVal": "PASS",
                "Value": "No"
            }
        }

        real_value = {}
        driver_compatibility_checker._check_regression(real_value, "name", "version", "cursor")

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._is_regression", side_effect=ValueError("Error"))
    def test__check_regression_error_positive(self, mocked__is_regression):
        expected_value = {
            "Regression": {
                "Message": "Error",
                "RetVal": "ERROR",
                "Value": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        real_value = {}
        driver_compatibility_checker._check_regression(real_value, "name", "version", "cursor")

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._is_latest_version", return_value=True)
    @patch("checkers_py.linux.driver_compatibility_checker._check_regression")
    def test__check_drivers_positive(self, mocked__check_regression, mocked__is_latest_version):
        mocked__check_regression.side_effect = lambda node, name, version, cursor: node.update({
            "Regression": {
                "RetVal": "PASS",
                "Value": "No"
            }
        })
        expected_value = {
            "GPU drivers information": {
                "RetVal": "INFO",
                "Value": {
                    "name": {
                        "RetVal": "INFO",
                        "Value": {
                            "Regression": {
                                "RetVal": "PASS",
                                "Value": "No"
                            },
                            "Version": {
                                "RetVal": "INFO",
                                "Value": "version"
                            }
                        }
                    }
                }
            }
        }

        real_value = {}
        driver_compatibility_checker._check_drivers(real_value, {"name": "version"}, "cursor")

        self.assertEqual(real_value, expected_value)

    def test__check_drivers_empty_drivers_positive(self):
        expected_value = {
            "GPU drivers information": {
                "Message": "There is no information about GPU driver(s).",
                "RetVal": "WARNING",
                "Value": {}
            }
        }

        real_value = {}
        driver_compatibility_checker._check_drivers(real_value, {}, "cursor")

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._is_latest_version", side_effect=ValueError("Error"))  # noqa: E501
    def test__check_drivers_error_positive(self, mocked__is_latest_version):
        expected_value = {
            "GPU drivers information": {
                "Message": "Error",
                "RetVal": "ERROR",
                "Value": {},
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        real_value = {}
        driver_compatibility_checker._check_drivers(real_value, {"name": "version"}, "cursor")

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._get_compatibilities_for_product", side_effect=[{"LevelZero": "1.0.19310", "OpenCL™": "21.11.19310"}])  # noqa: E501
    def test__check_compatibilities_env_positive(self, mocked__get_compatibilities_for_product):
        expected_value = {
            "Compatibility of the products in the environment": {
                "RetVal": "PASS",
                "Value": {
                    "name-version": {
                        "RetVal": "PASS",
                        "Value": "Yes"
                    }
                }
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {"name": "version"},
            {"LevelZero": "1.0.19310", "OpenCL™": "21.11.19310"},
            False,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._get_compatibilities_for_product", side_effect=[{"LevelZero": "1.1.19310", "OpenCL™": "21.11.19310"}])  # noqa: E501
    def test__check_compatibilities_env_not_compatible_positive(
            self, mocked__get_compatibilities_for_product):
        expected_value = {
            "Compatibility of the products in the environment": {
                "RetVal": "PASS",
                "Value": {
                    "name-version": {
                        "Message": "Installed version of LevelZero not compatible with the version of the name.",  # noqa: E501
                        "RetVal": "FAIL",
                        "Value": "No"
                    }
                }
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {"name": "version"},
            {"LevelZero": "1.0.19310", "OpenCL™": "21.11.19310"},
            False,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._get_compatibilities_for_product", side_effect=[{}])  # noqa: E501
    def test__check_compatibilities_empty_dep_positive(self, mocked__get_compatibilities_for_product):
        expected_value = {
            "Compatibility of the installed products": {
                "RetVal": "PASS",
                "Value": {
                    "name-version": {
                        "Message": "There is no information about name compatibilities. "
                                   "To get the latest version of oneAPI products, visit https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation.html.",  # noqa: E501,
                        "RetVal": "WARNING",
                        "Value": "Undefined"
                    }
                }
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {"name": "version"},
            {"LevelZero": "1.0.19310", "OpenCL™": "21.11.19310"},
            True,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    def test__check_compatibilities_empty_drivers_positive(self):
        expected_value = {
            "Compatibility of the installed products": {
                "Message": "There is no information about GPU driver(s).",
                "RetVal": "WARNING",
                "Value": {}
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {"name": "version"},
            {},
            True,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    def test__check_compatibilities_empty_product_positive(self):
        expected_value = {
            "Compatibility of the installed products": {
                "Message": "There are no products detected.",
                "RetVal": "WARNING",
                "Value": {}
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {},
            {"name": "version"},
            True,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.driver_compatibility_checker._get_compatibilities_for_product",
           side_effect=ValueError("Error"))
    def test__check_compatibilities_error_positive(self, mocked__get_compatibilities_for_product):
        expected_value = {
            "Compatibility of the installed products": {
                "Message": "Error",
                "RetVal": "ERROR",
                "Value": {},
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        real_value = {}
        driver_compatibility_checker._check_compatibilities(
            real_value,
            {"product_name": "product_version"},
            {"driver_name": "driver_version"},
            True,
            "cursor"
        )

        self.assertEqual(real_value, expected_value)

    @patch("sqlite3.connect")
    @patch("checkers_py.linux.driver_compatibility_checker._is_latest_version", side_effect=[True, True])
    @patch("checkers_py.linux.driver_compatibility_checker._is_regression", side_effect=[False, False])
    @patch("checkers_py.linux.driver_compatibility_checker._get_compatibilities_for_product", side_effect=[{"Intel® oneAPI Level Zero": "1.0.19310", "OpenCL™": "21.11.19310"}]*3)  # noqa: E501
    def test_check_compatibilities_positive(
            self,
            moked__get_compatibilities_for_product,
            moked__is_regression,
            mocked__is_latest_version,
            mocked_connect):
        expected_value = {
            "oneAPI products compatibilities with drivers": {
                "Value": {
                    "GPU drivers information": {
                        "Value": {
                            "Intel® oneAPI Level Zero": {
                                "Value": {
                                    "Version": {
                                        "Value": "1.0.19310",
                                        "RetVal": "INFO"
                                    },
                                    "Regression": {
                                        "Value": 'No',
                                        "RetVal": 'PASS'
                                    }
                                },
                                "RetVal": "INFO"
                            },
                            "OpenCL™": {
                                'Value': {
                                    'Version': {
                                        'Value': '21.11.19310',
                                        'RetVal': 'INFO'
                                    },
                                    'Regression': {
                                        'Value': 'No',
                                        'RetVal': 'PASS'
                                    }
                                },
                                'RetVal': 'INFO'
                            }
                        },
                        'RetVal': 'INFO'
                    },
                    'Compatibility of the installed products': {
                        'Value': {
                            'Intel® Advisor-2021.4.0': {
                                'Value': 'Yes',
                                'RetVal': 'PASS'
                            },
                            'Intel® Cluster Checker-2021.3.0': {
                                'Value': 'Yes',
                                'RetVal': 'PASS'
                            }
                        },
                        'RetVal': 'PASS'
                    },
                    'Compatibility of the products in the environment': {
                        'Value': {
                            'Intel® oneAPI Compiler-2021.4.0': {
                                'Value': 'Yes',
                                'RetVal': 'PASS'
                            }
                        },
                        'RetVal': 'PASS'
                    }
                },
                'RetVal': 'PASS'
            }
        }

        real_value = {}
        metadata = '''{
            "resources": [
                "https://iotdk.intel.com/diagnostics/databases"
            ],
            "databases": {
                "compatibility": [
                    {
                        "name": "compatibility_map_02022022.db",
                        "installation_name": "compatibility_map.db",
                        "version": "2022.1.2",
                        "date_of_creation": "02022022",
                        "compatibility": {
                            "driver_compatibility_check": [
                                1
                            ]
                        },
                        "hash": "ffe711b687b6732c637cd2f2306b5fb5a9381bc924518e014aa4741fb16c2a02c9b282bad96385244ba8ee0a3e18c7ea"
                    }
                ]
            }
        }'''  # noqa: E501
        with patch("builtins.open", mock_open(read_data=metadata)):
            driver_compatibility_checker.check_compatibilities(real_value, self.data)

        self.assertEqual(real_value, expected_value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
