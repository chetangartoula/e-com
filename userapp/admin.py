from django.contrib import admin

from .models import (Banner, Brand,Color, Customers, Main_Category, Orders, Category,Giftcard,SEO,Product, Sub_Category,
Tags,metadata,Product_Image,Product_type, Slider,Color,Size,Variants,Events)
# Register your models here.






class Product_ImageTabular(admin.TabularInline):
    model = Product_Image



class ProductAdmin(admin.ModelAdmin):
    list_display = ["pro_name","vendor","price","pro_collection","total_quantity","stock","pro_catagory"]
    inlines = [
        Product_ImageTabular,
        
    ]
    list_editable= ["pro_catagory","total_quantity","pro_collection"]



admin.site.site_header = "Ecommerce Main Admin"
admin.site.site_title = "Admin Ecommerce"
admin.site.index_title = "Ecommerce"

admin.site.register(Category)
admin.site.register(Main_Category)
admin.site.register(Sub_Category)
# admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Product_type)
admin.site.register(Giftcard)
admin.site.register(Product_Image)
admin.site.register(metadata)
admin.site.register(Product,ProductAdmin)

admin.site.register(SEO)
admin.site.register(Slider)
admin.site.register(Tags)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants)
admin.site.register(Orders)
admin.site.register(Customers)
admin.site.register(Events)
admin.site.register(Banner)


