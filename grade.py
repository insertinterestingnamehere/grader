from shutil import copyfile
from os import system, remove
from os.path import isfile, isdir
from glob import glob

# Usage: python grade.py <students> <student_filepath> <actual_solutions> <test_script>
# 
# This is meant to be run from a folder containing all the solutions for each student.
#
# <students> is the path to a text file containing the names of all the students.
#  Each of their corresponding directories is assumed to have the same name as
#  the one listed in the <students> text file.
#
# <student_filepath> is meant to be the path from within a given student's
#  directory to the folder containing the solutions to the lab.
#  It can contain multiple folders, but should not begin or end with ./, or /
#
# <test_script> is the file name for the test script.
#  It is generally assumed that this script will be in the same folder as 'grade.py'.
#  This script should import whatever is needed to test solutions from
#  both the student's solutions file and the solutions file included with each lab.
#  The import statements should be written as if all three python scripts
#  are contained within a single folder.
#  It should print some sort of output that the TA will be able to use to compare the
#  results from the student's code with the results from the accepted solution.
#
# <actual_solutions> is the file name for the solutions file corresponding the the
#  lab being graded. It is also assumed to be in the same folder as 'grade.py'.
#  It should not have the same name as any file in the directory
#  containing the solutions for any given student.
#
# Example:
# python grade.py students.txt Vol1s2/Section26 newton_test.py newton.py
#


# Helper functions that are made available to the test script.
def test(ftest, fname):
    """ Run the test 'ftest' on the function of name 'fname'.
    'ftest' should be a callable test function with a docstring
    that describes the test it is performing.
    'fname' should be a string giving the name of the function
    that is to be tested from both modules. """
    
    print ftest.__doc__
    print 'response should be: '
    r = exec('ftest(re.{0})'.format(fname))
    print r
    try:
        r = exec('ftest(st.{0})'.format(fname))
        print 'student response was: '
        print r
    except:
        print "Student's code caused an unexpected error: "
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    raw_input("Press Enter to continue...")

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
    t = exec('ftest(re.{0})'.format(fname))
    print t
    try:
        t = exec('ftest(st.{0})'.format(fname))
        print 'student time was:'
        print t
    except:
        # Skip printing the traceback.
        # That should be taken care of in the correctness tests.
        print "Student's code raised an error."
    raw_input('Press Enter to continue...')

class student(object):
    # A class to hold the various file destinations
    # we need to manipulate for an individual student.
    def __init__(self, name, folder, solution, test, grader):
        self.name = name
        self.folder = './{0}/{1}/'.format(name, folder)
        self.solution = './{0}/{1}/{2}'.format(name, folder, solution)
        self.test = './{0}/{1}/{2}'.format(name, folder, test)
        self.grader = './{0}/{1}/{2}'.format(name, folder, grader)
        self.score = None

class grader(object):
    
    # Store the file destinations of general interest.
    def __init__(self, location, students_file, folder, solution, test):
        self.location = location
        self.solution = solution
        self.test = test
        # Initialize the file locations for each student.
        with open(students_file, 'rU') as f:
            self.students = [student(l.strip(), folder, solution, test, location) for l in f]
    
    # Run a test for an individual student.
    def run_test(self, student):
        # Avoid overwriting any files that are already there.
        if isfile(student.solution) or isfile(student.test):
            raise ValueError('Do not overwrite student solutions files with the real solutions.')
        # Skip running the test if the student hasn't even made the directory yet.
        if not isdir(student.folder):
            print "Could not find the student's directory for this lab."
            return
        # Copy the test script and the real solution into their directory.
        copyfile(self.test, student.test)
        copyfile(self.solution, student.solution)
        copyfile(self.location, student.grader)
        # Run the test script.
        system('python ' + student.test)
        # Delete the test scripty and the real solution from their directory.
        remove(student.test)
        remove(student.solution)
        remove(student.grader)
        # Remove the compiled .pyc files after running the tests.
        for f in glob(student.folder + '*.pyc'):
            remove(f)
    
    # Get the grade and feedback for a given student.
    def get_grade(self, student):
        # Skip giving feedback if the student hasn't even made the directory yet.
        # Give a score of 0 in the grades file
        if not isdir(student.folder):
            student.score = 'None'
            return
        # Handle the expected case that the folder is really there.
        with open(student.folder+'feedback.txt', 'w') as f:
            score = raw_input('Enter score: ')
            student.score = score
            f.write('score: {0}\n'.format(score))
            print 'Now enter any other feedback you would like to give.'
            print 'enter an empty line to finish'
            for line in iter(raw_input, ''):
                f.write(line + '\n')
    
    # Run the tests for all given students.
    def run_all(self):
        for student in self.students:
            # Print some empty lines to separate output between students
            print
            print
            # Print the name of the file being executed.
            print student.test
            self.run_test(student)
            self.get_grade(student)
        # Write all the grades to file
        mode = 'w'
        if isfile('grades.txt'):
            mode = 'a'
        with open('grades.txt', mode) as f:
            f.write('\n')
            f.write(self.solution + '\n')
            for student in self.students:
                f.write('{0}: {1}\n'.format(student.name, student.score))

if __name__ == '__main__':
    # When this is run from command line, run the test script
    # on the code for all the students.
    from sys import argv
    grader(argv[0], argv[1], argv[2], argv[3], argv[4]).run_all()
