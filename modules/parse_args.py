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

import argparse

from pathlib import Path


def create_parser(version: str):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Diagnostics Utility for Intel® oneAPI Toolkits is a tool "
                    "designed to diagnose the system status for using Intel® software.",
        epilog=f"Important notes:\n"
               f"\n"
               f"1. The most popular use cases for Utility:\n"
               f" - For GPU diagnostics run 'python3 diagnostics.py --filter gpu'\n"
               f" - To get all information run 'python3 diagnostics.py --filter all'\n"
               f"\n"
               f"2. Check's status explanation:\n"
               f"PASS - the check passed, no further information will be given.\n"
               f"FAILED - check ran successfully and the check found a problem.\n"
               f"   For example if a GPU check is run on a system that does not have a GPU,\n"
               f"   the check will fail. A brief description will indicate why the check failed.\n"
               f"ERROR - check was not able to be run, a brief description will indicate why\n"
               f"   the check was not successful\n"
               f"WARNING - check ran successfully and but found incompatible or incorrect information.\n"
               f"   A brief description will indicate why.\n"
               f"\n"
               f"3. Basic rules how to interpret results:\n"
               f"   - Each category of checks contains multiple checks with different level of details.\n"
               f"   Please go throw all checks and analyze all failures before make decision what is wrong.\n"
               f"   Some checks may report that cannot get some information only, some checks provide\n"
               f"   diagnostics what wrong. There is no order or dependencies for these checks yet. \n"
               f"   Please, read all failures\\infos and combine it in one bird eye view\n"
               f"   - Output may have different format in case of using verbose mode\n"
               f"   (with -v or without the parameter). Both variants may be useful.\n"
               f"\n"
               f"4. For more details see online documentation:\n"
               f"   https://software.intel.com/content/www/us/en/develop/documentation/diagnostic-utility-user-guide/top.html\n"  # noqa: E501
               f"\n"
               f"Diagnostics Utility for Intel® oneAPI Toolkits {version}\n"
               f"Copyright (C) Intel Corporation. All rights reserved.",
        add_help=False
    )
    group_check_run = parser.add_mutually_exclusive_group()
    group_output_format = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "--filter",
        nargs="+",
        type=str,
        default=["not_initialized"],
        help="Filter checker results by tag or checker name\n"
             "tags, combine one or more checkers into groups.\n"
             "Each checker can be marked with one or more tags.\n"
             "To view all available checkers with their names and marked tags,\n"
             "run the Diagnostics Utility for Intel® oneAPI Toolkits\n"
             "with the \"--list\" option."
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="Show list of available checks."
    )
    group_check_run.add_argument(
        "-c", "--config",
        type=Path,
        metavar="PATH_TO_CONFIG",
        help="Path to the JSON config file to run a group of checks or particular check from checkers."
    )
    group_check_run.add_argument(
        "-s", "--single_checker",
        type=Path,
        metavar="PATH_TO_CHECKER",
        help="Path to the checker module file which can be a library, python module, or executable bash."
    )
    group_output_format.add_argument(
        "-o", "--output",
        type=Path,
        metavar="PATH_TO_OUTPUT",
        default=f"{Path.home()}/intel/diagnostics/logs",
        help="Path to the folder for saving the console output file and\n"
             "the JSON file with the results of the performed checks.\n"
             "(default: $HOME/intel/diagnostics/logs)"
    )
    group_output_format.add_argument(
        "-t", "--terminal_output",
        action="store_true",
        help="Allow output only to the terminal window without saving additional output files."
    )
    parser.add_argument(
        "-u", "--update",
        action="store_true",
        help="Download new databases if they are available."
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force the program to run on any operating system.")
    parser.add_argument(
        "-v", "--verbosity",
        action="count",
        help="Increase output verbosity. By default tool prints\n"
        "FAILUREs and ERRORs only. Use -v for get more details.\n"
        "Add additional v (like -vvvv) for next level of details",
        default=-1
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit.",
        default=argparse.SUPPRESS)
    return parser
