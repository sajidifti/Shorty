from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import UserSignUpForm, UserLoginForm, UserUpdateForm
from .decorators import unauthenticated_users_only, authenticated_users_only, admin_only


# Create your views here.


@unauthenticated_users_only
def customSignup(request):
    """
    Signup view
    """
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            group = Group.objects.get(name="generaluser")
            user.groups.add(group)

            # login(request, user)
            messages.success(
                request,
                f"Account created successfully for {user.username}. We sent a welcome email to {user.email}. Your request to sign up is under review. You will be notified once your account is approved. Thank you!",
            )
            return redirect("login")
        else:
            for field, error_messages in form.errors.items():
                for error_message in error_messages:
                    messages.error(request, error_message)
    else:
        form = UserSignUpForm()

    context = {"form": form}
    return render(request, "users/signup.html", context)


@authenticated_users_only
def customLogout(request):
    """
    Logout view
    """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


@unauthenticated_users_only
def customLogin(request):
    """
    Login view
    """
    next_url = request.GET.get("next")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        username = form.data.get("username")
        user = get_user_model().objects.filter(username=username).first()

        if user and not user.is_active:
            messages.error(request, "Your account is inactive.")
            return redirect("login")
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None and user.is_active:
                login(request, user)
                # messages.info(request, f"Logged in as {user.username}")

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
            else:
                messages.error(request, "Your account is inactive.")
                return redirect("login")
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


@login_required
def profile(request):
    """
    Profile view
    """
    username = request.user.username
    user = get_user_model().objects.filter(username=username).first()

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            for field, error_messages in form.errors.items():
                for error_message in error_messages:
                    messages.error(request, error_message)
            return redirect("profile")

    else:  # GET request
        form = UserUpdateForm(instance=user)

    return render(request, "users/profile.html", {"form": form})


@login_required
@admin_only
def customadmin(request):
    """
    Admin view
    """
    return render(request, "users/admin.html")


@login_required
@admin_only
def allusers(request):
    """
    allusers view
    """
    return render(request, "users/users.html")
