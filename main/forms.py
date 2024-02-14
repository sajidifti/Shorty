from django import forms
from .models import URLShortener


class URLShortenerForm(forms.ModelForm):
    class Meta:
        model = URLShortener
        fields = ["original_url", "custom_url"]

    def clean(self):
        cleaned_data = super().clean()
        original_url = cleaned_data.get("original_url")
        custom_url = cleaned_data.get("custom_url")

        if URLShortener.objects.filter(original_url=original_url).exists():
            self.add_error("original_url", "URL already exists.")

        if URLShortener.objects.filter(custom_url=custom_url).exists():
            self.add_error("custom_url", "Custom URL not available.")

        return cleaned_data
