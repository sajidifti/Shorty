from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
import os


# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model.
    """

    email = models.EmailField(
        unique=True,
    )

    def __str__(self):
        """
        Return a string representation of the object.
        """
        return self.username
