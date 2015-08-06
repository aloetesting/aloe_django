Using Aloe with Django
======================

Add ``aloe_django`` to your project's ``INSTALLED_APPS``.

If you're not already using `django_nose`_ you should also add this to
``INSTALLED_APPS`` and set the setting :attr:`TEST_RUNNER` to
``django_nose.NoseTestSuiteRunner``.

.. code-block:: python

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    # GHERKIN_TEST_CLASS =  # a TestCase used to execute Gherkin tests
    # GHERKIN_TEST_RUNNER =  # Nose test runner

.. attribute:: GHERKIN_TEST_CLASS = 'aloe_django.TestCase'

    An :class:`aloe.testclass.TestCase` to use to run the tests.

    By default this will be :class:`aloe_django.TestCase`, but you can
    inherit it to change the behaviour of items such as the Django test server
    (e.g. to enable a threaded server).

    See :ref:`Extending Aloe’s TestCase` for more details.

.. attribute:: GHERKIN_TEST_RUNNER = 'aloe_django.runner.GherkinTestRunner'

.. autoclass:: aloe_django.TestCase()
    :members:
