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

set(COMMON_LIB_NAME checkers_c_common)
  
aux_source_directory(src COMMON_SRC)

add_library(${COMMON_LIB_NAME} SHARED ${COMMON_SRC})
target_include_directories(${COMMON_LIB_NAME} PRIVATE include)
target_link_libraries(${COMMON_LIB_NAME} json-c-static)

if(BUILD_TESTS)
  aux_source_directory(tests TEST_SRC)
  add_executable(test_common ${TEST_SRC})
  target_include_directories(test_common PRIVATE include)
  target_link_libraries(test_common PRIVATE
      gtest
      gtest_main
      gmock
      gmock_main
      ${COMMON_LIB_NAME}
    )
  gtest_discover_tests(test_common)
  install(TARGETS test_common DESTINATION ${SOURCES_INSTALL_PREFIX}/tests/unittests)
endif()
