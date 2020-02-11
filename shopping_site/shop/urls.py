from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('categories/', views.categories, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:id_of_prod>', views.product, name='Products')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)