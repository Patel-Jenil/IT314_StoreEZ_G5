from django.shortcuts import render, redirect

def homepage(request):
    context = {}
    return render(request, 'homepage.html')



# Create your views here.
