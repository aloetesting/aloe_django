# Aloe-Django - Package for testing Django applications with Aloe
# Copyright (C) <2015> Alexey Kotlyarov <a@koterpillar.com>
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

"""
A minimal Django app, just one file.

See: http://olifante.blogs.com/covil/2010/04/minimal-django.html
"""

import os

from django.conf.urls.defaults import patterns
from django.core.mail import send_mail
from django.http import HttpResponse

filepath, extension = os.path.splitext(__file__)
ROOT_URLCONF = os.path.basename(filepath)
INSTALLED_APPS = (
    'aloe_django',
)


def mail(request):
    send_mail('Subject here', 'Here is the message.', 'from@example.com',
              ['to@example.com'], fail_silently=False)
    return HttpResponse('Mail has been sent')

urlpatterns = patterns('', (r'^mail/$', mail))
