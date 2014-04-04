# A driver for the import-by-path based version of the grading script.
from os import system, remove, fsync, listdir, rmdir, getcwd, chdir, chmod
from os.path import dirname, isdir, isfile, splitext
from imp import load_source, find_module, load_module
from traceback import print_exc
from sys import stdout
from glob import glob
from time import strftime
import subprocess as sp
from shutil import rmtree, copyfile
from errno import EACCES
from stat import S_IRWXU, S_IRWXG, S_IRWXO
import os, stat, shutil

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (rmdir, remove) and excvalue.errno == EACCES:
      chmod(path, S_IRWXU| S_IRWXG| S_IRWXO) # 0777
      func(path)
  else:
      raise

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

# A substitute for os.path.join that always uses forward slashes.
# Yes, this really does work on Windows.
# Writing it this way avoids having annoying paths that mix
# forward and backward shlashes on Windows.
def join(*args):
    return ('{}/'*(len(args) - 1) + '{}').format(*args)

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
        print 'Could not find student solutions file.'
        return
    return s

def load_cython_mod(student_dir, source_dir, setup_name=None, module_name=None):
    """ Build a Cython module contained in 'source_dir' that is
    a subdirectory of 'student_dir'. Specify the name of the setup
    file as 'setup_name' if possible. If 'setup_name' is specified, this function
    will build the module with setup file 'name' and then import
    the resulting .so or .pyd module and return a module object.
    If 'module_name' is specified, this function will import the
    resulting '.pyd' or '.so' file. The file extension for the module
    is not expected to be a part of the module name.
    If 'setup_name' is not specified, it will find a file with 'setup' or 'Setup'
    in its name and try to use it to build a module and then import
    the resulting module.
    This process probably won't work if there
    is more than one file in the directory with a name
    containing 'setup' or 'Setup'.
    If 'module_name' is not specified, it will
    look for new .so and .pyd files that were made by compilation.
    Note: this will delete all .pyd, and .so files in the build directory.
    A simple example would be
    load_cython_mod('path/to/student/directory', 'source/directory/in/folder', 'setup.py', 'mymodule') """
    directory = join(student_dir, source_dir)
    if not isdir(directory):
        print 'Student directory: {} not found!'.format(directory)
        return
    original_wd = getcwd()
    # Remove old pyd and so files so we are verifying
    # that the current version of the student's setup
    # file actually works.
    for ext in ['.pyd', '.so']:
        for f in glob('{}/*{}'.format(directory, ext)):
            remove(f)
    build_dir = join(directory, 'build')
    if isdir(build_dir):
        rmtree(build_dir)
    # Store the list of previous files.
    previous_files = set(listdir(directory))
    if setup_name is not None:
        print 'Building {}'.format(setup_name)
        command = 'python {} build_ext --inplace'.format(setup_name)
        # Store output of compilation without printing it.
        chdir(directory)
        out = sp.Popen(command, stdout=sp.PIPE).stdout.read()
        chdir(original_wd)
    else:
        chdir(directory)
        cond1 = '*setup*.py'
        cond2 = '*Setup*.py'
        try:
            f = next(iter(set(glob(cond1)) | set(glob(cond2))))
        except StopIteration:
            print 'Setup file not found.'
            # Returning None allows for the test script to
            # say each function is not found instead of
            # raising an error and stopping the test script.
            return
        print 'Building {}'.format(join(directory, f))
        command = 'python {} build_ext --inplace'.format(f)
        # Store output of compilation without printing it.
        out = sp.Popen(command, stdout=sp.PIPE).stdout.read()
        chdir(original_wd)
    current_files = set(listdir(directory))
    for f in current_files:
        filename, ext = splitext(f)
        # Remove everything except the relevant .o, .pyd, and .so files.
        # The rest of the files will be cleaned up when the
        # grade_all method of the Grader class is called.
        # This could cause trouble if a student is using some random file
        # extension instead of .o.
        if f not in previous_files:
            if ext not in ['.pyd', '.so', '.o']:
                full_filepath = join(directory, f)
                if isdir(full_filepath):
                    # Using rmtree also deletes the build directory if it was made.
                    # Be careful. This deletes folders as well as files.
                    rmtree(full_filepath, ignore_errors=False, onerror=handleRemoveReadonly)
                    #rmtree(join(directory, f))
                else:
                    remove(full_filepath)
    module_file = None
    for f in glob('{}/*.so'.format(directory)):
        module_file = f
    for f in glob('{}/*.pyd'.format(directory)):
        module_file = f
    module_file = module_file.replace("\\", '/')
    if module_name is None:
        module_name = 'solutions'
    filename = module_file.split('/')[-1]
    name_for_import, ext = splitext(filename)
    files_to_move = glob('{}/*.so'.format(directory)) + glob('{}/*.o'.format(directory)) + glob('{}/*.pyd'.format(directory))
    for f in files_to_move:
        fnew = f.replace("\\", '/')
        filename = fnew.split('/')[-1]
        if isfile(filename):
            remove(filename)
        copyfile(f, filename)
    print "module_file: ", module_file
    try:
        # There has really got to be a better way to do this.
        exec('import {} as s'.format(name_for_import))
        for f in files_to_move:
            remove(f)
        return s
    except ImportError:
        #chdir(original_wd)
        print 'Build failed. Unable to load module'
        print 'output from build was:'
        print '-'*60
        print out
        print '-'*60
        for f in files_to_move:
            remove(f)
        # Again, returning None, allows error handling for functions not
        # found to be handled by test function so as to not crash the
        # test script in the case that it has to load multiple modules.
        return

