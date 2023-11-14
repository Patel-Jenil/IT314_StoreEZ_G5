from turtle import st
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from mainapp.models import Farmer,Warehouse, Booking, Unit
from farmer.forms import EditProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime,date,time


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
    # return HttpResponse('Hi')

@login_required(login_url='login')
def editprofile(request):
    user=request.user
    farmer=get_object_or_404(Farmer,email=user.email)
    editprofile = EditProfile(instance=farmer)
    context = {'editprofile': editprofile,'user':request.user}
    if request.method == "POST":
        editprofile  = EditProfile(request.POST, request.FILES, instance=farmer)
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
            farmer_user.save()
            return redirect('farmer_profile')
        else:
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors}
    return render(request,'farmer/editprofile.html',context)

@login_required(login_url='login')
def currentbooking(request):
    contact_list = Warehouse.objects.all()
    paginator = Paginator(contact_list, 2)  # Show 25 contacts per page.
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
    contact_list = Warehouse.objects.all()
    paginator = Paginator(contact_list, 2)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count=Warehouse.objects.count()
    nums= "." *page_obj.paginator.num_pages
    context={
        "data": page_obj,
        'nums':nums,
    }
    return render(request, 'farmer/previousbooking.html', context)   
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
    
@login_required(login_url='login')  
def search(request):
    context = {}
    # unit = Booking.objects.all()
    
    if request.method == 'POST':
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        
        booked_units = Booking.objects.filter(start_date__range=[start_date, end_date], end_date__range=[start_date, end_date])\
                               .values_list('unit', flat=True)
        print(booked_units)
        # warehouses = Warehouse.objects.values_list('name', 'id')
        warehouses = Warehouse.objects.all()
        
        warehouses_with_unit = []
        for warehouse in warehouses:
            # units = warehouse.unit_set.all()
            units = warehouse.unit_set.exclude(id__in=booked_units.values_list('unit'))
            warehouses_with_unit.append({'warehouse': warehouse, 'units': units})
            print(units)
        context = {'warehouses_with_unit': warehouses_with_unit, 'startdate':start_date, 'enddate':end_date}
        # print(warehouses)
        
    return render(request,'farmer/search.html',context)


@login_required
def book(request,id, start, end):

    
    # Getting warehouse according to the url id
    warehouse = Warehouse.objects.get(id=id)
    
    #  Gettinng all the units of that warehouse
    all_units = warehouse.unit_set.all()
    
    # Getting all the 
    booked_units = Booking.objects.filter(start_date__range=[start, end], end_date__range=[start, end])\
                               .values_list('unit', flat=True)
    
    #  Excluding all the units that have been blocked
    unbooked_units = all_units.exclude(id__in=booked_units.values_list('unit'))
    
    # Taking the value from user-Which units are selected by user
    if request.method == 'POST':
        selected_unit = request.POST.getlist('checkbox') # Will have id of the unit as we return id as value from HTML
        description = request.POST.get('description')
        user = request.user
        myfarmer = get_object_or_404(Farmer, email=user.email)

        booking = Booking(start_date=start, end_date=end, description=description, farmer=myfarmer)
        booking.save()
        
        booking.unit.set(selected_unit) # Whenever there is many to many feild we have to .set method
        
        return HttpResponse("I am booking") # redirect to current booking. This is done temporarily
    
    context = {'startdate':start, 'enddate':end, 'units':unbooked_units}
    return render(request,'farmer/book.html',context)

