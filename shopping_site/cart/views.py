from django.shortcuts import render,HttpResponseRedirect
from .models import Cart
from shop.models import Product

# Create your views here.
def index(request):
    cart = Cart.objects.all()[0]
    # cart_length = len(cart)
    # print(type(cart))
    return render(request, 'cart.html', {'cart': cart})

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

# def delete_from_cart(request, id):
#     cart = Cart.objects.all()[0]
#     try:
#         product = Product.objects.get(id=id)
#     except product.DoesNotExist:
#         pass
#     if product in cart.products.all():
#         cart.products.remove(product)

#     cart.save()
#     return render(request, 'cart.html', {'cart': cart})