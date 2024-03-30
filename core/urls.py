from django.urls import path, include
from core import views


app_name = "core"


urlpatterns = [
    #home
    path("", views.index,name="index"),

    #products
    path("products/", views.product_list_view,name="product-list"),
    path("product/<pid>/", views.product_detail_view,name="product-detail"),

    #category
    path("category/", views.category_list_view,name="category-list"),
    path("category/<cid>/", views.category_product_list_view,name="category-product-list"),

    #vendor
    path("vendors/",views.vendor_list_view, name='vendor-list'),
    path("vendor/<vid>/",views.vendor_detail_view, name='vendor-detail'),

    #tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name = "tags"),

    # Add Review 
    path("ajax-add-reeview/<int:pid>/",views.ajax_add_review, name="ajax_add_review"),

    #search
    path("search/", views.search_view, name = "search"),

    #filter product url
    path("filter-products/", views.filter_product, name="filter-product"),

    #add to cart url
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    # cart Page url
    path("cart/", views.cart_view, name="cart"),
    #Delete Item From Cart
    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),
    #Update cart items
    path("update-cart/", views.update_cart, name="update-cart"),
    #checkout 
    path("checkout/", views.checkout_view, name="checkout"),
    #paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),
    #payment Successful
    path('payment-completed/', views.payment_completed_view, name="payment-completed"),
    #Payment Failed
    path('payment-failed/', views.payment_failed_view, name="payment-failed"),

    #Dashboard URL
    path('dashboard/', views.customer_dashboard, name="dashboard"),
    #Order Detail
    path('dashboard/order/<int:id>', views.order_detail, name="order-detail"),
    #Making Address Default
    path('make-default-address/', views.make_address_default, name="make-default-address"),
    #wishlist Page
    path('wishlist/', views.wishlist_view, name="wishlist"),
    #Adding to wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
    #Removing from wishlist
    path('remove-from-wishlist/', views.remove_from_wishlist, name="remove-from-wishlist"),



]
