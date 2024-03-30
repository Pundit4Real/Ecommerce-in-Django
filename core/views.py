from django.http import JsonResponse
from django.shortcuts import render, HttpResponse,get_object_or_404
from django.db.models import Count,Avg
from taggit.models import Tag
from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

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

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price) #7
    products = products.filter(price__lte=max_price) #250

    if len(categories)> 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors)> 0:
        products = products.filter(vendor__id__in=vendors).distinct()


    context = {
        "products": products
    }

    data = render_to_string("core/async/product-list.html", {"products": products})

    return JsonResponse({"data":data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid']

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount })
    else:
        messages.warning(request,"Your cart is empty")
        return render(request,"core/index.html")
    
#Deleting from cart functions
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount }) 
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})


#updating the cart items functions
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount }) 
    return JsonResponse({"data":context, 'totalcartitems':len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    #checking if cart_data_obj session exist
    if 'cart_data_obj' in request.session:

    #Getting total amount for paypal amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

    #Creating order objects
        order = CartOrder.objects.create(
            user=request.user,
            price = total_amount
        )
    #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id), #invoince_no-5
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])* float(item['price'])
            )


    host = request.get_host()
    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':cart_total_amount,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice':'INVOICE_NO-' + str(order.id),
        'currency_code':"USD",
        'notify_url':'http://{}{}'.format(host,reverse("core:paypal-ipn")),
        'return_url':'http://{}{}'.format(host,reverse("core:payment-completed")),
        'cancelled_url':'http://{}{}'.format(host,reverse("core:payment-failed"))
    }

    paypal_payment_button = PayPalPaymentsForm(initial= paypal_dict)

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
        return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'paypal_payment_button':paypal_payment_button })

@login_required
def payment_completed_view(request):
    return render(request, 'core/payment-completed.html')


@login_required
def payment_failed_view(request):
    return render(request,'core/payment-failed.html')