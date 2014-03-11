import newton as re
try:
    import solutions as st
except ImportError:
    raise ImportError('Could not find student solutions file.')
import traceback
import sys
import numpy as np
from numpy.random import rand
from math import cos
from matplotlib import pyplot as plt

def run_test(f, solution, student_solution):
    print f.__doc__
    print 'Response should be:'
    r = f(solution)
    print r
    try:
        r = f(student_solution)
        print 'Student response was:'
        print r
    except:
        print "Student's code caused an unexpected error:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    raw_input('Press Enter to continue...')

def test_newton_without_der(newton):
    """ Test Newton's method function without a given derivative. """
    # In the future, we should require that they deal with
    # higher dimensional arrays.
    G = rand(20)
    f = np.poly1d([1,2,3,4])
    return newton(G, f)[0]

def test_newton_with_der(newton):
    """ Test Newton's method function with a given derivative. """
    G = rand(20)
    f = np.poly1d([1,2,3,4])
    return newton(G, f, f.deriv())[0]

def test_newton_convergence(newton):
    """ Test to ensure the Newton's method function gives proper convergence results. """
    G = np.pi * (rand(20) - .5)
    f = np.sin
    return newton(G, f)[1]

def test_multi(multinewton):
    """ Test the multi-dimensional version of Newton's method. """
    # Use the example given as a homework problem in the text.
    F = lambda X: np.array([X[0] - X[1]**2 + 8 + cos(X[1]),
                            X[1] - X[0]**2 + 9 + 2 * cos(X[0])])
    v = np.array([np.pi, np.pi])
    return multinewton(v, F)[0]

def test_polyjulia(polyjulia):
    p = np.poly1d([1, 0, 0, 0, 2])
    polyjulia(p, -1, 1, -1, 1, res=101)
    # Show if the code hasn't already done that.
    # Does nothing if there is nothing to show.
    plt.show()

def test_polyplot(polyplot):
    polyplot()
    # Show if the code hasn't already done that.
    # Does nothing if there is nothing to show.
    plt.show()

def test_mandelbrot(mandelbrot):
    mandelbrot()

if __name__ == '__main__':
    # Use exec to execute each test so that all the tests run even
    # if the student didn't implement a given function.
    for test, actual, given in [('test_newton_without_der', 're.newton', 'st.newton'),
                                ('test_newton_with_der', 're.newton', 'st.newton'),
                                ('test_newton_convergence', 're.newton', 'st.newton'),
                                ('test_multi', 're.arr_newton', 'st.arr_newton'),
                                ('test_polyjulia', 're.polyjulia', 'st.polyjulia'),
                                ('test_polyplot', 're.polyplot', 'st.polyplot')#,
                                #('test_mandelbrot', 're.mandelbrot', 'st.mandelbrot')
                                ]:
        try:
            exec('run_test({0}, {1}, {2})'.format(test, actual, given))
        except AttributeError:
            print 'Student did not provide this function in their solutions'
