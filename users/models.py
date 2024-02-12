from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os


class CustomUser(AbstractUser):
    """
    Custom user model.
    """

    def image_upload_to(self, filename):
        """
        Upload image to user directory.
        """
        return os.path.join("profiles", self.username, filename)

    email = models.EmailField(unique=True)
    activation_email_sent = models.BooleanField(default=False)
    image = models.ImageField(default="default/default.png", upload_to=image_upload_to)

    def save(self, *args, **kwargs):
        """
        Resize the image and delete old image before saving the user instance.
        """
        if self.pk:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if self.image and self.image != old_instance.image:

                # if the old image is not default.png, delete it
                if old_instance.image.name != "default/default.png":
                    old_instance.image.delete(save=False)

        # Resize the new image before saving
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
