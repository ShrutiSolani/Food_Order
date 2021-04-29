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
import json

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
            return redirect('/user')
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
            return redirect('/Rlogin')
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
        print(rid_save_item)
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
    return render(request, 'cart4.html', {'items': items})


# def set_cookie(request):
#     if "rid_cart" in request.session:
#         rid = request.session["rid_cart"]
#     items = Item.objects.filter(rId = rid)
#     response = render(request, 'cart2.html', {'items': items})

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
    # restrolist = Restaurant.objects.filter()
    items = Item.objects.filter(rId = rId)
    return render(request, 'cart4.html', {'items': items})


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
    # ono = randint(100000, 999999)
    # request.session["ono_save"] = ono
    if "uid_save" in request.session:
        uid_save_item = request.session["uid_save"] 
    # order_details = Order.objects.filter(uId = uid_save_item)
    # itemidlist = []
    # restrolist = []
    # total = 0
    # for i in order_details:
    #     total += i.amount
    #     x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName','price')
    #     itemidlist.append(x)
    #     y = Restaurant.objects.filter(RId = i.rId.RId).values('RestroName')
    #     restrolist.append(y)

    # aftertax = total + (0.05*total)
    # delivery = aftertax + 5
    osummary = OrderSummary.objects.filter(uid = uid_save_item)
    osummary = osummary[len(osummary) - 1]
    print(osummary)
    jsonDec = json.decoder.JSONDecoder()
    itemidlist = []
   
    itemidlist.append(jsonDec.decode(osummary.itemslist))
    # itemidlist  = jsonDec.decode(osummary.itemslist)
    print(itemidlist)
    # print(itemidlist[0])
    # print(itemidlist[0][0])
    # print(itemidlist)
    # itemdetails = []
    # qt = []
    # for i in itemidlist:
    #     for j in i:
    #         for k in j:
    #             x = Item.objects.values_list('ItemName', 'price').get(ItemId = k['ItemId'])
    #             print(x)
    #             q = Order.objects.values_list('quantity').get(uId = uid_save_item, itemId = k['ItemId'])
    #             print(q)
    #             itemd = x + q
    #             print(itemd)
    #             print(type(itemd))
    #             # x = Item.objects.filter(ItemId = k['ItemId']).values('ItemName','price')
    #             # print(x)
    #             # itemdetails.append(x)
    #             # q = Order.objects.filter(uId = uid_save_item, itemId = k['ItemId']).values('quantity')
    #             # qt.append(int(q))
    #             # x.extra(
    #             #     select= {'qt': q}
    #             # )
    #             # print(x)
    #             # x['qt'] = q
    #             itemdetailes.append(itemd)

    restrodetails = []
    y = Restaurant.objects.values_list('RestroName').get(RId = osummary.rid.RId)
    restrodetails.append(y[0])
    qtlist = []
    for i in range(len(itemidlist)):
        print('i', i)
        for j in itemidlist[i]:
            print('j',j)
            print(type(j))
            print(j[0])
            x = Order.objects.values_list('quantity').get(itemId = j[0])
            # print('x' , x)
            x = list(x)
            qtlist.append(x)
            # print(itemidlist[i].index(j))
            # print(type(int(itemidlist[i].index(j))))
            # itemidlist[itemidlist[i].index(j)].append(x)
    print(itemidlist)
    print(qtlist)
    k = 0
    while k < len(qtlist):
        print('k',k)
        for i in itemidlist:
            for j in i:
                j.append(qtlist[k][0])
                k += 1

    print(itemidlist)
    # print(userdetails)
    # print(userdetails[0][0])
    # total = osummary[len(osummary) - 1].total 
    # after_tax = osummary[len(osummary) - 1].aftertax
    total = osummary.total
    after_tax = osummary.aftertax
    return render(request, 'myorders2.html', {'order': osummary, 'restro': y[0], 'item':itemidlist, 'total':total, 'tax': after_tax})
    # return render(request, 'myorders.html', {'ono':ono,
    # 'order':order_details, 'item':itemidlist, 
    # 'restro': restrolist ,'total':total,'tax':delivery})


