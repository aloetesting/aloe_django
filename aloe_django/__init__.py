# -*- coding: utf-8 -*-

"""
Django integration for Aloe
"""

from django.core.exceptions import ImproperlyConfigured


try:
    # In Django 1.8, transparently serving static files was moved from
    # LiveServerTestCase to StaticLiveServerTestCase
    # pylint:disable=no-name-in-module,import-error
    try:
        from django.contrib.staticfiles.testing import (
            StaticLiveServerTestCase as LiveServerTestCase)
    except ImportError:
        try:
            from django.test import LiveServerTestCase
        except ImportError:
            from django_liveserver.testcases import LiveServerTestCase
    # pylint:enable=no-name-in-module,import-error

    from aloe.testclass import TestCase as AloeTestCase

    # pylint:disable=abstract-method
    # Pylint cannot infer methods dynamically added by Aloe
    # pylint:disable=too-many-ancestors
    # Confused by the multitude of the import variants above?
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
    try:
        # In Django < 1.9, live_server_url is an instance property, but still
        # works when called on the class
        return testclass.live_server_url.__get__(testclass)
    except AttributeError:
        return testclass.live_server_url
