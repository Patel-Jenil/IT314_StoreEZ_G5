from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from mainapp.models import Farmer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required()
def display(request):
    user=request.user
    print(user.email)
    farmer=get_object_or_404(Farmer,email=user.email)
    # farmer = Farmer.objects.get(email = user.email)
    context={
        "farmer":farmer
    }
    return render(request,"farmer/farmer_display.html",context)
    # return HttpResponse('Hi')

def edit(request):
    
    # if request.POST:
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     email = request.POST.get('email')
    #     mobile = request.POST.get('mobile')
    #     city=request.POST.get('city')
    #     state=request.POST.get('state')
    #     user = request.user
    #     # if email and User.objects.filter(email=email).exclude(email=user.email).count():
    #     #     raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
    #     Contact = get_object_or_404(Farmer, email=user.email)
    #     Contact.first_name = first_name
    #     Contact.last_name = last_name
    #     Contact.email = email
    #     Contact.phone_no = mobile
    #     Contact.city = city
    #     Contact.state= state
    #     Contact.save()
    #     return redirect('farmer_display')
    # # context = {}
    #     print(request)
    # return render(request,"farmer/edit.html")
     return HttpResponse("Hiii:")