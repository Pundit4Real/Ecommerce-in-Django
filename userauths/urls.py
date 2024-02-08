from django.urls import path
from userauths import views


urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up')
]
