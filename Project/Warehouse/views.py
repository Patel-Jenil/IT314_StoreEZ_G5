from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainapp.models import Warehouse, Warehouse_owner, Unit, Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from Warehouse.forms import EditProfileForm
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q, Sum
# Create your views here.

@login_required(login_url='login')  
def Warehouse_Profile(request):
    user = request.user
    # warehouse_user = Warehouse_owner.objects.get(email = user.email)
    warehouse_user = get_object_or_404(Warehouse_owner, email=user.email)
    # print(warehouse_user)
    context = {
        "warehouse_user":warehouse_user
    }
    return render(request,'warehouse/profile.html',context)


@login_required(login_url='login')  
def editprofile(request):
    loggedin_user = request.user
    warehouse_owner = get_object_or_404(Warehouse_owner, email=loggedin_user.email)
    editprofile = EditProfileForm(instance=warehouse_owner)
    # context = {'editprofile': editprofile,'user':request.user, 'warehouse_owner_image':warehouse_owner.image}
    if request.method == "POST":
        print(request.FILES) 
        editprofile  = EditProfileForm(request.POST, request.FILES, instance=warehouse_owner)
        if editprofile.is_valid():
            user = editprofile.save(commit=False)
            warehouse_owner.first_name = user.first_name
            warehouse_owner.last_name = user.last_name
            warehouse_owner.phone_no = user.phone_no
            warehouse_owner.image = user.image
            if warehouse_owner.image == "": # If owner clears him image then set default value
                warehouse_owner.image = Warehouse_owner().image # default image in model
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
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors, 'warehouse_owner_image':warehouse_owner.image}
    context = {'editprofile': editprofile,'user':request.user, 'warehouse_owner_image':warehouse_owner.image}
    return render(request,'Warehouse/neweditprofile.html',context)

@login_required(login_url='login')  
def warehouses(request, id):
    warehouse = Warehouse.objects.get(id = id)
    context = {'warehouse':warehouse}
    return render(request,'warehouse/warehouse.html',context)

@login_required(login_url='login')  
def all_units(request, id):
    warehouse = Warehouse.objects.get(id = id)
    units = warehouse.unit_set.all()
    # print(units)
    context = {'units':units, 'warehouse':warehouse}
    return render(request,'warehouse/all_units.html',context)

@login_required(login_url='login')  
def unit(request, id, id1):
    warehouse = Warehouse.objects.get(id=id)
    unit = Unit.objects.get(id=id1)
    
    all_bookings = Booking.objects.filter(unit=id1)
    # print("booking :",all_bookings)
    
    current_date = timezone.now().date()
    
    current_booking = all_bookings.filter(end_date__gte=current_date).order_by('-end_date')
    prev_booking = all_bookings.filter(end_date__lt=current_date).order_by('-end_date')
    # print(prev_booking)
    context = {'warehouse':warehouse, 'unit':unit, 'current_booking':current_booking, 'prev_booking': prev_booking, 'id':id}
    return render(request, 'warehouse/unit.html', context)