def rorders(request):
    
    if "rid_save" in request.session:
            riD = request.session["rid_save"]
    # jsonDec = json.decoder.JSONDecoder()
    # myPythonList = jsonDec.decode(myModel.myList)
    # order_details = Order.objects.filter(rId = riD)
    # itemidlist = []
    # userlist = []
    # total = 0

    # for i in order_details:
    #     total += i.amount
    #     x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemName','price')
    #     itemidlist.append(x)
    #     y = RestroUser.objects.filter(id = i.uId.id).values('address1', 'address2', 'city')
    #     userlist.append(y)


    # aftertax = total + (0.05*total)
    # delivery = aftertax + 5

    osummary = OrderSummary.objects.filter(rid = riD)
    osummary = osummary[len(osummary) - 1]
    jsonDec = json.decoder.JSONDecoder()
    itemidlist = []
    itemidlist.append(jsonDec.decode(osummary.itemslist))
    # itemidlist  = jsonDec.decode(osummary[0].itemslist)
    print(itemidlist)
    print(itemidlist[0])
    print(itemidlist[0][0])
    # print(itemidlist)
    itemdetails = []
    # for i in itemidlist:
    #     for j in i:
    #         for k in j:
    #             x = Item.objects.filter(ItemId = k['ItemId']).values('ItemName','price')
    #             itemdetails.append(x)

    userdetails = []
    y = RestroUser.objects.values_list('address1', 'address2', 'city').get(id = osummary.uid.id)
        # y = RestroUser.objects.get(id = i.uid.id).only('address1', 'address2', 'city')
    userdetails.append(y)
    print(userdetails)
    print(userdetails[0][0])

    qtlist = []
    for i in range(len(itemidlist)):
        print('i', i)
        for j in itemidlist[i]:
            print('j',j)
            print(type(j))
            print(j[0])
            x = Order.objects.values_list('quantity').get(itemId = j[0])
            # print('x' , x)
            x = list(x)
            qtlist.append(x)
            # print(itemidlist[i].index(j))
            # print(type(int(itemidlist[i].index(j))))
            # itemidlist[itemidlist[i].index(j)].append(x)
    print(itemidlist)
    print(qtlist)
    k = 0
    while k < len(qtlist):
        print('k',k)
        for i in itemidlist:
            for j in i:
                j.append(qtlist[k][0])
                k += 1

    print(itemidlist)


    total = osummary.total
    after_tax = osummary.aftertax
    return render(request, 'rorders.html', {'order': osummary, 'item':itemidlist, 'address': {'1': userdetails[0][0], '2': userdetails[0][1], '3':userdetails[0][2] }, 'total':total, 'aftertax': after_tax})
    # return render(request, 'rorders.html', {'ono':ono,'order':order_details, 'item':itemidlist, 'address': userlist,'total':total,'tax':delivery})


def update_status(request, oid):
    x = OrderSummary.objects.filter(osid = oid)
    if request.method == 'POST':
        st = request.POST.get('status')
    
    for i in x:
        i.status = st
        i.save()
    return redirect('/')


# def order_summary(request):
#     ono = randint(100000, 999999)
#     if "uid_save" in request.session:
#         uid_save_item = request.session["uid_save"]
#         d = datetime.date.today()
#         order_details = Order.objects.filter(uId = uid_save_item, odate = d)
#         # d = order_details[0].date.date()
#         uid = order_details[0].uId
#     elif "rid_save" in request.session:
#         riD = request.session["rid_save"]
#         order_details = Order.objects.filter(rId = riD)
#         d = order_details[0].date.date()
#         uid = order_details[0].uId
    
#     itemidlist = []
#     total = 0

#     for i in order_details:
#         total += i.amount
#         x = Item.objects.filter(ItemId = i.itemId.ItemId).values('ItemId','ItemName','price')
#         itemidlist.append(list(x))
        
#     # print(itemidlist)
#     # print(type(itemidlist[0]))
#     total = total + (0.05*total)
#     total += 5
#     itemlist = json.dumps(itemidlist)
#     osummary = OrderSummary(ono=ono, uid = uid, rid= order_details[0].rId, date= d, itemslist= itemlist, total=total)
#     osummary.save()
#     return redirect('/Ulogin')


def order_summary(request):
    ono = randint(100000, 999999)
    if "uid_save" in request.session:
        uid_save_item = request.session["uid_save"]

        d = datetime.date.today()
        order_details = Order.objects.filter(uId = uid_save_item, odate = d)
        uid = order_details[0].uId
        
        itemidlist = []
        after_tax = 0.0
        total = 0
        for i in order_details:
            total += i.amount
            x = Item.objects.values_list('ItemId' ,'ItemName', 'price').get(ItemId = i.itemId.ItemId)
            itemidlist.append(x)
        after_tax = total + (0.05*total) + 5
        itemlist = json.dumps(itemidlist)
        osummary = OrderSummary(date = d, ono = ono, uid=uid, rid=order_details[0].rId, 
        itemslist= itemlist, total=total, aftertax=after_tax)
        osummary.save()
        return redirect('/Ulogin')
    else: 
        messages.info("Order not successfull")
        return redirect('user')
