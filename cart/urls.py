from django.urls import path
from cart import views

urlpatterns = [

    path('add_to_cart/<slug:slug>', views.add_to_cart, name='add_to_cart'),
    path('shopingcart/', views.shoptingcart, name='shopingcart'),
    path('removeitem/<int:id>', views.removeitem, name='removeitem'),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentsuccess/', views.paymentsuccessful, name='paymentsuccess'),
    path('paymentfailed/', views.paymentfailed, name='paymentfailed'),



    
]