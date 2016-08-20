# -*- coding: utf-8 -*-
"""
Test mail steps.
"""

import unittest
from tests.util import in_directory, run_scenario


class MailStepsTest(unittest.TestCase):
    """Test mail steps."""

    @in_directory(__file__, 'django', 'bamboo')
    def test_mail_count(self):
        'Mail count is checked through Lettuce steps'

        status, out = run_scenario('leaves', 'count', 1)
        self.assertEqual(status, 0, out)
        status, out = run_scenario('leaves', 'count', 2)
        self.assertEqual(status, 0, out)

        status, out = run_scenario('leaves', 'count', 3)
        self.assertNotEqual(status, 0)
        self.assertIn("Expected to send 1 email(s), got 2.", out)

    @in_directory(__file__, 'django', 'bamboo')
    def test_mail_content(self):
        'Mail content is checked through Lettuce steps'

        status, out = run_scenario('leaves', 'content', 1)
        self.assertEqual(status, 0, out)
        status, out = run_scenario('leaves', 'content', 2)
        self.assertEqual(status, 0, out)

        status, out = run_scenario('leaves', 'content', 4)
        self.assertNotEqual(status, 0)
        self.assertIn("No email contained expected text in the body.", out)
        self.assertIn("Sent emails:", out)
        self.assertIn(
            "Order ID: 10\nName: Fluffy Bear\nQuantity: Quite a few",
            out
        )

        status, out = run_scenario('leaves', 'content', 5)
        self.assertNotEqual(status, 0)
        self.assertIn("An email contained unexpected text in the body.", out)
        self.assertIn("Sent emails:", out)
        self.assertIn(
            "Order ID: 10\nName: Fluffy Badger\nQuantity: Quite a few",
            out
        )

    @in_directory(__file__, 'django', 'bamboo')
    def test_mail_content_html(self):
        """Test steps for checking HTML email content."""

        status, out = run_scenario('leaves', 'content', 3)
        self.assertEqual(status, 0, out)

        status, out = run_scenario('leaves', 'content', 6)
        self.assertNotEqual(status, 0)
        self.assertIn("No email contained the HTML", out)

    @in_directory(__file__, 'django', 'bamboo')
    def test_mail_fail(self):
        'Mock mail failure dies with error'

        status, out = run_scenario('leaves', 'mock-failure', 1)
        self.assertNotEqual(status, 0)
        self.assertIn("SMTPException: Failure mocked by aloe", out)
