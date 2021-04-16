from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
    

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
            user = RestroUser(username=username, password=password, first_name=fname,
            last_name=lname,email=email,phone_no=phone_no, address1 = address1, 
            address2=address2,city=city,state=state)
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
            restrolist = Restaurant.objects.filter()
            request.session["uid_save"] = user.id
            return render(request, 'userhome.html', {'restro': restrolist})
        else:
            messages.info(request, 'Invalid Credentials !')
            return render(request, 'registerUser.html')
    else:
        messages.info(request, 'Invalid Method !')
        return redirect('showUlogin')


def homepage(request):
    if "rid_save" in request.session:
            rid_save_item = request.session["rid_save"]

    getItems = Item.objects.filter(rId = rid_save_item)
    
    return render(request, 'example.html', {'items': getItems})


def showRlogin(request):
    return render(request, 'registerRestro.html')


def Rregister(request):
    if request.method == "POST" and request.FILES['logo']:
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone')
        address1 = request.POST.get('add1')
        address2 = request.POST.get('add2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        logo = request.FILES['logo']
        fs = FileSystemStorage()
        filename = fs.save(logo.name, logo)
        url = fs.url(filename)
        if Restaurant.objects.filter(email=email).exists():
            messages.info(request, "Already Registered")
            return render(request, 'registerRestro.html')
        else:
            user = Restaurant(RestroName=name, restro_phone=phone_no, password=password, 
            email=email, address1 = address1, address2=address2, city=city, state=state, 
            logo=url)
            user.save()
            return redirect('/home')
            # return render(request, 'example.html')
    else:
        return render(request, 'registerUser.html')


def Rlogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Restaurant.objects.get(email = email, password = password)
        print(user)
        if user is not None:
            rId = user.RId
            print(rId)
            # rId = Restaurant.objects.only('RId').get(email=email)
            request.session["rid_save"] = rId
            return render(request, 'example.html')
        else:
            messages.info(request, 'Invalid Credentials !')
            return render(request, 'registerUser.html')
    else:
        messages.info(request, 'Invalid Method !')
        return redirect('project_app:restro')


def menu(request):
    return render(request, 'menu.html')


def addItem(request):
    if request.method == 'POST' and request.FILES['dish']:
        rid_save_item = None
        if "rid_save" in request.session:
            rid_save_item = request.session["rid_save"]

        r_id = Restaurant.objects.only("RId").get(RId = rid_save_item)
        ItemName = request.POST.get('title')
        Description = request.POST.get('ingredients')
        price = request.POST.get('price')
        logo = request.FILES['dish']
        fs = FileSystemStorage()
        filename = fs.save(logo.name, logo)
        url = fs.url(filename)
        print(ItemName, Description, price, logo, url)
        saveitem = Item(rId = r_id, ItemName=ItemName, Description=Description, price=price,Image=url)
        saveitem.save()
        return redirect('/menu')
    else:
        messages.info(request, 'Invalid Method !')
        return redirect('/menu')


def showcart(request, rid):
    # if "uid_save" in request.session:
    #         uid_save_item = request.session["uid_save"]

    #     u_id = Restaurant.objects.only("RId").get(RId = rid_save_item)
    items = Item.objects.filter(rId = rid)
    print(rid)
    print(type(rid))
    request.session["rid_cart"] = rid
    return render(request, 'foodcart.html', {'items':items})


def placeorder(request):
    if "uid_save" in request.session:
            uid_save_item = request.session["uid_save"]

    if "rid_cart" in request.session:
            riD = request.session["rid_cart"]

    if request.method == 'POST':
        quant = request.method.get('qt')

    print(riD)
    print(type(riD))
    uId = RestroUser.objects.only("id").get(id= uid_save_item)
    rId = Restaurant.objects.only("RId").get(RId = riD)
    itemId = Item.objects.only("ItemId").get(ItemId = item)
    quantity = quant
    amount = Item.objects.only("price").get(ItemId = item) * quant

    order = Order(uId = uId, rId = rId, itemId = itemId, quantity = quantity, amount = amount)
    order.save()
    messages.info("Order places successfully")
    restrolist = Restaurant.objects.filter()
    return render(request, 'userhome.html', {'restro': restrolist})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mess = request.POST.get('message')

        send_mail('Contact Form', mess, settings.EMAIL_HOST_USER, [email id], fail_silently=False)

    return redirect('index')

    
