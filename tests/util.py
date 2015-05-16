"""
Utils for testing
"""

import os
from functools import wraps


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


def getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell."""
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None:
        sts = 0
    if text[-1:] == '\n':
        text = text[:-1]
    return sts, text


def run_scenario(application='', feature='', scenario='', **opts):
    """
    Runs a Django scenario and returns it's output vars
    """
    if application:
        application = ' {0}/features/'.format(application)

    if feature:
        feature = '{0}.feature'.format(feature)

    if scenario:
        scenario = ' -n {0:d}'.format(scenario)

    opts_string = ''
    for opt, val in opts.items():
        if not val:
            val = ''

        opts_string = ' '.join((opts_string, opt, val))

    cmd = 'python manage.py harvest -v 3 {0}{1}{2}{3}'.format(opts_string,
                                                              application,
                                                              feature,
                                                              scenario,
                                                              )

    return getstatusoutput(cmd)
