# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager



class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=10,
                                    error_messages={
                                        'unique': "A user with that phone number already exists."
                                    })
    address = models.TextField(blank=True)
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()
