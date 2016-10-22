#

"""
Utils for testing
"""

import os
import shutil
import sys
import subprocess
import tempfile
from functools import wraps


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def in_directory(file_, *components):
    """
    A decorator to execute a function in a directory relative to the current
    file.

    __file__ must be passed as first argument to determine the directory to
    start with.

    For preserving the ability to import aloe_django in child processes,
    the original directory is added to PYTHONPATH.
    """

    target = os.path.join(os.path.dirname(file_), *components)

    def decorate(func):
        """
        Decorate a function to execute in the given directory.
        """

        @wraps(func)
        def wrapped(*args, **kwargs):
            """
            Execute the function in the given directory.
            """

            oldpath = os.environ.get('PYTHONPATH', '')
            cwd = os.getcwd()

            os.chdir(target)
            os.environ['PYTHONPATH'] = cwd + oldpath

            try:
                return func(*args, **kwargs)
            finally:
                os.chdir(cwd)
                os.environ['PYTHONPATH'] = oldpath

        return wrapped

    return decorate


def in_temporary_directory(func):
    """
    A decorator to run a function in a temporary directory, cleaning up
    afterwards.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Execute the function in the temporary directory."""

        oldpath = os.environ.get('PYTHONPATH', '')
        cwd = os.getcwd()

        target = tempfile.mkdtemp()
        os.chdir(target)
        os.environ['PYTHONPATH'] = cwd + oldpath

        try:
            return func(*args, **kwargs)
        finally:
            os.chdir(cwd)
            os.environ['PYTHONPATH'] = oldpath
            shutil.rmtree(target)

    return wrapped


def run_scenario(application=None, feature=None, scenario=None, **opts):
    """
    Run a scenario and return the exit code and output.

    :param application: The application module to run the features in
    :param feature: The feature to run (without extension)
    :param scenario: The scenario index to run
    :param opts: Additional options to harvest. Single-letter options are
    prefixed with a dash, long options are formatted as --option=value.
    """

    if 'coverage' in sys.modules:
        # If running under coverage, run the subprocess covered too
        rcfile = os.path.join(BASE_DIR, '.coveragerc')
        args = ['coverage', 'run', '--rcfile', rcfile]
    else:
        args = ['python']

    args += ['manage.py', 'harvest']

    if feature:
        feature = '{0}.feature'.format(feature)

    if application:
        if feature:
            args.append('{0}/features/{1}'.format(application, feature))
        else:
            args.append(application)

    if scenario:
        opts['n'] = scenario

    opts.setdefault('v', 3)

    for opt, val in opts.items():
        if len(opt) == 1:
            args.append('-{0}'.format(opt))
            if val:
                args.append(str(val))
        else:
            if val:
                args.append('--{0}={1}'.format(opt, val))
            else:
                args.append('--{0}'.format(opt))

    proc = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text, _ = proc.communicate()
    text = text.decode('utf-8').rstrip()

    return proc.returncode, text
