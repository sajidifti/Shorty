from django.urls import path
from .views import home, myurls, allurls, shortened, redirect_to_original

urlpatterns = [
    path("", home, name="home"),
    path("myurls/", myurls, name="myurls"),
    path("allurls/", allurls, name="allurls"),
    path("shortened/<int:pk>/", shortened, name="shortened"),
    path("<str:custom_url>/", redirect_to_original, name="redirect_to_original"),
]
