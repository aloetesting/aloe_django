# -*- coding: utf-8 -*-
# Aloe-Django - Package for testing Django applications with Aloe
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Management command to run the Gherkin tests.
"""

from django.conf import settings
from django.test.utils import get_runner

from django.core.management.commands.test import Command as TestCommand

test_runner_class = getattr(settings, 'GHERKIN_TEST_RUNNER',
                            'aloe_django.runner.GherkinTestRunner')

TestRunner = get_runner(settings, test_runner_class)


class Command(TestCommand):
    help = "Run Gherkin tests"

    option_list = TestCommand.option_list + \
        tuple(getattr(TestRunner, 'options', []))

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

    def execute(self, *args, **options):
        """
        Fix option parsing between Django 1.8 (argparse) and
        Django-nose (optparse).
        """
        options['verbosity'] = int(options['verbosity'])
        return super(Command, self).execute(*args, **options)
