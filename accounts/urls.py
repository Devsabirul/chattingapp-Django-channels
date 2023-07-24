from django.urls import path
from .views import *

urlpatterns = [
    path("login", signin, name="signin"),
    path("register", signup, name="signup"),
    path("logout", logout_, name="logout_"),
]
