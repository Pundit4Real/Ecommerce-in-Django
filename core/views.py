from django.http import JsonResponse
from django.shortcuts import render, HttpResponse,get_object_or_404
from django.db.models import Count,Avg
from taggit.models import Tag
from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
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

    #Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Getting average reviews related to a product
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count ()

        if user_review_count > 0:
            make_review = False

    p_image =  product.p_images.all()

    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image":p_image,
        "reviews": reviews,
        "average_rating": average_rating,
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


def ajax_add_review(request,pid):

    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user':user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
       {
        'bool': True,
        'context': context,
        'average_reviews':average_reviews
       }
    )


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains= query).order_by('-date')

    context = {
        "products": products,
        "query": query,
    }

    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    prodeucts = Product.objects.filter(product_status="published").order_by("-id").distinct()

    if len(categories)> 0:
        prodeucts = prodeucts.filter(category__id__in=categories).distinct()

    if len(vendors)> 0:
        prodeucts = prodeucts.filter(vendor__id__in=vendors).distinct()


    context = {
        "products": prodeucts
    }

    data = render_to_string("core/async/product-list.html", {"products": prodeucts})

    return JsonResponse({"data":data})