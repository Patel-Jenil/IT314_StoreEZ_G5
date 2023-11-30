from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from mainapp.models import Farmer


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
    