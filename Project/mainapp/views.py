from django.shortcuts import render

def temp(request):
    context = {}
    return render(request, 'mainapp/temp.html', context)

# Create your views here.
