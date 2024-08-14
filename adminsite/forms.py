# forms.py
from django import forms
from .models import Category, MainCategory, Collection, Color, Material, Size, Product, ProductImage, Coupon


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('arrival_date', 'slug')  
        fields = [
            'product_name', 'category', 'maincategory', 'collection', 'price', 
            'descountprice', 'product_description', 'product_dtails_descripttion',
            'color_variant', 'size_variant', 'material_variant', 'is_trendy'
        ]
        
    color_variant = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=True
    )
    size_variant = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=True
    )
    material_variant = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=True
    )

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['catetory_name', 'slug']

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['name', 'slug', 'images']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'slug', 'description', 'image', 'discount']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


