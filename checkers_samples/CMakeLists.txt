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

add_subdirectory(c_checker_sample)

install(DIRECTORY py_checkers_samples/
    DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_samples
    USE_SOURCE_PERMISSIONS
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
  )

install(DIRECTORY exe_checkers_samples/${OS}/
    DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_samples
    USE_SOURCE_PERMISSIONS
    PATTERN ".gitkeep" EXCLUDE
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
  )
