from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .models import Farmer, Warehouse_owner
# from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    context = {}
    return render(request, 'homepage.html')

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        
        my_user = User.objects.get(username=username)
        my_user = authenticate(request, username=username, password=password)

        if my_user is not None:
            login(request, my_user)
            
            try:
                Farmer.objects.get(email=my_user.email)
            except Farmer.DoesNotExist:
                # return HttpResponse("Warehouse")
                return redirect("Warehouse_profile")
                
            return redirect("farmer_profile")
        else : 
            print("Invalid usrname or password") 
        

    return render(request, 'mainapp/signup.html')

def register(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        flag = request.POST.get('user')
        
        my_user = User.objects.create_user(username=email, email=email, password=pass1)
        login(request, my_user)
        # print(email, pass1, pass2, flag)
        # return HttpResponse("Warehouse Owner created !!!")
        if flag == "1":
            owner = Warehouse_owner.objects.create(email = my_user.email)
            return redirect('warehouse_editprofile')
        else :
            farmer = Farmer.objects.create(email = my_user.email)
            return redirect('farmer_editprofile')
        
    context = {
        'page':"register"
    }
    return render(request, 'mainapp/signup.html',context)


def aboutus(request):
    return render(request, 'mainapp/about_us.html')

def logoutUser(request):
    logout(request)
    return redirect('homepage')
