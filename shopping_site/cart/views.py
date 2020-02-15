from django.shortcuts import render,HttpResponseRedirect
from .models import Cart, CartItem
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
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        pass
    except:
        pass
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # if not cart_item in cart.cartitem_set.all():
    #     cart.items.add(cart_item)
    cart_item.save()

    total_price = 0.00
    for each in cart.cartitem_set.all():
        quant_total = float(each.product.price) * each.quantity
        total_price += quant_total
    cart.total = round(total_price, 2)
    cart.save()

    request.session['items_count'] = cart.cartitem_set.count()
    return render(request, 'cart.html', {'cart': cart})

def delete_from_cart(request, id):
    the_id = request.session['cart_id']
    cart = Cart.objects.get(id=the_id)
    try:
        product = Product.objects.get(id=id)
    except product.DoesNotExist:
        pass
    except:
        pass
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # if cart_item in cart.cartitem_set.all():
    #     cart.products.remove(cart_item)
    cart_item.delete()
    
    total_price = 0.00
    for each in cart.cartitem_set.all():
        quant_total = float(each.product.price) * each.quantity
        total_price += quant_total
    cart.total = round(total_price, 2)
    cart.save()

    request.session['items_count'] = cart.cartitem_set.count()    
    return render(request, 'cart.html', {'cart': cart})