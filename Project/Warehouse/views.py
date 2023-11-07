from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainapp.models import Warehouse, Warehouse_owner, Unit
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



# @login_required()
# def editprofile(request):
#     if request.POST:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         user = request.user
#         # if email and User.objects.filter(email=email).exclude(email=user.email).count():
#         #     raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         warehouse_user = get_object_or_404(Warehouse_owner, email=user.email)
#         warehouse_user.first_name = first_name
#         warehouse_user.last_name = last_name
#         warehouse_user.email = email
#         warehouse_user.phone_no = mobile
#         warehouse_user.save()
#         return redirect('Warehouse_profile')
#     context = {}
#     return render(request,'warehouse/editprofile.html',context)



def editprofile(request):
    editprofile = EditProfile()
    context = {'editprofile': editprofile,'user':request.user}
    if request.method == "POST":
        editprofile  = EditProfile(request.POST)
        if editprofile.is_valid():
            user = editprofile.save(commit=False)
            loggedin_user = request.user
            warehouse_user = get_object_or_404(Warehouse_owner, email=loggedin_user.email)
            warehouse_user.first_name = user.first_name
            warehouse_user.last_name = user.last_name
            warehouse_user.email = user.email
            warehouse_user.phone_no = user.phone_no
            warehouse_user.save()
            
            user = User.objects.get(username =loggedin_user.email)
            user.username = warehouse_user.email
            user.email = warehouse_user.email
            user.save()
            login_newuser = authenticate(username = user.email , password = loggedin_user.password)
            login(request,login_newuser)
            return redirect('Warehouse_profile')
        
        else:
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors}
    return render(request,'warehouse/editprofile.html',context)

def warehouses(request, id):
    warehouse = Warehouse.objects.get(id = id)
    context = {'warehouse':warehouse}
    return render(request,'warehouse/warehouse.html',context)


def units(request, id):
    # warehouse = Warehouse.objects.get(id = id)
    units = Warehouse.objects.get(id = id).unit_set.all()
    print(units)
    context = {'units':units}
    return render(request,'warehouse/units.html',context)

def index(request):
    user = request.user
    warehouses = Warehouse_owner.objects.get(email = user.email).warehouse_set.all()
    print(user.email, warehouses)
    context = {
        'warehouses':warehouses
    }
    return render(request,'warehouse/index.html',context)

@login_required()
def addunit(request, id):
    context = {}
    if request.method == "POST":
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        price = request.POST.get('price')
        warehouse = Warehouse.objects.get(id = id)
        
        
        unit = Unit(type=type, capacity=capacity, price=price, warehouse=warehouse)
        unit.save()
        return redirect('units', id=id)
        # print(type, capacity, price, warehouse)
        
        
    return render(request, 'warehouse/add_units.html', context)

def removeunit(request, id):
    return render(request, 'warehouse/removeunit.html')