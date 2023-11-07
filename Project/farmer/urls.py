from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("farmer/profile",views.farmer_profile,name='farmer_profile'),
    path("farmer/editprofile",views.editprofile,name='farmer_editprofile'),
]