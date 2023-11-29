from base64 import urlsafe_b64decode
from email.policy import default
from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .models import Farmer, Warehouse_owner
from .utils import send_verification_email
import string, random, re
# from django.contrib.auth.forms import UserCreationForm


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



def register(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        flag = request.POST.get('user')
        print(email,pass1,flag)
        
        if pass1 == pass2:           
            # strong pass
            pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$")
            if pattern.match(pass1) is None:
                messages.error(request, 'Your password should be of length between 8 and 12 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')
                return render(request, 'mainapp/signup.html')
            
            else:   
                try:
                    my_user = User.objects.create_user(username=email, email=email, password=pass1, is_active = False)
                except:
                    messages.error(request, "User already exists with same email.")
                    context = {
                     'page':"register"
                    }
                    return render(request, 'mainapp/signup.html',context)
                
                login(request, my_user)
                send_verification_email(request,my_user,flag)
                
                if my_user.is_active == True:
                    # print(email, pass1, pass2, flag)
                    # return HttpResponse("Warehouse Owner created !!!")
                    if flag == "1":
                        owner = Warehouse_owner.objects.create(email = my_user.email)
                        return redirect('warehouse_editprofile')
                    else :
                        farmer = Farmer.objects.create(email = my_user.email)
                        return redirect('farmer_editprofile')
                    
                else:
                    # return HttpResponse("Please activate your account using link from mail")
                    return render(request, 'mainapp/activate.html')
            
        else:
            print("Passwords do not match")
            messages.error(request, "Passwords do not match")
            
        
    context = {
        'page':"register"
    }
    return render(request, 'mainapp/signup.html',context)

