'''
X2CAMF: atomic mean-field spin-orbit integrals for exact two-component (X2C)
Hamiltonians (C99 implementation, ctypes binding).

    from x2camf import libx2camf      # amfi, atm_integrals, pcc_K
    from x2camf import x2camf         # molecular interface (requires pyscf)
'''

__version__ = '1.0.0'

from x2camf import libx2camf

# molecular interface; requires pyscf
try:
    from x2camf import x2camf
    amfi = x2camf.amfi
except ImportError:
    pass
