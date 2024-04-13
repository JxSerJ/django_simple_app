import datetime

from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Client, Product, Order, OrderDetail
from .forms import ProductForm


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
    title = 'Update Product'
    message = 'Update Product data'
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_id_from_request = form.cleaned_data.get('id')
            product = Product.objects.get(pk=product_id_from_request)
            product.name = form.cleaned_data.get('name')
            product.description = form.cleaned_data.get('description')
            product.price = form.cleaned_data.get('price')
            product.image = form.cleaned_data.get('image')
            product.save()
            message = 'Product updated successfully'
    else:
        message = 'Enter new data'
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'message': message, 'title': title})


def client_orders(request, client_id, *args, **kwargs):
    order_detail = OrderDetail.objects.filter(order__client_id=client_id).select_related('product', 'order').order_by('-order__date')
    for order in order_detail:
        print(order.order.date)

    # products_7_days = order_detail.filter(order__date__gte=timezone.now().date() - datetime.timedelta(days=7))
    # products_30_days = order_detail.filter(order__date__gte=timezone.now().date() - datetime.timedelta(days=30))
    # products_365_days = order_detail.filter(order__date__gte=timezone.now().date() - datetime.timedelta(days=365))

    products_7_days = []
    products_30_days = []
    products_365_days = []
    products = []

    for order_detail in order_detail:
        if (order_detail.order.date >= timezone.now().date() - datetime.timedelta(days=7)
                and order_detail.product not in products):
            products_7_days.append(order_detail.product)
            products.append(order_detail.product)

        elif (order_detail.order.date >= timezone.now().date() - datetime.timedelta(days=30)
              and order_detail.product not in products):
            products_30_days.append(order_detail.product)
            products.append(order_detail.product)

        elif (order_detail.order.date >= timezone.now().date() - datetime.timedelta(days=365)
              and order_detail.product not in products):
            products_365_days.append(order_detail.product)
            products.append(order_detail.product)

    context = {
        'title': f'Client {client_id} Orders',
        'products_7_days': products_7_days,
        'products_30_days': products_30_days,
        'products_365_days': products_365_days,
    }

    return render(request, 'products.html', context)
