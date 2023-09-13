from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced 
# Register your models here.

    
    
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderPlaced)
admin.site.register(Cart)


# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display  = ['id','title','selling_price','discounted_price','desciption','brand','category','product_image']
    

