from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from .models import Client, Product, Order, OrderDetail


def create_initial_data(request, *args, **kwargs):
    for i in range(10):
        client = Client(name=f'Client_{i}',
                        email=f'client_{i}@email.com',
                        phone=f'+7 999 999 999{i}',
                        address=f'adress_{i}')
        client.save()
        product = Product(name=f'Product_{i}',
                          description=f'Product_desc_{i}',
                          price=i * 1000 + 1)
        product.save()
    for i in range(10):
        client = Client.objects.get(pk=10 - i)
        order = Order(client=client)
        order.save()
        for j in range(10):
            product = Product.objects.get(pk=j + 1)
            order_detail = OrderDetail(product=product, quantity=i + 4, order=order)
            order_detail.save()
    orders = list(Order.objects.all())
    for order in orders:
        order.calculate_cost()
    return HttpResponse('ok')


def create_client(request, *args, **kwargs):
    client = Client(name=kwargs['name'],
                    email=kwargs['email'],
                    phone=kwargs['phone'],
                    address=kwargs['address'])
    client.save()
    return HttpResponse(f'Client id: {client.pk}')


def create_product(request, *args, **kwargs):
    product = Product(name=kwargs['name'],
                      description=kwargs['description'],
                      price=kwargs['price'])
    product.save()
    return HttpResponse(f'Product id: {product.pk}')


def create_order(request, *args, **kwargs):
    order = Order(client=Client.objects.get(pk=kwargs['client']))
    order.save()
    return HttpResponse(f'Order id: {order.pk}')


def create_order_detail(request, *args, **kwargs):
    order_detail = OrderDetail(order=Order.objects.get(pk=kwargs['order']),
                               product=Product.objects.get(pk=kwargs['product']),
                               quantity=kwargs['quantity'])
    order_detail.save()
    return HttpResponse(f'Order_detail id: {order_detail.pk}')


def delete_order(request, *args, **kwargs):
    if request.method == 'DELETE':
        order_id_from_request = request.DELETE.get('order')
        order = Order.objects.get(pk=order_id_from_request)
        order.delete()
        return HttpResponse(f'OK. Deleted {order}')


def delete_product(request, *args, **kwargs):
    if request.method == 'DELETE':
        product_id_from_request = request.DELETE.get('product')
        product = Product.objects.get(pk=product_id_from_request)
        product.delete()
        return HttpResponse(f'OK. Deleted {product}')


def update_product(request, *args, **kwargs):
    if request.method == 'PUT':
        product_id_from_request = request.PUT.get('product')
        product = Product.objects.get(pk=product_id_from_request)
        product.name = request.PUT.get('name')
        product.description = request.PUT.get('description')
        product.price = request.PUT.get('price')
        product.save()
        return HttpResponse(f'Product id: {product.pk} updated.')


def order_details_for_client(request, *args, **kwargs):
    client_id_from_request = request.GET.get('client')
    orders = list(Order.objects.filter(client=client_id_from_request))
    return HttpResponse(f'Ok')

