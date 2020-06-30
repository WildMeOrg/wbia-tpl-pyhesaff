add_custom_target(tests)

add_dependencies(test tests)

set(EXECUTABLE_OUTPUT_PATH ${TEST_OUTPUT_PATH})

# ---------- pyunit tests --------------
if(BUILD_PYTHON_BINDINGS)
  pyhesaff_add_pyunit(test_pyhesaff.py)
  pyhesaff_add_pyunit(test_pyhesaff_simple_parallel.py)
  pyhesaff_add_pyunit(test_pyhesaff_simple_iterative.py)
  pyhesaff_add_pyunit(test_patch_orientation.py)
  pyhesaff_add_pyunit(test_exhaustive_ori_extract.py)
  pyhesaff_add_pyunit(test_ellipse.py)
  pyhesaff_add_pyunit(test_draw_keypoint.py)
  pyhesaff_add_pyunit(test_cpp_rotation_invariance.py)
  pyhesaff_add_pyunit(test_adaptive_scale.py)
  pyhesaff_add_pyunit(pyhestest.py)
endif()
