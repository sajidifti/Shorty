from django.urls import path
from .views import (
    customSignup,
    customLogin,
    customLogout,
    profile,
    customadmin,
    allusers,
    activate,
    change_password,
    reset_password,
    verifyReset,
    delete_account,
)

urlpatterns = [
    path("signup/", customSignup, name="signup"),
    path("login/", customLogin, name="login"),
    path("logout/", customLogout, name="logout"),
    path("profile/", profile, name="profile"),
    path("deleteaccount/", delete_account, name="deleteaccount"),
    path("customadmin/", customadmin, name="customadmin"),
    path("allusers/", allusers, name="allusers"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("changepassword/", change_password, name="changepassword"),
    path("resetpassword/", reset_password, name="resetpassword"),
    path("reset/<uidb64>/<token>/", verifyReset, name="reset"),
]
