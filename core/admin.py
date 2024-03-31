from django.contrib import admin
from core.models import (Product,Vendor, Category, CartOrder,CartOrderItems,
                        ProductImages,ProductReview, Wishlist_model,Address,
                        ContactUs)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'products_image', 'price','category','vendor', 'featured', 'product_status','pid']
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']



class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user', 'price', 'paid_status','order_date', 'product_status']


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item','image', 'qty', 'price','total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class Wishlist_modelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address','status']
    list_display = ['user', 'address', 'status']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','subject']


# Register your models here.

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist_model,Wishlist_modelAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
