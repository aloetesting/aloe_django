Porting from Lettuce
====================

The following changes are required to port from Lettuce to `aloe_django`:

 * The deprecated decorators :func:`creates_model` and :func:`checks_existence`
   have been removed and should be replaced by :func:`writes_model` and
   :func:`tests_existence` respectively. The prototypes passed to the functions
   have now been made consistent.

 * :func:`hashes_data` has been removed. Switch to
   :func:`aloe.tools.guess_types`.

 * Tests are run inside the :class:`aloe_django.TestCase` so a :func:`clean_db`
   hook is no longer required.

 * The :func:`django_url` now expects a step as argument and returns the root
   url (instead of `django_url(reverse('some-url'))`, you must call
   `django_url(step) + reverse('some-url')`).

 * Lettuce-specific settings are not supported. Most of the functionality can
   be achieved by customizing the test class using `GHERKIN_TEST_CLASS` or
   by the same methods as for the regular Python tests.

 * `--debug-mode` is not supported. Use Django's `settings_override` decorator
   on the test class to set `DEBUG=True`.
