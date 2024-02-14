from django.urls import path
from core import views


app_name = "core"


urlpatterns = [
    #home
    path("", views.index,name="index"),
    path("products/", views.product_list_view,name="product-list"),
    #category
    path("category/", views.category_list_view,name="category-list"),
    path("category/<cid>/", views.category_product_list_view,name="category-product-list"),
    #vendor
    path("vendors/",views.vendor_list_view, name='vendor-list'),
    path("vendor/<vid>/",views.vendor_detail_view, name='vendor-detail'),

]
