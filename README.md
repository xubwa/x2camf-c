# x2camf (C implementation)

Atomic mean-field (AMF) spin-orbit integrals for exact two-component (X2C)
Hamiltonians, and the spherical atomic Dirac-Hartree-Fock behind them.
This is a C99 translation of the computational core of the C++
[X2CAMF](https://github.com/Warlocat/x2camf) code, line by line
(`csrc/TRANSLATION_CONVENTIONS.md`), with results equal to the C++/Eigen
implementation to SCF convergence.  One deliberate difference: in the
average-of-configuration (`aoc`) 4-component SCF the open-shell coupling
operator also treats the negative-energy orbitals as virtual, which makes a
single open-shell electron exact with the Gaunt term (the C++ code leaves a
small self-interaction there).  AMF integrals of open-shell atoms change at
the 1e-8..1e-10 relative level.  It links only BLAS/LAPACK, libm and
(optionally) OpenMP: no C++ runtime, Eigen or pybind11.

```python
from x2camf import libx2camf
amf = libx2camf.amfi(flavor, Z, nshell, nbas, 0, shell, exp_a)[0]
res = libx2camf.atm_integrals(flavor, Z, nshell, nbas, 0, shell, exp_a)
```

The Python functions (`amfi`, `atm_integrals`, `pcc_K`) have the same
arguments and return values as the pybind11 module of the C++ code, so
existing scripts run unchanged.  `x2camf.x2camf` is the molecular interface
for pyscf (`pip install x2camf[pyscf]`).

The shared library `libx2camf_c` is loaded through ctypes, so one wheel per
platform serves every Python 3 version.  Its C API is `c_api/x2camf_c.h`
(`x2camf_amfi`, `x2camf_atm_integrals`, `x2camf_pcc_k`).

## BLAS/LAPACK

The PyPI wheels carry OpenBLAS and OpenMP (Linux) or use Accelerate
without OpenMP (macOS 11 or newer; the C code then runs on one thread).  For
another library build from source; the CMake options are those of pyscf:

```bash
CMAKE_ARGS="-DBLAS_LIBRARIES=mkl_rt" pip install --no-binary x2camf x2camf
```

The C library alone builds with plain CMake (`cmake -S . -B build && cmake
--build build && cmake --install build`).

## Tests

```bash
python tests/test_smoke.py                     # no dependencies
python tests/test_atomic_dhf.py                # vs pyscf 4c DHF (needs pyscf)
X2CAMF_CPP_LIBRARY=/path/to/libx2camf.cpython-*.so python tests/test_against_cpp.py
```

## License

Apache License 2.0, see `LICENSE` and `NOTICE`.
