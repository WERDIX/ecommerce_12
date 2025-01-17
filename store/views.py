from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products, 'cartitems': cartitems
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartitems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartitems': cartitems
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
        cartitems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartitems': cartitems
    }
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product ID:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, _ = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['from']['total'])
        
        order.transaction_id = transaction_id

        if total == order.get_cart_total():
            order.complete = True
            order.save()

            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )
    else:
        return JsonResponse({"message": "User is not logged in"}, status=401)

    return JsonResponse({"message": "Payment complete!"}, safe=False)
