from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new", views.newPage, name="newPage"),
    path("wiki/random", views.random, name="random"),
    path("wiki/edit/<str:entryName>", views.editPage, name="editPage"),
    path("wiki/<str:entryName>", views.entryShow, name="entryShow")
]
