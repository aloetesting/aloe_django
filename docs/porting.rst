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
   hook is no longer required
