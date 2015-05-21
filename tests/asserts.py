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

import re
import sys
from contextlib import contextmanager
from difflib import ndiff
from io import StringIO
from itertools import tee

from nose.tools import assert_equals


@contextmanager
def capture_output():
    """
    Capture stdout and stderr for asserting their values
    """

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        yield sys.stdout, sys.stderr

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def yield_transitions(iterable):
    """
    Yield the tuples of (index, value) indicating the transitions in the
    iterable
    """

    register = None
    last_index = 0

    for i, elem in enumerate(iterable):
        if elem != register:
            if register:
                yield (last_index, i, register)

            register = elem
            last_index = i

    yield (last_index, i + 1, register)


def assert_lines_with_traceback(one, other):
    lines_one = one.splitlines()
    lines_other = other.splitlines()
    regex = re.compile('File "([^"]+)", line \d+, in.*')

    error = '%r should be in traceback line %r.\nFull output was:\n' + one
    for line1, line2 in zip(lines_one, lines_other):
        if regex.search(line1) and regex.search(line2):
            found = regex.search(line2)

            filename = found.group(1)
            params = filename, line1
            assert filename in line1, error % params

        else:
            assert_equals(line1, line2)
