Harvest
=======

.. toctree::
    :maxdepth: 2

The :command:`harvest` command exposed via Django's :command:`manage.py`
can be used to run Aloe tests under Django with the correct settings.

``harvest`` accepts the same flags as ``nosetests`` and so these are not
extensively documented here.

.. program:: harvest

.. option:: <feature>

    Run only the specified feature files.

.. option:: -n N[,N...]

    Only run the specified scenarios (by number, 1-based) in each
    feature. Makes sense when only specifying one feature to run, for example::

        aloe features/calculator.feature -n 1
