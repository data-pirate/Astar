from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Order, OrderItem, BillingAddress, ItemImages, Profile
from .forms import CheckoutForm, AddProduct, EditProduct, ProfileEditForm, UserEditForm
from django.forms import modelformset_factory
# Create your views here.

# for adding product
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
                except Exception as e:
                    break
            return redirect('shop:index')
            
    else:
        form = AddProduct()
        formset = ImageFormset(queryset=ItemImages.objects.none())
    context = {
            'form': form,
            'formset': formset
        }
    return render(request, 'add_product.html', context)


# Edit the existing product using its id
def edit_product(request, id):
    item = get_object_or_404(Item, id=id)
    ImageFormset = modelformset_factory(ItemImages, fields=('image',), extra=5)
    if item.user != request.user:
        raise Http404()
    if request.method == 'POST':
        form = EditProduct(request.POST or None, instance=item)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            for each in formset:
                if each.cleaned_data:
                    if each.cleaned_data['id'] is None:
                        images = ItemImages(item=item, image=each.cleaned_data['image'])
                        images.save()


            return HttpResponseRedirect(item.get_absolute_url())
    else:
        form = EditProduct(instance=item)
    context = {
        'form': form,
        'item': item
    }

    return render(request, 'edit_product.html', context)

# delete_product
@login_required
def delete_product(request, id):
    item = get_object_or_404(Item, id=id)
    if item.user != request.user:
        raise Http404()
    item.delete()
    return redirect('shop:index')

# landing page
class HomeView(ListView):
    model = Item
    paginate_by = 15
    template_name = 'index.html'

# Product detail view
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


# logic for adding something to the cart
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


# for adding item using cart 
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


# delete product
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


# remove single product from cart
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

# cart summary
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

# for search
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


# checkout
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


# just renders the payment view
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')


# profile edit page
@login_required
def edit_profile(request):
    p_form = get_object_or_404(Profile, user=request.user) 

    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('shop:myprofile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


#

def blog(request):
    return render(request, 'blog.html')

def cart(request):
    return render(request, 'cart.html')

def categories(request):
    return render(request, 'categories.html')
