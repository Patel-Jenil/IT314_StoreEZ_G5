from turtle import st
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from mainapp.models import Farmer,Warehouse, Booking, Unit
from farmer.forms import EditProfileForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime,date
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse
from math import cos, asin, sqrt, pi

@login_required(login_url='login')
def farmer_profile(request):
    user=request.user
    print(user.email)
    farmer=get_object_or_404(Farmer,email=user.email)
    # farmer = Farmer.objects.get(email = user.email)
    context={
        "farmer":farmer
    }
    return render(request,"farmer/profile2.html",context)
    # return HttpResponse('Hi')

@login_required(login_url='login')
def editprofile(request):
    user=request.user
    farmer=get_object_or_404(Farmer,email=user.email)
    editprofile = EditProfileForm(instance=farmer)
    context = {'editprofile': editprofile,'user':request.user, 'farmer_image':farmer.image}
    if request.method == "POST":
        editprofile  = EditProfileForm(request.POST, request.FILES, instance=farmer)
        if editprofile.is_valid():
            user = editprofile.save(commit=False)
            loggedin_user = request.user
            farmer_user = get_object_or_404(Farmer, email=loggedin_user.email)
            farmer_user.first_name = user.first_name
            farmer_user.last_name = user.last_name
            farmer_user.phone_no = user.phone_no
            farmer_user.city = user.city
            farmer_user.state = user.state
            farmer_user.image = user.image
            print(user.image)
            if farmer_user.image == "":
                farmer_user.image = Farmer().image 
            farmer_user.save()
            return redirect('farmer_profile')
        else:
            context = {'editprofile': editprofile,'user_id':request.user.id ,'farmer_image':farmer.image ,'errors':editprofile.errors}
    return render(request,'farmer/editprofile.html',context)

@login_required(login_url='login')
def currentbooking(request):
    data_list = []
    current_user = request.user
    current_farmer = Farmer.objects.get(email=current_user.email)
    farmer_current_bookings = Booking.objects.filter(farmer = current_farmer, end_date__gte = date.today()).order_by("id")
    for booking in farmer_current_bookings: # selecting individual bookings and finding it's corresponding warehouse
        print('-->','booking:',booking)
        all_booked_units = booking.unit.all()
        print('all_booked_units:',all_booked_units)
        if len(all_booked_units) == 0:
            continue
        one_booked_unit = all_booked_units[0]
        print('one_booked_unit:',one_booked_unit)
        per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
        print("Price per day:",per_day_price)
        total_days = (booking.end_date - booking.start_date).days + 1
        print("Total Days:",total_days)
        price = total_days * per_day_price
        print('price:',price)
        booked_warehouse = one_booked_unit.warehouse
        print('booked_warehouse:',booked_warehouse)
        data_list.append((booking,booked_warehouse, price))
    print('==>',data_list)
    paginator = Paginator(data_list, 5)  # Show 10 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages


    context={
        "data": page_obj,
        'nums':nums,
    }
    return render(request, 'farmer/currentbooking.html', context)

@login_required(login_url='login')
def previousbooking(request):
    data_list = []
    current_user = request.user
    current_farmer = Farmer.objects.get(email=current_user.email)
    farmer_current_bookings = Booking.objects.filter(farmer = current_farmer, end_date__lt = date.today()).order_by("id")
    for booking in farmer_current_bookings: # selecting individual bookings and finding it's corresponding warehouse
        print('-->','booking:',booking)
        all_booked_units = booking.unit.all()
        print('all_booked_units:',all_booked_units)
        if len(all_booked_units) == 0:
            continue
        one_booked_unit = all_booked_units[0]
        print('one_booked_unit:',one_booked_unit)
        per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
        print("Price per day:",per_day_price)
        total_days = (booking.end_date - booking.start_date).days + 1
        print("Total Days:",total_days)
        price = total_days * per_day_price
        print('price:',price)
        booked_warehouse = one_booked_unit.warehouse
        print('booked_warehouse:',booked_warehouse)
        data_list.append((booking,booked_warehouse, price))
    print('==>',data_list)
    paginator = Paginator(data_list, 5)  # Show 10 Bookings per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={
        "data": page_obj,
        'nums':nums,
    }
    return render(request, 'farmer/previousbooking.html', context)   


@login_required(login_url='login') 
def farmer_invoice(request,id):
    user = request.user
    farmer = get_object_or_404(Farmer,email=user.email)
    booking = get_object_or_404(Booking,id=id)
    all_booked_units = booking.unit.all()
    print('all_booked_units:',all_booked_units)
    total_units = len(all_booked_units)
    print(total_units)
    if total_units:
        one_booked_unit = all_booked_units[0]
    else:
        messages.error(request,"No units are booked for this period.")
        return render(request, 'farmer/booking.html', {})
    print('one_booked_unit:',one_booked_unit)
    per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
    print("Price per day:",per_day_price)
    total_days = (booking.end_date - booking.start_date).days + 1
    print("Total Days:",total_days)
    price = total_days * per_day_price
    print('price:',price)
    warehouse = one_booked_unit.warehouse
    print('warehouse:',warehouse)
    back_page = request.GET.get('back')
    context = {'farmer':farmer,'booking':booking,'all_booked_units':all_booked_units, 'per_day_price':per_day_price,
               'total_days':total_days, 'price':price, 'warehouse':warehouse, 'total_units':total_units, 'back':back_page}
    return render(request, 'farmer/invoice.html', context)
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
    #  return HttpResponse("Hiii:")
    
    
def computeDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def sortFunc(e):
    return e['distance']


@login_required(login_url='login')  
def search(request):
    # unit = Booking.objects.all()
    
    # if request.method == 'POST':
    start_date = request.GET.get('startdate','')
    end_date = request.GET.get('enddate', '')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    # print("------------------------",type(latitude))
    
    if (not start_date and end_date) or (not end_date and start_date) or start_date > end_date:
        messages.error(request, "Invalid Dates")
        context = {'startdate':date.today().strftime('%Y-%m-%d'), 'enddate':date.today().strftime('%Y-%m-%d')}
    else:
        if start_date == '':
            start_date = date.today().strftime('%Y-%m-%d')
        # else:
            # pass
            # start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        if end_date == '':
            end_date = date.today().strftime('%Y-%m-%d')
        # else:
            # pass
            # end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # booked_units = Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
        # booked_units = Booking.objects.filter(Q(Q(start_date__lte=end_date) & Q(end_date__gte=end_date)) | Q(Q(start_date__lte=start_date) & Q(end_date__gte=start_date)))\
        #                     .values_list('unit', flat=True)
        # booked_units = Booking.objects.filter(Q(start_date__lte=end_date,end_date__gte=end_date) | Q(start_date__lte=start_date,end_date__gte=start_date)). \
        
        # Jenil: booked_units = Booking.objects.filter(Q(start_date__gte=start_date,start_date__lte=end_date) | Q(end_date__gte=start_date,end_date__lte=end_date)). \
        # Algorithm made by JENIL PATEL (202101074)
        booked_units = Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date). \
            values_list('unit', flat=True).exclude(unit=None).distinct()
        # print(booked_units)
        # print("Bookings: ",Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date).values_list(flat=True))
        # print("Booked_units: ",booked_units)
        
        
        # warehouses = Warehouse.objects.values_list('name', 'id')
        warehouses = Warehouse.objects.all()
        
        warehouses_with_unit = []
        for warehouse in warehouses:
            # units = warehouse.unit_set.all()
            units = warehouse.unit_set.exclude(id__in=booked_units.values_list('unit'))
            # for x in units:
            #     print(x.type)
            hot_units = 0
            cold_units = 0
            hot_capacity = 0
            cold_capacity = 0
            if len(units) > 0:
                for x in units:
                    if x.type == "Hot":
                        hot_units += 1
                        hot_capacity += x.capacity
                    else:
                        cold_units += 1
                        cold_capacity += x.capacity
            if len(units) > 0:
                warehouses_with_unit.append({'warehouse': warehouse, 'hot_units': hot_units, 'hot_capacity':hot_capacity, 'cold_units':cold_units, 'cold_capacity':cold_capacity, 'latitude':warehouse.latitude, 'longitude':warehouse.longitude})
            # print(units)
        # print(warehouses_with_unit,longitude,latitude)
        
        
        nearby_warehouse_list = []
        
        if latitude != None:
            latitude = float(latitude)
            longitude = float(longitude)
            for w in warehouses_with_unit:
                curr_dist = computeDistance(w['latitude'], w['longitude'], latitude, longitude)
                w['distance'] = round(curr_dist, 2)
                nearby_warehouse_list.append(w)

            nearby_warehouse_list.sort(key=sortFunc)
        else:
            nearby_warehouse_list = warehouses_with_unit
        # print(longitude,latitude)
        # print(nearby_warehouse_list)
        print(nearby_warehouse_list)
        context = {'warehouses_with_unit': nearby_warehouse_list, 'startdate':start_date, 'enddate':end_date}
    # print(warehouses)
        
    return render(request,'farmer/search.html',context)
    # unit = Booking.objects.all()
    
    # if request.method == 'POST':
    start_date = request.GET.get('startdate','')
    end_date = request.GET.get('enddate', '')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    print("------------------------",type(latitude))
    
    if (not start_date and end_date) or (not end_date and start_date) or start_date > end_date:
        messages.error(request, "Invalid Dates")
        context = {'startdate':date.today().strftime('%Y-%m-%d'), 'enddate':date.today().strftime('%Y-%m-%d')}
    else:
        if start_date == '':
            start_date = date.today().strftime('%Y-%m-%d')
        # else:
            # pass
            # start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        if end_date == '':
            end_date = date.today().strftime('%Y-%m-%d')
        # else:
            # pass
            # end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # booked_units = Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
        # booked_units = Booking.objects.filter(Q(Q(start_date__lte=end_date) & Q(end_date__gte=end_date)) | Q(Q(start_date__lte=start_date) & Q(end_date__gte=start_date)))\
        #                     .values_list('unit', flat=True)
        # booked_units = Booking.objects.filter(Q(start_date__lte=end_date,end_date__gte=end_date) | Q(start_date__lte=start_date,end_date__gte=start_date)). \
        
        # Jenil: booked_units = Booking.objects.filter(Q(start_date__gte=start_date,start_date__lte=end_date) | Q(end_date__gte=start_date,end_date__lte=end_date)). \
        # Algorithm made by JENIL PATEL (202101074)
        booked_units = Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date). \
            values_list('unit', flat=True).exclude(unit=None).distinct()
        # print(booked_units)
        print("Bookings: ",Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date).values_list(flat=True))
        print("Booked_units: ",booked_units)
        # warehouses = Warehouse.objects.values_list('name', 'id')
        warehouses = Warehouse.objects.all()
        
        warehouses_with_unit = []
        for warehouse in warehouses:
            # units = warehouse.unit_set.all()
            units = warehouse.unit_set.exclude(id__in=booked_units.values_list('unit'))
            # for x in units:
            #     print(x.type)
            hot_units = 0
            cold_units = 0
            hot_capacity = 0
            cold_capacity = 0
            if len(units) > 0:
                for x in units:
                    if x.type == "Hot":
                        hot_units += 1
                        hot_capacity += x.capacity
                    else:
                        cold_units += 1
                        cold_capacity += x.capacity
            if len(units) > 0:
                warehouses_with_unit.append({'warehouse': warehouse, 'hot_units': hot_units, 'hot_capacity':hot_capacity, 'cold_units':cold_units, 'cold_capacity':cold_capacity, 'latitude':warehouse.latitude, 'longitude':warehouse.longitude})
            # print(units)
        # print(warehouses_with_unit,longitude,latitude)
        
        
        nearby_warehouse_list = []
        
        if latitude != None:
            latitude = float(latitude)
            longitude = float(longitude)
            for w in warehouses_with_unit:
                curr_dist = computeDistance(w['latitude'], w['longitude'], latitude, longitude)
                w['distance'] = round(curr_dist, 2)
                nearby_warehouse_list.append(w)

            nearby_warehouse_list.sort(key=sortFunc)
        print(longitude,latitude)
        print(nearby_warehouse_list)
        context = {'warehouses_with_unit': warehouses_with_unit, 'startdate':start_date, 'enddate':end_date}
    # print(warehouses)
        
    return render(request,'farmer/search.html',context)


