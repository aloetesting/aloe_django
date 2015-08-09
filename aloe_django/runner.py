#

"""
Test runner running the Gherkin tests.
"""

import optparse  # pylint:disable=deprecated-module
import os
import sys

import django

from django_nose.plugin import DjangoSetUpPlugin, ResultPlugin, TestReorderer
from django_nose.runner import NoseTestSuiteRunner, _get_plugins_from_settings

from aloe.plugin import GherkinPlugin
from aloe.runner import Runner


def plugin_options(plugin):
    """
    Options that a Nose plugin exports.
    """

    parser = optparse.OptionParser()
    # Copy built-in options to filter them out later
    original_options = parser.option_list[:]

    plugin().options(parser)

    return tuple(
        option
        for option in parser.option_list
        if option not in original_options
    )


class GherkinTestRunner(NoseTestSuiteRunner):
    """
    A runner enabling the Gherkin plugin in nose.
    """

    def run_suite(self, nose_argv):
        """
        Use Gherkin main program to run Nose.
        """

        # Django-nose, upon seeing '-n', copies it to nose_argv but not its
        # argument (e.g. -n 1)
        scenario_indices = []
        for i, arg in enumerate(sys.argv):
            if arg == '-n':
                try:
                    scenario_indices.append(sys.argv[i + 1])
                except KeyError:
                    # -n was last? Nose will complain later
                    pass

        # Remove lone '-n'
        nose_argv = [
            arg for arg in nose_argv if arg != '-n'
        ]
        # Put the indices back into nose_argv
        for indices in scenario_indices:
            nose_argv += ['-n', indices]

        result_plugin = ResultPlugin()
        plugins_to_add = [DjangoSetUpPlugin(self),
                          result_plugin,
                          TestReorderer()]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)

        try:
            django.setup()  # pylint:disable=no-member
        except AttributeError:
            # Setup isn't necessary in Django < 1.7
            pass

        # Set up Gherkin test subclass
        test_class = getattr(django.conf.settings, 'GHERKIN_TEST_CLASS',
                             'aloe_django.TestCase')
        env = os.environ.copy()
        env['NOSE_GHERKIN_CLASS'] = test_class

        Runner(argv=nose_argv, exit=False,
               addplugins=plugins_to_add,
               env=env)
        return result_plugin.result

# Django 1.8 uses argparse, including for 'test' command
if hasattr(NoseTestSuiteRunner, 'options'):
    GherkinTestRunner.options = NoseTestSuiteRunner.options + \
        plugin_options(GherkinPlugin)
else:
    def add_arguments(cls, parser):
        """
        Convert parser (optparse) arguments into argparse.
        """
        super(GherkinTestRunner, cls).add_arguments(parser)

        for option in plugin_options(GherkinPlugin):
            option_strings = str(option).split('/')
            parser.add_argument(
                *option_strings,
                dest=option.dest,
                action=option.action,
                default=option.default,
                help=option.help
            )

    GherkinTestRunner.add_arguments = classmethod(add_arguments)
