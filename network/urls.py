
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("profile/<str:userProfile>", views.profile, name="profile"),
    path("following", views.following, name="following"),
               
    # API ROUTES
    path("toggle_like", views.toggle_like, name="toggle_like"),
    path("save_post", views.save_post, name="save_post")
]
