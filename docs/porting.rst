Porting from Lettuce
====================

The following changes are required to port from Lettuce to `aloe_django`:

 * The deprecated decorators :func:`creates_model` and :func:`checks_existence`
   have been removed and should be replaced by :func:`writes_model` and
   :func:`tests_existence` respectively. The prototypes passed to the functions
   have now been made consistent.

 * :func:`hashes_data` used to accept a :class:`aloe.Step` or
   :func:`aloe.Step.hashes`. It now only accepts the latter.
