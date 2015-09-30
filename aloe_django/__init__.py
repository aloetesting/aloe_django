# -*- coding: utf-8 -*-

"""
Django integration for Aloe
"""

from django.core.exceptions import ImproperlyConfigured


try:
    # In Django 1.8, transparently serving static files was moved from
    # LiveServerTestCase to StaticLiveServerTestCase
    try:
        # pylint:disable=no-name-in-module
        from django.contrib.staticfiles.testing import (
            StaticLiveServerTestCase as LiveServerTestCase)
        # pylint:enable=no-name-in-module
    except ImportError:
        from django.test import LiveServerTestCase

    from aloe.testclass import TestCase as AloeTestCase

    # pylint:disable=abstract-method
    # Pylint cannot infer methods dynamically added by Aloe
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
