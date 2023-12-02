from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from mainapp.models import Farmer,Warehouse_owner, Warehouse, Unit
from django.contrib.messages import get_messages

print("=> Jenil Testing: Edit Profile")
class TestFarmerEditProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.farmer = Farmer.objects.create(email = self.testemail)
        self.client.login(username=self.testemail,password=self.testpassword)
        self.url = reverse('farmer_editprofile')
    
    def test_validcase(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name':'Patel',
            'phone_no': 1234567890,
            'city':'Test city',
            'state': 'Test state',
        })
        print(response)
        # self.assertRedirects(response, reverse('farmer_profile'), status_code=302)
        self.assertTrue(response.url == reverse('farmer_profile') and response.status_code == 302)
        
    def test_invalid_empty_first_name(self):
        response = self.client.post(self.url, {
            'first_name': '',
            'last_name':'Patel',
            'phone_no': 1234567890,
            'city':'Test city',
            'state': 'Test state',
        })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass
        
    def test_invalid_empty_last_name(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name':'',
            'phone_no': 1234567890,
            'city':'Test city',
            'state': 'Test state',
        })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass

    def test_invalid_shorter_phone_no(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name': 'Patel',
            'phone_no': 123456,
            'city' : 'Test city',
            'state': 'Test state',
        })
        self.assertTrue(response.url == reverse('farmer_editprofile') and response.status_code == 302)

    def test_invalid_longer_phone_no(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name': 'Patel',
            'phone_no': 12345678901,
            'city':'Test city',
            'state': 'Test state',
        })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass
        
    def test_invalid_empty_city(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name':'Patel',
            'phone_no': 1234567890,
            'city':'',
            'state': 'Test state',
        })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass
        
    def test_invalid_empty_state(self):
        response = self.client.post(self.url, {
            'first_name': 'Jenil',
            'last_name':'Patel',
            'phone_no': 1234567890,
            'city':'Test city',
            'state': '',
        })
        self.assertTrue(response.status_code == 200) # Because Form will become invalid and if clause will pass

print("=> Jenil Testing: Farmer Searching Warehouse")
class TestWarehouseSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.farmer = Farmer.objects.create(email = self.testemail)
        self.owner = Warehouse_owner.objects.create(email = "2"+ self.testemail)
        self.warehouse = Warehouse.objects.create(owner=self.owner,poc_phone_no=6543219870)
        self.unit = Unit.objects.create(warehouse=self.warehouse,capacity=50,price=6000.25)
        self.client.login(username=self.testemail,password=self.testpassword)
        self.url = reverse('search')
    
    def test_validcase(self):
        response = self.client.get(self.url, {
            'start_date':'2023-12-02',
            'end_date':'2023-12-05',
            'latitude': 23.02,
            'longitude': 72.57, 
        })
        # print(response.content)
        self.assertContains(response, 'Jenil Testing: All Good')
        # self.assertRedirects(response, reverse('farmer_profile'), status_code=302)
        # self.assertTrue(response.url == reverse('search') and response.status_code == 302)
    
    def test_end_date_greater_than_start_date(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-05',
            'enddate':'2023-12-01',
            'latitude': 23.022505,
            'longitude': 72.5713621, 
        })
        # print(response.content)    
        self.assertContains(response,'Jenil Testing: Invalid Dates')
    
    def test_wrong_latitude(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': -100,
            'longitude': 72.5713621,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Latitude')
        
    def test_wrong_latitude2(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': 100,
            'longitude': 72.5713621,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Latitude')
        
    def test_wrong_longitude(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': -10.50,
            'longitude': 192.5,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Longitude')
        
    def test_wrong_longitude2(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': -50.50,
            'longitude': -192.5,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Longitude')
        
    def test_wrong_latitude_and_longitude(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': -100,
            'longitude': 272.5713621,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Latitude and Longitude')
        
    def test_wrong_latitude_and_longitude2(self):
        response = self.client.get(self.url, {
            'startdate':'2023-12-01',
            'enddate':'2023-12-05',
            'latitude': 165.64,
            'longitude': -201.79,
        })
        self.assertContains(response, 'Jenil Testing: Invalid Latitude and Longitude')