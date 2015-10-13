"""
Steps for putting in a stock application to test.
"""

from contextlib import contextmanager

from django.test import Client

from aloe import around, step, world


@around.all
@contextmanager
def with_client():
    world.client = Client()
    yield
    delattr(world, 'client')


@step(r'I visit site page "([^"]+)"')
def visit_page(self, page):
    world.response = world.client.get(page)


@step(r'I should see "([^"]+)"')
def see_text(self, text):
    assert text in world.response.content.decode(), world.response
