from django.db import models
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
# Create your models here.


STATUS_CHOICES = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered")
)


STATUS = (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In review"),
    ("published","Published")
)


RATING = (
    (1,"⭐☆☆☆☆"),
    (2,"⭐⭐☆☆☆"),
    (3,"⭐⭐⭐☆☆"),
    (4,"⭐⭐⭐⭐☆"),
    (5,"⭐⭐⭐⭐⭐")
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet= "abcdefgh12345")
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet= "abcdefgh12345")

    title= models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null = True, blank=True, default="I'm an amazing vendor")

    address= models.CharField(max_length=100, default="123 Main Street.")
    contact = models.CharField(max_length=100, default="+233 (598) 193277")
    chat_resp_time = models.CharField(max_length=100,default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    authentic_rating = models.CharField(max_length=100,default="100")
    days_return = models.CharField(max_length=100,default="100")
    warranty_period = models.CharField(max_length=100,default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    class meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prd", alphabet= "abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,null=True, related_name='vendor')

    title = models.CharField(max_length=100, default="Fresh items")
    image = models.ImageField(upload_to=user_directory_path,default="product.jpg")
    description = models.TextField(null = True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="")
    old_price = models.DecimalField(max_digits=999999999, decimal_places=2, default="")

    specifications = models.TextField(null = True, blank=True, default="")
    # tags = models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)

    product_status = models.CharField(choices=STATUS,max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet= "1234567890")

    date = models.DateField(auto_now_add = True)
    updated_date = models.DateField(null=True,blank=True)


    class meta:
        verbose_name_plural = "Products"

    def products_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        percentage_change = ((self.price - self.old_price) / self.old_price) * 100
        return percentage_change



class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    date = models.DateField(auto_now_add=True)


    class meta:
        verbose_name_plural = "Product images"


################################ cart, Order , OrderItems and Address ########################
################################ cart, Order , OrderItems and Address ########################
################################ cart, Order , OrderItems and Address ########################
################################ cart, Order , OrderItems and Address ########################
        
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES,max_length=10, default="processing")


    class meta:
        verbose_name_plural = "Cart Order"



class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="")
    total = models.DecimalField(max_digits=9999999999,decimal_places=2,default="")


    class meta:
        verbose_name_plural = "Cart Order Items"


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    

################################ Product Review, Wishlists, Address ########################
################################ Product Review, Wishlists, Address ########################
################################ Product Review, Wishlists, Address ########################
################################ Product Review, Wishlists, Address ########################
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.CharField(max_length=255)
    rating = models.IntegerField(choices= RATING, default=None)
    date = models.DateField(auto_now=True)

    class meta:
        verbose_name_plural = "Product Reviews"

    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=True)

    class meta:
        verbose_name_plural = "Wishlists"

    
    def __str__(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    address = models.CharField( max_length=100, null= True)
    status= models.BooleanField(default=False)

    class meta:
        verbose_name_plural = "Address"
