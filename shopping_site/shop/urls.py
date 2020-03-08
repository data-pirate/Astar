from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('product/<pk>/<slug>', views.ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<pk>/<slug>',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<pk>/<slug>',views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<pk>/<slug>',views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('single_item_add_to_cart/<pk>/<slug>',views.single_item_add_to_cart, name='single_item_add_to_cart'),
    path('cart_summary',views.CartSummary.as_view(), name='cart_summary'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('payment/<payment_option/', views.PaymentView.as_view(), name='payment'),
    path('categories/', views.categories, name='category'),
    path('s/', views.search, name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('<id>/edit_product/', views.edit_product, name='edit_product'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)