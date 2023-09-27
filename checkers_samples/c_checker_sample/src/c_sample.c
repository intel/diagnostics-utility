/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "checker_list_interface.h"
#include "checker_interface.h"

#include <stdio.h>
#include <string.h>

#define API_VERSION "0.2"

#define SOME_JSON \
    "{\"CheckResult\": {\"GPU (OpenCL™ Vendors)\": {\"CheckResult\": {\"Intel\": {\"CheckResult\": {\"OpenCL2.0\": {\"CheckResult\": \"test\", \"Verbosity\": 2, \"Message\": \"\", \"CheckStatus\": \"PASS\" }, \"OpenCL1.2\": {\"CheckResult\": \"test\", \"Verbosity\": 2, \"Message\": \"Please do something\", \"CheckStatus\": \"ERROR\" }}, \"Verbosity\": 1, \"Message\": \"\", \"CheckStatus\": \"PASS\" }, \"AMD\": {\"CheckResult\": {\"OpenCL1.0\": {\"CheckResult\": \"test\", \"Verbosity\": 1, \"Message\": \"\", \"CheckStatus\": \"PASS\" }}, \"Verbosity\": 1, \"Message\": \"\", \"CheckStatus\": \"PASS\" }}, \"CheckStatus\": \"PASS\", \"Verbosity\": 0, \"Message\": \"\" }, \"Test1\": {\"CheckResult\": \"test\", \"Message\": \"\", \"CheckStatus\": \"PASS\" }}}"

char some_result[1024 * 100];
char api_version[MAX_STRING_LEN];

struct CheckResult sample_func(char *data)
{
    sprintf(some_result, "%s", SOME_JSON);

    struct CheckResult ret = {.result = some_result};

    return ret;
}

int main()
{
    printf("%s", SOME_JSON);
    return 0;
}

REGISTER_CHECKER(c_sample,
                 "c_check_sample",
                 "GetData",
                 "sample,c",
                 "This is an sample of c/cpp module.",
                 "{}",
                 0,
                 10,
                 2,
                 sample_func)

static struct Check *checkers[] =
    {&c_sample, NULL};

EXPORT_API char *get_api_version(void)
{
    sprintf(api_version, "%s", API_VERSION);
    return api_version;
}

EXPORT_API struct Check **get_check_list(void)
{
    return checkers;
}
