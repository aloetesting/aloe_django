# -*- coding: utf-8 -*-
"""
Management command to run the Gherkin tests.
"""

from django.conf import settings
from django.core.management.commands.test import Command as TestCommand
from django.test.utils import get_runner

# pylint:disable=invalid-name
test_runner_class = getattr(settings, 'GHERKIN_TEST_RUNNER',
                            'aloe_django.runner.GherkinTestRunner')

TestRunner = get_runner(settings, test_runner_class)
# pylint:enable=invalid-name


class Command(TestCommand):
    """Django command: harvest"""

    help = "Run Gherkin tests"

    requires_system_checks = False

    def run_from_argv(self, argv):
        """
        Set the default Gherkin test runner for its options to be parsed.
        """

        self.test_runner = test_runner_class
        super(Command, self).run_from_argv(argv)

    def handle(self, *test_labels, **options):
        """
        Set the default Gherkin test runner.
        """
        if not options.get('testrunner', None):
            options['testrunner'] = test_runner_class

        return super(Command, self).handle(*test_labels, **options)
