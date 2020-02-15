from django.shortcuts import render,HttpResponseRedirect
from .models import Cart
from shop.models import Product

# Create your views here.
def index(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        return render(request, 'cart.html', {'cart': cart})
    else:
        return render(request, 'cart.html', {'empty': True})

def update_cart(request, id):
    cart = Cart.objects.all()[0]
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not product in cart.products.all():
        cart.products.add(product)

    total_price = 0.00
    for each in cart.products.all():
        total_price += float(each.price)
    cart.total = round(total_price, 2)
    cart.save()

    return render(request, 'cart.html', {'cart': cart})

def delete_from_cart(request, id):
    cart = Cart.objects.all()[0]
    try:
        product = Product.objects.get(id=id)
    except product.DoesNotExist:
        pass
    if product in cart.products.all():
        cart.products.remove(product)
    
    total_price = 0.00
    for each in cart.products.all():
        total_price += float(each.price)
    cart.total = round(total_price, 2)
    cart.save()

    cart.save()
    return render(request, 'cart.html', {'cart': cart})