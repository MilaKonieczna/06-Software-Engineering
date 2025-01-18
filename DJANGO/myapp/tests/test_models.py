from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from decimal import Decimal

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name='Temporary product', price=Decimal('1.99'), available=True
        )
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, Decimal('1.99'))
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Invalid product', price=-1.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=Decimal('1.99'), available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_price(self):
        product = Product(name='No Price', available=True)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_availability(self):
        product = Product(name='No Availability', price=Decimal('1.99'))
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_name_length_edge_values(self):
        product_min = Product(name='X', price=Decimal('9.99'), available=True)
        product_min.full_clean()
        self.assertEqual(product_min.name, 'X')

        long_name = 'X' * 255
        product_max = Product(name=long_name, price=Decimal('9.99'), available=True)
        product_max.full_clean()
        self.assertEqual(product_max.name, long_name)

        with self.assertRaises(ValidationError):
            product_invalid = Product(name='X' * 256, price=Decimal('9.99'), available=True)
            product_invalid.full_clean()

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            product_invalid = Product.objects.create(
                name='Invalid Format', price=Decimal('9.999'), available=True
            )
            product_invalid.full_clean()

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name='Temporary product', price=Decimal('1.99'), available=True
        )
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, Decimal('1.99'))
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Invalid product', price=-1.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=Decimal('1.99'), available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_price(self):
        product = Product(name='No Price', available=True)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_availability(self):
        product = Product(name='No Availability', price=Decimal('1.99'))
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_name_length_edge_values(self):
        product_min = Product(name='X', price=Decimal('9.99'), available=True)
        product_min.full_clean()
        self.assertEqual(product_min.name, 'X')

        long_name = 'X' * 255
        product_max = Product(name=long_name, price=Decimal('9.99'), available=True)
        product_max.full_clean()
        self.assertEqual(product_max.name, long_name)

        with self.assertRaises(ValidationError):
            product_invalid = Product(name='X' * 256, price=Decimal('9.99'), available=True)
            product_invalid.full_clean()


    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            product_invalid = Product.objects.create(
                name='Invalid Format', price=Decimal('9.999'), available=True
            )
            product_invalid.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(name="Spencer Morgan", address="123 Washington St")
        self.assertEqual(customer.name, "Spencer Morgan")
        self.assertEqual(customer.address, "123 Washington St")

    def test_create_customer_with_missing_name(self):
        customer = Customer(address="123 Washington St")
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_blank_name(self):
        customer = Customer(name="", address="123 Washington St")
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_missing_address(self):
        customer = Customer(name="Spencer Morgan")
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        customer = Customer(name="Spencer Morgan", address="")
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_customer_with_name_length_edge_values(self):
        customer_min = Customer(name="X", address="123 Washington St")
        customer_min.full_clean()
        self.assertEqual(customer_min.name, "X")

        long_name = "X" * 100
        customer_max = Customer(name=long_name, address="123 Washington St")
        customer_max.full_clean()
        self.assertEqual(customer_max.name, long_name)

        invalid_long_name = "X" * 101
        customer_invalid = Customer(name=invalid_long_name, address="123 Washington St")
        with self.assertRaises(ValidationError):
            customer_invalid.full_clean()

    def test_create_customer_with_address_length_edge_values(self):
        customer_min = Customer(name="Spencer Morgan", address="X")
        customer_min.full_clean()
        self.assertEqual(customer_min.address, "X")
        long_address = "X" * 255
        customer_max = Customer(name="Spencer Morgan", address=long_address)
        customer_max.full_clean()
        self.assertEqual(customer_max.address, long_address)

        invalid_long_address = "X" * 256
        customer_invalid = Customer(name="Spencer Morgan", address=invalid_long_address)
        with self.assertRaises(ValidationError):
            customer_invalid.full_clean()


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Spencer Morgan", address="123 Washington St")

        self.product1 = Product.objects.create(name="Product 1", price=Decimal('10.00'), available=True)
        self.product2 = Product.objects.create(name="Product 2", price=Decimal('20.00'), available=True)
        self.product3 = Product.objects.create(name="Unavailable Product", price=Decimal('30.00'), available=False)

    def test_order_creation_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.set([self.product1, self.product2])

        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, "New")
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())

    def test_order_creation_with_missing_customer(self):
        order = Order(status="New")
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_order_creation_with_invalid_status(self):
        invalid_status = "Invalid"
        order = Order(customer=self.customer, status=invalid_status)
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_order_creation_with_missing_status(self):
        order = Order(customer=self.customer)
        order.full_clean()
        self.assertEqual(order.status, "New")

    def test_total_price_calculation_with_valid_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.set([self.product1, self.product2])

        self.assertEqual(order.total_price(), Decimal('30.00'))

    def test_total_price_calculation_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.set([])

        self.assertEqual(order.total_price(), 0)

    def test_order_can_be_fulfilled_with_all_available_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.set([self.product1, self.product2])

        self.assertTrue(order.fulfilled())

    def test_order_cannot_be_fulfilled_with_unavailable_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.set([self.product1, self.product3])

        self.assertFalse(order.fulfilled())
