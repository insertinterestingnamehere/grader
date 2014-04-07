from grade_imp import load_solutions, test
import numpy as np
from numpy.random import rand, seed
from matplotlib import pyplot as plt

def test_basis_functions(N):
    """ Test the b-spline basis function 'N' """
    # Warning. I'm giving it mostly integer input.
    t = [0, 0, 1, 3, 6, 10, 10]
    k = 4
    i = 1
    X = np.linspace(1, 10, 4)
    return [N(x, i, k, t) for x in X]

def test_circle_interp(circle_interp):
    """ Test the circle_interp function that uses splev. """
    circle_interp(100, 4, res=201)
    # Show if they haven't already done that.
    plt.show()

def test_my_circle_interp(my_circle_interp):
    """ Test the my_circle_interp function that uses their spline evaluation function. """
    my_circle_interp(7, 3, res=201)
    # Show if they haven't already done that.
    plt.show()

if __name__ == '__main__':
    from sys import argv
    solutions = load_solutions(argv[1])
    test(test_basis_functions, 'N', solutions)
    test(test_circle_interp, 'circle_interp', solutions)
    test(test_my_circle_interp, 'my_circle_interp', solutions)
