from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'product': products})

def search(request):
    try:
        q = request.GET['q']
    except:
        q = None
    
    if q:
        products = Product.objects.filter(product_name__icontains=q)
        results = {'query': q, 'products': products}
        return render(request, 'results.html', results)
    else:
        results = {}
        return render(request, 'index.html')

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