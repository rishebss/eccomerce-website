from django.contrib import admin
from .models import Product,Magazine,Shop,Cart,OrderCart,Like,OrderDesign


class OrderCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'amount', 'order_confirmed', 'shipped', 'delivered', 'created_at')
    list_filter = ('order_confirmed', 'shipped', 'delivered')
    fields = ('user', 'info', 'product_name', 'color', 'size', 'amount', 'payment_id', 'paid', 
              'order_confirmed', 'shipped', 'delivered', 'created_at')

class OrderDesignAdmin(admin.ModelAdmin):
    list_display = ('user', 'design_name', 'amount', 'order_confirmed', 'shipped', 'delivered', 'created_at')
    list_filter = ('order_confirmed', 'shipped', 'delivered')
    fields = ('user', 'info', 'design_name', 'designcolor', 'designsize', 'amount', 'payment_id', 
              'paid', 'order_confirmed', 'shipped', 'delivered', 'created_at')

# Register your models here.
admin.site.register(Product)
admin.site.register(Magazine)
admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(OrderCart)
admin.site.register(Like)
admin.site.register(OrderDesign)