@login_required(login_url='login')  
def warehouses(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print(search_query)
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
    print(warehouses)
    # print(user.email, warehouses)
    context = {
        'warehouses':warehouses, 
    }
    return render(request,'warehouse/warehouses.html',context)

@login_required(login_url='login')  
def addunit(request, id):
    # print(id)
    if request.POST:
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        price = request.POST.get('price')
        flag = False
        if capacity == "" or int(capacity) <= 0:
            messages.error(request, "Invalid Capacity")
            flag = True
        
        if price == "" or float(price) <= 0:
            messages.error(request, "Invalid Price")
            flag = True
            
        warehouse = Warehouse.objects.get(id = id)
        if flag:
            return redirect('addunit', id=id )
        
        
        unit = Unit(type=type, capacity=capacity, price=price, warehouse=warehouse)
        unit.save()
        return redirect('all_units', id=id)
        # print(type, capacity, price, warehouse)
    # print("id:",id)   
    context = {'id': id}
    return render(request, 'warehouse/add_units.html', context)


@login_required(login_url='login')  
def removeunit(request, id):
    if request.method == "POST":
        unit = request.POST.get('unit')
        # print("id: ",unit)
        del_unit = Unit.objects.get(id=unit)
        print(del_unit)
        del_unit.delete()
        return redirect('all_units', id=id)
    
    units = Warehouse.objects.get(id = id).unit_set.all()   
    # print(units.count())
    context = {'units': units,'id':id}
    return render(request, 'warehouse/removeunit.html', context)


@login_required(login_url='login')  
def editunit(request, id, id1):
    return render(request, 'warehouse/editunit.html')

@login_required(login_url='login')  
def addwarehouse(request):
    warehouse_image = Warehouse().image
    print(warehouse_image)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        poc_name = request.POST.get('poc_name')
        phone_no = request.POST.get('phone_no')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
    
        print(request.user.id)
        warehouse_owner = Warehouse_owner.objects.get(email = request.user.email)
        print(warehouse_owner)
        user = Warehouse(name = name, address = address, city = city, state = state, poc_name = poc_name , poc_phone_no=phone_no,owner = warehouse_owner , longitude = longitude , latitude = latitude)
        user.save()
        return redirect('warehouses')
    context = {
        'user_id':request.user.id,
        'warehouse_image':warehouse_image
    }
    return render(request,'warehouse/newaddwarehouse.html',context)

@login_required(login_url='login')  
def removewarehouse(request, id):
    print(id)
    context = {'id':id}
    if request.method == "POST":
        del_warehouse = Warehouse.objects.get(id=id)
        print(del_warehouse)
        del_warehouse.delete()
        return redirect('warehouses')
    

    # print(units.count())
    context = {'id':id}
    return render(request, 'warehouse/remove_warehouse.html', context)


@login_required(login_url='login')  
def warehouse_bookings(request,id):
    warehouse = get_object_or_404(Warehouse,id=id)
    owner = get_object_or_404(Warehouse_owner,email=request.user.email) 
    assert(owner == warehouse.owner) # To check if the right owner is accessing this page
    data_list = []
    all_bookings = Booking.objects.all().order_by("id")
    for booking in all_bookings:
        all_booked_units = booking.unit.all()
        if len(all_booked_units) == 0:
            continue
        one_booked_unit = all_booked_units[0]
        warehouse_of_booked_unit = one_booked_unit.warehouse
        if warehouse == warehouse_of_booked_unit:
            data_list.append((booking,booking.farmer))
    paginator = Paginator(data_list, 10)  # Show 10 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={'data':page_obj,'warehouse':warehouse,'nums':nums}
    return render(request, 'warehouse/warehouse_bookings.html',context)


@login_required(login_url='login')  
def warehouse_invoice(request, id):
    booking = get_object_or_404(Booking,id=id)
    farmer = booking.farmer
    all_booked_units = booking.unit.all()
    total_units = len(all_booked_units)
    if total_units:
        one_booked_unit = all_booked_units[0]
    else:
        messages.error(request,"No units are booked for this period.")
        return render(request, 'warehouse/booking.html', {})
    per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
    # print("Price per day:",per_day_price)
    total_days = (booking.end_date - booking.start_date).days + 1
    # print("Total Days:",total_days)
    price = total_days * per_day_price
    # print('price:',price)
    warehouse = one_booked_unit.warehouse
    assert(warehouse.owner.email==request.user.email)
    # print('warehouse:',warehouse)
    back_page = request.GET.get('back')
    
    context = {'farmer':farmer,'booking':booking,'all_booked_units':all_booked_units, 'per_day_price':per_day_price,
               'total_days':total_days, 'price':price, 'warehouse':warehouse, 'total_units':total_units, 'back':back_page}
    return render(request, 'warehouse/invoice.html', context)