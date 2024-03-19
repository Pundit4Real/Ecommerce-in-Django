from django.urls import path
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

]
