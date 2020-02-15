from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='cart'),
    path('update_cart/<id>', views.update_cart, name='update_cart'),
    path('delete_from_cart/<id>', views.delete_from_cart, name='delete_from_cart'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)