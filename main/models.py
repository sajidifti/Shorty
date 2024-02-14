from django.db import models
from django.conf import settings

class URLShortener(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_url = models.URLField(unique=True)
    custom_url = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Original URL: {self.original_url}, Custom URL: {self.custom_url}"
