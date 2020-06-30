set(PKG_DESC "Image Tools for Wildbook IA")
set(pkg_conf_file ${CMAKE_CURRENT_BINARY_DIR}/pyhesaff.pc)
configure_file(pyhesaff.pc.in ${pkg_conf_file} @ONLY)
install(
  FILES ${pkg_conf_file}
  DESTINATION ${HESAFF_LIB_INSTALL_DIR}/pkgconfig/
  COMPONENT pkgconfig)
