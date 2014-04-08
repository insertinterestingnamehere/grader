import numpy as np
from numpy.random import rand, seed
from os import remove

# This is the data file to use for this test.
# It needs to be downloaded separately and placed
# in the same folder as this test script.
__datafile__ = 'Amazon0302.txt'
__datasize__ = 262111

# a helper function.
def write_bool_mat(n, filename):
    A = rand(n, n)
    A = A < .1
    with open(filename, 'w') as f:
        f.write('# Some sample data for the Page Rank lab.\n')
        for i in xrange(A.shape[0]):
            for j in xrange(A.shape[1]):
                if A[i,j]:
                    f.write('{0} {1}\n'.format(i, j))
    return A

def test_adj_mat(adj_mat):
    """ Test adj_mat """
    seed(31)
    A = write_bool_mat(10, 'test_pages.txt')
    A2 = adj_mat('test_pages.txt', 10).todense().astype(bool)
    A += (A.sum(axis=1, keepdims=True) == 0)
    remove('test_pages.txt')
    return (A2 == A).all() or (A2.T == A).all()

def test_page_rank_dense(page_rank_dense_iter):
    """ Test the dense version of the Page rank algorithm """
    filename = 'test_dense_iter.txt'
    seed(429)
    A = write_bool_mat(20, filename)
    print page_rank_dense_iter(filename, .85, 30)
    remove(filename)

def test_page_rank_sparse_small(sparse_pr):
    """ Test the dense version of the Page rank algorithm """
    filename = 'test_sparse_iter.txt'
    seed(429)
    A = write_bool_mat(20, filename)
    print sparse_pr(filename, .85, 30)
    remove(filename)

def test_page_rank_sparse(sparse_pr):
    """ Test the sparse version of the Page rank algorithm """
    return sparse_pr(__datafile__, .85, __datasize__)

if __name__ == '__main__':
    from grade_imp import test, load_solutions
    from sys import argv
    solutions = load_solutions(argv[1])
    test(test_adj_mat, 'adj_mat', solutions)
    test(test_page_rank_dense, 'page_rank_dense_iter', solutions)
    test(test_page_rank_sparse_small, 'sparse_pr', solutions)
    test(test_page_rank_sparse, 'sparse_pr', solutions)
