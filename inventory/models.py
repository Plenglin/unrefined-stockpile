from django.core.exceptions import ValidationError
from django.db import models
from enum import Enum


CONTAINER_TYPE_CHOICES = [
    ('BX', 'box'),
    ('SL', 'shelf'),
    ('DR', 'drawer'),
    ('RM', 'room'),
    ('SR', 'surface'),
    ('WL', 'wall'),
    ('OT', 'other')
]


class Container(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)
    description = models.TextField('description', blank=True)
    location = models.TextField('location', blank=True)
    container_type = models.CharField(
        max_length=2,
        choices=CONTAINER_TYPE_CHOICES,
        blank=False,
        default='BX'
    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.location != '':
            return f'{self.name} at {self.location}'
        return self.name

    def __repr__(self):
        return f'Container#{self.id}({self.name})'

    def clean(self):
        # Ensure there are no circular parents
        node = self
        while node.parent is not None:
            node = node.parent
            if node == self:
                raise ValidationError('Containers cannot be circularly contained within themselves... with current technology.')


class ItemTag(models.Model):
    name = models.CharField(verbose_name='name', max_length=30, primary_key=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'ItemTag({self.name})'


class Item(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)
    description = models.TextField('description', blank=True)
    quantity = models.IntegerField('quantity', default=0)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(ItemTag)

    def __str__(self):
        return f'{self.name} × {self.quantity}'

    def __repr__(self):
        return f'Item#{self.id}({self.name})'