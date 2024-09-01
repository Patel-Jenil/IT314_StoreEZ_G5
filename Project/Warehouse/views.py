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
from datetime import date
# Create your views here.

@login_required(login_url='login')
def Warehouse_Profile(request):
    user = request.user
    # warehouse_user = Warehouse_owner.objects.get(email = user.email)
    warehouse_user = get_object_or_404(Warehouse_owner, email=user.email)
    if not warehouse_user.image:
        warehouse_user.image= Warehouse_owner().image
        warehouse_user.save()
    context = {
        "warehouse_user":warehouse_user,
        'image':Warehouse_owner().image
    }
    return render(request,'Warehouse/profile.html',context)


@login_required(login_url='login')
def editprofile(request):
    loggedin_user = request.user
    warehouse_owner = get_object_or_404(Warehouse_owner, email=loggedin_user.email)
    if not warehouse_owner.image:
        warehouse_owner.image= Warehouse_owner().image
        warehouse_owner.save()
    editprofile = EditProfileForm(instance=warehouse_owner)
    # context = {'editprofile': editprofile,'user':request.user, 'warehouse_owner_image':warehouse_owner.image}
    if request.method == "POST":
        print(request.FILES)
        editprofile  = EditProfileForm(request.POST, request.FILES, instance=warehouse_owner)
        if editprofile.is_valid():
            user = editprofile.save(commit=False)
            # Validations
            flag=False
            if user.phone_no =="" or int(user.phone_no) <1000000000 or int( user.phone_no) >9999999999:
                messages.error(request,"Phone number should contain 10 digits.")
                flag=True

            if user.first_name.strip() =="" :
                messages.error(request,"Invalid First name!")
                flag=True

            if user.last_name.strip() =="" :
                messages.error(request,"Invalid Last name!")
                flag=True

            if flag:
                return redirect('warehouse_editprofile' )
            warehouse_owner.first_name = user.first_name.strip()
            warehouse_owner.last_name = user.last_name.strip()
            warehouse_owner.phone_no = user.phone_no
            warehouse_owner.image = user.image
            if warehouse_owner.image == "": # If owner clears him image then set default value
                warehouse_owner.image = Warehouse_owner().image # default image in model
            print(user.phone_no, user.image, user.first_name, user.last_name)
            warehouse_owner.save()

            return redirect('Warehouse_profile')

        else:
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors, 'warehouse_owner_image':warehouse_owner.image}
    context = {'editprofile': editprofile,'user':request.user, 'warehouse_owner_image':warehouse_owner.image}
    return render(request,'Warehouse/editprofile.html',context)

@login_required(login_url='login')
def warehouses(request, id):
    warehouse = Warehouse.objects.get(id = id)
    context = {'warehouse':warehouse}
    return render(request,'Warehouse/warehouse.html',context)

@login_required(login_url='login')
def all_units(request, id):
    warehouse = Warehouse.objects.get(id = id)
    units = warehouse.unit_set.all()
    paginator = Paginator(units, 12)  # TODO:Show 12/16 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={'data':page_obj,'warehouse':warehouse,'nums':nums, 'units':units,}
    return render(request,'Warehouse/all_units.html',context)

@login_required(login_url='login')
def unit(request, id, id1):
    warehouse = Warehouse.objects.get(id=id)
    unit = Unit.objects.get(id=id1)

    all_bookings = Booking.objects.filter(unit=id1).order_by('-end_date')
    # print("booking :",all_bookings)
    data_list = []
    for booking in all_bookings:
        if booking.end_date >= date.today():
            booking_status = 'On going'
        else:
            booking_status = 'Completed'
        data_list.append((booking,booking_status))

    # current_booking = all_bookings.filter(end_date__gte=current_date).order_by('-end_date')
    # prev_booking = all_bookings.filter(end_date__lt=current_date).order_by('-end_date')
    # print(prev_booking)
    paginator = Paginator(data_list, 5)  # TODO:Show 10/15 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={'data':page_obj,'warehouse':warehouse,'nums':nums, 'unit':unit, 'id':id}
    return render(request, 'Warehouse/unit.html', context)


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
    return render(request,'Warehouse/warehouses.html',context)

