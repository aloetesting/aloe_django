# -*- coding: utf-8 -*-

"""
Django integration for Aloe
"""

from django.core.exceptions import ImproperlyConfigured

# To enable static files transparently, uses the StaticLiveServerTestCase,
# available in Django 1.8, or fall back to default LiveServerTestCase, that
# does the same as the first in older django versions
try:
    from django.contrib.staticfiles.testing import (
            StaticLiveServerTestCase as LiveServerTestCase)
except ImportError:
    from django.test import LiveServerTestCase

try:

    from aloe.testclass import TestCase as AloeTestCase

    class TestCase(LiveServerTestCase, AloeTestCase):
        """
        Base test class for Django Gherkin tests.

        Inherits from both :class:`aloe.testclass.TestCase` and
        :class:`django.test.LiveServerTestCase`.
        """

        pass

except (ImproperlyConfigured, ImportError):
    # Probably running tests for Aloe-Django and Django isn't configured
    pass


def django_url(step):
    """
    The base URL for the test server.

    :param step: A Gherkin step
    """

    testclass = step.testclass
    return testclass.live_server_url.__get__(testclass)
