import linesweep as re
from linesweep import metric
try:
    import solutions as st
except ImportError:
    raise ImportError('Could not find student solutions file.')
import traceback
import sys
import numpy as np
from numpy.random import rand, seed
from timeit import Timer
from matplotlib import pyplot as plt

# Helper function
def test(ftest, fname):
    """ Run the test 'ftest' on the function of name 'fname'.
    'ftest' should be a callable test function with a docstring
    that describes the test it is performing.
    'fname' should be a string giving the name of the function
    that is to be tested from both modules. """
    print ftest.__doc__
    print 'response should be: '
    r = ftest(getattr(re, fname))
    print r
    try:
        r = ftest(getattr(st, fname))
        print 'student response was: '
        print r
    except:
        print "Student's code caused an unexpected error: "
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    raw_input("Press Enter to continue...")

# Another helper function.
def speed_test(ftest, fname):
    """ Run the speed test 'ftest' on the function of name 'fname'.
    'ftest' should be a callable test function with a docstring
    that describes the test that it performs.
    It should return the time taken for whatever test it is running.
    'fname' should be a string giving the name of the function
    that is to be tested from both modules. """
    
    # The logic for this function is pretty much identical to the
    # logic in the test function. The primary difference is that the
    # output is descriptive of a speed test instead of a correctness test.
    print ftest.__doc__
    print 'Reference time was:'
    t = ftest(getattr(re, fname))
    print t
    try:
        t = ftest(getattr(st, fname))
        print 'student time was:'
        print t
    except:
        # Skip printing the traceback.
        # That should be taken care of in the correctness tests.
        print "Student's code raised an error."
    raw_input('Press Enter to continue...')

def mindist_simple_correctness(mindist_simple):
    """ Correctness of mindist_simple function. """
    seed(42)
    X = rand(1000, 4)
    return mindist_simple(X, re.metric)

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
    speed_test(mindist_simple_speed_low_dim, 'mindist_simple')
    speed_test(mindist_simple_speed_high_dim, 'mindist_simple')
    speed_test(mindist_speed_low_dim, 'mindist')
    speed_test(mindist_speed_high_dim, 'mindist')