# Internal class for this script.
# It is designed to store the relevant information for each student.
class student(object):
    def __init__(self, name, path):
        # Store the Student's:
        # name
        # path to solutions file
        # path to the directory containing the solutions file.
        self.name = name
        self.solution = join(name, path)
        if isdir(self.solution):
            self.path = self.solution
        else:
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
        feedback = join(student.path, 'feedback.txt')
        if isfile(feedback):
            if raw_input("Feedback file already found. Overwrite? y/n") not in ['y', 'Y']:
                with open(feedback, 'r') as f:
                    old_score = next(f).split()[-1]
                    try:
                        student.score = int(old_score)
                    except ValueError:
                        if old_score in ['None', 'none']:
                            student.score = 'None'
                        else:
                            print 'Warning! detected score is not an integer or None.'
                            student.score = old_score
                return
        with open(feedback, 'w') as f:
            score = raw_input('Enter score: ')
            student.score = score
            f.write('score: {}\n'.format(score))
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
            fsync(f.fileno())
            # Process each student.
            for student in self.students:
                # Run the test script here.
                system('python {} {}'.format(self.test, student.solution))
                # Remove any compiled files after running the tests.
                # Any additional cleanup can be taken care of by the
                # individual test script.
                for extension in ['pyc', 'pyd', 'so', 'o']:
                    # Use glob to remove all files with the given extension
                    # in the folder containing each student's solutions file.
                    for compiled in glob('{}/*.{}'.format(student.path, extension)):
                        remove(compiled)
                # When each test script has run to completion, ask the
                # person grading to assign a grade and give some feedback.
                self.get_grade(student)
                # Write the student's grade to the 'grades.txt' file.
                f.write('{}: {}\n'.format(student.name, student.score))
                # make sure that all changes have been saved to disk before
                # processing the next student.
                f.flush()
                fsync(f.fileno())
        # Remove ALL .o, .so, and .pyd files in current directory.
        # This needs to be done because of the hack to get pyd imports working.
        for f in glob('*.pyd') + glob('*.o') + glob('*.so'):
            remove(f)

if __name__ == '__main__':
    from sys import argv
    # Construct a grader object and use it to do all the desired grading.
    grader(*argv[1:]).grade_all()

