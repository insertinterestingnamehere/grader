from grade_imp import test, load_solutions
import numpy as np
from numpy.random import seed

# helper function from lab
def grid(d=3, n=100):
    linspaces = [np.linspace(0, 1, n, endpoint=False) for i in xrange(d)]
    flatmesh = [x.flatten() for x in np.meshgrid(*linspaces)]
    return np.column_stack(flatmesh)

def test_eval_avg(eval_avg):
    """ Test eval_avg """
    return eval_avg(grid(d=3, n=87))

def test_monte_carlo(n, d):
    """ Test monte_carlo """
    seed(852)
    return monte_carlo(200000, 15)

if __name__ == '__main__':
    from sys import argv
    solutions = load_solutions(argv[1])
    test(test_eval_avg, 'eval_avg', solutions)
    test(test_monte_carlo, 'monte_carlo', solutions)
