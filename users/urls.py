from django.urls import path
from .views import customSignup, customLogin, customLogout, profile, customadmin, allusers, activate

urlpatterns = [
    path("signup/", customSignup, name="signup"),
    path("login/", customLogin, name="login"),
    path("logout/", customLogout, name="logout"),
    path("profile/", profile, name="profile"),
    path("customadmin/", customadmin, name="customadmin"),
    path("allusers/", allusers, name="allusers"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
