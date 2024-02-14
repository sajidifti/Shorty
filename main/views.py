from django.contrib.auth.decorators import login_required
from users.decorators import admin_only
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from .forms import URLShortenerForm
from .models import URLShortener


@login_required
def home(request):
    allerrors = ""

    if request.method == "POST":
        form = URLShortenerForm(request.POST)
        if form.is_valid():

            url_shortener = form.save(commit=False)
            url_shortener.user = request.user
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


def redirect_to_original(request, custom_url):
    try:
        url_shortener = URLShortener.objects.get(custom_url=custom_url)
        return redirect(url_shortener.original_url)
    except URLShortener.DoesNotExist:
        raise Http404("Shortened URL does not exist.")


@login_required
@admin_only
def allurls(request):
    if request.method == "POST":
        url_id = request.POST.get("url_id")
        url_shortener = get_object_or_404(URLShortener, pk=url_id)
        url_shortener.delete()
        messages.success(request, "URL deleted successfully.")
        return redirect("allurls")

    urls = URLShortener.objects.all()
    return render(request, "main/allURLs.html", {"urls": urls})


@login_required
def myurls(request):
    user = request.user

    if request.method == "POST":
        url_id = request.POST.get("url_id")
        url_shortener = get_object_or_404(URLShortener, pk=url_id)
        url_shortener.delete()
        messages.success(request, "URL deleted successfully.")
        return redirect("myurls")

    urls = URLShortener.objects.filter(user=user)

    return render(request, "main/myURLs.html", {"urls": urls})


@login_required
def shortened(request, pk):
    user = request.user
    url_shortener = get_object_or_404(URLShortener, pk=pk)
    url_user = url_shortener.user

    if user != url_user:
        return redirect("home")

    return render(request, "main/shortened.html", {"url_shortener": url_shortener})
