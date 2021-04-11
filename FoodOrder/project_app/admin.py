from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RestroUser)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Review)