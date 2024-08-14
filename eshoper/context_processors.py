# context_processors.py
from cart.models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0

    return {
        'cart_item_count': cart_item_count,
    }
