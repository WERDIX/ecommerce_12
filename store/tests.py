from django.test import TestCase
from .models import Order
from django.contrib.auth.models import User

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.order = Order.objects.create(customer=self.user.customer, complete=False, transaction_id='12345')

    def test_order_creation(self):
        self.assertEqual(self.order.transaction_id, '12345')
        self.assertFalse(self.order.complete)
        self.assertEqual(str(self.order), self.order.transaction_id) 

    def test_order_total(self):

        self.assertEqual(self.order.get_cart_total(), 0) 
