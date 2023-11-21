from django.urls import path
from . import views

urlpatterns = [
    path("warehouse/", views.warehouses, name="warehouses"),
    path("warehouse/profile", views.Warehouse_Profile, name="Warehouse_profile"),
    path("warehouse/editprofile", views.editprofile, name="warehouse_editprofile"),
    # path("warehouse/<int:id>", views.warehouses, name='warehouses'),
    path("warehouse/<int:id>/all_units", views.all_units, name='all_units'),
    path("warehouse/<int:id>/unit/<int:id1>/", views.unit, name='unit'),
    path("warehouse/<int:id>/units/addunit", views.addunit, name='addunit'),
    path("warehouse/<int:id>/units/removeunit/", views.removeunit, name='removeunit'),
    path("warehouse/<int:id>/unit/<int:id1>/editunit", views.editunit, name='editunit'),
    path("warehouse/add", views.addwarehouse, name='add_warehouse'),
    path("warehouse/<int:id>/remove", views.removewarehouse, name='remove_warehouse'),
    path("warehouse/<int:id>/bookings", views.warehouse_bookings, name='warehouse_bookings'),
    path("warehouse/invoice/<int:id>",views.warehouse_invoice, name='warehouse_invoice'),
]   