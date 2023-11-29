from urllib import request
from django import forms
from .models import EditProfile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = EditProfile
        fields = ('first_name', 'last_name', 'phone_no', 'image')     
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last name'
        self.fields['phone_no'].widget.attrs['placeholder'] = 'Enter Phone number'
        self.fields['phone_no'].widget.attrs['min'] = 1000000000
        self.fields['phone_no'].widget.attrs['max'] = 9999999999
        self.fields['phone_no'].widget.attrs['oninvalid'] = "this.setCustomValidity('Phone number should contain 10 digits.')"
        # self.fields['image'].widget.attrs['placeholder'] = 'Enter image'
        

        
        
# class UpdateProfile(forms.ModelForm):

#     class Meta:
#         model = Warehouse_owner
#         fields = ("first_name", "last_name", "email", "phone_no")

#     def clean_email(self):
#         username = self.cleaned_data.get('email')
#         email = self.cleaned_data.get('email')

#         if email and User.objects.filter(email=email).exclude(username=username).count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email

#     def save(self, commit=True):
#         user = super(Warehouse_owner, self).save(commit=False)
#         user.email = self.cleaned_data['email']

#         if commit:
#             user.save()

#         return user