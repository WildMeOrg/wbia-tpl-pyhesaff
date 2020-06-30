# ##############################################################################
# Find PyHesaff
#
# This sets the following variables: PYHESAFF_FOUND - True if PyHesaff was
# found. PYHESAFF_INCLUDE_DIRS - Directories containing the PyHesaff include
# files. PYHESAFF_LIBRARIES - Libraries needed to use PyHesaff.
# PYHESAFF_DEFINITIONS - Compiler flags for PyHesaff.

find_package(PkgConfig)
pkg_check_modules(PC_PYHESAFF pyhesaff)
set(PYHESAFF_DEFINITIONS ${PC_PYHESAFF_CFLAGS_OTHER})

find_path(PYHESAFF_INCLUDE_DIR pyhesaff/pyhesaff.hpp
          HINTS ${PC_PYHESAFF_INCLUDEDIR} ${PC_PYHESAFF_INCLUDE_DIRS})

find_library(PYHESAFF_LIBRARY pyhesaff HINTS ${PC_PYHESAFF_LIBDIR}
                                             ${PC_PYHESAFF_LIBRARY_DIRS})

set(PYHESAFF_INCLUDE_DIRS ${PYHESAFF_INCLUDE_DIR})
set(PYHESAFF_LIBRARIES ${PYHESAFF_LIBRARY})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(PyHesaff DEFAULT_MSG PYHESAFF_LIBRARY
                                  PYHESAFF_INCLUDE_DIR)

mark_as_advanced(PYHESAFF_LIBRARY PYHESAFF_INCLUDE_DIR)
