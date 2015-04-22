"""
Utils for testing
"""

import os
from functools import wraps

import commands


def in_directory(file_, *components):
    """
    A decorator to execute a function in a directory relative to the current
    file.

    __file__ must be passed as first argument to determine the directory to
    start with.
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

            cwd = os.getcwd()
            os.chdir(target)
            try:
                return func(*args, **kwargs)
            finally:
                os.chdir(cwd)

        return wrapped

    return decorate


def run_scenario(application='', feature='', scenario='', **opts):
    """
    Runs a Django scenario and returns it's output vars
    """
    if application:
        application = ' {0}/features/'.format(application)

    if feature:
        feature = '{0}.feature'.format(feature)

    if scenario:
        scenario = ' -s {0:d}'.format(scenario)

    opts_string = ''
    for opt, val in opts.iteritems():
        if not val:
            val = ''

        opts_string = ' '.join((opts_string, opt, val))

    cmd = 'python manage.py harvest -v 3 -T {0}{1}{2}{3}'.format(opts_string,
                                                                 application,
                                                                 feature,
                                                                 scenario,
                                                                 )
    return commands.getstatusoutput(cmd)
