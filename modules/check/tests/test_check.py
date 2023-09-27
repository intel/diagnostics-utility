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
from copy import deepcopy  # noqa: E402

import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

from modules.check.check import BaseCheck, CheckMetadataPy, CheckSummary, _result_summary_is_correct, \
                                 check_correct_metadata, check_correct_summary  # noqa: E402


correct_result_dict_1 = {
    "CheckResult": {
        "Check1": {
            "CheckResult": "CheckValue1",
            "Verbosity": 0,
            "CheckStatus": "PASS"
        },
        "Check2": {
            "CheckResult": "CheckValue12",
            "Verbosity": 0,
            "CheckStatus": "PASS"
        }
    }
}

correct_result_dict_2 = {
    "CheckResult": {
        "Check1": {
            "Verbosity": 0,
            "Message": "Message is not required filed",
            "CheckStatus": "PASS",
            "CheckResult": {
                "Subcheck1": {
                    "Verbosity": 1,
                    "Command": "Command is not required filed",
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "PASS"
                },
                "Subcheck2": {
                    "Verbosity": 2,
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "PASS"
                }
            }
        },
        "Check2": {
            "CheckStatus": "PASS",
            "CheckResult": {
                "Subcheck1": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "PASS"
                },
                "Subcheck2": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "PASS"
                }
            }
        }
    }
}

correct_result_dict_3 = {
    "CheckResult": {
        "Check1": {
            "CheckResult": 1,
            "CheckStatus": "PASS"
        },
        "Check2": {
            "CheckResult": None,
            "CheckStatus": "PASS"
        }
    }
}

correct_result_dict_4 = {
    "CheckResult": {
        "Check1": {
            "CheckResult": 1,
            "CheckStatus": "WARNING"
        },
        "Check2": {
            "CheckResult": None,
            "CheckStatus": "PASS"
        }
    }
}

correct_result_dict_5 = {
    "CheckResult": {
        "Check1": {
            "CheckResult": 1,
            "CheckStatus": "FAIL"
        },
        "Check2": {
            "CheckResult": None,
            "CheckStatus": "PASS"
        }
    }
}

correct_result_dict_6 = {
    "CheckResult": {
        "Check1": {
            "CheckResult": 1,
            "CheckStatus": "ERROR"
        },
        "Check2": {
            "CheckResult": None,
            "CheckStatus": "PASS"
        }
    }
}

correct_result_dict_7 = {
    "CheckResult": {
        "Check1": {
            "CheckStatus": "PASS",
            "CheckResult": {
                "Subcheck1": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "WARNING"
                }
            }
        }
    }
}

correct_result_dict_8 = {
    "CheckResult": {
        "Check1": {
            "CheckStatus": "PASS",
            "CheckResult": {
                "Subcheck1": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "FAIL"
                }
            }
        }
    }
}

correct_result_dict_9 = {
    "CheckResult": {
        "Check1": {
            "CheckStatus": "PASS",
            "CheckResult": {
                "Subcheck1": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "ERROR"
                }
            }
        }
    }
}

correct_result_dict_10 = {
    "CheckResult": {
        "Check1": {
            "CheckStatus": "FAIL",
            "CheckResult": {
                "Subcheck1": {
                    "CheckResult": "SubcheckValue1",
                    "CheckStatus": "ERROR"
                }
            }
        }
    }
}

incorrect_dict_with_wrong_root_verbosity = {
    "CheckResult": {
        "Check1": {
            "Verbosity": 1,
            "CheckResult": "CheckValue1",
            "CheckStatus": "PASS"
        },
    }
}

incorrect_dict_with_wrong_message = {
    "CheckResult": {
        "Check1": {
            "Message": {},
            "CheckResult": "CheckValue1",
            "CheckStatus": "PASS"
        },
    }
}

incorrect_dict_with_wrong_command = {
    "CheckResult": {
        "Check1": {
            "Command": {},
            "CheckResult": "CheckValue1",
            "CheckStatus": "PASS"
        },
    }
}

incorrect_dict_without_check_value = {
    "CheckResult": {
        "Check1": {
            "CheckStatus": "PASS"
        },
    }
}

incorrect_dict_with_wrong_return_value = {
    "CheckResult": {
        "Check1": {
            "CheckResult": "CheckValue1",
            "CheckStatus": "DONE"
        },
    }
}


incorrect_dict_with_wrong_verbosity = {
    "CheckResult": {
        "Check1": {
            "Verbosity": "1",
            "CheckResult": "CheckValue1",
            "CheckStatus": "PASS"
        },
    }
}


incorrect_dict_with_wrong_message = {
    "CheckResult": {
        "Check1": {
            "Message": 0,
            "CheckResult": "CheckValue1",
            "CheckStatus": "PASS"
        },
    }
}

