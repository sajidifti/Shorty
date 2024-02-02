from django.urls import path
from .views import userSignup

urlpatterns = [path("signup",  userSignup, name="signup"),
               ]
