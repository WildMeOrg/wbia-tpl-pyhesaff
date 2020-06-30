macro(GET_OS_INFO)
  string(REGEX MATCH "Linux" OS_IS_LINUX ${CMAKE_SYSTEM_NAME})
  string(REGEX MATCH "Darwin" OS_IS_MACOS ${CMAKE_SYSTEM_NAME})
  set(HESAFF_LIB_INSTALL_DIR "lib${LIB_SUFFIX}")
  set(HESAFF_INCLUDE_INSTALL_DIR
      "include/${PROJECT_NAME_LOWER}-${PYHESAFF_MAJOR_VERSION}.${PYHESAFF_MINOR_VERSION}"
  )
endmacro(GET_OS_INFO)

macro(DISSECT_VERSION)
  # Find version components
  message(STATUS "PYHESAFF_VERSION = ${PYHESAFF_VERSION}")
  string(REGEX REPLACE "^([0-9]+).*" "\\1" PYHESAFF_VERSION_MAJOR
                       "${PYHESAFF_VERSION}")
  string(REGEX REPLACE "^[0-9]+\\.([0-9]+).*" "\\1" PYHESAFF_VERSION_MINOR
                       "${PYHESAFF_VERSION}")
  string(REGEX REPLACE "^[0-9]+\\.[0-9]+\\.([0-9]+)" "\\1"
                       PYHESAFF_VERSION_PATCH ${PYHESAFF_VERSION})
  string(REGEX REPLACE "^[0-9]+\\.[0-9]+\\.[0-9]+(.*)" "\\1"
                       PYHESAFF_VERSION_CANDIDATE ${PYHESAFF_VERSION})
  set(HESAFF_SOVERSION "${PYHESAFF_VERSION_MAJOR}.${PYHESAFF_VERSION_MINOR}")
  message(STATUS "HESAFF_SOVERSION = ${PYHESAFF_SOVERSION}")
endmacro(DISSECT_VERSION)

macro(pyhesaff_add_pyunit file)
  # find test file
  set(_file_name _file_name-NOTFOUND)
  find_file(_file_name ${file} ${CMAKE_CURRENT_SOURCE_DIR})
  if(NOT _file_name)
    message(FATAL_ERROR "Can't find pyunit file \"${file}\"")
  endif(NOT _file_name)

  # add target for running test
  string(REPLACE "/" "_" _testname ${file})
  add_custom_target(
    pyunit_${_testname}
    COMMAND ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/bin/run_test.py
            ${_file_name}
    DEPENDS ${_file_name}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/test
    VERBATIM
    COMMENT "Running pyunit test(s) ${file}")
  # add dependency to 'test' target
  add_dependencies(pyunit_${_testname} pyhesaff)
  add_dependencies(test pyunit_${_testname})
endmacro(pyhesaff_add_pyunit)
