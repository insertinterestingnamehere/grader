from grade_imp import test, load_cython_mod
from numpy import zeros, linspace, meshgrid, sin, pi
from numpy.random import rand, seed, randint
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def test_ssor_square(ssor, resolution=100, rstride=5):
    # Construct initial values for iteration.
    U = zeros((resolution, resolution))
    X = linspace(0, 1, resolution)
    U[0] = sin(2 * pi * X)
    U[-1] = - U[0]
    # Call C or Fortran routine
    ssor(U, 1.9)
    # Plot the results.
    X, Y = meshgrid(X, X, copy=False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, U, rstride=rstride)
    plt.show()

def test_ssor_nonsquare(ssor, resolution=100, contraction=2, rstride=5):
    # Construct initial values for iteration.
    U = zeros((resolution, resolution // contraction))
    X = linspace(0, 1, resolution // contraction)
    U[0] = sin(2 * pi * X)
    U[-1] = - U[0]
    # Call C or Fortran routine
    ssor(U, 1.9)
    # Plot the results.
    X, Y = meshgrid(X, linspace(0, 1, resolution), copy=False)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, U, rstride=rstride)
    plt.show()

def test_permutation_min(PyPermutation):
    seed(1337)
    P = PyPermutation(randint(1, 21, (4, 15)))
    P.reduce()
    return P.get_min()

def test_permutation_trace_inv(PyPermutation):
    seed(1337)
    P = PyPermutation(randint(1, 21, (4, 15)).tolist())
    P.reduce()
    return P.trace_inverse(5)

def test_permutation_power(PyPermutation):
    seed(1337)
    P = PyPermutation(randint(1, 21, (4, 15)).tolist())
    P.reduce()
    return P**1232125

if __name__ == '__main__':
    from sys import argv
    directory = argv[1]
    fssor = load_cython_mod(directory, 'fssor')
    test(test_ssor_square, 'cyssor', fssor)
    test(test_ssor_nonsquare, 'cyssor', fssor)
    cssor = load_cython_mod(directory, 'cssor')
    test(test_ssor_square, 'cyssor', cssor)
    test(test_ssor_nonsquare, 'cyssor', cssor)
    # These tests aren't working.
    # Some sort of fix to the load_cython function is needed.
    #permutations = load_cython_mod(directory, 'permutations')
    #test(test_permutation_min, 'PyPermutation', permutations)
    #test(test_permutation_trace_inv, 'PyPermutation', permutations)
    #test(test_permutation_power, 'PyPermutation', permutations)
