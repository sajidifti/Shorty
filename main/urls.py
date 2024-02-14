from django.urls import path
from .views import home, myurls, allurls, shortened

urlpatterns = [
    path("", home, name="home"),
    path("myurls/", myurls, name="myurls"),
    path("allurls/", allurls, name="allurls"),
    path("shortened/<int:pk>/", shortened, name="shortened"),
]
