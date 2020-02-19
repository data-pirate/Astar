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

def product(request, id, name):
    product = Product.objects.get(id=id)
    return render(request, 'product.html', {'product': product})

def categories(request):
    return render(request, 'categories.html')

def signup(request):
    return render(request, 'signup.html')

def handle_signup(request):
    if request.method == 'POST':
        fullname = request.POST['reg_fullname']
        username = request.POST['reg_username']
        email = request.POST['reg_email']
        password = request.POST['reg_password']
        confirm_password = request.POST['reg_password_confirm']
        gender = request.POST['reg_gender']
        print(fullname, username, email, gender, password, confirm_password)       
def login(request):
    return render(request, 'login.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')