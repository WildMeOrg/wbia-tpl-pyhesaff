#include_directories(${CMAKE_SOURCE_DIR}/include algorithms ext util nn .)

message(STATUS "HESAFF_CHECKPOINT = TRUE")

message(STATUS "PYHESAFF_VERSION = ${PYHESAFF_VERSION}")
set(HESAFF_VERSION ${PYHESAFF_VERSION})
message(STATUS "HESAFF_VERSION = ${HESAFF_VERSION}")
add_definitions(-D_PYHESAFF_VERSION=${PYHESAFF_VERSION})
add_definitions(-DPYHESAFF_VERSION_=${PYHESAFF_VERSION})
add_definitions(-DPYHESAFF_VERSION=${PYHESAFF_VERSION})
add_definitions(-D_HESAFF_VERSION=${HESAFF_VERSION})
add_definitions(-DHESAFF_VERSION_=${HESAFF_VERSION})
add_definitions(-DHESAFF_VERSION=${HESAFF_VERSION})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/hesaff/config.h.in ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/config.h)

set(CPP_SOURCES 
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/hesaff.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/pyramid.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/helpers.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/affine.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/orientation.cpp
    # ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/python_bindings.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/hesaff/siftdesc.cpp)

add_library(pyhesaff_s STATIC ${CPP_SOURCES})
target_link_libraries(pyhesaff_s ${OpenCV_LIBRARIES})

if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_CLANG)
    set_target_properties(pyhesaff_s PROPERTIES COMPILE_FLAGS -fPIC)
endif()
set_property(TARGET pyhesaff_s PROPERTY COMPILE_DEFINITIONS HESAFF_STATIC)

if(CMAKE_SYSTEM_NAME STREQUAL "Linux" AND CMAKE_COMPILER_IS_GNUCC)
    set_target_properties(pyhesaff PROPERTIES LINKER_LANGUAGE CXX)
    target_link_libraries(pyhesaff -Wl,-whole-archive pyhesaff_s -Wl,-no-whole-archive)
else()
    add_library(pyhesaff SHARED ${CPP_SOURCES})
    target_link_libraries(pyhesaff ${OpenCV_LIBRARIES})
    set_target_properties(pyhesaff PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS YES)
endif()

set_target_properties(pyhesaff PROPERTIES
   VERSION ${PYHESAFF_VERSION}
   SOVERSION ${HESAFF_SOVERSION}
   DEFINE_SYMBOL HESAFF_EXPORTS
)

if(NOT SKBUILD)
    # Skip this part if running via setup.py

    install (
        TARGETS pyhesaff pyhesaff_s
        EXPORT ${targets_export_name}
        INCLUDES DESTINATION include
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION ${HESAFF_LIB_INSTALL_DIR}
        ARCHIVE DESTINATION ${HESAFF_LIB_INSTALL_DIR}
    )

    install (
        DIRECTORY pyhesaff
        DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
    )

else()
    # Only install the library files when building with skbuild
    install (
        TARGETS pyhesaff pyhesaff_s
        EXPORT ${targets_export_name}
        LIBRARY DESTINATION ${HESAFF_LIB_INSTALL_DIR}
        ARCHIVE DESTINATION ${HESAFF_LIB_INSTALL_DIR}
    )
endif()