@login_required(login_url='login')
def addunit(request, id):
    # print(id)
    # warehouse = get_object_or_404(Warehouse_owner, id=id)
    warehouse = Warehouse.objects.get(id=id)
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

        if type != 'Hot' and type != 'Cold':
            messages.error(request, "Don't mess with Dev tools")
            flag = 1

        warehouse = Warehouse.objects.get(id = id)
        if flag:
            return redirect('addunit', id=id )


        unit = Unit(type=type, capacity=capacity, price=price, warehouse=warehouse)
        unit.save()
        return redirect('all_units', id=id)
        # print(type, capacity, price, warehouse)
    # print("id:",id)
    context = {'id': id, 'warehouse':warehouse}
    return render(request, 'Warehouse/add_units.html', context)


@login_required(login_url='login')
def removeunit(request, id):
    warehouse = Warehouse.objects.get(id=id)
    if request.method == "POST":
        unit = request.POST.get('unit')
        # print("id: ",unit)
        del_unit = Unit.objects.get(id=unit)
        print(del_unit)
        del_unit.delete()
        return redirect('all_units', id=id)

    units = Warehouse.objects.get(id = id).unit_set.all()
    # print(units.count())
    context = {'units': units,'id':id, 'warehouse':warehouse}
    return render(request, 'Warehouse/removeunit.html', context)


@login_required(login_url='login')
def editunit(request, id, id1):
    return render(request, 'Warehouse/editunit.html')

@login_required(login_url='login')
def addwarehouse(request):
    warehouse_image = Warehouse().image
    # print(warehouse_image)
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        address = request.POST.get('address').strip()
        city = request.POST.get('city').strip()
        state = request.POST.get('state').strip()
        poc_name = request.POST.get('poc_name').strip()
        phone_no = request.POST.get('phone_no')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Validations
        flag=False
        if phone_no =="" or int(phone_no) <1000000000 or int(phone_no) >9999999999:
            messages.error(request,"Phone number should contain 10 digits.")
            flag=True

        if not( -90 <= float(latitude) <= 90):
            messages.error(request,"Invalid latitude!")
            flag=True

        if not( -180 <= float(longitude) <= 180):
            messages.error(request,"Invalid latitude!")
            flag=True

        if name =="" :
            messages.error(request,"Invalid Name!")
            flag=True

        if city =="" :
            messages.error(request,"Invalid city!")
            flag=True

        if state =="" :
            messages.error(request,"Invalid state!")
            flag=True

        if poc_name =="" :
            messages.error(request,"Invalid Point of contact person Name!")
            flag=True

        if address =="" :
            messages.error(request,"Invalid address!")
            flag=True

        if flag:
            return redirect('add_warehouse' )
        # print(request.user.id)
        warehouse_owner = Warehouse_owner.objects.get(email = request.user.email)
        # print(warehouse_owner)
        user = Warehouse(name = name, address = address, city = city, state = state, poc_name = poc_name , poc_phone_no=phone_no,owner = warehouse_owner , longitude = longitude , latitude = latitude)
        user.save()
        return redirect('warehouses')
    context = {
        'user_id':request.user.id,
        'warehouse_image':warehouse_image
    }
    return render(request,'Warehouse/add_warehouse.html',context)

@login_required(login_url='login')
def removewarehouse(request, id):
    print(id)
    context = {'id':id}
    del_warehouse = Warehouse.objects.get(id=id)
    if request.method == "POST":
        del_warehouse.delete()
        return redirect('warehouses')


    # print(units.count())
    context = {'id':id, 'warehouse': del_warehouse}
    return render(request, 'Warehouse/remove_warehouse.html', context)


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
            if booking.end_date >= date.today():
                booking_status = 'On going'
            else:
                booking_status = 'Completed'
            data_list.append((booking,booking.farmer,booking_status))
    paginator = Paginator(data_list, 10)  # Show 10 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={'data':page_obj,'warehouse':warehouse,'nums':nums}
    return render(request, 'Warehouse/warehouse_bookings.html',context)


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
        return render(request, 'Warehouse/booking.html', {})
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
    return render(request, 'Warehouse/invoice.html', context)