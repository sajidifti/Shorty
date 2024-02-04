from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import UserSignUpForm, UserLoginForm
from .decorators import unauthenticated_users_only, authenticated_users_only


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


@authenticated_users_only
def customLogout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


@unauthenticated_users_only
def customLogin(request):
    next_url = request.GET.get("next")

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

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
        else:
            for field, error_messages in form.errors.items():
                for error_message in error_messages:
                    if (
                        field == "captcha"
                        and error_message == "This field is required."
                    ):
                        custom_error_message = "You must pass the reCAPTCHA test. "
                        messages.error(request, custom_error_message)
                    else:
                        messages.error(request, error_message)

            # Store form data in session only if there's a validation error
            request.session["login_form_data"] = form.cleaned_data
            return redirect(request.path)

    else:
        form = UserLoginForm()
        # Repopulate the form with prevoius form data
        form_data = request.session.pop("login_form_data", {})
        form = UserLoginForm(request, initial=form_data)

    return render(request, "users/login.html", {"form": form})
