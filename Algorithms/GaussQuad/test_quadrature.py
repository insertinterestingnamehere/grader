from grade_imp import test, load_solutions
import numpy as np
from numpy.random import rand, seed
from matplotlib import pyplot as plt
from numpy.polynomial.legendre import leggauss

def test_shift(shift_function, res=101):
    """ Test shift_function """
    seed(932)
    X = np.linspace(-1, 1, 13)
    Y = rand(*(X.shape))
    f = lambda x: np.interp(np.sin(x), X, Y)
    a, b = - 2 * np.pi, 4 * np.pi
    X0 = np.linspace(a, b, res)
    X1 = np.linspace(-1, 1, res)
    plt.plot(X1, f(X0))
    plt.plot(X1, shift_function(f, a, b)(X1))
    plt.show()

def test_funcplot(funcplot, res=101):
    """ Test funcplot """
    seed(84)
    X = np.linspace(-1, 1, 13)
    Y = rand(*(X.shape))
    f = lambda x: np.interp(np.sin(x), X, Y)
    a, b = - 2 * np.pi, 4 * np.pi
    X0 = np.linspace(a, b, res)
    X1 = np.linspace(-1, 1, res)
    plt.plot(X0, f(X0))
    plt.show()
    plt.plot(X1, f(X0))
    plt.show()
    funcplot(f, a, b, n=res)
    plt.show()

def test_shift_example(shift_example):
    """ Test shift_example """
    shift_example()
    plt.show()

def test_integral_estimation(estimate_integral):
    """ Test integral_estimation """
    points, weights = leggauss(92)
    X = np.linspace(-1, 1, 13)
    Y = rand(*(X.shape))
    f = lambda x: np.interp(np.cos(x), X, Y)
    return estimate_integral(f, 8, 14, points, weights)

def test_jacobi(construct_jacobi, n = 9):
    """ Test formation of the Jacobi matrix """
    i = np.arange(1, n + 1, dtype=float)
    a = (2 * i - 1) / i
    b = np.zeros_like(i)
    c = (i - 1) / i
    # return the lower corner so it isn't a mess to print.
    return construct_jacobi(a, b, c)[5:,5:]

def test_points_and_weights(points_and_weights):
    """ Test points_and_weights """
    n = 121
    points, weights = points_and_weights(n)
    weights = weights[points.argsort()]
    points.sort()
    return points[100:], weights[100:]

def test_normal_cdf(normal_cdf):
    """ Test normal_cdf """
    test_points = np.linspace(-.8, .8, 6)
    return np.vectorize(normal_cdf)(test_points)

if __name__ == '__main__':
    from sys import argv
    solutions = argv[1]
    solutions = load_solutions(solutions)
    test(test_shift, 'shift_function', solutions)
    test(test_funcplot, 'funcplot', solutions)
    test(test_shift_example, 'shift_example', solutions)
    test(test_integral_estimation, 'estimate_integral', solutions)
    test(test_jacobi, 'construct_jacobi', solutions)
    test(test_points_and_weights, 'points_and_weights', solutions)
    test(test_normal_cdf, 'normal_cdf', solutions)