wrong_check_1 = {
    "NotCheck_Result": {
        "CheckResult": {
            "Check1": {
                "CheckResult": "CheckValue1"
            }
        }
    }
}

wrong_check_2 = {
    "CheckResult": {
        "CheckResult": {
            "Check1": {
                "CheckResult": "CheckValue1"
            }
        }
    }
}

wrong_check_3 = {
    "CheckResult": {
        "Check1": {
            "SubCheck1": {
                "CheckResult": "SubCheckValue1"
            }
        }
    }
}

wrong_check_4 = {
    "CheckResult": {
        "Check1": "CheckValue1"
    }
}

wrong_check_5 = {
    "CheckResult": {
        "Check1": "CheckValue1"
    }
}


class TestResultSummury(unittest.TestCase):

    def test_no_error_with_correct_dict_without_recursive_call(self):
        _result_summary_is_correct(correct_result_dict_1)

    def test_no_error_with_correct_dict_with_recursive_call(self):
        _result_summary_is_correct(correct_result_dict_2)

    def test_no_error_with_correct_dict_3(self):
        _result_summary_is_correct(correct_result_dict_3)

    def test_raise_error_when_data_is_empty(self):
        self.assertRaises(ValueError, _result_summary_is_correct, {})

    def test_raise_error_when_root_verbosity_is_not_zero(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_root_verbosity)

    def test_raise_error_when_message_is_not_string(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_message)

    def test_raise_error_when_command_is_not_string(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_command)

    def test_raise_error_when_dict_do_not_have_check_value(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_without_check_value)

    def test_raise_error_when_return_value_is_wrong(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_return_value)

    def test_raise_error_when_verbosity_is_not_int(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_verbosity)

    def test_raise_error_when_message_is_not_int(self):
        self.assertRaises(ValueError, _result_summary_is_correct, incorrect_dict_with_wrong_message)

    def test_raise_error_when_check_data_is_wrong_1(self):
        self.assertRaises(ValueError, _result_summary_is_correct, wrong_check_1)

    def test_raise_error_when_check_data_is_wrong_2(self):
        self.assertRaises(ValueError, _result_summary_is_correct, wrong_check_2)

    def test_raise_error_when_check_data_is_wrong_3(self):
        self.assertRaises(ValueError, _result_summary_is_correct, wrong_check_3)

    def test_raise_error_when_check_data_is_wrong_4(self):
        self.assertRaises(ValueError, _result_summary_is_correct, wrong_check_4)

    def test_raise_error_when_check_data_is_wrong_5(self):
        self.assertRaises(ValueError, _result_summary_is_correct, wrong_check_5)

    def test_no_error_init_check_summary_with_correct_data_check_pass(self):
        expected_error_code = 0

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_1)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_check_warning(self):
        expected_error_code = 1

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_4)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_check_fail(self):
        expected_error_code = 2

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_5)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_check_error(self):
        expected_error_code = 3

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_6)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_warning_rewrite_pass(self):
        expected_error_code = 1

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_7)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_fail_rewrite_pass(self):
        expected_error_code = 2

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_8)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_error_rewrite_pass(self):
        expected_error_code = 3

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_9)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_no_error_init_check_summary_with_correct_data_error_rewrite_fail(self):
        expected_error_code = 3

        actual = CheckSummary(
            result=json.dumps(correct_result_dict_10)
        )

        self.assertEqual(expected_error_code, actual.error_code)

    def test_raise_error_init_check_summary_with_incorrect_data(self):
        with self.assertRaises(ValueError):
            CheckSummary(
                result=json.dumps(wrong_check_1)
            )

    def test_check_summary_decorator_no_error(self):
        class temp:
            result = None

            def func(self):
                self.result = json.dumps(correct_result_dict_1)
                return self

        obj = temp()
        check_correct_summary(temp.func)(obj)

    def test_check_summary_decorator_raise_error(self):
        class temp:
            result = None

            def func(self):
                self.result = json.dumps(wrong_check_1)
                return self

        obj = temp()
        with self.assertRaises(ValueError):
            check_correct_summary(temp.func)(obj)


