from django.test import TestCase
from django.urls import reverse, resolve
from .views import store, cart, checkout
from .models import Customer, Product, Order, OrderItem
from django.contrib.auth.models import User

# Todo: test status, function, url add to cart, home, checkout
class TestHomeView(TestCase):
    def setUp(self):
        # Todo: have to setUp database first before get response

        self.url = reverse('store')
        self.user = User.objects.create_user(username='donga', password='abcsdmme2231d', email='donga.ftu2@gmail.com')
        
        # phai tao ra customer bang signal.
        self.customer = Customer.objects.create(user=self.user)

        self.client.login(username='donga', password='abcsdmme2231d')
        self.product_1 = Product.objects.create(name="test_1", price=200000, image="inear.jpeg")
        self.product_2 = Product.objects.create(name="test_2", price=300000, image="inear.jpeg")
        self.response = self.client.get(self.url)
        


    def test_view(self):
        url_cart = reverse('cart')

        # Todo: test contains cart
        self.assertContains(self.response, 'href="{0}"'.format(url_cart))

        # Todo: test store view
        self.assertEqual(self.response.status_code, 200)

    def test_product_in_store(self):
        self.assertContains(self.response, 'test_1')
        self.assertContains(self.response, 200000)
        self.assertContains(self.response, 'src="/images/inear.jpeg"')
        self.assertContains(self.response, 'Add to cart')

    def test_function(self):
        view = resolve("/")
        self.assertEqual(view.func, store)
    
    def test_csrf_token(self):
        self.assertContains(self.response, 'csrftoken')

    def test_order_created(self):
        self.assertTrue(Order.objects.get(customer=self.customer))

    def test_order_items(self):
        order = Order.objects.get(customer=self.customer)
        OrderItem.objects.create(product=self.product_1, order=order, quantity=1)
        OrderItem.objects.create(product=self.product_2, order=order, quantity=1)
        response = self.client.get(reverse('store'))
        cart_items = response.context.get('cart_items')
        self.assertEquals(cart_items, 2)



class TestUserAddToCart(TestCase):
    def setUp(self):
        
        self.url = reverse('store')
        self.user = User.objects.create_user(username='donga', password='abcsdmme2231d', email='donga.ftu2@gmail.com')
        
        # phai tao ra customer bang signal.
        self.customer = Customer.objects.create(user=self.user)

        self.client.login(username='donga', password='abcsdmme2231d')
        product_1 = Product.objects.create(name="test_1", price=200000, image="inear.jpeg")
        product_2 = Product.objects.create(name="test_2", price=300000, image="inear.jpeg")
        self.response = self.client.get(self.url)

        # click add_to_cart, chua can lam vi chua biet lam


    def test_login(self):
        user = self.response.context.get('user')
        self.assertTrue(user.is_authenticated)


    def test_add_to_cart(self):
        # Todo: button in store and in cart view.
        pass

    


class TestCartView(TestCase):

    def test_view(self):
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        url_checkout = reverse('checkout')

        # Todo: test contains checkout url
        self.assertContains(response, 'href="{0}"'.format(url_checkout))

    def test_function(self):
        view = resolve("/cart/")
        self.assertEqual(view.func, cart)




class TestCheckOutView(TestCase):

    def test_view(self):
        url = reverse('checkout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_function(self):
        view = resolve("/checkout/")
        self.assertEqual(view.func, checkout)



