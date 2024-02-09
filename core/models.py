from django.db import models
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
# Create your models here.


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet= "abcdefgh12345")
    title = models.CharField(max_length=100, default="food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet= "abcdefgh12345")
    title= models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null = True, blank=True)
    address= models.CharField(max_length=100, default="123 Main Street.")
    contact = models.CharField(max_length=100, default="+233 (598) 193277")
    chat_resp_time = models.CharField(max_length=100,default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    authentic_rating = models.CharField(max_length=100,default="100")
    days_return = models.CharField(max_length=100,default="100")
    warranty_period = models.CharField(max_length=100,default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prd", alphabet= "abcdefgh12345")
    title = models.CharField(max_length=100, default="Fresh items")
    image = models.ImageField(upload_to=user_directory_path,default="product.jpg")

    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null = True, blank=True, default="This is the product")



