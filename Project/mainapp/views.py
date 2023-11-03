from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    context = {}
    return render(request, 'homepage.html')

# def register(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#         flag = request.POST.get('user')
        
#         my_user = User.objects.create_user(email, email, pass1)
#         my_user.save()
#         print(email, pass1, pass2, flag)
#         # return HttpResponse("Warehouse Owner created !!!")
#         if flag == "1":
#             return HttpResponse("Warehouse Owner created !!!")
#         else :
#             return HttpResponse("Farmer created !!!")
        
         
#     return render(request, 'mainapp/register.html') 

def loginUser(request):
    return render(request, 'mainapp/log-in.html')

def register(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        flag = request.POST.get('user')
        
        my_user = User.objects.create_user(username=email, email=email, password=pass1)
        my_user.save()
        # print(email, pass1, pass2, flag)
        # return HttpResponse("Warehouse Owner created !!!")
        if flag == "1":
            return HttpResponse("Warehouse Owner created !!!")
        else :
            return HttpResponse("Farmer created !!!")
            
    return render(request, 'mainapp/sign-up.html') 


# Create your views here.
