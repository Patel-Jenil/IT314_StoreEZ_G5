from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .models import Farmer, Warehouse_owner
# from django.contrib.auth.forms import UserCreationForm

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
    return render(request, 'homepage.html')

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
                
                try:
                    Farmer.objects.get(email=my_user.email)
                except Farmer.DoesNotExist:
                    return redirect("Warehouse_profile") 
                # messages.success(request, "You have succesfully Logged In")  
                return redirect("farmer_currentbooking")

            else : 
                messages.error(request, "Invalid username or password")
                print("Invalid username or password") 
        except:
            messages.error(request, "Invalid username or password")

    return render(request, 'mainapp/signup.html')

def register(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        flag = request.POST.get('user')
        
        if pass1 == pass2:
            try:
                my_user = User.objects.create_user(username=email, email=email, password=pass1)
            except:
                messages.error(request, "User already exists with same email.")
                context = {
                    'page':"register"
                }
                return render(request, 'mainapp/signup.html',context)
            login(request, my_user)
            # print(email, pass1, pass2, flag)
            # return HttpResponse("Warehouse Owner created !!!")
            if flag == "1":
                owner = Warehouse_owner.objects.create(email = my_user.email)
                return redirect('warehouse_editprofile')
            else :
                farmer = Farmer.objects.create(email = my_user.email)
                return redirect('farmer_editprofile')
            
        else:
            print("Passwords do not match")
            messages.error(request, "Passwords do not match")
            
        
    context = {
        'page':"register"
    }
    return render(request, 'mainapp/signup.html',context)


def aboutus(request):
    return render(request, 'mainapp/about_us.html')

def logoutUser(request):
    logout(request)
    return redirect('homepage')
