# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
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

    def handle(self, *test_labels, **options):
        if not options.get('testrunner', None):
            options['testrunner'] = test_runner_class

        return super(Command, self).handle(*test_labels, **options)
