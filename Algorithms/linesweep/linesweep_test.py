try:
    import solutions as s
except ImportError:
    raise ImportError('Could not find student solutions file.')
import traceback
import numpy as np
from numpy.random import rand, seed
from timeit import Timer
from matplotlib import pyplot as plt

def metric(p, X):
    dif = (X - p)
    return np.sqrt((dif * dif).sum(axis=-1))

# Helper function
def test(ftest, fstr):
    print ftest.__doc__
    try:
        f = getattr(s, fstr)
    except AttributeError:
        print "Function not found in student's solutions file."
        return
    try:
        print ftest(f)
    except:
        print "Student's code caused an unexpected error: "
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

def mindist_simple_correctness(mindist_simple):
    """ Correctness of mindist_simple function. """
    seed(42)
    X = rand(1000, 4)
    return mindist_simple(X, metric)

def mindist_correctness(mindist, tol=1E-6):
    """ Correctness of mindist function. """
    seed(168646)
    X = rand(1000, 4)
    return mindist(X)

def test_farthest(farthest):
    """ Farthest point problem. """
    # This is a very basic test.
    # A better test would be able to test
    # specifically for the cases that the
    # maximum distance lies on the edge of the box
    # or that the maximum distance
    # lies at one of the corners.
    seed(149)
    X = rand(150, 2)

def test_triangulate(triangulate):
    triangulate(20)
    # Show the plot if the function didn't do it already.
    plt.show()

def mindist_simple_speed_low_dim(mindist_simple):
    """ Speed of mindist_simple function for lower dimensions. """
    seed(12)
    X = rand(1000000, 2)
    T = Timer(lambda: mindist_simple(X, metric))
    return T.timeit(number=3)

def mindist_simple_speed_high_dim(mindist_simple):
    """ Speed of mindist_simple function for higher dimensions. """
    seed(42)
    X = rand(10000, 8)
    T = Timer(lambda: mindist_simple(X, metric))
    return T.timeit(number=10)

def mindist_speed_low_dim(mindist):
    """ Speed of mindist function for lower dimensions. """
    seed(18)
    X = rand(10000000, 2)
    T = Timer(lambda: mindist(X, metric))
    return T.timeit(number=2)

def mindist_speed_high_dim(mindist):
    """ Speed of mindist function for higher dimensions. """
    seed(25)
    X = rand(10000, 8)
    T = Timer(lambda: mindist(X, metric))
    return T.timeit(number=2)

if __name__ == '__main__':
    test(mindist_simple_correctness, 'mindist_simple')
    test(mindist_correctness, 'mindist')
    #test(test_farthest, 'farthest')
    test(test_triangulate, 'triangulate')
    test(mindist_simple_speed_low_dim, 'mindist_simple')
    test(mindist_simple_speed_high_dim, 'mindist_simple')
    test(mindist_speed_low_dim, 'mindist')
    test(mindist_speed_high_dim, 'mindist')
