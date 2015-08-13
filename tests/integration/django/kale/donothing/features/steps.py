# -*- coding: utf-8 -*-
#

from aloe import step


@step
def passes(self):
    """Step passes"""


@step
def fails(self):
    """Step fails"""

    raise AssertionError("This step fails")
