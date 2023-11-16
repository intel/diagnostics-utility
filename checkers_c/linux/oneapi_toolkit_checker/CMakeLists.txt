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

set(CHECKERS_LIB_NAME oneapi_toolkit_checker)
  
aux_source_directory(src CHECKERS_SRC)
aux_source_directory(../common/src COMMON_SRC)

add_library(${CHECKERS_LIB_NAME} SHARED ${CHECKERS_SRC} ${COMMON_SRC})
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE include)
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE ../common/include)
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE ../../../include)
target_link_libraries(${CHECKERS_LIB_NAME} json-c-static sqlite3)

install(TARGETS ${CHECKERS_LIB_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_c)

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  set(CHECKERS_EXE_NAME oneapi_toolkit_checker_exe)

  add_executable (${CHECKERS_EXE_NAME} ${CHECKERS_SRC} ${COMMON_SRC})
  target_include_directories(${CHECKERS_EXE_NAME} PRIVATE include)
  target_include_directories(${CHECKERS_EXE_NAME} PRIVATE ../common/include)
  target_include_directories(${CHECKERS_EXE_NAME} PRIVATE ../../../include)
  target_link_libraries(${CHECKERS_EXE_NAME} json-c-static sqlite3)

  install(TARGETS ${CHECKERS_EXE_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_c)
endif()

if(BUILD_TESTS)
  aux_source_directory(tests TEST_SRC)
  add_executable(test_oneapi_toolkit_checker ${TEST_SRC})
  target_include_directories(test_oneapi_toolkit_checker PRIVATE ../../../include)
  target_include_directories(test_oneapi_toolkit_checker PRIVATE ../common/include)
  target_include_directories(test_oneapi_toolkit_checker PRIVATE include)
  target_link_libraries(test_oneapi_toolkit_checker PRIVATE
      gtest
      gtest_main
      gmock
      gmock_main
      ${CHECKERS_LIB_NAME}
    )
  gtest_discover_tests(test_oneapi_toolkit_checker)
  install(TARGETS test_oneapi_toolkit_checker DESTINATION ${SOURCES_INSTALL_PREFIX}/tests/unittests)
endif()
