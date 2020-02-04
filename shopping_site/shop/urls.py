from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('cart/', views.cart, name='cart'),
    path('categories/', views.categories, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', views.product, name='Products')
]