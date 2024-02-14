from core.models import Product,Vendor, Category, CartOrder,CartOrderItems, ProductImages,ProductReview, Wishlist,Address


def default(request):
    categories = Category.objects.all()
    return {
        'categories':  categories,
    }