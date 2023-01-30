from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("not_found", views.not_found, name="not_found"),
    path("search", views.search, name="search"),

]

