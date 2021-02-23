import json
from .models import Product, Order, OrderItem, ShippingAddress, Customer

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {
        'get_cart_quantity': 0,
        'get_cart_total': 0,
        'shipping': False
    }
    cart_items = order['get_cart_quantity']
    
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            cart_items += cart[i]['quantity']
        
            if product.digital == False:
                order["shipping"] = True
            total = product.price * (cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_quantity'] += cart[i]['quantity']
            item = {'product': {'name': product.name, 'price': product.price, 'image_url': product.image_url, 'id': i}, 'quantity': cart[i]['quantity'], 'get_total': total}
            items.append(item)
        except:
            pass
    return {'cart_items': cart_items, 'order': order, 'items': items}
        
def data_cart(request):
    user = request.user
    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
        cart_items = order.get_cart_quantity()
        return {'cart_items': cart_items, 'order': order, 'items': items}
    else:
        return cookie_cart(request)



def guest_order(request, data):
    print('hello')
    name = data['form']['name']
    email = data['form']['email']
    total = data['form']['total']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            product=product,
            quantity=item['quantity'],
            order=order,
        )
        
    return customer, order

