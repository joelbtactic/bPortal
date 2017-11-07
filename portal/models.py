# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Layout(models.Model):

    module = models.CharField(max_length=50)
    VIEW_CHOICES = (
        ('list', 'List View'),
        ('edit', 'Edit View'),
        ('create', 'Create View'),
    )
    view = models.CharField(max_length=30, choices=VIEW_CHOICES)
    fields = models.TextField()

    class Meta:
        unique_together = ("module", "view")

    def __str__(self):
        return self.module + ' - ' + self.view + ' view'

class Role(models.Model):

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

class RolePermission(models.Model):

    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    module = models.CharField(max_length=50)
    ACTION_CHOICES = (
        ('read', 'Read'),
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    grant = models.BooleanField()
    order = models.IntegerField()

    class Meta:
        unique_together = ("role", "module", "action")

    def __str__(self):
        return self.role.name + ' - ' + self.action.title() + ' ' + self.module

class RoleUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.role.name + ' - ' + self.user.username
