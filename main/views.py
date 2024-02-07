from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import admin_only

# Create your views here.
@login_required
def home(request):
    return render(request, "main/index.html")

@login_required
def myurls(request):
    return render(request, "main/myURLs.html")

@login_required
@admin_only
def allurls(request):
    return render(request, "main/allURLs.html")

@login_required
def shortened(request):
    return render(request, "main/shortened.html")
