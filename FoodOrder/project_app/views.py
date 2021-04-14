from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')
    
def showRlogin(request):
    return render(request, 'registerUser.html')

def showUlogin(request):
    return render(request, 'registerUser.html')

def Uregister(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone')
        address1 = request.POST.get('add1')
        address2 = request.POST.get('add2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if RestroUser.objects.filter(email=email).exists():
            messages.info(request, "Already Registered")
            return render(request, 'registerUser.html')
        else:
            user = RestroUser(username=username, password=password, first_name=fname, last_name=lname,
            email=email,phone_no=phone_no, address1 = address1, address2=address2,city=city,state=state)
            user.save()
            return render(request, 'example.html')
    else:
        return render(request, 'registerUser.html')

def Ulogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = RestroUser.objects.get(username = username, password = password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return render(request, 'example.html')
        else:
            messages.info(request, 'Invalid Credentials !')
            return render(request, 'registerUser.html')
    else:
        messages.info(request, 'Invalid Method !')
        return redirect('showUlogin')

def homepage(request):
    return render(request, 'example.html')

