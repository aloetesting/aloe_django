"""
Test running features in a freshly created Django application.
"""

from __future__ import absolute_import, print_function

import os
import shutil
import subprocess
import unittest

from tests.util import in_temporary_directory, run_scenario


def find_file(name):
    """
    Find a file with the specified name somewhere in the current directory.
    """

    for dirpath, dirnames, filenames in os.walk('.'):
        if name in dirnames + filenames:
            return os.path.join(dirpath, name)

    raise ValueError("File named {0} not found.".format(name))


# Directory with source files to copy
SOURCE_DIR = os.path.join(
    os.path.dirname(__file__), 'django', 'lychee')


class DjangoAppTest(unittest.TestCase):
    """Test running features in a freshly created Django application."""

    @in_temporary_directory
    def test_django_app(self):
        """Create a stock Django app and test running features for it."""

        # Create the project and the application
        subprocess.check_call(('django-admin', 'startproject', 'lychee'))
        os.chdir('lychee')
        subprocess.check_call(('django-admin', 'startapp', 'lychee_app'))

        # Add the created application and Aloe-Django to installed
        with open(find_file('settings.py'), 'a') as settings:
            settings.write("""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite',
    }
}

INSTALLED_APPS += ('aloe_django', 'lychee_app')
""")

        app_root = find_file('lychee_app')

        # Add a view and a template
        with open(find_file('views.py'), 'a') as views:
            views.write("""
from django.views.generic import TemplateView
class HelloView(TemplateView):
    template_name = 'hello.html'
""")

        templates_dir = os.path.join(app_root, 'templates')
        os.mkdir(templates_dir)
        with open(os.path.join(templates_dir, 'hello.html'), 'w') as template:
            template.write("World!")

        # Add the view to URLs
        with open(find_file('urls.py'), 'a') as urls:
            urls.write("""
from lychee_app.views import HelloView
urlpatterns += [url(r'^hello/', HelloView.as_view())]
""")

        # Create a features directory
        features_dir = os.path.join(app_root, 'features')
        os.mkdir(features_dir)

        # Copy in a feature and steps for it
        for filename in (
                'hello.feature',
                '__init__.py',
                'steps.py',
        ):
            shutil.copyfile(
                os.path.join(SOURCE_DIR, filename),
                os.path.join(features_dir, filename),
            )

        ret, output = run_scenario()

        print(output)

        self.assertEqual(ret, 0, "Should succeed")
        self.assertIn("Ran 1 test", output)
