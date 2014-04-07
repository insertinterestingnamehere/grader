import numpy as np
from numpy.random import rand, seed

def test_singplot(singplot):
    """ Test 'singplot' function """
    f = lambda z: 1. / (z**3 * (3 * z - 1.0j)**2 * (3 * z - np.sqrt(3) / 2. + .5j)**2 * (3 * z + np.sqrt(3) / 2. + .5j)**2)**3
    singplot(f)
    singplot(f, kind='imag')
    singplot(f, kind='abs')

def test_partial_fractions(partial_fractions):
    """ Test partial fraction decomposition """
    seed(82)
    p = np.poly1d(rand(4))
    q = np.poly1d(rand(10))
    return partial_fractions(p, q)

def test_cpv(cpv):
    """ Test cauchy principal value evaluation """
    seed(743)
    p = np.poly1d(rand(3))
    q = np.poly1d(rand(8))
    return cpv(p, q)

def test_count_roots(count_roots):
    """ Test the root counting function """
    seed(1098752)
    p = np.poly1d(rand(4)) * np.poly1d([1, -.25])
    return count_roots(p)

if __name__ == '__main__':
    from sys import argv
    from grade_imp import test, load_solutions
    solutions = load_solutions(argv[1])
    test(test_singplot, 'singplot', solutions)
    test(test_partial_fractions, 'partial_fractions', solutions)
    test(test_cpv, 'cpv', solutions)
    test(test_count_roots, 'count_roots', solutions)
