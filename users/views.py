from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import UserSignUpForm, UserLoginForm
from .decorators import unauthenticated_users_only


# Create your views here.


@unauthenticated_users_only
def customSignup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Account created successfully for {user.username}"
            )
            return redirect("home")
        else:
            for error in list(form.errors.values()):
                # print(error)
                messages.error(request, error)
    else:
        form = UserSignUpForm()

    context = {"form": form}
    return render(request, "users/signup.html", context)


@login_required
def customLogout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


@unauthenticated_users_only
def customLogin(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {user.username}")
                return redirect("home")
        else:
            for error in list(form.errors.values()):
                # print(error)
                messages.error(request, error)

    form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})
