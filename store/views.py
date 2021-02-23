import json
from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import datetime
from .utils import cookie_cart, data_cart, guest_order

def store(request):
    cookie = data_cart(request)
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cookie['cart_items']}
        
    return render(request, 'store/store.html', context=context)


def cart(request):
    
    cookie = data_cart(request)

    context = {'items': cookie['items'], 'order': cookie['order'], 'cart_items': cookie['cart_items']}
    return render(request, 'store/cart.html', context=context)



def checkout(request):
    cookie = data_cart(request)

    context = {'items': cookie['items'], 'order': cookie['order'], 'cart_items': cookie['cart_items']}
    
    return render(request, 'store/checkout.html', context=context)




def update_item(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        order_item.quantity += 1

    elif action == "remove":
        order_item.quantity -=1
    
    order_item.save()

    if order_item.quantity <=0:
        order_item.delete()

    
    return JsonResponse('done', safe=False)

from django.views.decorators.csrf import csrf_exempt 

@csrf_exempt
def process_order(request):
    transaction = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if  order.shipping:
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    
    return JsonResponse('Shipping submited..', safe=False)




