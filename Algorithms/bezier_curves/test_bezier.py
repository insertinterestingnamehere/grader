from grade_imp import load_solutions, test
import numpy as np
from numpy.random import rand, seed
from matplotlib import pyplot as plt

def test_decasteljau(decasteljau):
    """ Test decasteljau """
    seed(10)
    pts = rand(9, 3)
    t = rand(1)[0]
    return decasteljau(pts, t)

def test_bernstein_1(bernstein):
    """ Test Bernstein Polynomials. """
    return bernstein(2, 4)

def test_bernstein_2(bernstein):
    """ Test Bernstein Polynomials. """
    return bernstein(1, 5)

def test_bernstein_3(bernstein):
    """ Test Bernstein Polynomials. """
    return bernstein(1, 3)

def test_bernstein_pt_approx(bernstein_pt_aprox):
    """ Test bernstein_pt_approx. """
    seed(32)
    pts = rand(5, 2)
    x, y = bernstein_pt_aprox(pts)
    # Allow them to return a numpy array, or any sort of callable object.
    # A poly1d object would be ideal for this though.
    if isinstance(x, np.ndarray):
        return np.polyval(x, .7), np.polyval(y, .7)
    return x(.7), y(.7)

def test_compare_plot(compare_plot):
    """ Test compare_plot """
    seed(20)
    compare_plot(30)
    plt.show()

if __name__ == '__main__':
    from sys import argv
    solutions = load_solutions(argv[1])
    test(test_decasteljau, 'decasteljau', solutions)
    test(test_bernstein_1, 'bernstein', solutions)
    test(test_bernstein_2, 'bernstein', solutions)
    test(test_bernstein_3, 'bernstein', solutions)
    test(test_bernstein_pt_approx, 'bernstein_pt_aprox', solutions)
    test(test_compare_plot, 'compare_plot', solutions)
