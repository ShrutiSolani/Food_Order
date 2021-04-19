from django.contrib import admin
from django.urls import path, include
from . import views
# from django.conf import settings
# from django.conf.urls.static import static


app_name = 'project_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.showUlogin, name='user'),
    path('restro/', views.showRlogin, name='restro'),
    path('Ulogin/', views.Ulogin, name='Ulogin'),
    path('home/', views.homepage, name='home'),
    path('Uregister/', views.Uregister, name='Uregister'),
    path('Rregister/', views.Rregister, name='Rregister'),
    path('Rlogin/', views.Rlogin, name='Rlogin'),
    path('menu/', views.menu, name='Menu'),
    path('additem/', views.addItem, name='additem'),
    path('showmenu/<int:rid>/', views.showcart, name='cart' ),
    path('placeorder/<int:item>/', views.placeorder, name='placeorder'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.gohome, name='logout'),
    path('myorders/', views.myorders, name='myorders'),
    path('rorders/', views.rorders, name='rorders'),
    path('update/<int:oid>/', views.update_status, name='update')

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
