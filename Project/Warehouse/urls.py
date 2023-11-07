from django.urls import path
from . import views

urlpatterns = [
    path("warehouse/", views.index, name="index"),
    path("warehouse/profile", views.Warehouse_Profile, name="Warehouse_profile"),
    path("warehouse/editprofile", views.editprofile, name="warehouse_editprofile"),
    # path("warehouse/<int:id>", views.warehouses, name='warehouses'),
    path("warehouse/<int:id>/units", views.units, name='units'),
    path("warehouse/<int:id>/units/addunit", views.addunit, name='addunit'),
    path("warehouse/<int:id>/units/removeunit/", views.removeunit, name='removeunit'),
    path("warehouse/add", views.addwarehouse, name='add_warehouse')
]