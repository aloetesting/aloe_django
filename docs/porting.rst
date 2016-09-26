Porting from Lettuce
====================

The following changes are required to port from Lettuce to `aloe_django`:

 * The decorators :func:`creates_model` and :func:`checks_existence` have been
   removed and should be replaced by :func:`writes_model` and
   :func:`tests_existence` respectively. The prototypes passed to the functions
   have now been made consistent.

 * :func:`hashes_data` has been removed. Switch to
   :func:`aloe.tools.guess_types`.

 * Tests are run inside the :class:`aloe_django.TestCase` so a :func:`clean_db`
   hook is no longer required.

 * The :func:`django_url` now expects a step as argument. Instead of
   :code:`django_url(reverse('some-url'))`, you must call
   :code:`django_url(step, reverse('some-url'))`.
   :code:`step.test.live_server_url` can also be used to get the root URL of
   the test server.

 * :code:`LETTUCE_USE_TEST_DATABASE` is not supported, the tests are always run
   using the test database. For a possible speed-up of the test suite, use
   `--keepdb` option from the Django test runner.

 * :code:`LETTUCE_APPS` is not supported. Without any arguments, `harvest` will
   run all the feature files found in packages in the current directory. To run
   a subset of tests, specify the features directories as arguments to
   `harvest`.

 * :code:`--debug-mode` is not supported. Use Django's
   :code:`settings_override` decorator on the test class to set
   :code:`DEBUG=True`.
