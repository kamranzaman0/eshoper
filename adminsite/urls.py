from django.urls import path
from adminsite import views



urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/showproduct', views.showproduct, name='showproduct'),
    path('dashboard/addproduct', views.addproduct, name='addproduct'),
    path('products/update/<int:id>/', views.updateproduct, name='updateprodect'),                              
    path('products/delete/<int:id>/', views.deleteproduct, name='deleteproduct'),

    
    # Category URLs
    path('dashboard/category/', views.category_list, name='category_list'),
    path('dashboard/category/create/', views.category_create, name='category_create'),
    path('dashboard/category/update/<int:id>/', views.category_update, name='category_update'),
    path('dashboard/category/delete/<int:id>/', views.category_delete, name='category_delete'),
    
    
    # MainCategory URLs
    path('dashboard/maincategory/', views.maincategory_list, name='maincategory_list'),
    path('dashboard/maincategory/create/', views.maincategory_create, name='maincategory_create'),
    path('dashboard/maincategory/update/<int:id>/', views.maincategory_update, name='maincategory_update'),
    path('dashboard/maincategory/delete/<int:id>/', views.maincategory_delete, name='maincategory_delete'),

    # Collection URLs
    path('dashboard/collection/', views.collection_list, name='collection_list'),
    path('dashboard/collection/create/', views.collection_create, name='collection_create'),
    path('dashboard/collection/update/<int:id>/', views.collection_update, name='collection_update'),
    path('dashboard/collection/delete/<int:id>/', views.collection_delete, name='collection_delete'),
    
    # # Color URLs
    # path('colors/', views.ColorListView.as_view(), name='color_list'),
    # path('color/add/', views.ColorCreateView.as_view(), name='color_add'),
    # path('color/<int:pk>/', views.ColorDetailView.as_view(), name='color_detail'),
    # path('color/<int:pk>/edit/', views.ColorUpdateView.as_view(), name='color_edit'),
    # path('color/<int:pk>/delete/', views.ColorDeleteView.as_view(), name='color_delete'),

    # # Material URLs
    # path('materials/', views.MaterialListView.as_view(), name='material_list'),
    # path('material/add/', views.MaterialCreateView.as_view(), name='material_add'),
    # path('material/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    # path('material/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_edit'),
    # path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),

    # # Size URLs
    # path('sizes/', views.SizeListView.as_view(), name='size_list'),
    # path('size/add/', views.SizeCreateView.as_view(), name='size_add'),
    # path('size/<int:pk>/', views.SizeDetailView.as_view(), name='size_detail'),
    # path('size/<int:pk>/edit/', views.SizeUpdateView.as_view(), name='size_edit'),
    # path('size/<int:pk>/delete/', views.SizeDeleteView.as_view(), name='size_delete'),

    # # Product URLs
    # path('products/', views.ProductListView.as_view(), name='product_list'),
    # path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
    # path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    # path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # # ProductImage URLs
    # path('product_images/', views.ProductImageListView.as_view(), name='productimage_list'),
    # path('product_image/add/', views.ProductImageCreateView.as_view(), name='productimage_add'),
    # path('product_image/<int:pk>/', views.ProductImageDetailView.as_view(), name='productimage_detail'),
    # path('product_image/<int:pk>/edit/', views.ProductImageUpdateView.as_view(), name='productimage_edit'),
    # path('product_image/<int:pk>/delete/', views.ProductImageDeleteView.as_view(), name='productimage_delete'),

    # # Coupon URLs
    # path('coupons/', views.CouponListView.as_view(), name='coupon_list'),
    # path('coupon/add/', views.CouponCreateView.as_view(), name='coupon_add'),
    # path('coupon/<int:pk>/', views.CouponDetailView.as_view(), name='coupon_detail'),
    # path('coupon/<int:pk>/edit/', views.CouponUpdateView.as_view(), name='coupon_edit'),
    # path('coupon/<int:pk>/delete/', views.CouponDeleteView.as_view(), name='coupon_delete'),
]

