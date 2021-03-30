from django.contrib import admin
from .models import *

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_deisplay = ['name']

admin.site.register(Category, AdminCategory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
#admin.site.register(Orders)
#admin.site.register(OrderItem)
#admin.site.register(ShippingAddress)
admin.site.register(Contact)
admin.site.register(Customer)