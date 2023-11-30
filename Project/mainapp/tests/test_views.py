from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User


class TestSignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.testemail = "Jenil_test@gmail.com"
        self.testpassword = "testpassword"
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        self.url = reverse('login')
    
    def test_validcase(self):
        response = self.client.post(self.url, {
            'username': self.testemail,
            'password': self.testpassword
        })
        print(response)
        # self.assertRedirects(response, reverse('Warehouse_profile'), status_code=302)
        self.assertTrue(response.url == reverse('Warehouse_profile') and response.status_code == 302)
    
    def test_invalid_email(self):
        response = self.client.post(self.url, {
            'username': '@gmail.com',
            'password': self.testpassword
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)

    def test_invalid_email2(self):
        response = self.client.post(self.url, {
            'username': 'test@.com',
            'password': self.testpassword
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)  
        
    def test_invalid_email3(self):
        response = self.client.post(self.url, {
            'username': 'test@',
            'password': self.testpassword
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
    
    def test_invalid_password(self):
        response = self.client.post(self.url, {
            'username': self.testemail,
            'password': ''
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)
    
    def test_invalid_password2(self):
        response = self.client.post(self.url, {
            'username': self.testemail,
            'password': 'abra_k4_dabra!'
        })
        self.assertTrue(response.url == self.url and response.status_code == 302)



class TestSignUp(TestCase):
    

    def setUp(self):
        self.client = Client()
        self.testemail = "Jeniltest@gmail.com"
        self.testpassword = "Jenil_Test1!"
        self.url = reverse('register')
    
    def test_validcase(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': self.testpassword,
            'password2': self.testpassword,
            'user': 0,
        })
        print(response)
        # self.assertRedirects(response, reverse('Warehouse_profile'), status_code=302)
        # self.assertTrue(response.url == reverse('farmer_editprofile') and response.status_code == 302)
        self.assertTrue(response.status_code == 200) # Because User will be created and sent to activation code email page
        
    def test_existing_email(self):
        self.user = User.objects.create_user(self.testemail,self.testemail, self.testpassword)
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': self.testpassword,
            'password2': self.testpassword,
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
        
    def test_invalid_chars_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': '1234(da;]ff',
            'password2': '1234(da;]ff',
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_spaces_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "Jen il_Test1! ",
            'password2': "Jen il_Test1! ",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
    
    def test_invalid_longer_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "Jenil_Test1-Longer!#012",
            'password2': "Jenil_Test1-Longer!#012",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)

    def test_invalid_shorter_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "Je_Te1!",
            'password2': "Je_Te1!",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_no_numbers_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "Jenil_Test-!#",
            'password2': "Jenil_Test-!#",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_no_lowercase_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "JENIL_TEST-12!#",
            'password2': "JENIL_TEST-12!#",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_no_special_chars_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "JenilTest012",
            'password2': "JenilTest012",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
    
    def test_invalid_no_uppercase_in_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "jenil_test-12!#",
            'password2': "jenil_test-12!#",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_both_blank_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "",
            'password2': "",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
        
    def test_invalid_one_blank_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "JENIL_TEST-12!#",
            'password2': "JENIL_TEST-12!#",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
    
    def test_invalid_mismatch_password(self):
        response = self.client.post(self.url, {
            'email': self.testemail,
            'password1': "JENIL_TEST-12!#",
            'password2': "JENIL1_TEST-!#2",
            'user': 0,
        })
        self.assertTrue(response.url == reverse('register') and response.status_code == 302)
