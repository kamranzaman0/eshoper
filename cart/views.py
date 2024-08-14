from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import Cart, CartItem, Order,OrderItem
from adminsite.models import Product, Color, Size
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect
from .forms import BillingForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


def shoptingcart(request):

    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []
  
    subtotal_price = sum(item.get_product_descountprice() for item in cart_items)
    total_price = subtotal_price + 10
    context = {
        'cart_items' : cart_items,
        'subtotal_price': subtotal_price,
        'total_price': total_price,
        

    }
    return render (request, 'cart/cart.html', context)



@login_required
def add_to_cart(request, slug):
    
    product = Product.objects.get(slug = slug)
   
    sizess = request.GET.getlist('sizes')
    colorss = request.GET.getlist('colors')

    colors = []
    for color_names in colorss:
        for color_name in color_names.split(','):  # Split by commas
            color_obj = Color.objects.filter(colorname__iexact=color_name.strip()).first()  # Strip whitespace
            if color_obj:
                colors.append(color_obj)
            else:
                print(f"Color '{color_name}' not found.")

    sizes = []
    for size_names in sizess:
        for size_name in size_names.split(','):  
            size_obj = Size.objects.filter(sizename__iexact=size_name.strip()).first()  
            if size_obj:
                sizes.append(size_obj)
            else:
                print(f"Size '{size_name}' not found.")



    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItem.objects.create(cart=cart, product=product)
    cart_item.color_variants.add(*colors)
    cart_item.size_variants.add(*sizes)
    cart_item.save()

    messages.success(request, f"{product.product_name} has been added to your cart.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeitem(request, id):

    cart_item = CartItem.objects.get(id = id)
    cart_item.delete()
    return redirect('shopingcart')


import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Cart, CartItem
from .forms import BillingForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []
    subtotal_price = sum(item.get_product_descountprice() for item in cart_items)
    total_price = subtotal_price + 10

    if request.method == 'POST':
        form = BillingForm(request.POST)
        payment_method = request.POST.get('payment')

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            address_line1 = form.cleaned_data['address_line1']
            address_line2 = form.cleaned_data['address_line2']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

            order = Order(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                address_line1=address_line1,
                address_line2=address_line2,
                country=country,
                city=city,
                state=state,
                zip_code=zip_code,
                total_price=total_price,
            )
            order.save()

            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product_name=item.product.product_name,
                    price=item.get_product_descountprice(),
                    color=", ".join(item.get_color_variants_list()),
                    size=", ".join(item.get_size_variants_list())
                )
                order_item.save()

            if payment_method == 'stripe':
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Order',
                            },
                            'unit_amount': int(total_price * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/cart/paymentsuccess/') + '?order_id=' + str(order.id) + '&session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/cart/paymentfailed/'),
                )
                return redirect(session.url, code=303)

            elif payment_method == 'paypal':
                # Implement PayPal payment processing
                pass

            cart.is_paid = True
            cart.save()
            
            return redirect('paymentsuccess', order_id=order.id)
        else:
            print('Form is not valid')

    else:
        form = BillingForm()

    context = {
        'cart_items': cart_items,
        'subtotal_price': subtotal_price,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'cart/Checkout.html', context)


def paymentsuccessful(request):
    order_id = request.GET.get('order_id')
    session_id = request.GET.get('session_id')

    if not order_id:
        print('No order ID provided')
        return render(request, 'cart/paymentfailed.html', {'error': 'No order ID provided'})
    
    if not session_id:
        print('No session ID provided')
        return render(request, 'cart/paymentfailed.html', {'error': 'No session ID provided'})

    # Fetch the order using the order_id
    order = get_object_or_404(Order, id=order_id)

    try:
        # Retrieve the Stripe session
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return render(request, 'cart/paymentfailed.html', {'error': 'Invalid session ID'})


    if session.payment_status == 'paid':
        order.is_paid = True
        order.save()
        print('order is paind true')

        cart = Cart.objects.filter(user=order.user, is_paid=False).first()
        if cart:
            cart.is_paid = True
            cart.save()
            print('cart is paind true')

        order_items = OrderItem.objects.filter(order=order)

        context = {
            'order': order,
            'order_items': order_items
        }

        return render(request, 'cart/paymentsuccess.html', context)
    else:
        return render(request, 'cart/paymentfailed.html', {'error': 'Payment not successful'})




def paymentfailed(request):

    # product = Product.objects.get(id=product_id)

    # return render(request, 'payment-failed.html', {'product': product})
    return render(request, 'cart/paymentfailed.html')


