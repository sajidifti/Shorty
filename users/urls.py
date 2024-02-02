from django.urls import path
from .views import customSignup, customLogin, customLogout

urlpatterns = [
    path("signup", customSignup, name="signup"),
    path("login", customLogin, name="login"),
    path("logout", customLogout, name="logout"),
]
