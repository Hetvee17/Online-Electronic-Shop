from django.shortcuts import render, redirect
from .models import *
from math import ceil
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password 
from django.views.generic import View


# Create your views here.
class Index(View):
    def get(self, request):
        allProds = []
        catprods = Product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])

        params = {'allProds':allProds}
        print('You are : ',request.session.get('email')) #users email will be printed in terminal
        return render(request, 'index.html', params)
  
class Product_view(View):
    def get(self, request, myid):
        product=Product.objects.filter(id=myid)
        print(product)
        return render(request, 'product_view.html',  {'product' : product[0]})

def validateCustomer(customer):
    error_message = None
    if (not customer.first_name):
        error_message = "First Name Required !!"
    elif (not customer.last_name):
        error_message = "Last Name Required !!"
    elif not customer.phone:
        error_message = 'Phone Number required'
    elif len(customer.phone) < 10:
        error_message = "Please enter valid phone number...!"
    elif len(customer.password) < 6:
        error_message = "Password must be 6 characters long...!"
    elif customer.isExists():
        error_message = "Email Already Registered..."
    
    return error_message

def registerUser(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    #validation
    # 'values' are sent to the signup
    value = {
        'first_name' : first_name,
        'last_name' : last_name,
        'phone' : phone,
        'email' : email
    }
    error_message = None

    customer = Customer(first_name = first_name,
                        last_name = last_name,
                        phone = phone,
                        email = email,
                        password = password)

    error_message = validateCustomer(customer)

    #saving
    if not error_message:  
        print(first_name, last_name, phone, email, password)
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('ShopHome')

    else: 
        data = {
                'error' : error_message,
                'values' : value
        }
        return render(request, 'signup.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    else: 
        return registerUser(request)
        
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                # id and email is saved in session
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                return redirect("ShopHome")
            else:
                error_message = "Email or password is Invalid"
        else:
            error_message = "Email or password is Invalid"
        print(email, password)
        return render(request, 'login.html', {'error':error_message})
        
def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'contact.html')

def add_to_cart(request):
    user = request.user
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.price)
                amount += temp_amt
            return render(request, 'addtocart.html', {'carts' : cart, 'amount' : amount})
        else:
            return render(request, 'emptycart.html')

def update_cart_item(request):
    ciid = request.POST.get('cid')
    cart_item = Cart.objects.get(id = ciid)
    cart_item.quantity = request.POST.get('qty')
    cart_item.price = int(cart_item.quantity) * int(cart_item.product.price)
    cart_item.save()
    return redirect(cart)

def remove_from_cart(request):
    cid = request.POST.get('cid')
    cart_item = Cart.objects.get(id = cid)
    cart_item.delete()
    return redirect(cart)

def checkout(request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total = 0 
        cart_product = [item for item in Cart.objects.all() if item.user == request.user]
        
        for item in cart_items:
            if(cart_product):
                total = total + (item.product.price * item.quantity)
        context = {
            'user': user,
            'cart_items': cart_items, 
            'total': total,
        }
        return render(request, "checkout.html", context)

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        user = None
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return render(request, "orders.html")

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return (request,'orders.html',{'order_placed':op})