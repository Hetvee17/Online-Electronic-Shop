#from django.contrib import admin
from . import views
from django.urls import path
from .views import Index, Product_view, Login

urlpatterns = [
    path("", views.signup, name="Signup"),
    path("index/", Index.as_view(), name="ShopHome"),
    path("contact/", views.contact, name="ContactUs"),
    path("products/<int:myid>", Product_view.as_view(), name="Product_View"),
    path("checkout/", views.checkout, name="Checkout"),
    path("paymentdone", views.payment_done, name="paymentdone"),
    path("cart/", views.cart, name="Cart"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),    
    path("removefromcart", views.remove_from_cart, name="removefromcart"),
    path('updatecartitem', views.update_cart_item, name="updatecratitem"),
    path("login/", Login.as_view(), name="Login"),
    path('order/', views.orders, name='orders')
]
