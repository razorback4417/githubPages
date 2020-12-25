from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
               
    path("home", views.home, name="home"),
    path("becomeTutor", views.becomeTutor, name="becomeTutor"),
    path("findTutor", views.findTutor, name="findTutor"),
    path("requests", views.requests, name="requests"),
    path("editrequest", views.editrequest, name="editrequest")
]
