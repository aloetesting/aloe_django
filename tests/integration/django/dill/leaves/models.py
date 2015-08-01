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

from django.db import models


class Garden(models.Model):
    name = models.CharField(max_length=100)
    area = models.IntegerField()
    raining = models.BooleanField(default=None)

    @property
    def howbig(self):
        if self.area < 50:
            return 'small'
        elif self.area < 150:
            return 'medium'
        else:
            return 'big'


class Field(models.Model):
    name = models.CharField(max_length=100)


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden)
    ripe_by = models.DateField()
    fields = models.ManyToManyField(Field)


class Bee(models.Model):
    name = models.CharField(max_length=100)
    pollinated_fruit = models.ManyToManyField(Fruit,
                                              related_name='pollinated_by')


class Goose(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "geese"


class Harvester(models.Model):
    make = models.CharField(max_length=100)
    rego = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden, blank=True, null=True)


class Panda(models.Model):
    """
    Not part of a garden, but still an important part of any good application
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
