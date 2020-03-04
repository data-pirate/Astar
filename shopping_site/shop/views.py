from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem, BillingAddress, ItemImages
from .forms import CheckoutForm, AddProduct
from django.forms import modelformset_factory
# Create your views here.

@login_required
def add_product(request):
    ImageFormset = modelformset_factory(ItemImages, fields=('image',), extra=5)
    if request.method == 'POST':
        form = AddProduct(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            for each in formset:
                try:
                    images = ItemImages(item=item, image=each.cleaned_data['image'])
                    images.save()
                    return redirect('add_product')
                except Exception as e:
                    break

    else:
        form = AddProduct()
        formset = ImageFormset(queryset=ItemImages.objects.none())
    context = {
            'form': form,
            'formset': formset
        }
    return render(request, 'add_product.html', context)


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
            messages.info(
                request, 'Product was removed from cart successfully')
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
                messages.info(
                    request, 'Product was removed from cart successfully')
                return redirect("shop:cart_summary")
            order_item.quantity -= 1
            order_item.save()
            messages.info(
                request, 'Product was removed from cart successfully')
            return redirect("shop:cart_summary")
        else:
            messages.info(request, 'product isn\'t in the cart ')
            return redirect("shop:cart_summary")
    else:
        messages.info(request, 'you don\'t have active order')
        return redirect("shop:cart_summary")
# #


class CartSummary(LoginRequiredMixin, View):
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

def search(request):
    try:
        q = request.GET['q']
    except:
        q = None

    if q:
        products = Item.objects.filter(title__icontains=q)
        results = {'query': q, 'products': products}
        return render(request, 'results.html', results)
    else:
        results = {'empty': True}
        return render(request, 'index.html')


class Checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data('first_name')
                last_name = form.cleaned_data('last_name')
                address1 = form.cleaned_data('address1')
                address2 = form.cleaned_data('address2')
                company = form.cleaned_data('company')
                country = form.cleaned_data('country')
                zip_code = form.cleaned_data('zip_code')
                terms = form.cleaned_data('terms')
                newsletter = form.cleaned_data('newsletter')
                method_of_payment = form.cleaned_data('method_of_payment')
                save_info = form.cleaned_data('save_info')
                phone = form.cleaned_data('phone')
                email = form.cleaned_data('email')
                billing_address = BillingAddress(
                    user = self.request.user,
                    country = country,
                    address1 = address1,
                    first_name = first_name,
                    last_name = last_name,
                    address2 = address2,
                    newsletter = newsletter,
                    company = company,
                    zip_code = zip_code,
                    phone = phone

                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('shop:checkout')
            messages.warning(self.request, 'failed !!!')
            return redirect('shop:checkout')
        except ObjectDoesNotExist:
            return render(self.request, 'shop:checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')

#

def index(request):

    products = Item.objects.all()
    return render(request, 'index.html', {'product': products})


def blog(request):
    return render(request, 'blog.html')


def cart(request):
    return render(request, 'cart.html')


def categories(request):
    return render(request, 'categories.html')


def signup(request):
    return render(request, 'signup.html')
