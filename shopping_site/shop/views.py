from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem
from .forms import CheckoutForm
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 15
    template_name = 'index.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

@login_required
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

@login_required
def single_item_add_to_cart(request, pk, slug):
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
            messages.info(request, 'Product was updated successfully')
            return redirect("shop:cart_summary")
        else:
            order.items.add(order_item)
            messages.info(request, 'Product was added to cart successfully')
            return redirect("shop:cart_summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    messages.info(request, 'Product was added to cart successfully')
    return redirect("shop:cart_summary")

@login_required
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
@login_required
def remove_single_item_from_cart(request, pk, slug):
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
            if order_item.quantity <= 1:
                order.items.remove(order_item)
                messages.info(request, 'Product was removed from cart successfully')
                return redirect("shop:cart_summary")
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, 'Product was removed from cart successfully')
            return redirect("shop:cart_summary")
        else:
            messages.info(request, 'product isn\'t in the cart ')
            return redirect("shop:cart_summary")
    else:
        messages.info(request, 'you don\'t have active order')
        return redirect("shop:cart_summary")
# #

class CartSummary(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            context = {
                'empty': True
            }
            return render(self.request, 'cart.html', context)

class Checkout(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('form is valid')
            return redirect('shop:checkout')







# 

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

def categories(request):
    return render(request, 'categories.html')


def signup(request):
    return render(request, 'signup.html')