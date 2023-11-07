from django.urls import path
from . import views

urlpatterns = [
    path("warehouse/", views.index, name="index"),
    path("warehouse/profile", views.Warehouse_Profile, name="Warehouse_profile"),
    path("warehouse/editprofile", views.editprofile, name="warehouse_editprofile"),
    # path("warehouse/<int:id>", views.warehouses, name='warehouses'),
    path("warehouse/units/<int:id>", views.units, name='units'),
    path("warehouse/units/addunit/<int:id>", views.addunit, name='addunit'),
    path("warehouse/units/removeunit/<int:id>", views.removeunit, name='removeunit'),
    
]