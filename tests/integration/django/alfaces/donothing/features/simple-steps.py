# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import urllib2
from lxml import html
from nose.tools import assert_equals
from aloe import world, before, step
from aloe_django import django_url
from django.test.client import Client

@before.all
def set_client():
    world.browser = Client()

@step(r'I navigate to "(.*)"')
def given_i_navigate_to_group1(step, url):
    url = django_url(url)
    assert_equals(url, 'http://127.0.0.1:8000/')

    raw = urllib2.urlopen(url).read()
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
