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

set(CHECKERS_LIB_NAME c_checker_sample)

AUX_SOURCE_DIRECTORY(src CHECKERS_SRC)

add_library(${CHECKERS_LIB_NAME} SHARED ${CHECKERS_SRC})
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE ../../include)

if(${OS} STREQUAL "windows")
  install(TARGETS ${CHECKERS_LIB_NAME} RUNTIME DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_samples)
else()
  install(TARGETS ${CHECKERS_LIB_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_samples)
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  set(CHECKERS_EXE_NAME c_checker_sample_exe)

  add_executable (${CHECKERS_EXE_NAME} ${CHECKERS_SRC})
  target_include_directories(${CHECKERS_EXE_NAME} PRIVATE ../../include)

  install(TARGETS ${CHECKERS_EXE_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_samples)
endif()

if(BUILD_TESTS)
  add_executable(test_c_sample
      tests/test_c_sample.cpp
    )
  target_include_directories(test_c_sample PRIVATE ../../include)
  target_link_libraries(test_c_sample PRIVATE
      gtest
      gtest_main
      gmock
      gmock_main
      ${CHECKERS_LIB_NAME}
    )
  gtest_discover_tests(test_c_sample)
  install(TARGETS test_c_sample DESTINATION ${SOURCES_INSTALL_PREFIX}/tests/unittests)
endif()
