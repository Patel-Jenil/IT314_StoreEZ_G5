from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from mainapp.models import Warehouse, Warehouse_owner
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from Warehouse.forms import EditProfile

# Create your views here.

@login_required()
def Warehouse_Profile(request):
    user = request.user
    # warehouse_user = Warehouse_owner.objects.get(email = user.email)
    warehouse_user = get_object_or_404(Warehouse_owner, email=user.email)
    # print(warehouse_user)
    context = {
        "warehouse_user":warehouse_user
    }
    return render(request,'warehouse/profile.html',context)


def index(request):
    context = {}
    return render(request,'warehouse/index.html',context)


@login_required()
def editprofile(request):
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        user = request.user
        # if email and User.objects.filter(email=email).exclude(email=user.email).count():
        #     raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        warehouse_user = get_object_or_404(Warehouse_owner, email=user.email)
        warehouse_user.first_name = first_name
        warehouse_user.last_name = last_name
        warehouse_user.email = email
        warehouse_user.phone_no = mobile
        warehouse_user.save()
        return redirect('Warehouse_profile')
    context = {}
    return render(request,'warehouse/editprofile.html',context)