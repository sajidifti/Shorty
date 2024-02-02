from django.urls import path
from .views import home, custom

urlpatterns = [
    path("", home, name="home"),
    path("custom/", custom, name="custom"),
]
