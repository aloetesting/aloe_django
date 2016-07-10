# -*- coding: utf-8 -*-

"""
Django integration for Aloe
"""

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin  # pylint:disable=import-error

from django.core.exceptions import ImproperlyConfigured


try:
    from django.contrib.staticfiles.testing import (
        StaticLiveServerTestCase as LiveServerTestCase)

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


def django_url(step, url=None):
    """
    The URL for a page from the test server.

    :param step: A Gherkin step
    :param url: If specified, the relative URL to append.
    """

    base_url = step.test.live_server_url

    if url:
        return urljoin(base_url, url)
    else:
        return base_url
