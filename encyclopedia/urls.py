from django.urls import path, include

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:name>/", views.entryTest, name="entryTest"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("createR", views.createR, name="createR"),
    path("random", views.randomPage, name="random"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("editPage", views.editPage, name="editPage"),
]
