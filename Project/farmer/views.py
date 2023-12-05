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
    return render(request,"farmer/profile.html",context)

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
            # Validations
            flag=False
            if user.phone_no =="" or int(user.phone_no) <1000000000 or int( user.phone_no) >9999999999:
                messages.error(request,"Phone number should contain 10 digits.")
                flag=True

            if user.first_name.strip() == "" :
                messages.error(request,"Invalid First name!")    
                flag=True

            if user.last_name.strip() == "" :
                messages.error(request,"Invalid Last name!")    
                flag=True 

            if user.city.strip() == "" :
                messages.error(request,"Invalid city!")    
                flag=True
        
            if user.state.strip() == "" :
                messages.error(request,"Invalid state!")    
                flag=True
                
            if flag:
                return redirect('farmer_editprofile' )
            loggedin_user = request.user
            farmer_user = get_object_or_404(Farmer, email=loggedin_user.email)
            farmer_user.first_name = user.first_name.strip()
            farmer_user.last_name = user.last_name.strip()
            farmer_user.phone_no = user.phone_no
            farmer_user.city = user.city.strip()
            farmer_user.state = user.state.strip()
            farmer_user.image = user.image
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
        all_booked_units = booking.unit.all()
        if len(all_booked_units) == 0:
            continue
        one_booked_unit = all_booked_units[0]
        per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
        total_days = (booking.end_date - booking.start_date).days + 1
        price = total_days * per_day_price
        booked_warehouse = one_booked_unit.warehouse
        data_list.append((booking,booked_warehouse, price))
    paginator = Paginator(data_list, 10)  # Show 10 Bookings per page.
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
        all_booked_units = booking.unit.all()
        if len(all_booked_units) == 0:
            continue
        one_booked_unit = all_booked_units[0]
        per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
        total_days = (booking.end_date - booking.start_date).days + 1
        price = total_days * per_day_price
        booked_warehouse = one_booked_unit.warehouse
        data_list.append((booking,booked_warehouse, price))
    paginator = Paginator(data_list, 10)  # Show 10 Bookings per page.
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
    total_units = len(all_booked_units)
    if total_units:
        one_booked_unit = all_booked_units[0]
    else:
        messages.error(request,"No units are booked for this period.")
        return render(request, 'farmer/invoice.html', {})
    per_day_price = all_booked_units.aggregate(total=Sum('price'))['total']
    total_days = (booking.end_date - booking.start_date).days + 1
    price = total_days * per_day_price
    warehouse = one_booked_unit.warehouse
    back_page = request.GET.get('back')
    context = {'farmer':farmer,'booking':booking,'all_booked_units':all_booked_units, 'per_day_price':per_day_price,
               'total_days':total_days, 'price':price, 'warehouse':warehouse, 'total_units':total_units, 'back':back_page}
    return render(request, 'farmer/invoice.html', context)
    
    
def computeDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def sortFunc(e):
    return e['distance']


