"""
Test runner running the Gherkin tests.
"""

import os

import django

from django_nose.plugin import DjangoSetUpPlugin, ResultPlugin, TestReorderer
from django_nose.runner import NoseTestSuiteRunner, _get_plugins_from_settings

from aloe.runner import Runner

from aloe_django import TestCase


class GherkinTestRunner(NoseTestSuiteRunner):
    """
    A runner enabling the Gherkin plugin in nose.
    """

    def run_suite(self, nose_argv):
        """
        Use Gherkin main program to run Nose.
        """

        result_plugin = ResultPlugin()
        plugins_to_add = [DjangoSetUpPlugin(self),
                          result_plugin,
                          TestReorderer()]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)

        try:
            django.setup()
        except AttributeError:
            # Setup isn't necessary in Django < 1.7
            pass

        # Set up Gherkin test subclass
        env = os.environ.copy()

        try:
            test_class_name = django.conf.settings.GHERKIN_TEST_CLASS
        except AttributeError:
            # TODO: How to reference the full class name?
            test_class_name = TestCase.__module__ + '.' + TestCase.__name__

        env['NOSE_GHERKIN_CLASS'] = test_class_name

        Runner(argv=nose_argv, exit=False,
               addplugins=plugins_to_add,
               env=env)
        return result_plugin.result
