from django.contrib.auth.decorators import login_required
from users.decorators import admin_only
from django.shortcuts import render, redirect, get_object_or_404

import random
import string
from django.contrib import messages
from .forms import URLShortenerForm
from .models import URLShortener


def generate_random_custom_url(length=6):
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def home(request):
    allerrors = ""

    if request.method == "POST":
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            custom_url = form.cleaned_data["custom_url"]

            if not custom_url:
                custom_url = generate_random_custom_url()

                while URLShortener.objects.filter(custom_url=custom_url).exists():
                    custom_url = generate_random_custom_url()

            else:
                url_shortener = form.save(commit=False)
                url_shortener.user = request.user
                url_shortener.custom_url = custom_url
                url_shortener.save()

                messages.success(request, "URL shortened successfully.")
                return redirect("shortened", pk=url_shortener.pk)
        else:
            for field, error_messages in form.errors.items():
                for error_message in error_messages:
                    allerrors = allerrors + " " + error_message
            messages.error(request, allerrors)
            return redirect("home")

    form = URLShortenerForm()
    return render(request, "main/index.html", {"form": form})


@login_required
def myurls(request):
    return render(request, "main/myURLs.html")


@login_required
@admin_only
def allurls(request):
    return render(request, "main/allURLs.html")


@login_required
def shortened(request, pk):
    url_shortener = get_object_or_404(URLShortener, pk=pk)
    return render(request, "main/shortened.html", {"url_shortener": url_shortener})
