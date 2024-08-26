from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry_func, name="entry"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save_entry, name="save")
]
