from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from .forms import UserSignUpForm


# Create your views here.
def userSignup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            for error in list(form.errors.values()):
                print(error)
    else:
        form = UserSignUpForm()

    context = {"form": form}
    return render(request, "users/signup.html", context)
