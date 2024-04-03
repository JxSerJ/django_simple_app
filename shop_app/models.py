from django.db import models
from django.db.models import QuerySet, Sum


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=400)
    register_date = models.DateField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    creation_date = models.DateField(auto_now=True)


class Order(models.Model):
    cost = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=False)
    date = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def calculate_cost(self):
        order_details = OrderDetail.objects.filter(order_id=self).all()
        cost_result = 0
        for order_detail in order_details:
            cost_result += order_detail.product.price
        self.cost = cost_result
        self.save()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
