from django.contrib import admin
from . models import Contact,Register,Product,Wishlist,Cart,Transaction
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

# Register your models here.
admin.site.site_header = 'Anil'
admin.site.register(Contact)
admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Transaction)