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

import sys
import os
import platform

from pathlib import Path
from typing import Dict, List, Optional

from modules.check import BaseCheck, CheckMetadataPy, load_checks_from_config, load_default_checks, \
                          load_checks_from_env, run_checks, create_dependency_order
from modules.db_downloader import are_database_updates_available, update_databases, print_available_updates
from modules.files_helper import configure_output_files, get_checks_to_run_from_config_data, \
                                 read_config_data, save_json_output_file
from modules.filter import process_filter, get_filtered_checks
from modules.os_helper import check_that_os_is_supported
from modules.parse_args import create_parser
from modules.log import configure_logger, configure_file_logging

from modules.printing import print_metadata, print_summary, print_epilog
from modules.printing.printer import print_ex, enable_stdout_printing

VERSION = "2022.2"
API_VERSION = "0.1"


def main():
    # Parse command line arguments
    parser = create_parser(VERSION)
    args = parser.parse_args()
    # Disable printing to STDOUT
    if args.json:
        enable_stdout_printing(False)
    # Check that OS is supported
    if not args.force:
        check_that_os_is_supported()

    # Configure environment
    if args.path:
        sep = ";" if platform.system() == "Windows" else ":"
        DIAGUTIL_PATH_ENV = os.getenv("DIAGUTIL_PATH")
        os.environ["DIAGUTIL_PATH"] = f"{sep.join(args.path)}{sep}{DIAGUTIL_PATH_ENV}" if DIAGUTIL_PATH_ENV \
            else sep.join(args.path)

    # Configure logger
    configure_logger(args.verbosity)

    # Configure output files
    txt_output_file: Optional[Path] = None
    json_output_file: Optional[Path] = None
    if not args.terminal_output:
        txt_output_file, json_output_file = configure_output_files(args)

    # Configure file logging
    if txt_output_file is not None:
        configure_file_logging(args.verbosity, txt_output_file)

    # Load checks from default storage, environment and config
    loaded_checks_map: Dict[Path, CheckMetadataPy] = {}
    loaded_checks: List[BaseCheck] = []

    loaded_checks.extend(load_default_checks(API_VERSION, loaded_checks_map))
    loaded_checks.extend(load_checks_from_env(API_VERSION, loaded_checks_map))
    if args.config:  # Load checks from config
        loaded_checks.extend(load_checks_from_config(args.config, API_VERSION, loaded_checks_map))

    checks_paths = list(loaded_checks_map.keys())
    checks_metadate = list(loaded_checks_map.values())
    for index, metadata in enumerate(checks_metadate):
        the_same_name_checks_metadate = [
            checks_metadate[i]
            for i in range(index+1, len(checks_metadate))
            if checks_metadate[i].name == metadata.name
        ]
        if len(the_same_name_checks_metadate) > 0:
            print_ex(f"Several checks of the same {metadata.name} name was loaded:", txt_output_file)
            print_ex(f"on path {checks_paths[checks_metadate.index(metadata)]} with version  \
                     {metadata.version}", txt_output_file)
            for m in the_same_name_checks_metadate:
                print_ex(f"on path {checks_paths[checks_metadate.index(m)]} with version {m.version}",
                         txt_output_file)
            exit(1)

    # If checks we not specified, tool should say that it runs with limited set pf checks
    is_filter_not_initialized = len(args.filter) == 1 and args.filter[0] == "not_initialized"
    if not args.list and is_filter_not_initialized and not args.config and not args.update:
        print_ex("Default checks will be run. For information on how to run other checks, "
                 "see 'python3 diagnostics.py --help'", txt_output_file)
        print_ex("", txt_output_file)

    # --list argument processing
    if args.list:
        # Get checks to print
        checks_to_print: List[BaseCheck] = get_filtered_checks(loaded_checks, args.filter) \
            if not is_filter_not_initialized else loaded_checks
        # Print checks metadata
        print_metadata(checks_to_print, txt_output_file)
        print_epilog(txt_output_file, None, VERSION)
        exit(0)

    # Check DB updates
    if not args.skip_update:
        print_ex("Checking for available updates of compatibility database...", txt_output_file)
        resource, metadata, databases = are_database_updates_available(loaded_checks)
        print_ex("Checking for available updates completed successfully.", txt_output_file)
        if args.update:
            exit(update_databases(resource, metadata, databases))
        else:
            print_available_updates(databases)
            print_ex("", txt_output_file)

    # Filter processing: Run all checks from config or set default filter if it is not initialized
    filter = set()
    if args.config:
        config_data = read_config_data(args.config)
        filter = get_checks_to_run_from_config_data(config_data)
    else:
        filter = process_filter(args.filter)

    # Select the checks to run in right order
    checks_to_print, checks_to_run = create_dependency_order(loaded_checks, filter)
    if len(checks_to_print) != len(checks_to_run):
        checks_to_run_without_print = " ".join(
            set([check.get_metadata().name for check in checks_to_run]) - set(checks_to_print))
        print_ex("Some checks have dependencies that are not on the list of checks to run.", txt_output_file)
        print_ex(f"The following checks will run, but will not be displayed: {checks_to_run_without_print}",
                 txt_output_file)
        print_ex("", txt_output_file)

    # Run selected checks
    run_checks(checks_to_run)

    # Print results to user
    print_summary(get_filtered_checks(checks_to_run, checks_to_print), args.verbosity, txt_output_file)

    if json_output_file and txt_output_file:
        save_json_output_file(checks_to_run, json_output_file, False)

    print_epilog(txt_output_file, json_output_file, VERSION)

    # Print json onto STDOUT
    if args.json:
        save_json_output_file(checks_to_run, None, True)


if __name__ == "__main__":
    sys.exit(main())
