from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, first_name='', last_name='', password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError("User must have a username.")

        user = self.model(
            email=self.normalize_email(email),  # all letters in email to lower case
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superadmin = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    # user types
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def get_account(self):
        return self

    def time_in_range(self, time, begin, end):
        if begin < time < end:
            return True
        return False

    def user_is_free(self, date, start, end):
        appointments = self.appointment_set.filter(date=date)

        for appt in appointments:
            if (self.time_in_range(start, appt.start_time, appt.end_time) or
                    self.time_in_range(end, appt.start_time, appt.end_time)):
                return False

            if start == appt.start_time or end == appt.end_time:
                return False
            # ako terminot preklopuva drug termin
            if start < appt.start_time and appt.end_time < end:
                return False

        return True