@login_required(login_url='login')  
def search(request):
    
    start_date = request.GET.get('startdate','')
    end_date = request.GET.get('enddate', '')
    latitude = request.GET.get('latitude','')
    longitude = request.GET.get('longitude','')
    
    if (not start_date and end_date) or (not end_date and start_date) or start_date > end_date:
        messages.error(request, "Invalid Dates")
        isError = 'Invalid Dates'
        context = {'isError': isError,'startdate':date.today().strftime('%Y-%m-%d'), 'enddate':date.today().strftime('%Y-%m-%d')}
    elif (latitude!='' and longitude!='') and (not(-90<= float(latitude) <=90) or not(-180<=float(longitude) <= 180)): 
        latitude = float(latitude)
        longitude = float(longitude)
        context = {'startdate':start_date,'enddate':end_date}
        if not(-90<= latitude <=90) and not(-180<=longitude <= 180):
            messages.error(request,'Invalid Latitude (-90 to 90) and Longitude (-180 to 180).')
            context['isError'] = 'Invalid Latitude and Longitude'
        elif not(-90<= latitude <=90):
            messages.error(request,'Invalid Latitude. It ranges from -90 to 90.')
            context['longitude'] = longitude
            context['isError'] = 'Invalid Latitude'
        elif not(-180<=longitude <= 180):
            messages.error(request,'Invalid Longitude. It ranges from -180 to 180.')
            context['latitude'] = latitude
            context['isError'] = 'Invalid Longitude'
    else:
        if start_date == '':
            start_date = date.today().strftime('%Y-%m-%d')

        if end_date == '':
            end_date = date.today().strftime('%Y-%m-%d')
        # Algorithm made by JENIL PATEL (202101074)
        booked_units = Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date). \
            values_list('unit', flat=True).exclude(unit=None).distinct()
                
        warehouses = Warehouse.objects.all()
        
        warehouses_with_unit = []
        for warehouse in warehouses:
            units = warehouse.unit_set.exclude(id__in=booked_units.values_list('unit'))
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
        
        nearby_warehouse_list = []
        if latitude != '' and longitude != '':
            latitude = float(latitude)
            longitude = float(longitude)
            for w in warehouses_with_unit:
                curr_dist = computeDistance(w['latitude'], w['longitude'], latitude, longitude)
                w['distance'] = round(curr_dist, 2)
                nearby_warehouse_list.append(w)

            nearby_warehouse_list.sort(key=sortFunc)
        else:
            nearby_warehouse_list = warehouses_with_unit
        paginator = Paginator(nearby_warehouse_list, 6)  # Show 6 Bookings per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        count=Warehouse.objects.count()
        nums= "." *page_obj.paginator.num_pages

        context={
            "data": page_obj, # Keep it data as 'data' is used in template more than one place
            'nums':nums,
            'startdate':start_date,
            'enddate':end_date,
            'latitude':latitude,
            'longitude':longitude,
        }
        
    return render(request,'farmer/search.html',context)

@login_required(login_url='login')
def book(request,id, start, end):

    # Getting warehouse according to the url id
    warehouse = Warehouse.objects.get(id=id)
    
    #  Gettinng all the units of that warehouse
    all_units = warehouse.unit_set.all()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    start_date = datetime.strptime(start, '%Y-%m-%d').date()

    # Algorithm made by JENIL PATEL (202101074)
    booked_units = Booking.objects.filter(start_date__lte=end_date,end_date__gte=start_date). \
            values_list('unit', flat=True).exclude(unit=None).distinct()
    unbooked_units = all_units.exclude(id__in=booked_units.values_list('unit'))

    # Total Days    
    total_days = (end_date - start_date).days + 1
    assert(total_days>0)
    
    # Taking the value from user-Which units are selected by user
    if request.method == 'POST':
        selected_units = request.POST.getlist('checkbox') # Will have id of the unit as we return id as value from HTML
        ## When its POST request that means Confirm button was pressed but between selecting units and booking them there might some other booking done
        ## So check if they are still available
        assert(len(selected_units) > 0)
        if any(int(unit) in list(booked_units) for unit in selected_units):
            messages.error(request,"Oops, Looks like you are late.\nSome of your selected units got booked in your selected Date Range")
            return redirect(reverse('book', args=(id,start,end)))
        
        description = request.POST.get('description')
        user = request.user
        myfarmer = get_object_or_404(Farmer, email=user.email)
        booking = Booking(start_date=start, end_date=end, description=description, farmer=myfarmer)
        booking.save()
        
        booking.unit.set(selected_units) # Whenever there is many to many feild we have to .set method
        
        return redirect(reverse('farmer_invoice', args=(booking.id,))) # redirect to current booking. This is done temporarily
    
    context = {'startdate':start, 'enddate':end, 'units':unbooked_units, 'total_days':total_days,'id':warehouse.id, 'warehouse':warehouse}
    return render(request,'farmer/book.html',context)

