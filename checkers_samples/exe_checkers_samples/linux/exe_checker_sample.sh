#!/bin/bash
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

METADATA=0
SUMMARY=0
API=0

function parse_args() {
    if [[ "$#" != 1 ]]; then
		exit 1
    else
        if [[ "$1" == "--get_metadata" ]]; then
			METADATA=1
        elif [[ "$1" == "--get_summary" ]]; then
			SUMMARY=1
        elif [[ "$1" == "--get_api_version" ]]; then
			API=1
        else
            exit 1
        fi
	fi

}

function run() {
    echo "Run check"
}

function get_metadata() {
    echo '{"name": "exe_check_sample","type": "Data","tags": "sample,exe","descr": "This is a sample of the exe module","dataReq": "{}","merit": 0,"timeout": 1,"version": 1,"run": ""}'
}

function get_summary() {
    #run
    echo '{"result": "{\"Value\": {\"Exe sample check\": {\"RetVal\": \"PASS\",\"Value\": \"Exe sample value\"}}}"}'
}

function get_api_version() {
    #run
    echo "0.1"
}

parse_args $@
if [[ $METADATA == 1 ]]; then
    get_metadata
elif [[ $SUMMARY == 1 ]]; then
    get_summary
elif [[ $API == 1 ]]; then
    get_api_version
fi
