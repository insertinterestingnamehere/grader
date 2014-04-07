import numpy as np
from sympy import mpmath as mp
from mayavi import mlab as ml
from matplotlib import pyplot as plt

# This one can be a pain if someone uses mayavi improperly
# A timeout should be added to prevent freezing.
# That will allow Python to kill the process nicely.
def test_plotting(plot_real):
    """ Test plotting functions. """
    # Student's code should show the solutions.
    f = lambda x: np.sin(2 * x) + np.sinh(2 * x)
    plot_real(f)

def test_nroot_real(nroot_real):
    """ Test nroot_real. """
    nroot_real(3)

def test_nroot_imag(nroot_imag):
    """ Test nroot_imag. """
    nroot_imag(3)

def test_contour_int(contour_int):
    """ Test contour_int. """
    r = lambda t: 3 + mp.sin(10 * t)
    c = lambda t: r(t) * mp.exp(1.0j * t)
    f = lambda z: z + mp.sin(z) * mp.cosh(z)
    return contour_int(f, c, 0, 2 * np.pi)

def test_cauchy_formula(cauchy_formula):
    """ Test student verification of Cauchy's Integral formula. """
    r = lambda t: 3 + mp.sin(10 * t)
    c = lambda t: r(t) * mp.exp(1.0j * t)
    f = lambda z: z + mp.sin(z) * mp.cosh(z)
    print f(1.1 + 1.1j)
    cauchy_formula(f, c, 1.1 + 1.1j, 0, 2 * np.pi)(1.1 + 1.1j)

def test_cauchy_formula4arg(cauchy_formula):
    """ Test student verification of Cauchy's Integral formula. """
    r = lambda t: 3 + mp.sin(10 * t)
    c = lambda t: r(t) * mp.exp(1.0j * t)
    f = lambda z: z + mp.sin(z) * mp.cosh(z)
    print f(1.1 + 1.1j)
    print cauchy_formula(f, c, 1.1 + 1.1j, 0, 2 * np.pi)

if __name__ == '__main__':
    from grade_imp import test, load_solutions
    from sys import argv
    solutions = load_solutions(argv[1])
    test(test_plotting, 'plot_real', solutions)
    test(test_plotting, 'plot_imag', solutions)
    test(test_plotting, 'plot_both', solutions)
    test(test_nroot_real, 'nroot_real', solutions)
    test(test_nroot_imag, 'nroot_imag', solutions)
    test(test_contour_int, 'contour_int', solutions)
    test(test_cauchy_formula, 'cauchy_formula', solutions)
    
