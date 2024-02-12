from django.shortcuts import render, HttpResponse
from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address

# Create your views here.


def index(request):
    # product = Product.objects.all().order_by("-id")
    products = Product.objects.filter(featured=True)

    context = {
        "products":products
    }
    return render(request,"core/index.html", context)
