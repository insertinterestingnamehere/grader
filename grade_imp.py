# A driver for the import-by-path based version of the grading script.
from os import system, remove, fsync
from os.path import dirname, isdir, isfile
from imp import load_source
from traceback import print_exc
from sys import stdout
from glob import glob
from time import strftime

# Usage:
# python grade_abs_imp.py <test> <students> <filepath>
# <test> should be an executable script.
#  It should accept a file path as its first command line argument and
#  should run the desired tests by importing the Python script found at
#  that location.
# <students> should be a text file containing the names of the students.
# <filepath> should be the remainder of the filepath required to get to
#  the desired solutions file within a given student's directory tree.
#
# Example: python grade_imp.py linesweep_test_imp.py students.txt Vol1s2/Section27/solutions.py

# Helper function for test scripts
def test(ftest, fstr, module):
    print ftest.__doc__
    try:
        f = getattr(module, fstr)
    except AttributeError:
        print "Function {0} not found in student's solutions file.".format(fstr)
        return
    try:
        val = ftest(f)
        if val is not None:
            print val
    except:
        print "Student's code caused an unexpected error: "
        print '-'*60
        print_exc(file=stdout)
        print '-'*60

# Another helper function for test scripts
def load_solutions(source):
    try:
        s = load_source('solutions', source)
    except IOError:
        raise ImportError('Could not find student solutions file.')
    return s

class student(object):
    def __init__(self, name, path):
        self.name = name
        self.solution = '{0}/{1}'.format(name, path)
        print self.solution
        self.path = dirname(self.solution)

class grader(object):
    def __init__(self, test, students, solutions):
        with open(students) as f:
            self.students = [student(s.strip(), solutions) for s in f]
        self.test = test
    
    def get_grade(self, student):
        # Skip giving feedback if the student hasn't even made the directory yet.
        # Give a score of 0 in the grades file
        if not isdir(student.path):
            student.score = 'None'
            return
        # Handle the expected case that the folder is really there.
        with open('{0}/feedback.txt'.format(student.path), 'w') as f:
            score = raw_input('Enter score: ')
            student.score = score
            f.write('score: {0}\n'.format(score))
            print 'Now enter any other feedback you would like to give.'
            print 'enter an empty line to finish'
            for line in iter(raw_input, ''):
                f.write(line + '\n')
    
    def grade_all(self):
        mode = 'w'
        if isfile('grades.txt'):
            mode = 'a'
        with open('grades.txt', mode) as f:
            f.write('\n')
            f.write(self.test + '\n')
            f.write(strftime('%m/%d/%Y  %H:%M:%S\n'))
            f.flush()
            fsync()
            for student in self.students:
                system('python {0} {1}'.format(self.test, student.solution))
                # Remove various compiled files after running the tests.
                for extension in ['pyc', 'pyd', 'so', 'o']:
                    for compiled in glob('{0}/*.{1}'.format(student.path, extension)):
                        remove(compiled)
                self.get_grade(student)
                f.write('{0}: {1}\n'.format(student.name, student.score))
                f.flush()
                fsync()

if __name__ == '__main__':
    from sys import argv
    grader(*argv[1:]).grade_all()