@login_required(login_url='login')
def book(request,id, start, end):

    # Getting warehouse according to the url id
    warehouse = Warehouse.objects.get(id=id)
    
    #  Gettinng all the units of that warehouse
    all_units = warehouse.unit_set.all()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    # Getting all the 
    # booked_units = Booking.objects.filter(start_date__range=[start, end], end_date__range=[start, end])\
    #                            .values_list('unit', flat=True)
    # Adit: booked_units = Booking.objects.filter(Q(start_date__lte=end) & Q(end_date__gte=end) | Q(start_date__lte=start) & Q(end_date__gte=start))\
    #                            .values_list('unit', flat=True) This it accepts already booked units also. Contact me to know more
    # Jenil: booked_units = Booking.objects.filter(Q(start_date__gte=start_date,start_date__lte=end_date) | Q(end_date__gte=start_date,end_date__lte=end_date)). \
    # Algorithm made by JENIL PATEL (202101074)
    booked_units = Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date). \
            values_list('unit', flat=True).exclude(unit=None).distinct()
    # print(booked_units)
    print("Bookings: ",Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date))
    print("Booked_units: ",booked_units)
    #  Excluding all the units that have been blocked
    unbooked_units = all_units.exclude(id__in=booked_units.values_list('unit'))
    # Total Days
    
    total_days = (end_date - start_date).days + 1
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Total:",total_days,"Days")
    # Taking the value from user-Which units are selected by user
    if request.method == 'POST':
        selected_unit = request.POST.getlist('checkbox') # Will have id of the unit as we return id as value from HTML
        print(selected_unit)
        description = request.POST.get('description')
        user = request.user
        myfarmer = get_object_or_404(Farmer, email=user.email)

        booking = Booking(start_date=start, end_date=end, description=description, farmer=myfarmer)
        booking.save()
        
        booking.unit.set(selected_unit) # Whenever there is many to many feild we have to .set method
        
        return redirect(reverse('farmer_invoice', args=(booking.id,))) # redirect to current booking. This is done temporarily
    
    context = {'startdate':start, 'enddate':end, 'units':unbooked_units, 'total_days':total_days,'id':warehouse.id}
    return render(request,'farmer/book.html',context)

