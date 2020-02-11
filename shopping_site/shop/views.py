from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    product = {'product': products}
    return render(request, 'index.html', product)

def blog(request):
    return render(request, 'blog.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def product(request, id_of_prod):
    product = Product.objects.filter(id=id_of_prod)
    
    return render(request, 'product.html', {'product': product[0]})

def categories(request):
    return render(request, 'categories.html')