class TestCheckMetadataPy(unittest.TestCase):

    def test_no_error_init_check_metadata_with_correct_data(self):
        CheckMetadataPy(
            name='example',
            type='data',
            groups='group',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

    def test_no_error_init_check_metadata_with_correct_right_admin(self):
        CheckMetadataPy(
            name='example',
            type='data',
            groups='group',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

    def test_no_error_init_check_metadata_with_correct_two_groups(self):
        CheckMetadataPy(
            name='example',
            type='data',
            groups='group1,group2',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

    def test_no_error_init_check_metadata_with_correct_two_groups_with_space_after_comma(self):
        CheckMetadataPy(
            name='example',
            type='data',
            groups='group1,group2',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

    def test_raise_error_init_check_metadata_with_incorrect_datareq(self):
        with self.assertRaises(ValueError):
            CheckMetadataPy(
                name='example',
                type='data',
                groups='group',
                descr='decription',
                dataReq='not_json_data',
                merit=0,
                timeout=1,
                version=2,
                run='run'
            )

    def test_raise_error_init_check_metadata_with_incorrect_name(self):
        with self.assertRaises(ValueError):
            CheckMetadataPy(
                name='name with spaces',
                type='data',
                groups='group',
                descr='decription',
                dataReq='{}',
                merit=0,
                timeout=1,
                version=2,
                run='run'
            )

    def test_raise_error_init_check_metadata_with_incorrect_group(self):
        with self.assertRaises(ValueError):
            CheckMetadataPy(
                name='example',
                type='data',
                groups='group with spaces',
                descr='decription',
                dataReq='{}',
                merit=0,
                timeout=1,
                version=2,
                run='run'
            )

    def test_check_metadata_decorator_with_correct_data(self):
        class temp:
            self.metadata = None

            def func(self):
                self.metadata = CheckMetadataPy(
                    name='example',
                    type='data',
                    groups='group',
                    descr='decription',
                    dataReq='{}',
                    merit=0,
                    timeout=1,
                    version=2,
                    run='run'
                )

        obj = temp()
        check_correct_metadata(temp.func)(obj)

    def test_check_metadata_decorator_with_incorrect_datareq(self):
        class temp:
            self.metadata = None

            def func(self):
                self.metadata = CheckMetadataPy(
                    name='example',
                    type='data',
                    groups='group',
                    descr='decription',
                    dataReq='not_json_data',
                    merit=0,
                    timeout=1,
                    version=2,
                    run='run'
                )

    def test_check_metadata_decorator_with_incorrect_name(self):
        class temp:
            self.metadata = None

            def func(self):
                self.metadata = CheckMetadataPy(
                    name='name with spaces',
                    type='data',
                    groups='group',
                    descr='decription',
                    dataReq='{}',
                    merit=0,
                    timeout=1,
                    version=2,
                    run='run'
                )

        obj = temp()
        with self.assertRaises(ValueError):
            check_correct_metadata(temp.func)(obj)

    def test_check_metadata_decorator_with_incorrect_group(self):
        class temp:
            self.metadata = None

            def func(self):
                self.metadata = CheckMetadataPy(
                    name='example',
                    type='data',
                    groups='group with spaces',
                    descr='decription',
                    dataReq='{}',
                    merit=0,
                    timeout=1,
                    version=2,
                    run='run'
                )

        obj = temp()
        with self.assertRaises(ValueError):
            check_correct_metadata(temp.func)(obj)

    @patch("logging.warning")
    def test_check_metadata_decorator_without_metadata(self, mock_log):
        class temp:
            self.data = None

            def func(self):
                self.data = 1

        obj = temp()
        check_correct_metadata(temp.func)(obj)
        mock_log.assert_called_once()


class TestBaseCheck(unittest.TestCase):

    def setUp(self):
        self.correct_metadata = CheckMetadataPy(
            name='example',
            type='data',
            groups='group',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

        self.correct_summary = CheckSummary(
            result=json.dumps(correct_result_dict_1)
        )

        self.check = BaseCheck(
            metadata=self.correct_metadata,
            summary=self.correct_summary
        )

    def test_base_check_get_metadata_is_correct(self):
        expected = self.correct_metadata

        actual = self.check.get_metadata()

        self.assertEqual(expected, actual)

    def test_base_check_get_summary_is_correct(self):
        expected = self.correct_summary

        actual = self.check.get_summary()

        self.assertEqual(expected, actual)

    def test_base_check_update_metadata_is_correct(self):
        expected = CheckMetadataPy(
            name='updated_example',
            type='data',
            groups='group',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

        temp_check = deepcopy(self.check)
        temp_check.update_metadata({"name": "updated_example", "not_valid_key": ""})
        actual = temp_check.get_metadata()

        self.assertEqual(expected.__dict__, actual.__dict__)


class TestTimeoutDecorator(unittest.TestCase):

    def setUp(self):
        self.correct_metadata = CheckMetadataPy(
            name='example',
            type='data',
            groups='group',
            descr='decription',
            dataReq='{}',
            merit=0,
            timeout=1,
            version=2,
            run='run'
        )

        self.correct_summary = CheckSummary(
            result=json.dumps(correct_result_dict_1)
        )

        self.check = BaseCheck(
            metadata=self.correct_metadata,
            summary=self.correct_summary
        )


if __name__ == '__main__':
    unittest.main()
