from django.shortcuts import render, HttpResponse
from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address

# Create your views here.


def index(request):
    product = Product.objects.all().order_by("-id")

    context = {
        "products":product
    }
    return render(request,"core/index.html", context)
