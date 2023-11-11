from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from mainapp.models import Farmer,Warehouse
from farmer.forms import EditProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required()
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

@login_required()
def editprofile(request):
    editprofile = EditProfile()
    context = {'editprofile': editprofile,'user':request.user}
    if request.method == "POST":
        editprofile  = EditProfile(request.POST)
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
            
            # user = User.objects.get(username =loggedin_user.email)
            # user.username = farmer_user.email
            # user.email = farmer_user.email
            # user.save()
            # login_newuser = authenticate(username = user.email , password = loggedin_user.password)
            # login(request,login_newuser)
            return redirect('farmer_profile')
        
        else:
            context = {'editprofile': editprofile,'user_id':request.user.id , 'errors':editprofile.errors}
    return render(request,'farmer/editprofile.html',context)


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
    
    
@login_required
def book(request,id):
    warehouse = Warehouse.objects.get(id=id)
    units = warehouse.unit_set.all()
    # print(warehouse,"--", units)
    context = {
        'warehouse':warehouse,
        'units':units
    }
    return render(request,'farmer/book.html',context)