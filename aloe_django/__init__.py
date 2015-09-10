# -*- coding: utf-8 -*-
#

"""
Django integration for Aloe
"""

from django.core.exceptions import ImproperlyConfigured

try:
    import django.test

    from aloe.testclass import TestCase as AloeTestCase

    class TestCase(django.test.LiveServerTestCase, AloeTestCase):
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
