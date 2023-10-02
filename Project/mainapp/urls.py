from django.urls import path
from . import views

urlpatterns = [
    path("", views.temp, name="temp"),
]