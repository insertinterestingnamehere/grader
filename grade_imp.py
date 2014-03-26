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

# Notes on implementation:
# The idea here is that this script will be called from a directory containing
# subdirectories for each of the students.
# Each test script is expected to take a file path as input.
# All the test script does is use the load_solutions function below
# to load the solutions file from each student (if it exists),
# and then (in an `if __name__ == "__main__":` block) run each test
# function for the solutions file.
# Each test function is expected to be something that accepts a callable
# function as input, constructs the desired test case, then calls the function
# with the arguments it has constructed.
# The test function below is designed to run a test using proper
# error handling. It is meant to be imported by each test script then used
# to run each test and print the output.
# More utility functions could be added to this file as needed.

# Helper function for test scripts
# Run a test and print its output.
# Print the docstring for the test function so the person grading
# can see which test is being run.
def test(ftest, fstr, module):
    """ Run a test function ftest on function 'fstr' that is a part of
    'module'. 'fstr' is a string for the name of the function. """
    # Note: passing the name of the function instead of the function itself
    # allows all the error handling for failed imports to be dealt with in
    # this function instead of in each individual test file.
    # It also avoids having to deal with the error handling for imports
    # on a function-by-function basis.
    print ftest.__doc__
    # Try to import the desired function from the student's solutions.
    # Print that it was not found if it cannot be found.
    try:
        f = getattr(module, fstr)
    except AttributeError:
        print "Function {0} not found in student's solutions file.".format(fstr)
        return
    # Try calling the student's function.
    # Display the error but do not stop the script if an error is raised.
    try:
        val = ftest(f)
        # Don't bother to print extra None's as output.
        if val is not None:
            print val
    except:
        # Print the error without stopping the script.
        print "Student's code caused an unexpected error: "
        print '-'*60
        print_exc(file=stdout)
        print '-'*60

# Another helper function for test scripts
# Returns a module object corresponding to the python script found at
# file location 'source'.
# Raises a descriptive error if the file cannot be found.
def load_solutions(source):
    """ Returns a module object made by importing the Python file at
    location 'source'. Raises a descriptive error if the file is not found. """
    try:
        # Use the load_source command to import from a file location.
        s = load_source('solutions', source)
    except IOError:
        raise ImportError('Could not find student solutions file.')
    return s

# Internal class for this script.
# It is designed to store the relevant information for each student.
class student(object):
    def __init__(self, name, path):
        # Store the Student's:
        # name
        # path to solutions file
        # path to the directory containing the solutions file.
        self.name = name
        self.solution = '{0}/{1}'.format(name, path)
        self.path = dirname(self.solution)

# This is another internal class.
# It is designed to drive all the tests using the data
# stored in the different student objects.
class grader(object):
    def __init__(self, test, students, solutions):
        # Construct a list of student objects that need grading.
        with open(students) as f:
            self.students = [student(s.strip(), solutions) for s in f]
        # Cache the name of the test script.
        self.test = test
    
    def get_grade(self, student):
        # Ask the TA to give a grade and leave feedback.
        # All this is currently done directly in the command line.
        # Skip giving feedback if the student hasn't even made the directory yet.
        # Give a score of None in the grades file
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
            # write lines to file until an empty line is given.
            for line in iter(raw_input, ''):
                f.write(line + '\n')
    
    # Call the grading script for each student, write all the grades to
    # a file called 'grades.txt' in the same folder as this script.
    # Also call the get_grade method to get the feedback from the TA for each student.
    def grade_all(self):
        # Initialize the writing mode so that it adds to the grades.txt file
        # if it already exists.
        # Have it write to it directly if it does not.
        mode = 'w'
        if isfile('grades.txt'):
            mode = 'a'
        # Open the grades file and write to it as grading goes.
        with open('grades.txt', mode) as f:
            # Separate the entry in the grades.txt file by a space.
            f.write('\n')
            # Write out the name of the test file being run.
            f.write(self.test + '\n')
            # Also write the day and time the tests were started.
            f.write(strftime('%m/%d/%Y  %H:%M:%S\n'))
            # Use flush and fsync to write all current changes to disk.
            f.flush()
            fsync()
            # Process each student.
            for student in self.students:
                # Run the test script here.
                system('python {0} {1}'.format(self.test, student.solution))
                # Remove any compiled files after running the tests.
                # Any additional cleanup can be taken care of by the
                # individual test script.
                for extension in ['pyc', 'pyd', 'so', 'o']:
                    # Use glob to remove all files with the given extension
                    # in the folder containing each student's solutions file.
                    for compiled in glob('{0}/*.{1}'.format(student.path, extension)):
                        remove(compiled)
                # When each test script has run to completion, ask the
                # person grading to assign a grade and give some feedback.
                self.get_grade(student)
                # Write the student's grade to the 'grades.txt' file.
                f.write('{0}: {1}\n'.format(student.name, student.score))
                # make sure that all changes have been saved to disk before
                # processing the next student.
                f.flush()
                fsync()

if __name__ == '__main__':
    from sys import argv
    # Construct a grader object and use it to do all the desired grading.
    grader(*argv[1:]).grade_all()

