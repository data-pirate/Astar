from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('s/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('categories/', views.categories, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<id>/<name>', views.product, name='products')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)