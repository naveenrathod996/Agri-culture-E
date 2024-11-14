from typing import ContextManager
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.views.generic.edit import CreateView
from .forms import CreateUserForm, Usertype
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .models import *

# Create your views here.

def SellerRegister(request):
      form = CreateUserForm()

      if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                  form.save()
                  user = form.cleaned_data.get('username')
                  email = form.cleaned_data.get('email')
                  
                  messages.success(request, 'Account was successfully created for ' + user)

                  customer, created = Customer.objects.get_or_create(name = user, email = email, type = 2)

                  return redirect('seller_login')


      context = {'form': form}
      return render(request, 'store/seller_register.html', context)


def SellerLogin(request):
      if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                  login(request, user)
                  request.session['last_activity'] = timezone.now()  # Reset last activity
                  return redirect('seller_home')

            else:
                  messages.info(request, 'Username or Password is incorrect')
      context = {}
      return render(request, 'store/seller_login.html', context)


def BuyerRegister(request):
      form = CreateUserForm()

      if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                  form.save()
                  user = form.cleaned_data.get('username')
                  
                  messages.success(request, 'Account was successfully created for ' + user)

                  return redirect('buyer_login')


      context = {'form': form}
      return render(request, 'store/buyer_register.html', context)

def BuyerLogin(request):

      if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                  login(request, user)
                  request.session['last_activity'] = timezone.now()  # Reset last activity
                  return redirect('buyer_login')

            else:
                  messages.info(request, 'Username or Password is incorrect')
      context = {}
      return render(request, 'store/buyer_login.html', context)


def logoutUser(request):
      logout(request)
      return redirect('/')


def main(request):
      languages = Language.objects.all()
      customer = Customer.objects.all()
      name = request.user.username
      return render(request,'main.html',{'languages': languages,'customer':customer,'name': name})

def Sellermain(request):
      languages = Language.objects.all()
      customer = Customer.objects.all()
      name = request.user.username
      return render(request,'seller_main.html',{'languages': languages,'customer':customer,'name': name})

def SellerHome(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/seller.html', context)

def store(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/store.html', context)

def cart(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      customer = Customer.objects.all()
      context = {'items':items, 'order':order, 'cartItems': cartItems,'logged': logged,'name': name,'customer':customer}
      return render(request, 'store/cart.html', context)

def checkout(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      customer = Customer.objects.all()
      context = {'items':items, 'order':order, 'cartItems': cartItems, 'logged': logged,'name': name,'customer':customer}
      return render(request, 'store/checkout.html', context)


def SellerCart(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      customer = Customer.objects.all()
      context = {'items':items, 'order':order, 'cartItems': cartItems,'logged': logged,'name': name,'customer':customer}
      return render(request, 'store/seller_cart.html', context)

def SellerCheckout(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      customer = Customer.objects.all()
      context = {'items':items, 'order':order, 'cartItems': cartItems, 'logged': logged,'name': name,'customer':customer}
      return render(request, 'store/seller_checkout.html', context)

def fruits(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name}
      return render(request, 'store/fruits.html', context)

def vegetables(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name}
      return render(request, 'store/vegetables.html', context)

def updateItem(request):
      data = json.loads(request.body)
      productId = data['productId']
      action = data['action']

      print('Action : ',action)
      print('Product ID :', productId)

      name = request.user.username
      email = request.user.email
      customer, created = Customer.objects.get_or_create(name = name, email = email)
      product = Product.objects.get(id=productId)
      order, created =  Order.objects.get_or_create(customer = customer, name =name, complete=False)

      orderItem, created = OrderItem.objects.get_or_create(order = order , product = product)

      if product.prod_quantity != 0:
            if action == 'add':
                  orderItem.quantity = (orderItem.quantity + 1)
                  product.prod_quantity = (product.prod_quantity - 1)
      if product.prod_quantity != -1:
            if action == 'remove':
                  orderItem.quantity = (orderItem.quantity - 1)
                  product.prod_quantity = (product.prod_quantity + 1)

            orderItem.save()
            product.save()

            if orderItem.quantity <= 0:
                  orderItem.delete()

            return JsonResponse('Item was added', safe=False)

      else:
            if action == 'add':
                  messages.info(request, 'Sorry! This Product is out of stock!')

def processOrder(request):
      transaction_id = datetime.datetime.now().timestamp()
      data = json.loads(request.body)

      if request.user.is_authenticated:
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer = customer, name =name, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                  order.complete = True
            order.save()

            ShippingAddress.objects.create(
                  customer = customer,
                  order = order,
                  address = data['shipping']['address'],
                  city = data['shipping']['city'],
                  state = data['shipping']['state'],
                  zipcode = data['shipping']['zipcode'],
            )

      else:
            print('User is not logged in..')
      return JsonResponse('Payment Complete!', safe=False)

def searchResult(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      if request.method == "POST":
            searched = request.POST['searched']
            products = Product.objects.get_or_create(name__contains=searched)
            
            context = {'searched': searched,'cartItems': cartItems,'products' :products,'items': items,'logged': logged,'name': name}
            return render(request, 'store/search_result.html', context)
      else:
            print('Please search something!')
            context = {'cartItems': cartItems,'logged': logged,'name': name}
            return render(request, 'store/search_result.html', context)

def product_details(request):
      
      context ={}
      return render (request, 'store/product_details.html', context)

def Profile(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            orders = Order.objects.all()
      else:
            name = 'none'
            orders = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      customer = Customer.objects.all()
      last_login = request.user.last_login.strftime('%y-%m-%d %a %H:%M:%S')
      context = {'customer':customer,'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'email': email,'orders': orders,'last_login': last_login}
      return render(request, 'store/profile.html', context)

def OrderStatus(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            orders = Order.objects.all()
      else:
            name = 'none'
            orders = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      customer = Customer.objects.all()
      user = request.user
      context = {'user':user,'customer':customer,'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'email': email,'orders': orders}
      return render (request, 'store/order_status.html', context)

def SellerProfile(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            orders = Order.objects.all()
      else:
            name = 'none'
            orders = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      customer = Customer.objects.all()
      last_login = request.user.last_login.strftime('%y-%m-%d %a %H:%M:%S')
      context = {'customer':customer,'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'email': email,'orders': orders,'last_login': last_login}
      return render(request, 'store/seller_profile.html', context)

def SellerOrderStatus(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created =  Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            orders = Order.objects.all()
      else:
            name = 'none'
            orders = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      customer = Customer.objects.all()
      user = request.user
      context = {'user':user,'customer':customer,'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'email': email,'orders': orders}
      return render (request, 'store/seller_order_status.html', context)

def CropPred(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/crop_pred.html', context)

def FertPred(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/fertilizer_pred.html', context)


def CropRes(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/crop_pred_res.html', context)

def FertRes(request):
      if request.user.is_authenticated:
            logged = True
            name = request.user.username
            email = request.user.email
            customer, created = Customer.objects.get_or_create(name = name, email = email)
            order, created = Order.objects.get_or_create(customer=customer, name =name, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
      else:
            name = 'none'
            logged = False
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

      products = Product.objects.all()
      context = {'products' :products, 'cartItems': cartItems,'logged': logged,'name': name,'items': items}
      return render(request, 'store/fert_pred_res.html', context)