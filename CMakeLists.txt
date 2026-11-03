cmake_minimum_required(VERSION 3.15)
project(x2camf_c LANGUAGES C)

# BLAS/LAPACK: pass BLAS_LIBRARIES (and LAPACK_LIBRARIES, if separate) to use
# a given library, e.g. -DBLAS_LIBRARIES=mkl_rt, as pyscf/lib does; otherwise
# FindBLAS/FindLAPACK (BLA_VENDOR selects the vendor).
# Numerically unsafe flags (-ffast-math) are avoided to keep agreement with
# the C++/Eigen implementation.

option(ENABLE_OPENMP "Compile with OpenMP" ON)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_C_FLAGS_RELEASE "-O3 -funroll-loops")

set(_blas_user_provided TRUE)
if(NOT BLAS_LIBRARIES)
  set(_blas_user_provided FALSE)
  find_package(BLAS REQUIRED)
endif()
if(NOT LAPACK_LIBRARIES)
  if(_blas_user_provided)
    # a user-supplied BLAS (mkl_rt, OpenBLAS) also provides LAPACK
    set(LAPACK_LIBRARIES "")
  else()
    find_package(LAPACK REQUIRED)
  endif()
endif()
message(STATUS "BLAS libraries: ${BLAS_LIBRARIES}")
message(STATUS "LAPACK libraries: ${LAPACK_LIBRARIES}")

add_library(x2camf_c SHARED
  csrc/x2c_mat.c
  csrc/x2c_general.c
  csrc/x2c_int_sph_basic.c
  csrc/x2c_int_sph.c
  csrc/x2c_int_sph_gaunt.c
  csrc/x2c_int_sph_gauge.c
  csrc/x2c_dhf_sph.c
  csrc/x2c_dhf_sph_ca.c
  csrc/x2c_dhf_sph_pcc.c
  c_api/x2camf_c.c
)
target_include_directories(x2camf_c PRIVATE csrc c_api)
set_target_properties(x2camf_c PROPERTIES PUBLIC_HEADER c_api/x2camf_c.h)
target_link_libraries(x2camf_c PRIVATE ${LAPACK_LIBRARIES} ${BLAS_LIBRARIES} m)
if(ENABLE_OPENMP)
  find_package(OpenMP)
  if(OpenMP_C_FOUND)
    target_link_libraries(x2camf_c PRIVATE OpenMP::OpenMP_C)
  endif()
endif()

# export only the x2camf_* C API
if(APPLE)
  target_link_options(x2camf_c PRIVATE
    "LINKER:-exported_symbols_list,${CMAKE_CURRENT_SOURCE_DIR}/c_api/exports.txt")
elseif(UNIX)
  target_link_options(x2camf_c PRIVATE
    "LINKER:--version-script=${CMAKE_CURRENT_SOURCE_DIR}/c_api/exports.map")
endif()

if(SKBUILD)
  # inside the Python package directory, next to libx2camf.py
  set(X2CAMF_LIB_DIR x2camf)
  set(X2CAMF_INCLUDE_DIR x2camf/include)
else()
  include(GNUInstallDirs)
  set(X2CAMF_LIB_DIR ${CMAKE_INSTALL_LIBDIR})
  set(X2CAMF_INCLUDE_DIR ${CMAKE_INSTALL_INCLUDEDIR})
endif()
install(TARGETS x2camf_c
  LIBRARY DESTINATION ${X2CAMF_LIB_DIR}
  RUNTIME DESTINATION ${X2CAMF_LIB_DIR}
  ARCHIVE DESTINATION ${X2CAMF_LIB_DIR}
  PUBLIC_HEADER DESTINATION ${X2CAMF_INCLUDE_DIR})
