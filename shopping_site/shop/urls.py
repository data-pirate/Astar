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

    # 
    # path('blog/', views.blog, name='blog'),
    # path('s/', views.search, name='search'),
    # path('signup/', views.signup, name='signup'),
    # path('handle_signup', views.handle_signup, name='handle_signup'),
    # path('handle_login', views.handle_login, name='handle_login'),
    # path('login/', views.login, name='login'),
    # path('forgot_pass/', views.forgot_password, name='forgot_password'),
    # path('categories/', views.categories, name='category'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)