from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
import os


# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model.
    """

    def image_upload_to(self, instance=None):
        """
        Upload image to user directory.
        """
        if instance:
            return os.path.join("profiles", self.username, instance)

        return None

    email = models.EmailField(
        unique=True,
    )

    image = models.ImageField(
        default="default/default.png",
        upload_to=image_upload_to,
    )

    def __str__(self):
        """
        Return a string representation of the object.
        """
        return self.username
