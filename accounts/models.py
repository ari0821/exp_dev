# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class ExpUserManager(BaseUserManager):
    def create_user(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        if request_data.get('profile'):
            profile = request_data['profile']
        else:
            profile = ""

        user = self.model(
            username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            last_login=now,
            date_joined=now,
            profile=profile,
        )

        user.set_password(request_data['password'])

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        request_data = {
            'username': username,
            'email': email,
            'password': password
        }
        user = self.create_user(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class ExpUser(AbstractBaseUser):
    username    = models.CharField(_('username'), max_length=30, unique=True)
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    tennant_id  = models.CharField(_('tenant_id'), max_length=32, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    profile     = models.CharField(_('profile'), max_length=255, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = ExpUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def user_has_perm(user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = 'api_user'
        swappable = 'AUTH_USER_MODEL'

from django.contrib.auth import get_user_model

class EmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and  user.check_password(password):
                return user
        return None
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
