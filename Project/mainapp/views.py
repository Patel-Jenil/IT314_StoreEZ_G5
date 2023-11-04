from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Farmer, Warehouse_owner
# from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    context = {}
    return render(request, 'homepage.html')

def loginUser(request):
    page ='login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        
        my_user = User.objects.get(username=username)
        my_user = authenticate(request, username=username, password=password)

        if my_user is not None:
            login(request, my_user)
            
            try:
                Farmer.objects.get(user=my_user)
            except Farmer.DoesNotExist:
                return HttpResponse("Warehouse")
                
            return HttpResponse("Farmer")
        else : 
            print("Invalid usrname or password") 
        
    context = {'page':page}
    return render(request, 'mainapp/signup.html', context)

def register(request):  
    page ='register'
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        flag = request.POST.get('user')
        # print(flag)
        
        my_user = User.objects.create_user(username=email, email=email, password=pass1)
        print(email, pass1, pass2, flag)
        # return HttpResponse("Warehouse Owner created !!!")
        if flag == "1":
            owner = Warehouse_owner.objects.create(user=my_user)
            return HttpResponse("Warehouse Owner created !!!")
        else :
            farmer = Farmer.objects.create(user=my_user)
            return HttpResponse("Farmer created !!!")
    context = {'page':page}
    return render(request, 'mainapp/signup.html', context) 



    
    
    # try:
    #         user = User.objects.get(username=username)
    #     except:
    #         messages.error(request,'User does not exist')
        
    #     user = authenticate(request, username=username, password=password)
        
    #     if user is not None:
    #         login(request, user)
    #         return redirect(request.GET['next'] if 'next' in request.GET else 'account')
    #     else:
    #         messages.error(request,'Username or password is incorrect')