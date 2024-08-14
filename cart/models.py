from django.db import models
from adminsite.models import Product, Color, Size
from django.contrib.auth.models import User

# Create your models here.



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
        return sum(price)
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variants = models.ManyToManyField(Color, blank=True)
    size_variants = models.ManyToManyField(Size, blank=True)

    def get_product_descountprice(self):
        return self.product.descountprice

    def get_color_variants_list(self):
        return list(self.color_variants.values_list('colorname', flat=True))

    def get_size_variants_list(self):
        return list(self.size_variants.values_list('sizename', flat=True))
    
    def get_product_image_url(self):
        if self.product and self.product.product_images.exists():
            return self.product.product_images.first().image.url
        return None


from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=True, blank=True, default='Pending')

    def __str__(self):
        return f'Order {self.id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100, default='Unknown')  # Default value 'Unknown'
    size = models.CharField(max_length=100, default='Unknown')   # Default value 'Unknown'

    def __str__(self):
        return f'{self.product_name}'


