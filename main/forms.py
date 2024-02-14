from django import forms
from .models import URLShortener
import random
import string


def generate_random_custom_url(length=6):
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class URLShortenerForm(forms.ModelForm):
    class Meta:
        model = URLShortener
        fields = ["original_url", "custom_url"]


    def clean(self):
        cleaned_data = super().clean()
        original_url = cleaned_data.get("original_url")
        custom_url = cleaned_data.get("custom_url")

        if custom_url:
            if URLShortener.objects.filter(custom_url=custom_url).exists():
                self.add_error("custom_url", "Custom URL not available.")
        else:
            custom_url = generate_random_custom_url()
            while URLShortener.objects.filter(custom_url=custom_url).exists():
                custom_url = generate_random_custom_url()

            cleaned_data["custom_url"] = custom_url

        # if URLShortener.objects.filter(original_url=original_url).exists():
        #     self.add_error("original_url", "URL already exists.")

        return cleaned_data
