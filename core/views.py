from django.shortcuts import render, HttpResponse,get_object_or_404
from taggit.models import Tag
from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address
# Create your views here.


def index(request):
    # product = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published",featured=True)

    context = {
        "products":products
    }
    return render(request,"core/index.html", context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")

    context = {
        "products":products
    }
    return render(request,"core/product-list.html", context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products=Product.objects.filter(category=product.category).exclude(pid=pid)
    p_image =  product.p_images.all()

    context = {
        "p": product,
        "p_image":p_image,
        "products": products,
    }
    return render(request, "core/product-detail.html", context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request,"core/category-list.html", context)


def category_product_list_view(request, cid):
    category=Category.objects.get(cid=cid)
    products= Product.objects.filter(product_status="published",category=category)

    context = {
        "category":category,
        "products":products,
    }
    return render(request,"core/category-product-list.html",context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors
    }
    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "core/vendor-detail.html", context)


def tag_list(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag =None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products":products,
        "tag": tag
    }
   
    return render(request,"core/tag.html",context)

