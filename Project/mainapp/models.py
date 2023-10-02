from django.db import models
from datetime import date

class Units(models.Model):
    type = models.CharField(max_length=100) # Check box feild
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  


class Bookings(models.Model):
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default= date.today)
    description = models.TextField()
    unit_id = models.ManyToManyField(Units)


class Farmer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    
    
class Warehouses(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    poc_name = models.CharField(max_length=100)
    poc_phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    unit_id = models.ForeignKey(Units, on_delete=models.CASCADE)

    
class Warehouse_owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    warehouse_id = models.ForeignKey(Warehouses, on_delete=models.CASCADE)