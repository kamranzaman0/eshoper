from django.shortcuts import render, HttpResponseRedirect, HttpResponse,get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Color, Size, Material, Category, MainCategory, Collection
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm, CategoryForm, MainCategoryForm, CollectionForm, ProductImageForm
from .models import ProductImage, Product
from django.contrib.auth.decorators import user_passes_test



# Create your views here.

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='/login/')
def dashboard(request):
    username = request.session.get('username')  # Get the username from the session or use 'Guest' as default
    context = {
        'username': username,
    }
    print(username)
    
    return render(request, 'adminsite/dashboard.html', context)


@user_passes_test(is_staff, login_url='/login/')
def showproduct(request):
    products = Product.objects.all()
    
    return render(request, 'adminsite/product/showproduct.html', {'products': products})


from django.forms import modelformset_factory

ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3,can_delete=True)  # Adjust the 'extra' value as needed

@user_passes_test(is_staff, login_url='/login/')
def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()  # Save many-to-many relationships

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, f'Product {product.product_name} added successfully!')
            return redirect('addproduct')  # Redirect to a page of your choice
        
    else:
        form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'adminsite/product/addproduct.html', {'form': form, 'formset': formset})
@user_passes_test(is_staff, login_url='/login/')
def updateproduct(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))

        if form.is_valid():
            form.save()
        else:
            print("ProductForm errors:", form.errors)

        if formset.is_valid():
            formset.save()
        else:
            print("ProductImageFormSet errors:", formset.errors)
            
        if form.is_valid() and formset.is_valid():
            messages.success(request, f'Product {product.product_name} updated successfully!')
            return redirect('showproduct')
        else:
            messages.error(request, 'There were errors in the form. Please correct them and try again.')

    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(queryset=ProductImage.objects.filter(product=product))

    return render(request, 'adminsite/product/updateproduct.html', {'form': form, 'formset': formset, 'product': product})
@user_passes_test(is_staff, login_url='/login/')
def deleteproduct(request, id):    
    product = Product.objects.get(id = id)
    product.delete()
    return redirect('showproduct')

#--------------------------------------Category---------------------------------------------------
@user_passes_test(is_staff, login_url='/login/')
def category_list(request):
    category = Category.objects.all()
    return render(request, 'adminsite/category/category_list.html', {'category': category})

@user_passes_test(is_staff, login_url='/login/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, f'catogry{category.catetory_name} is saved successfully')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'adminsite/category/category_form.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def category_update(request, id):
    category = Category.objects.get(id = id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid:
            form.save()
            return redirect('category_list')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)    
    return render(request, 'adminsite/category/category_update.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def category_delete(request, id):
    category = Category.objects.get(id = id)
    category.delete()
    return redirect('category_list')


#--------------------------------------Main Category---------------------------------------------------
@user_passes_test(is_staff, login_url='/login/')
def maincategory_list(request):
    maincategory = MainCategory.objects.all()
    return render(request, 'adminsite/maincategory/maincategory_list.html', {'maincategory': maincategory})

@user_passes_test(is_staff, login_url='/login/')
def maincategory_create(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST,request.FILES)
        if form.is_valid():
            maincategory = form.save(commit=False)
            maincategory.save()
            
            messages.success(request, f'Maincatogry {maincategory.name} is saved successfully')
            return redirect('maincategory_list')
    else:
        form = MainCategoryForm()
    return render(request, 'adminsite/maincategory/maincategory_form.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def maincategory_update(request, id):
    maincategory = MainCategory.objects.get(id = id)
    if request.method == 'POST':
        form = MainCategoryForm(request.POST,request.FILES, instance=maincategory)
        if form.is_valid:
            form.save()
            return redirect('maincategory_list')
        else:
            print(form.errors)
    else:
        form = MainCategoryForm(instance=maincategory)
    
    return render(request, 'adminsite/maincategory/maincategory_update.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def maincategory_delete(request, id):
    
    maincategory = MainCategory.objects.get(id = id)
    maincategory.delete()
    return redirect('maincategory_list')


#--------------------------------------Collection---------------------------------------------------
@user_passes_test(is_staff, login_url='/login/')
def collection_list(request):
    collection = Collection.objects.all()
    return render(request, 'adminsite/collections/collection_list.html', {'collection': collection})

@user_passes_test(is_staff, login_url='/login/')
def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST,request.FILES)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.save()
            
            messages.success(request, f'collection {collection.name} is saved successfully')
            return redirect('collection_list')
    else:
        form = CollectionForm()
    return render(request, 'adminsite/collections/collection_form.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def collection_update(request, id):
    collection = Collection.objects.get(id = id)
    if request.method == 'POST':
        form = CollectionForm(request.POST,request.FILES, instance=collection)
        if form.is_valid:
            form.save()
            return redirect('collection_list')
        else:
            print(form.errors)
    else:
        form = CollectionForm(instance=collection)
    
    return render(request, 'adminsite/collections/collection_update.html', {'form': form})

@user_passes_test(is_staff, login_url='/login/')
def collection_delete(request, id):
    
    collection = Collection.objects.get(id = id)
    collection.delete()
    return redirect('collection_list')

