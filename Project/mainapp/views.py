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

def homepage(request):
    # context = {}
    # flag = 2
    # my_user = request.user
    # print(my_user)
    # if not request.user.is_anonymous:
        
    #     if Farmer.objects.get(email=my_user.email) is None:
    #         flag = 0   # warehouse owner
    #         print("Heloo")
    #     else:
    #         flag = 1
    #         print("Bye")
    # print(flag)
    # context = {'flag': flag}
    
    # As we have farmerbase.html for farmer URLs we only need to see for homepage is it is a farmer or not 
    user_email = request.user.email if request.user.is_authenticated else None
    # For Homepage when farmer is logged in
    is_farmer = Farmer.objects.filter(email=user_email).exists()
    context= {'is_farmer': is_farmer}
    return render(request, 'homepage.html', context)

def activate(request,uidb64, token,flag):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError,ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        print(flag, type(flag))
        if flag == 1:
            owner = Warehouse_owner.objects.create(email = user.email)
            return redirect('warehouse_editprofile')
        else :
            farmer = Farmer.objects.create(email = user.email)
            return redirect('farmer_editprofile')
    else:
        messages.error(request,'Invalid activation link')
    return render(request, 'mainapp/signup.html')


def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        
        try:
            my_user = User.objects.get(username=username)
            my_user = authenticate(request, username=username, password=password)

            if my_user is not None:
                login(request, my_user)
                next_page = request.POST.get('next')
                print(next_page)
                try:
                    Farmer.objects.get(email=my_user.email)
                except Farmer.DoesNotExist:
                    return redirect("Warehouse_profile") 
                # messages.success(request, "You have succesfully Logged In")  
                return redirect(next_page) if next_page else redirect("farmer_currentbooking")

            else : 
                messages.error(request, "Invalid username or password")
                print("Invalid username or password") 
        except:
            messages.error(request, "Invalid username or password")
            
    # Do not remove elif as it is used for Next Page and validations Error message from POST request will pass through the last render
    elif request.GET:
        next_page = request.GET['next']
        context = {'next':next_page}
        print(next_page)
        return render(request, 'mainapp/signup.html',context)
    return render(request, 'mainapp/signup.html')

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

def aboutus(request):
    user = request.user
    print(user)
    farmer = Farmer.objects.filter(email=user)
    if not farmer:
        return render(request, 'mainapp/about_us.html')
    else:
        return render(request, 'mainapp/about_us_farmer.html')
        

def about_us(request):
    return render(request, 'mainapp/farmer_about_us.html')

def logoutUser(request):
    logout(request)
    return redirect('homepage')
