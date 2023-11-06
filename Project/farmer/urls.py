from django.contrib import admin
from django.urls import path
from farmer.views import *

urlpatterns = [
    path("farmer/profile",display,name='farmerdis'),
    path("farmer/edit",edit,name='edit'),
]