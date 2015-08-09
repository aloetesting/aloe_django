# -*- coding: utf-8 -*-
#

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from lxml import html

from nose.tools import assert_equals
from aloe import world, before, step
from django.test.client import Client


@before.all
def set_client():
    world.browser = Client()


@step(r'I navigate to "(.*)"')
def given_i_navigate_to_group1(step, url):
    # TODO: Make this a property of the step
    testclass = step.testclass
    base_url = testclass.live_server_url.__get__(testclass)

    # Django 1.4 returns str, not unicode
    try:
        base_url = base_url.decode()
    except AttributeError:
        pass

    url = urljoin(base_url, url)
    assert_equals(url, 'http://localhost:8081/')

    raw = urlopen(url).read()
    world.dom = html.fromstring(raw)


@step(r'I see the title of the page is "(.*)"')
def then_i_see_the_title_of_the_page_is_group1(step, title):
    element = world.dom.xpath("//head/title")[0]
    assert_equals(element.text, title)


@step(r'I look inside de 1st paragraph')
def when_i_look_inside_de_1st_paragraph(step):
    world.element = world.dom.cssselect("p")[0]


@step(r'I see it has no attributes')
def then_i_see_it_has_no_attributes(step):
    assert not world.element.attrib, \
        'the <p> tag should have no attributes'


@step(r'its content is "(.*)"')
def and_that_its_content_is_group1(step, content):
    assert_equals(world.element.text, content)


@step(r'When I look inside de 1st header')
def when_i_look_inside_de_1st_header(step):
    world.element = world.dom.cssselect("h1")[0]


@step(r'And that its id is "(.*)"')
def and_that_its_id_is_group1(step, id):
    assert_equals(world.element.attrib['id'], id)
