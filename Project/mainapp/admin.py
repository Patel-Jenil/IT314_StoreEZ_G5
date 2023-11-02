from django.contrib import admin

# Register your models here.
from .models import Unit, Booking, Farmer, Warehouse, Warehouse_owner

admin.site.register(Unit)
admin.site.register(Booking)
admin.site.register(Farmer)
admin.site.register(Warehouse)
admin.site.register(Warehouse_owner)