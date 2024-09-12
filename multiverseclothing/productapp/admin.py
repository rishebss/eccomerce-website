from django.contrib import admin
from .models import Product,Magazine,Shop,Cart,OrderCart,OrderItem


# Register your models here.
admin.site.register(Product)
admin.site.register(Magazine)
admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(OrderCart)
admin.site.register(OrderItem)




