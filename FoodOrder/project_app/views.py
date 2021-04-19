from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from collections import Counter
import datetime
from django.contrib.auth import logout
from random import randint

# Create your views here.
def index(request):
    items = Item.objects.all()
    return render(request,'index.html', {'items': items})
    

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
            return redirect('user')
            # return render(request, 'example.html')
    else:
        return render(request, 'registerUser.html')


def Ulogin(request):
    if request.user.is_authenticated:
        restrolist = Restaurant.objects.filter()
        request.session["uid_save"] = request.user.id
        now = datetime.datetime.now()
        print(now)
        myorders = Order.objects.filter(uId = request.user.id)
        print(myorders)
        itemidlist = []
        for i in myorders:
            x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName', 'Image')
            print(x)
            print(type(x))
            itemidlist.append(x)
    
        print(itemidlist)
        return render(request, 'userhome.html', {'restro': restrolist, 'orders': itemidlist})
    else:   
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(username)
            # print(password)
            user = RestroUser.objects.get(username = username, password = password)
            # print(user)
            if user is not None:
                auth.login(request, user)
                restrolist = Restaurant.objects.filter()
                request.session["uid_save"] = user.id
                now = datetime.datetime.now()
                print(now)
                myorders = Order.objects.filter(uId = user.id)
                print(myorders)
                itemidlist = []
                for i in myorders:
                    x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName', 'Image')
                    print(x)
                    print(type(x))
                    itemidlist.append(x)
            
                print(itemidlist)
                return render(request, 'userhome.html', {'restro': restrolist, 'orders': itemidlist})
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
    myorders = Order.objects.filter(rId = rid_save_item)
    print(myorders)
    itemidlist = []
    for i in myorders:
        x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName', 'Image')
        print(x)
        print(type(x))
        itemidlist.append(x)
    return render(request, 'example.html', {'items': getItems, 'orders': itemidlist})


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
            return redirect('Rlogin')
            # return render(request, 'example.html')
    else:
        return render(request, 'registerUser.html')


def Rlogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Restaurant.objects.get(email = email, password = password)
        # print(user)
        if user is not None:
            rId = user.RId
            # print(rId)
            # rId = Restaurant.objects.only('RId').get(email=email)
            request.session["rid_save"] = rId

            getItems = Item.objects.filter(rId = rId)
            myorders = Order.objects.filter(rId = rId)
            print(myorders)
            itemidlist = []
            for i in myorders:
                x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName', 'Image')
                print(x)
                print(type(x))
                itemidlist.append(x)
            return render(request, 'example.html', {'items': getItems, 'orders': itemidlist})
    
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
    # print(rid)
    # print(type(rid))
    request.session["rid_cart"] = rid
    return render(request, 'cart3.html', {'items': items})


def set_cookie(request):
    if "rid_cart" in request.session:
        rid = request.session["rid_cart"]
    items = Item.objects.filter(rId = rid)
    response = render(request, 'cart2.html', {'items': items})

def placeorder(request, item):
    print('in placeorder')
    if "uid_save" in request.session:
            uid_save_item = request.session["uid_save"]

    if "rid_cart" in request.session:
            riD = request.session["rid_cart"]

    if request.method == 'POST':
        quant = request.POST.get('quant')

    print('quant ',quant)
    uId = RestroUser.objects.only("id").get(id= uid_save_item)
    rId = Restaurant.objects.only("RId").get(RId = riD)
    itemId = Item.objects.only("ItemId").get(ItemId = item)
    print(itemId.price)
    print(type(itemId.price))
    amount = (itemId.price)*int(quant)
    print('amt - ', amount)
    order = Order(uId = uId, rId = rId, itemId = itemId, quantity = quant, amount = amount)
    order.save()
    print(' order saved ')
    messages.info(request, "Order places successfully")
    restrolist = Restaurant.objects.filter()
    return render(request, 'userhome.html', {'restro': restrolist})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mess = request.POST.get('message')

        # send_mail('Contact Form', mess, settings.EMAIL_HOST_USER, [email id], fail_silently=False)

    return redirect('index')

    
def gohome(request):
    logout(request)
    return redirect('/')


def myorders(request):
    ono = randint(100000, 999999)
    request.session["ono_save"] = ono
    if "uid_save" in request.session:
        uid_save_item = request.session["uid_save"] 
    order_details = Order.objects.filter(uId = uid_save_item)
    itemidlist = []
    restrolist = []
    total = 0
    for i in order_details:
        total += i.amount
        x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName','price')
        itemidlist.append(x)
        y = Restaurant.objects.filter(RId = i.rId.RId).values('RestroName')
        restrolist.append(y)

    aftertax = total + (0.05*total)
    delivery = aftertax + 5
    return render(request, 'myorders.html', {'ono':ono,'order':order_details, 'item':itemidlist, 'restro': restrolist ,'total':total,'tax':delivery})


def rorders(request):
    ono = randint(100000, 999999)
    # if "ono_save" in request.session:
    #     ono_item = request.session["ono_save"]
    
    if "rid_save" in request.session:
            riD = request.session["rid_save"]

    order_details = Order.objects.filter(rId = riD)
    itemidlist = []
    userlist = []
    total = 0

    for i in order_details:
        total += i.amount
        x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName','price')
        itemidlist.append(x)
        y = RestroUser.objects.filter(id = i.uId.id).values('address1', 'address2', 'city')
        userlist.append(y)


    aftertax = total + (0.05*total)
    delivery = aftertax + 5
    return render(request, 'rorders.html', {'ono':ono,'order':order_details, 'item':itemidlist, 'address': userlist,'total':total,'tax':delivery})


def update_status(request, oid):
    x = Order.objects.filter(OrderId = oid)
    if request.method == 'POST':
        st = request.POST.get('status')
    
    for i in x:
        i.status = st
        i.save()
    return redirect('/')