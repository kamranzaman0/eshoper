from django.urls import path, include
from usersite import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from .views import CustomPasswordResetConfirmView




urlpatterns = [
    path('cart', include('cart.urls')),

    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('contect/', views.contact, name='contect'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('shopingcart/', views.shoptingcart, name='shopingcart'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('userprofile/', views.user_profile, name='userprofile'),
    path('userlogout/', views.userlogout, name='userlogout'),


    path('check-user-exists/', views.check_user_exists, name='check_user_exists'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='usersite/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usersite/password/password_reset_complete.html'), name='password_reset_complete'),


    # path('userlogout/', views.userlogout, name='userlogout'),
    # path('404/', views.errorpage, name='404'),


    path('category/<str:slug>/', views.category_view, name='category'),

    # maincatagory details page
    path('maincategory/<slug:slug>/', views.maincategory_detail, name='maincategory_detail'),

    # Collections details page
    path('collection/<slug:slug>/', views.collection_detail, name='collection_detail'),
    
    # Collections details page
    path('subscribe/', views.subscribe, name='subscribe'),


    path('shop/', views.product_list, name='product_list'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),



]
