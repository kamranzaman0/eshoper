from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from adminsite.models import Profile, Color, Size
from django.contrib import messages
from adminsite.models import Product, Category, MainCategory, Collection
from django.db.models.signals import post_save
from django.dispatch import receiver
from usersite.models import UserProfile
from django.db.models import Count
from .forms import SubscribeForm

# -------------------for email---------------------
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from usersite.models import UserProfile
from cart.models import Order, OrderItem
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):

    product = Product.objects.all()
    category = Category.objects.all()
    maincategories = MainCategory.objects.annotate(product_count=Count('products'))
    collection = Collection.objects.all()

    trendy_products = Product.objects.filter(is_trendy=True)

    today = timezone.now().date()
    last_30_days = today - timezone.timedelta(days=30)
    products = Product.objects.filter(arrival_date__gte=last_30_days)# Fetch products that arrived in the last 30 days
    just_arrived_products = products.order_by('?')[:8] # Order the products randomly and limit to 8


    context = {
        'products': product,
        'categories': category,
        'maincategory' : maincategories,
        'collection' : collection,
        'trendy_products': trendy_products,
        'just_arrived_products': just_arrived_products,

    }
  
    return render(request, 'usersite/index.html',context)

def shop(request):
    product = Product.objects.all()
    category = Category.objects.all()
    # Price filter
    price_filter = request.GET.getlist('price')
    if price_filter:
        for price_range in price_filter:
            lower, upper = map(int, price_range.split('-'))
            product = product.filter(price__gte=lower, price__lte=upper)
            
    # Color filter
    color_filter = request.GET.getlist('color')
    if color_filter and 'all' not in color_filter:
        product = product.filter(color_variant__id__in=color_filter).distinct()

    # Size filter
    size_filter = request.GET.getlist('size')
    if size_filter and 'all' not in size_filter:
        product = product.filter(size_variant__id__in=size_filter).distinct()


    context = {
        'products' : product,
        'categories' : category,
        'selected_colors': color_filter,
        'selected_sizes': size_filter,
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
    }

  
    return render(request, 'usersite/shop.html',context)

def detail(request, id):
    product = Product.objects.get(id = id)

    context = {
        'product': product
    }
    return render (request, 'usersite/detail.html', context)

def contact(request):
    product = Product.objects.all()
    category = Category.objects.all()
    context = {
        'products' : product,
        'categories' : category
    }

    return render (request, 'usersite/contact.html', context)



def userlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    
        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/userlogin/') 
        
        user = authenticate(request, username = username, password = password)
        
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/userlogin/')
        else:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            return redirect('index')
        
    return render (request, 'usersite/userlogin.html')

def userlogout(request):
    logout(request)
    return redirect('/userlogin/')

def usersignup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.is_active = False 
            user.save()

            send_verification_email(request, user)

            messages.success(request, 'Account created successfully. Please check your email to activate your account.')
            return redirect('userlogin')         
    return render (request, 'usersite/usersignup.html')


def check_user_exists(request):
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    data = {
        'email_exists': User.objects.filter(email=email).exists(),
        'username_exists': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('usersite/email/email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    user.email_user(subject, message)



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now login.')
        return redirect('userlogin')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('usersignup')
  


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# Password Reset Method
# views.py
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'usersite/password/password_reset_form.html'

# views.py
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'usersite/password/password_reset_confirm.html'



import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client
def send_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

@login_required
def user_profile(request):
    user = request.user
    profile = user.userprofile  # Ensure this is linked correctly
    user_orders = Order.objects.filter(user=request.user)


    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')

        # Update the profile fields first
        profile.first_name = first_name
        profile.last_name = last_name
        profile.address = address
        profile.date_of_birth = date_of_birth

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Check if the phone number has changed
        # if profile.phone_number != phone_number:
        #     otp = f"{random.randint(100000, 999999)}"
        #     profile.otp_code = otp
        #     profile.otp_expires_at = timezone.now() + timedelta(minutes=10)
        #     profile.is_phone_verified = False
        #     send_otp(phone_number, otp)
        #     messages.info(request, 'A verification code has been sent to your new phone number.')

        #     # Temporarily save the new phone number in the session
        #     request.session['new_phone_number'] = phone_number
        #     profile.save()
        #     return redirect('verify_phone_number')

        # If phone number is not changed, save the profile directly
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('userprofile')
       
        

    context = {
        'user': user,
        'profile': profile,
        'orders' : user_orders,
    }
    return render(request, 'usersite/userprofile.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }

    return render(request, 'usersite/order_detail.html', context)


def verify_phone_number(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        profile = user.userprofile

        if profile.otp_code == otp and profile.otp_expires_at > timezone.now():
            profile.otp_code = otp
            profile.otp_expires_at = None
            profile.is_phone_verified = True
            # Retrieve the new phone number from the session
            new_phone_number = request.session.get('new_phone_number')
            if new_phone_number:
                profile.phone_number = new_phone_number
                del request.session['new_phone_number']  # Clear the session data
            print(profile.is_phone_verified)
            profile.save()
            messages.success(request, 'Phone number verified successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Invalid or expired verification code.')

    return render(request, 'account/verify_phone_number.html')



#Navbar View Code for the Category

def category_view(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    categories = Category.objects.all()
    context = {
        'products' : products,
        'category': category,
        'categories' : categories
    }

    return render (request, 'usersite/category.html', context)

# main category details page

def maincategory_detail(request, slug):
    maincategory = get_object_or_404(MainCategory, slug=slug)
    products = maincategory.products.all()
    
    context = {
        'maincategory': maincategory,
        'products': products
    }
    
    return render(request, 'usersite/maincategory_details.html', context)

# main Collections details page

def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    products = collection.products.all()  # Assuming your Collection model has a related_name='products' in the Product model.
    
    context = {
        'collection': collection,
        'products': products
    }
    
    return render(request, 'usersite/collection_detail.html', context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed!')
            return redirect('index')
    else:
        form = SubscribeForm()

    return render(request, 'subscribe.html', {'form': form})





#--------------------------Filter methods------------------------------------------------------

def product_list(request):
    # Get filters from request
    price_filter = request.GET.getlist('price')
    color_filter = request.GET.getlist('color')
    size_filter = request.GET.getlist('size')

    # Initial queryset
    products = Product.objects.all()

    # Apply filters
    if price_filter:
        products = products.filter(price__in=price_filter)
    if color_filter:
        products = products.filter(color__in=color_filter)
    if size_filter:
        products = products.filter(size__in=size_filter)

    context = {
        'products': products,
    }
    return render(request, 'usersite/shop.html', context)
