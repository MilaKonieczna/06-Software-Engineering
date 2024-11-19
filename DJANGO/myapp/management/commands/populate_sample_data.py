from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name= 'Product 1',
            price=19.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Product 2',
            price=14.99,
            available=True
        )
        product3 = Product.objects.create(
            name='Product 3',
            price=23.49,
            available=False
        )

        customer1 = Customer.objects.create(
            name='John Doe',
            address='123 Elm St, Springfield'
        )

        customer2 = Customer.objects.create(
            name='Alice Johnson',
            address='456 Oak St, Springfield'
        )

        customer3 = Customer.objects.create(
            name='Bob Smith',
            address='789 Pine St, Sunnyville'
        )

        order1 = Order.objects.create(
            customer=customer1,
            status='In Progress'
        )

        order2 = Order.objects.create(
            customer=customer2,
            status='New'
        )

        order3 = Order.objects.create(
            customer=customer3,
            status='Complete'
        )

        order1.products.add(product1, product3)
        order2.products.add(product3)
        order3.products.add(product2, product2)
        self.stdout.write("Data created successfully.")