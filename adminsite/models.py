from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# from cart.models import CartItem


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name = 'profile')
    is_email_varified = models.BooleanField(default=False)
    email_tokan = models.CharField(max_length=100, null=True, blank= True)
    profile_image = models.ImageField(upload_to='profileimage/')


class Category(models.Model):
    catetory_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs ):
        self.slug = slugify(self.catetory_name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.catetory_name
    

class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    images = models.ImageField(upload_to='maincategory_images/', default='default.jph')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MainCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='collection_images/', null=True, blank=True)
    discount = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Color(models.Model):
    colorname = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.colorname
    
class Material(models.Model):
    materialname = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.materialname
    
class Size(models.Model):
    sizename = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.sizename


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  
    price = models.IntegerField()
    descountprice = models.IntegerField(default=0)
    product_description = models.TextField()
    product_dtails_descripttion = models.TextField(default=None)
    color_variant = models.ManyToManyField(Color, blank=True)
    size_variant = models.ManyToManyField(Size, blank=True)
    material_variant = models.ManyToManyField(Material, blank=True)
    is_trendy = models.BooleanField(default=False)
    arrival_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.product_name


    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/', default='default.jpg')


class Coupon(models.Model):
    Coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimun_amount = models.IntegerField(default=500)




