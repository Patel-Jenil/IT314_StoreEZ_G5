from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("farmer/profile",views.farmer_profile,name='farmer_profile'),
    path("farmer/editprofile",views.editprofile,name='farmer_editprofile'),
    path("farmer/currentbooking",views.currentbooking,name='farmer_currentbooking'),
    path("farmer/previousbooking",views.previousbooking,name='farmer_previousbooking'),
    path("farmer/book/<int:id>",views.book,name='book'),
    path("farmer/search",views.search,name='search'),
]