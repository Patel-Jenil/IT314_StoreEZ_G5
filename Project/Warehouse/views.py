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
            warehouse_owner = get_object_or_404(Warehouse_owner, email=loggedin_user.email)
            warehouse_owner.first_name = user.first_name
            warehouse_owner.last_name = user.last_name
            warehouse_owner.phone_no = user.phone_no
            warehouse_owner.image = user.image
            print(user.phone_no, user.image, user.first_name, user.last_name)
            warehouse_owner.save()
            
            # user = User.objects.get(username =loggedin_user.email)
            # user.username = farmer_user.email
            # user.email = farmer_user.email
            # user.save()
            # login_newuser = authenticate(username = user.email , password = loggedin_user.password)
            # login(request,login_newuser)
            return redirect('Warehouse_profile')
        
        else:
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors}
    return render(request,'Warehouse/editprofile.html',context)

@login_required()
def warehouses(request, id):
    warehouse = Warehouse.objects.get(id = id)
    context = {'warehouse':warehouse}
    return render(request,'warehouse/warehouse.html',context)


def units(request, id):
    # warehouse = Warehouse.objects.get(id = id)
    units = Warehouse.objects.get(id = id).unit_set.all()
    # print(units)
    context = {'units':units, 'warehouse_id':id}
    return render(request,'warehouse/units.html',context)

# def index(request):
#     user = request.user
#     warehouses = Warehouse_owner.objects.get(email = user.email).warehouse_set.all()
#     print(user.email, warehouses)
#     context = {
#         'warehouses':warehouses
#     }
#     return render(request,'warehouse/index.html',context)

def index(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    user = request.user
    all_warehouses = Warehouse_owner.objects.get(email = user.email).warehouse_set.all()

    filtered_warehouse = all_warehouses.filter(name__icontains = search_query)
    warehouses = ''
    if not filtered_warehouse:
        print("empty")
        warehouses = all_warehouses
        print(warehouses)
    else:
        print("not ")
        warehouses = filtered_warehouse
    
    # print(user.email, warehouses)
    context = {
        'warehouses':warehouses, 
    }
    return render(request,'warehouse/index.html',context)

@login_required()
def addunit(request, id):
    # print(id)
    if request.method == "POST":
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        price = request.POST.get('price')
        warehouse = Warehouse.objects.get(id = id)
        
        
        unit = Unit(type=type, capacity=capacity, price=price, warehouse=warehouse)
        unit.save()
        return redirect('units', id=id)
        # print(type, capacity, price, warehouse)
    # print("id:",id)   
    context = {'id': id}
    return render(request, 'warehouse/add_units.html', context)

def removeunit(request, id):
    context = {}
    if request.method == "POST":
        unit = request.POST.get('unit')
        # print("id: ",unit)
        del_unit = Unit.objects.get(id=unit)
        print(del_unit)
        del_unit.delete()
        return redirect('units', id=id)
    
    units = Warehouse.objects.get(id = id).unit_set.all()   
    # print(units.count())
    context = {'units': units}
    return render(request, 'warehouse/removeunit.html', context)

@login_required()
def addwarehouse(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        poc_name = request.POST.get('poc_name')
        phone_no = request.POST.get('phone_no')
        print(request.user.id)
        warehouse_owner = Warehouse_owner.objects.get(email = request.user.email)
        print(warehouse_owner)
        user = Warehouse(name = name, address = address, city = city, state = state, poc_name = poc_name , poc_phone_no=phone_no,owner = warehouse_owner)
        user.save()
    context = {
        'user_id':request.user.id
    }
    return render(request,'warehouse/add_warehouse.html',context)

def removewarehouse(request, id):
    print(id)
    context = {}
    if request.method == "POST":
        del_warehouse = Warehouse.objects.get(id=id)
        print(del_warehouse)
        del_warehouse.delete()
        return redirect('index')
    

    # print(units.count())
    context = {}
    return render(request, 'warehouse/remove_warehouse.html', context)