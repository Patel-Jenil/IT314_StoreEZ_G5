from django.test import TestCase, Client
from django.urls import reverse, resolve
from Warehouse.views import editprofile
from django.contrib.auth.models import User
from mainapp.models import Warehouse_owner, Warehouse
from django.contrib.messages import get_messages


print("=> Jenil Testing: Warehouse owner Edit Profile")
class TestWarehouseOwnerEditProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.owner = Warehouse_owner.objects.create(email = self.testemail)
        self.client.login(username=self.testemail,password=self.testpassword)
        self.edit_profile_url = reverse('warehouse_editprofile')
    
    def test_validcase(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': 'Jenil',
            'last_name':'Patel',
            'phone_no': 1234567890
        })
        print(response)
        # self.assertRedirects(response, reverse('Warehouse_profile'), status_code=302)
        self.assertTrue(response.url == reverse('Warehouse_profile') and response.status_code == 302)
        
    def test_empty_first_name(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': "",
            'last_name':'Patel',
            'phone_no': 1234567890
            })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass
        
    def test_last_name(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': "Jenil",
            'last_name':'',
            'phone_no': 1234567890
            })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass
        
    def test_shorter_phone_no(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': "Jenil",
            'last_name':'Patel',
            'phone_no': 1234567
            })
        self.assertTrue(response.url == reverse('warehouse_editprofile') and response.status_code == 302)
        
    def test_longer_phone_no(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': "Jenil",
            'last_name':'Patel',
            'phone_no': 1234567890123
            })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass


print("=> Jenil Testing: Add Warehouse")
class TestAddWarehouse(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.owner = Warehouse_owner.objects.create(email = self.testemail)
        self.client.login(username=self.testemail,password=self.testpassword)
        self.url = reverse('add_warehouse')
        
    def test_validcase(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('warehouses') and response.status_code == 302)
    
    def test_empty_name(self):
        response = self.client.post(self.url, {
            'name':"",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_address(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_city(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_state(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_poc_name(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
        
    def test_empty_shorter_phone_no(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':987654,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_longer_phone_no(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':98765432101234,
            'latitude': 60,
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
        
    def test_empty_invalid_latitude(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': -100, # should be in range (-90,90)
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
        
    def test_empty_invalid_latitude2(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 100, # should be in range (-90,90)
            'longitude':120,
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_invalid_longitude(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude': -200, # should be in range (-180,180)
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)
    
    def test_empty_invalid_longitude2(self):
        response = self.client.post(self.url, {
            'name':"Test Warehouse",
            'address':"Test Address",
            'city':"Test city",
            'state':'Test state',
            'poc_name':'Test POC',
            'phone_no':9876543210,
            'latitude': 60,
            'longitude':200, # should be in range (-180,180)
        })
        self.assertTrue(response.url == reverse('add_warehouse') and response.status_code == 302)


print("=> Jenil Testing: Add Warehouse Unit")
class TestAddUnit(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.owner = Warehouse_owner.objects.create(email = self.testemail)
        self.warehouse = Warehouse.objects.create(
            name = "Test Warehouse",
            address="Test Address",
            city="Test city",
            state='Test state',
            poc_name='Test POC',
            poc_phone_no = 9876543210,
            latitude = 60,
            longitude =200,
            owner = self.owner)
        self.client.login(username=self.testemail,password=self.testpassword)
        self.url = reverse('addunit', args=(self.warehouse.id,))
        
    def test_validcase(self):
        response = self.client.post(self.url, {
            'type': "Hot",
            'capacity': 50,
            'price':5000.50,
        })
        self.assertTrue(response.url == reverse('all_units',args=(self.warehouse.id,)) and response.status_code == 302)
        
    def test_invalid_type(self):
        response = self.client.post(self.url, {
            'type': "Rainy",
            'capacity': 50,
            'price':5000,
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
        
    def test_invalid_capacity(self):
        response = self.client.post(self.url, {
            'type': "Cold",
            'capacity': 0,
            'price':5000,
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
        
    def test_invalid_capacity2(self):
        response = self.client.post(self.url, {
            'type': "Cold",
            'capacity': -50,
            'price':5000.5,
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
        
    def test_invalid_price(self):
        response = self.client.post(self.url, {
            'type': "Hot",
            'capacity': 50,
            'price': 0,
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
    
    def test_invalid_price2(self):
        response = self.client.post(self.url, {
            'type': "Hot",
            'capacity': 50,
            'price': -600,
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)