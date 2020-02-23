from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, Order, OrderItem

# Create your views here.


class HomeView(ListView):
    model = Item
    template_name = 'index.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


def add_to_cart(request, pk, slug):
    item = get_object_or_404(Item, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_query = Order.objects.filter(user=request.user, ordered=False)
    if order_query.exists():
        order = order_query[0]
        # check if the order is already in the cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    messages.info(request, 'Product was added to cart successfully')
    return redirect("shop:product", pk=pk, slug=slug)


def remove_from_cart(request, pk, slug):
    item = get_object_or_404(Item, id=pk)
    query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if query_set.exists():
        order = query_set[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'Product was removed from cart successfully')
            return redirect("shop:product", pk=pk, slug=slug)
        else:
            messages.info(request, 'product isn\'t in the cart ')
            return redirect("shop:product", pk=pk, slug=slug)
    else:
        messages.info(request, 'you don\'t have active order')
        return redirect("shop:product", pk=pk, slug=slug)
# #


def index(request):

    products = Item.objects.all()
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
        if password == confirm_password:
            try:
                user = User.objects.get(username=username)
                return render(request, 'signup.html', {'error': True, 'message': 'Username already exists'})
            except:
                user = User.objects.create_user(
                    username=username, password=password)
                return redirect('login')
        else:
            return render(request, 'signup.html', {'error': True, 'message': 'Passwords don\'t match'})
    else:
        return render(request, 'signup.html', {'error': True, 'message': 'Something went Wrong ! please try again'})


def login(request):
    return render(request, 'login.html')


def handle_login(request):
    if request.method == 'POST':
        username = request.POST['lg_username']
        password = request.POST['lg_password']
        remember = request.POST['lg_remember']
        if not remember:
            remember = 'off'
        user = auth.authenticate(username=username, password=password)
        if not user is None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': True, 'message': 'Invalid  Credentials'})


def forgot_password(request):
    return render(request, 'forgot_password.html')
