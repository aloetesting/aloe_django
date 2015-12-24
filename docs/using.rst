Using Aloe with Django
======================

Add ``aloe_django`` to your project's ``INSTALLED_APPS``.

If you want to run ordinary Python tests using Nose, you should also add
`django_nose`_ to ``INSTALLED_APPS`` and set the setting ``TEST_RUNNER`` to
``django_nose.NoseTestSuiteRunner``.

.. attribute:: GHERKIN_TEST_CLASS = 'aloe_django.TestCase'

    An :class:`aloe.testclass.TestCase` to use to run the tests.

    By default this will be :class:`aloe_django.TestCase`, but you can
    inherit it to change the behaviour of items such as the Django test server
    (e.g. to enable a threaded server).

    See :ref:`Extending Aloe’s TestCase <aloe:extending_aloe>` for more details.

.. attribute:: GHERKIN_TEST_RUNNER = 'aloe_django.runner.GherkinTestRunner'

    A Nose test runner used when running :command:`manage.py harvest`.

.. autoclass:: aloe_django.TestCase()
    :members:

.. autofunction:: aloe_django.django_url
